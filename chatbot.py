"""Creates an NLTK-based chatbot running on Flask."""

import re
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

def is_valid_user(user):
    """Valid usernames may contain alphanumeric chars and hyphens"""
    return re.fullmatch("[-a-zA-Z0-9]+", user)

def is_valid_gist_id(gist_id):
    """Valid gist_ids are 32-digit hex numbers"""
    return re.fullmatch("[a-f0-9]{32}", gist_id)

def build_bot_from_yaml(yamltext, gist_id):
    """Build a chatbot from formatted YAML"""
    chatbot = yamltext
    bot = {}
    pairs = []
    for pair in chatbot:
        if "name" in pair:
            bot["name"] = pair["name"]
        if "match" in pair:
            pairs.append((pair["match"], pair["replies"]))
    if "name" not in bot:
        bot["name"] = "Anonymous Bot"
    bot["pairs"] = Chat(pairs, reflections)
    bots[gist_id] = {"name": bot["name"], "pairs": bot["pairs"]}


def get_bot_from_gist(user, gist_id):
    """Get chatbot YAML from a GitHub Gist"""
    if is_valid_user(user) and is_valid_gist_id(gist_id):
        gist_url = f'https://gist.githubusercontent.com/{user}/{gist_id}/raw/bot.yaml'
        r = requests.get(gist_url, timeout=10)
        if r.status_code != 200:
            return False
        yamltext = yaml.safe_load(r.text)
        build_bot_from_yaml(yamltext, gist_id)
        return True
    return False


@app.route("/chat-api")
def get_generic_response():
    """No bot specified, return response from ELIZA"""
    text = request.args.get('text')
    if not text:
        return "I'm sorry, I didn't understand that."
    bot = nltk.chat.eliza
    return bot.eliza_chatbot.respond(text)

@app.route("/chat/<user>/<gist_id>")
def get_bot(user, gist_id):
    """Get a bot based on the user and gist_id"""
    if gist_id in bots or request.args.get('reload') or get_bot_from_gist(user, gist_id):
        bot = bots[gist_id]
        bot_name = bot["name"]
        intro = bot["pairs"].respond("intro")
    else:
        bot_name = "ELIZA"
        intro = "Hello, what would you like to discuss today?"
        user = "ERROR"
        gist_id = "ERROR"
    return render_template('chat.html', botname=bot_name, user=user, intro=intro, gist_id=gist_id)

@app.route("/chat-api/<user>/<gist_id>")
def get_bot_response(user, gist_id):
    """Get a bot response based on the user and gist_id"""
    if gist_id in bots or get_bot_from_gist(user, gist_id):
        bot = bots[gist_id]["pairs"]
    else:
        bot = nltk.chat.eliza.eliza_chatbot
    text = request.args.get('text')
    if not text:
        text = ""
    return bot.respond(text)

@app.route("/test/")
def test():
    """A simple route for testing"""
    return "this is a test"

@app.route("/chat/")
def chat():
    """A generic route to load the ELIZA chatbot"""
    return render_template("chat.html",
                           botname="ELIZA",
                           intro="Hello, what would you like to discuss today?",
                           gist_id="")
