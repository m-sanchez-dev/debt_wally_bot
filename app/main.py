# import everything
import re
from flask import Flask, request
import telegram
from app.credentials import bot_token, bot_user_name, URL

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

# start the flask app
app = Flask(__name__)


def get_response(msg):
    """
    you can place your mastermind AI here
    could be a very basic simple response like ""
    or a complex LSTM network that generate appropriate answer
    """
    return "Aupa!"


@app.route("/{}".format(TOKEN), methods=["POST"])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode("utf-8").decode()
    print("got text message :", text)

    response = get_response(text)
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)

    return "ok"


@app.route("/setwebhook", methods=["GET", "POST"])
def set_webhook():
    s = bot.setWebhook(URL)
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route("/", methods=["POST"])
def another_route():
        # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    dummy_message = 'something'

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
