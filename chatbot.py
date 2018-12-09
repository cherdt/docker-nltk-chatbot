from flask import Flask
from flask import request
from flask_cors import CORS
import nltk.chat
from nltk.chat.util import Chat, reflections
app = Flask(__name__)
CORS(app)

with open('./chat.html') as f:
    chat_form_html = f.read()

@app.route("/chat-api")
def what():
    text = request.args.get('text')
    if (not text):
        return "I'm sorry, I didn't understand that."
    bot = nltk.chat.eliza
    return bot.eliza_chatbot.respond(text)

@app.route("/test/")
def test():
    return "this is a test"

@app.route("/chat/")
def chat():
    return chat_form_html
