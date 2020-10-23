#!/bin/sh

# Build the container using buildah instead of Docker

# Retrieve container
CONTAINER=$(buildah from centos:centos7)
echo $CONTAINER

# Mount the container filesystem
MNT=$(buildah mount $CONTAINER)
echo $MNT

# Install python3 within the container path
yum --assumeyes install --installroot $MNT python3

# Install python libraries within the container path
pip3 install --prefix=$MNT/usr/ Flask flask-cors nltk pyyaml requests uwsgi

# Remove unnecessary cache files
rm -rf $MNT/var/cache $MNT/var/log/*

# Copy chatbot app files
cp chatbot.py $MNT/
cp chat.html $MNT/

# Set container config options (port, entrypoint)
buildah config --port 9500/tcp $CONTAINER
buildah config --entrypoint 'uwsgi --http :9500 --manage-script-name --mount /=chatbot:app' $CONTAINER

# Commit the changes to nltk-eliza
buildah commit $CONTAINER cherdt/nltk-chatbot
