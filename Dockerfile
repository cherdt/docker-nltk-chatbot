FROM centos:centos7

RUN /usr/bin/yum --assumeyes install gcc python3 python3-devel python3-pip
RUN /usr/bin/pip3 install Flask flask-cors nltk pyyaml requests uwsgi

COPY chat.html ./
COPY chatbot.py ./

CMD ["/usr/local/bin/uwsgi", "--http", ":9500", "--manage-script-name", "--mount", "/=chatbot:app"]
