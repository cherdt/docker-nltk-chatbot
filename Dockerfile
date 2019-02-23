FROM centos:centos7

RUN /usr/bin/yum --assumeyes install epel-release gcc
RUN /usr/bin/yum --assumeyes install python python-devel python-pip
RUN /usr/bin/pip install Flask flask-cors nltk pyyaml requests uwsgi

COPY chat.html ./
COPY chatbot.py ./

CMD ["/usr/bin/uwsgi", "--http", ":9500", "--manage-script-name", "--mount", "/=chatbot:app"]
