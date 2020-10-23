ELIZA chatbot Docker image
==========================

Docker image to run the Python NLTK ELIZA chatbot in a web form from within a container. This image is also available at https://hub.docker.com/r/cherdt/nltk-chatbot/

How to build
------------

    git clone https://github.com/cherdt/docker-nltk-chatbot.git
    cd docker-nltk-chatbot
    docker build --tag nltk-chatbot .

How to run
----------

Once built:

    docker run -d -p 9500:9500 nltk-chatbot

How to interact
---------------

Visit http://localhost:9500/chat/

Alternative build intructions
-----------------------------

Run `sh build.sh` to create the image using [buildah](https://buildah.io/)

This requires that the host where you are building the image has some of the necessary dependencies, but it creates a smaller container image.
