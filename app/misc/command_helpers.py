from app.classes.command import Command

from app.misc.helpers import (
    parse_message,
)


def get_response(message, amountPinned: float = 0):
    """
    Gets the message send by user and checks the command
    Available commands:
    /add: Will add a new record to database
    /total: Will show how much the last debt is
    /set: Will set the debt amount
    /reset: Resets debt to 0 after paying rent
    /despierta: Wake up the bot, returns message
    /help: Will show some examples
    """
    command, args = parse_message(message)

    command_obj = Command(command, args, amountPinned)
    return command_obj.execute()
