""" Main module for the bot,
containing the API routes to interact with the bot """

import os

import telegram
from flask import Flask, request

from app.classes.debug import Debugger
from app.misc.exceptions import (
    InvalidCommand,
    InvalidUser,
    NotEnoughtRights,
    UnknownCommand,
)
from app.misc.helpers import get_response, user_validation

global bot
global TOKEN

TOKEN = os.getenv("BOT_TOKEN")


# Function to create and return the Telegram Bot instance
def create_bot():
    return telegram.Bot(token=TOKEN)


# start the flask app
app = Flask(__name__)

debug = Debugger()


@app.route("/setwebhook", methods=["GET", "POST"])
def set_webhook():
    bot = create_bot()
    s = bot.setWebhook(os.getenv("URL"))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route("/w4lly-t3l3gram-b0t", methods=["POST"])
def telegram_message():
    bot = create_bot()
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    debug.log(update)

    try:

        chat_id = update.effective_message.chat.id
        user = update.effective_message.from_user

        username = user["username"]

        user_validation(username)

        # Telegram understands UTF-8, so encode text for unicode compatibility
        text = update.effective_message.text.encode("utf-8").decode()
        debug.log("got text message :", text)
        debug.log("from user :", username)

        messages = get_response(text, username)
        for message in messages:
            bot.sendMessage(chat_id=chat_id, text=message)

    except AttributeError:
        debug.log("Received a notification, this is not a message")

    except (
        InvalidCommand,
        NotEnoughtRights,
        UnknownCommand,
        InvalidUser,
    ) as error_message:

        bot.sendMessage(chat_id=chat_id, text=str(error_message))

    return "ok"


@app.route("/")
def home_view():
    return "<h1>Welcome to Debt_bot</h1>"