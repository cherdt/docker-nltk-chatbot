from flask import Flask
from flask import render_template
from flask import request
from flask_cors import CORS
import nltk.chat
from nltk.chat.util import Chat, reflections
import requests
import yaml
app = Flask(__name__)
CORS(app)

bots = {}

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
    return render_template('chat.html', botname=bots[hash]["name"], user=user, intro=bots[hash]["pairs"].respond("intro"), hash=hash)
 
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
    return render_template("chat.html", botname="ELIZA", intro="Hello, what would you like to discuss today?", hash="")
