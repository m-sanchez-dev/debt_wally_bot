from app.classes.debug import Debugger


def test_debugger_log(capsys):
    debugger = Debugger()
    debugger.log("Hello", "World")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello World"


def test_debugger_log_empty(capsys):
    debugger = Debugger()
    debugger.log()
    captured = capsys.readouterr()
    assert captured.out.strip() == ""


def test_debugger_with_args(capsys):
    number = 10
    debugger = Debugger()
    debugger.log("Hello", number)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello 10"
