from flask import Flask
from flask import request
from flask_cors import CORS
import nltk.chat
from nltk.chat.util import Chat, reflections
import re
import requests
import yaml
app = Flask(__name__)
CORS(app)

bots = {}

with open('./chat.html') as f:
    chat_form_html = f.read()

def get_bot_from_gist(user, hash):
    r = requests.get('https://gist.githubusercontent.com/' + user + '/' + hash + '/raw/bot.yaml')
    if r.status_code != 200:
        return "Bad request", r.status_code
    chatbot = yaml.safe_load(r.text)
    bot = {}
    pairs = []
    for pair in chatbot:
        if "name" in pair:
            bot["name"] = pair["name"]
        if "match" in pair:
            pairs.append((pair["match"], pair["replies"]))
    if "name" not in bot:
        bot["name"] = "Anonymous Bot";
    bot["pairs"] = Chat(pairs, reflections)
    bots[hash] = {"name": bot["name"], "pairs": bot["pairs"]}

@app.route("/chat-api")
def what():
    text = request.args.get('text')
    if (not text):
        return "I'm sorry, I didn't understand that."
    bot = nltk.chat.eliza
    return bot.eliza_chatbot.respond(text)

@app.route("/chat/<user>/<hash>")
def get_bot(user, hash):
    if hash not in bots or request.args.get('reload'):
       get_bot_from_gist(user, hash)
    # TODO: us a jinja2 template
    return re.sub('<h1>[^<]+</h1>', '<h1>' + bots[hash]["name"] + '</h1>', chat_form_html).replace("BOTNAME", bots[hash]["name"]).replace("Hello, what would you like to discuss today?", bots[hash]["pairs"].respond("intro")).replace("/chat-api", "/chat-api/" + user + "/" + hash).replace('<p id="credit"></p>', '<p id="credit">Bot created by ' + user + '. <a href="https://gist.github.com/' + user + '/' + hash + '">View source</a>. <a href="?reload">Reload Source</a>.</p>')
 
@app.route("/chat-api/<user>/<hash>")
def get_bot_response(user, hash):
    if hash not in bots:
        get_bot_from_gist(user, hash)
    text = request.args.get('text')
    if (not text):
        text = ""
    return bots[hash]["pairs"].respond(text)

@app.route("/test/")
def test():
    return "this is a test"

@app.route("/chat/")
def chat():
    return chat_form_html.replace("BOTNAME", "ELIZA").replace('<p id="credit"></p>', '<p id="credit">This is a demo of the eliza submodule of the <a href="http://www.nltk.org/api/nltk.chat.html">NLTK chat module</a>.</p>')
