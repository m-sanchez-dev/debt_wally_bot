import pytest
from app.app import app
from app.misc.exceptions import InvalidCommand, InvalidUser
from app.misc.helpers import (
    calculate_rent_amount,
    check_message_and_split,
    extract_username_and_validate,
    parse_message,
    retrieve_pinned_message_amount,
)


# Mock token for testing purposes
MOCK_TOKEN = "your_mock_token"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()

    yield client


def test_check_message_and_split():
    # Test case 1: Valid input
    splitted_message = ["asunto", "cantidad"]
    assert check_message_and_split(splitted_message) == tuple(["asunto", "cantidad"])

    # Test case 2: Invalid input (missing elements)
    splitted_message = ["asunto"]
    with pytest.raises(InvalidCommand):
        check_message_and_split(splitted_message)

    # Test case 3: Invalid input (extra elements)
    splitted_message = ["asunto", "cantidad", "extra"]
    with pytest.raises(InvalidCommand):
        check_message_and_split(splitted_message)


def test_retrieve_pinned_message_amount():
    # Test case 1: Valid input with number amount
    pinned_message = "The total amount is £10.50"
    assert retrieve_pinned_message_amount(pinned_message) == 10.5

    # Test case 2: Valid input without number amount
    pinned_message = "No number amount in this message."
    assert retrieve_pinned_message_amount(pinned_message) is None

    # Test case 3: Real message
    pinned_message = "Deuda actual: £85.68"
    assert retrieve_pinned_message_amount(pinned_message) == 85.68


def test_calculate_rent_amount():
    # Test case 1: Valid input
    amount_pinned = 100
    assert calculate_rent_amount(amount_pinned) == 550

    # Test case 2: Valid input with zero amount pinned
    amount_pinned = 0
    assert calculate_rent_amount(amount_pinned) == 650

    # Test case 3: Valid input with negative amount pinned
    amount_pinned = -50
    assert calculate_rent_amount(amount_pinned) == 700


def test_extract_username_and_validate():
    # Test case 1: Valid username
    user = {}
    user["username"] = "debt_wally_bot"
    try:
        extract_username_and_validate(user)
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

    # Test case 2: Invalid username
    user = "john@doe"
    with pytest.raises(InvalidUser):
        extract_username_and_validate(user)

    # Test case 3: Empty username
    user = ""
    with pytest.raises(InvalidUser):
        extract_username_and_validate(user)


def test_parse_message():
    # Test case 1: Valid input
    message = "/add asunto cantidad"
    expected_command = "add"
    expected_args = ["asunto", "cantidad"]
    assert parse_message(message) == (expected_command, expected_args)

    # Test case 2: Valid input with no arguments
    message = "/set"
    expected_command = "set"
    expected_args = []
    assert parse_message(message) == (expected_command, expected_args)

    # Test case 3: Valid input with multiple arguments
    message = "/help arg1 arg2 arg3"
    expected_command = "help"
    expected_args = ["arg1", "arg2", "arg3"]
    assert parse_message(message) == (expected_command, expected_args)

    # Test case 4: Raises error on invalid command
    message = "/command arg1 arg2 arg3"
    with pytest.raises(InvalidCommand):
        parse_message(message)
