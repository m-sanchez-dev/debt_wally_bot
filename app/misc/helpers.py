""" Module containing helper methods """

import re
from typing import Union

from app.classes.debug import Debugger
from app.misc.constants import VALID_COMMANDS
from app.misc.exceptions import (
    InvalidCommand,
)

debug = Debugger()


def get_elements_from_message(splitted_message) -> Union[str, str]:
    """
    From splitted_message gets the matter (position 0) and
    amount (position 1)
    """
    matter = splitted_message[0]
    amount = splitted_message[1]
    return matter, amount


def check_message_and_split(splitted_message):
    if len(splitted_message) != 2:
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


def parse_message(message):
    """
    Parses the message and returns the command and arguments
    """
    splitted_message = message.split(" ")
    command = splitted_message[0][1:]
    args = splitted_message[1:]
    if command not in VALID_COMMANDS:
        raise InvalidCommand(
            """Alguien no sabe lo que escribe...
            No son horas de beber!"""
        )
    return command, args
