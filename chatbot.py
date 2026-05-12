from flask import Flask
from flask import render_template
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

# valid usernames may contain alphanumeric characters and hypens
def is_valid_user(user):
    return re.fullmatch("[-a-zA-Z0-9]+", user)

# valid hashes are 32-digit hexidecimal numbers
def is_valid_hash(hash):
    return re.fullmatch("[a-f0-9]{32}", hash)

def build_bot_from_yaml(yamltext, user, hash):
    chatbot = yamltext
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


def get_bot_from_gist(user, hash):
    if is_valid_user(user) and is_valid_hash(hash):
        r = requests.get('https://gist.githubusercontent.com/' + user + '/' + hash + '/raw/bot.yaml')
        if r.status_code != 200:
            return False
        yamltext = yaml.safe_load(r.text)
        build_bot_from_yaml(yamltext, user, hash)
        return True
    else:
        return False


@app.route("/chat-api")
def what():
    text = request.args.get('text')
    if (not text):
        return "I'm sorry, I didn't understand that."
    bot = nltk.chat.eliza
    return bot.eliza_chatbot.respond(text)

@app.route("/chat/<user>/<hash>")
def get_bot(user, hash):
    if hash in bots or request.args.get('reload') or get_bot_from_gist(user, hash):
        bot = bots[hash]
        bot_name = bot["name"]
        intro = bot["pairs"].respond("intro")
    else:
        bot_name = "ELIZA"
        intro = "Hello, what would you like to discuss today?"
        user = "ERROR"
        hash = "ERROR"
    return render_template('chat.html', botname=bot_name, user=user, intro=intro, hash=hash)
 
@app.route("/chat-api/<user>/<hash>")
def get_bot_response(user, hash):
    if hash in bots or get_bot_from_gist(user, hash):
        bot = bots[hash]["pairs"]
    else:
        bot = nltk.chat.eliza.eliza_chatbot
    text = request.args.get('text')
    if (not text):
        text = ""
    return bot.respond(text)

@app.route("/test/")
def test():
    return "this is a test"

@app.route("/chat/")
def chat():
    return render_template("chat.html", botname="ELIZA", intro="Hello, what would you like to discuss today?", hash="")
