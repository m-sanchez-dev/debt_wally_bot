""" Module containing helper methods """
from typing import Union

from app.classes.database_conection import DatabaseConection
from app.misc.constants import POUND_SYMBOL
from app.misc.exceptions import (
    InvalidCommand,
    InvalidUser,
    NotEnoughtRights,
    UnknownCommand,
)


def get_total_from_result(result) -> int:

    return result[6]


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
            "No contiene la minima cantidad de elementos: /commando asunto cantidad"
        )

    return get_elements_from_message(splitted_message)


def get_actual_debt():
    cuentas_connection = DatabaseConection()
    cuentas_connection.get_last_record()
    result = cuentas_connection.get_result()
    return get_total_from_result(result)


def calculate_new_debt(amount: float) -> float:
    """
    Retrieves the previous debt from the db and
    calculates the new one using the debt
    """
    # Get previous debt
    debt = get_actual_debt()

    new_amount = debt + amount

    return new_amount


def get_calculation_elements(amount, matter, user):
    """
    Creates all the elements for the new debt calculus
    It also creates all the elements for the query insert
    And calls the insert method
    """
    divide = False
    original_amount = amount

    if "/" in amount:
        amount = float(amount.split("/")[0])
        original_amount = amount
        divide = True

    if divide:
        amount = amount / 2

    calculated_debt = calculate_new_debt(float(amount))

    cuentas_connection = DatabaseConection()
    cuentas_connection.save_to_db(
        user, matter, float(original_amount), divide, amount, calculated_debt
    )
    cuentas_connection.close_connection()


def reset_debt(user):
    """
    Creates all the elements for the new debt calculus
    It also creates all the elements for the query insert
    And calls the insert method
    """
    if user == "Wallyx":
        cuentas_connection = DatabaseConection()
        cuentas_connection.save_to_db(user, "Pago-Alquiler", 0, False, 0, 0)
        cuentas_connection.close_connection()
    else:
        raise NotEnoughtRights("Eres muy joven para hacer esa operacion")


def get_response(message, user):
    """
    Gets the message send by user and checks the command
    Available commands /add and /show
    /add: Will add a new record to database
    /total: Will show how much the last debt is
    /reset: Will reset the debt amount
    /despierta: Wake up the bot, returns message
    /help: Will show some examples
    """

    splitted_message = message.split(" ")
    command = splitted_message[0]

    messages = []

    if command == "/add":
        # Add new amount
        matter, amount = check_message_and_split(splitted_message)
        get_calculation_elements(amount, matter, user)
        messages.append("Nuevo pago agregado a la deuda")
        messages.append(f"Asunto: {matter}")
        messages.append(f"Cantidad: {POUND_SYMBOL}{amount}")
        debt = get_actual_debt()
        message = f"Deuda actualizada: {POUND_SYMBOL}{debt}"
        messages.append(message)

    elif command == "/total":
        # Show total amount
        debt = get_actual_debt()
        message = f"Deuda actual: {POUND_SYMBOL}{debt}"
        messages.append(message)

    elif command == "/reset":
        # Adds a new line to reset the debt to 0
        reset_debt(user)
        message = "Alquiler pagado, deuda reseteada a 0"
        messages.append(message)

    elif command == "/help":
        pass

    elif command == "/despierta":
        message = "Oye! Seras tu el que esta dormido!"
        messages.append(message)
    else:
        raise UnknownCommand("Alguien no sabe lo que escribe... No son horas de beber!")

    return messages


def user_validation(user_to_validate):

    valid_users = ["Trmpy", "Wallyx"]

    if user_to_validate not in valid_users:
        raise InvalidUser("A tu casa")