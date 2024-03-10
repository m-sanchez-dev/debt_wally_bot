""" Module containing helper methods """

import re
from typing import Union

from app.classes.debug import Debugger
from app.misc.constants import POUND_SYMBOL
from app.misc.exceptions import (
    InvalidCommand,
    InvalidUser,
    UnknownCommand,
)

debug = Debugger()


def get_elements_from_message(splitted_message) -> Union[str, str]:
    """
    From splitted_message gets the matter (position 1) and
    amount (position 2)
    """
    matter = splitted_message[1]
    amount = splitted_message[2]
    return matter, amount


def check_message_and_split(splitted_message):
    if len(splitted_message) != 3:
        raise InvalidCommand(
            """No contiene la minima cantidad de elementos:
            /commando asunto cantidad"""
        )

    return get_elements_from_message(splitted_message)


def calculate_new_debt(amount: float, debtAmount: float = 0) -> float:
    """
    Adds debt to the amount
    """
    return debtAmount + amount


def get_calculation_elements(amount, debtAmount: float = 0) -> float:
    """
    Creates all the elements for the new debt calculus
    It also creates all the elements for the query insert
    And calls the insert method
    """
    divide = False

    if "/" in amount:
        amount = float(amount.split("/")[0])
        divide = True

    if divide:
        amount = amount / 2

    calculated_debt = calculate_new_debt(float(amount), debtAmount)

    return calculated_debt


def calculate_rent_amount(amountPinned: float) -> float:
    rentAmount = 650
    return rentAmount - amountPinned


def retrieve_pinned_message_amount(pinned_message) -> float:
    # Define a regular expression pattern to match the number amount
    pattern = r"£([\d.]+)"

    # Use re.search to find the match in the message
    match = re.search(pattern, pinned_message)

    # Extract the matched number amount
    if match:
        number_amount = float(match.group(1))
        debug.log("Extracted number amount:", number_amount)
        return number_amount
    else:
        debug.log("No number amount found in the message.")


def get_response(message, user, amountPinned: float = 0):
    """
    Gets the message send by user and checks the command
    Available commands /add and /show
    /add: Will add a new record to database
    /total: Will show how much the last debt is
    /set: Will set the debt amount
    /reset: Resets debt to 0 after paying rent
    /despierta: Wake up the bot, returns message
    /help: Will show some examples
    """

    splitted_message = message.split(" ")
    command = splitted_message[0]

    messages = []

    if command == "/add":
        # Add new amount
        matter, amount = check_message_and_split(splitted_message)
        debt = get_calculation_elements(amount, amountPinned)
        messages.append("Nuevo pago agregado a la deuda")
        messages.append(f"Asunto: {matter}")
        messages.append(f"Cantidad: {POUND_SYMBOL}{amount}")
        messages.append(f"Deuda actualizada: {POUND_SYMBOL}{debt}")

    elif command == "/total":
        message = f"Deuda actual: {POUND_SYMBOL}{amountPinned}"
        messages.append(message)

    elif command == "/set":
        message = f"Deuda actual: {POUND_SYMBOL}{splitted_message[1]}"
        messages.append(message)

    elif command == "/reset":
        rentAmountToPay = calculate_rent_amount(amountPinned)
        messages.append(f"Alquiler a pagar, {rentAmountToPay}")
        messages.append("Alquiler pagado, deuda reseteada a 0")
        messages.append(f"Deuda actual: {POUND_SYMBOL}0")

    elif command == "/help":
        pass

    elif command == "/despierta":
        message = "Oye! Seras tu el que esta dormido!"
        messages.append(message)
    else:
        raise UnknownCommand(
            """Alguien no sabe lo que escribe...
            No son horas de beber!"""
        )

    return messages


def user_validation(user_to_validate):
    valid_users = ["Trmpy", "Wallyx", "debt_wally_bot"]

    if user_to_validate not in valid_users:
        raise InvalidUser("A tu casa")
