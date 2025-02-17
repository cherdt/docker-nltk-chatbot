FROM alpine:latest

RUN apk add gcc python3 py3-flask py3-flask-cors py3-nltk py3-yaml py3-requests uwsgi uwsgi-http uwsgi-python3

COPY chat.html ./
COPY chatbot.py ./

CMD ["/usr/sbin/uwsgi", "--plugins", "http,python", "--http", ":9500", "--manage-script-name", "--mount", "/=chatbot:app"]
