from app.misc.constants import POUND_SYMBOL
from app.misc.exceptions import UnknownCommand
from app.misc.helpers import (
    calculate_rent_amount,
    check_message_and_split,
    get_calculation_elements,
)


class Command:

    def __init__(self, command, args, amountPinned: float = 0):
        self.command = command
        self.args = args
        self.amountPinned = amountPinned

    def execute(self):
        if self.command == "add":
            return self._handle_add()
        elif self.command == "total":
            return self._handle_total()
        elif self.command == "set":
            return self._handle_set()
        elif self.command == "reset":
            return self._handle_reset()
        elif self.command == "despierta":
            return self._handle_despierta()
        elif self.command == "help":
            return self._handle_help()
        else:
            raise UnknownCommand(
                """Alguien no sabe lo que escribe...
                No son horas de beber!"""
            )

    def _handle_add(self):
        matter, amount = check_message_and_split(self.args)
        debt = get_calculation_elements(amount, self.amountPinned)
        return [
            "Nuevo pago agregado a la deuda",
            f"Asunto: {matter}",
            f"Cantidad: {POUND_SYMBOL}{amount}",
            f"Deuda actual: {POUND_SYMBOL}{debt}",
        ]

    def _handle_total(self):
        return [f"Deuda actual: {POUND_SYMBOL}{self.amountPinned}"]

    def _handle_set(self):
        return [f"Deuda actual: {POUND_SYMBOL}{self.args[0]}"]

    def _handle_reset(self):
        rentAmountToPay = calculate_rent_amount(self.amountPinned)
        return [
            f"Alquiler a pagar, {POUND_SYMBOL}{rentAmountToPay}",
            "Alquiler pagado, deuda reseteada a 0",
            f"Deuda actual: {POUND_SYMBOL}0",
        ]

    def _handle_despierta(self):
        return ["Oye! Seras tu el que esta dormido!"]

    def _handle_help(self):
        return [
            "Available commands:",
            "/add: Will add a new record to database",
            "/total: Will show how much the last debt is",
            "/set: Will set the debt amount",
            "/reset: Resets debt to 0 after paying rent",
            "/despierta: Wake up the bot, returns message",
            "/help: Will show this message",
        ]
