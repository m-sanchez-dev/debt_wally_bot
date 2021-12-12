""" Main module for the bot, containing the API routes to interact with the bot """
import re
import os

import telegram
from flask import Flask, request

global bot
global TOKEN

TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

# start the flask app
app = Flask(__name__)


@app.route("/setwebhook", methods=["GET", "POST"])
def set_webhook():
    s = bot.setWebhook(os.getenv("URL"))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route("/", methods=["POST"])
def another_route():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    dummy_message = "something"

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode("utf-8").decode()
    print("got text message :", text)

    bot.sendMessage(chat_id=chat_id, text=dummy_message, reply_to_message_id=msg_id)

    return "ok"


@app.route("/")
def home_view():
    return "<h1>Welcome to Debt_bot</h1>"
