from app.classes.command import Command


def test_handle_add():
    command = Command("add", ["RentPayment", "100"], 50)
    result = command.execute()
    assert result == [
        "Nuevo pago agregado a la deuda",
        "Asunto: RentPayment",
        "Cantidad: £100",
        "Deuda actual: £150.0",
    ]


def test_handle_total():
    command = Command("total", "", 200)
    result = command.execute()
    assert result == ["Deuda actual: £200"]


def test_handle_set():
    command = Command("set", ["300"], 200)
    result = command.execute()
    assert result == ["Deuda actual: £300"]


def test_handle_reset():
    command = Command("reset", "", 100)
    result = command.execute()
    assert result == [
        "Alquiler a pagar, £550",
        "Alquiler pagado, deuda reseteada a 0",
        "Deuda actual: £0",
    ]


def test_handle_reset_without_debt():
    command = Command("reset", "", 0)
    result = command.execute()
    assert result == [
        "Alquiler a pagar, £650",
        "Alquiler pagado, deuda reseteada a 0",
        "Deuda actual: £0",
    ]


def test_handle_despierta():
    command = Command("despierta", "", 0)
    result = command.execute()
    assert result == ["Oye! Seras tu el que esta dormido!"]


def test_handle_help():
    command = Command("help", "", 0)
    result = command.execute()
    assert result == [
        "Available commands:",
        "/add: Will add a new record to database",
        "/total: Will show how much the last debt is",
        "/set: Will set the debt amount",
        "/reset: Resets debt to 0 after paying rent",
        "/despierta: Wake up the bot, returns message",
        "/help: Will show this message",
    ]
