""" Main module for the bot,
containing the API routes to interact with the bot """

import os

import telegram
from flask import Flask, request

from app.classes.debug import Debugger
from app.misc.command_helpers import get_response
from app.misc.exceptions import (
    InvalidCommand,
    NotEnoughtRights,
    UnknownCommand,
)
from app.misc.helpers import (
    retrieve_pinned_message_amount,
)

global bot
global TOKEN

TOKEN = os.getenv("BOT_TOKEN")


# Function to create and return the Telegram Bot instance
def create_bot():
    return telegram.Bot(token=TOKEN)


# start the flask app
app = Flask(__name__)
app.debug = True


@app.route("/setwebhook", methods=["GET", "POST"])
async def set_webhook():
    bot = create_bot()
    s = await bot.setWebhook(os.getenv("URL"))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route("/w4lly-t3l3gram-b0t", methods=["POST"])
async def telegram_message():
    debug = Debugger()
    bot = create_bot()
    debt_amount = 0

    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    try:
        chat_id = update.effective_message.chat.id

        # Telegram understands UTF-8, so encode text for unicode compatibility
        text = update.effective_message.text.encode("utf-8").decode()
        debug.log("got text message :", text)

        chat = await bot.get_chat(chat_id=chat_id)
        if chat.pinned_message:
            pinned_text = chat.pinned_message.text.encode("utf-8").decode()
            debt_amount = retrieve_pinned_message_amount(pinned_text)
        else:
            await bot.sendMessage(
                chat_id=chat_id,
                text="""Revisa el mensaje fijado porque no se ha
                encontrado el mensaje con el total.""",
            )
            await bot.sendMessage(
                chat_id=chat_id,
                text="""Usa el siguiente commando para poner una cantidad
                /set 23.32""",
            )

        messages = get_response(text, debt_amount)
        for message in messages:
            sent_message = await bot.sendMessage(chat_id=chat_id, text=message)

            if "Deuda actual:" in message:
                await bot.pin_chat_message(
                    chat_id=chat_id, message_id=sent_message["message_id"]
                )
                if not chat.pinned_message:
                    return "ok"

                await bot.unpin_chat_message(
                    chat_id=chat_id, message_id=chat.pinned_message.message_id
                )

    except AttributeError as error_message:
        debug.log(error_message)
        debug.log("Received a notification, this is not a message")

    except (
        InvalidCommand,
        NotEnoughtRights,
        UnknownCommand,
    ) as error_message:

        await bot.sendMessage(chat_id=chat_id, text=str(error_message))

    return "ok"


@app.route("/")
def home_view():
    return "<h1>Welcome to Debt_bot</h1>"
