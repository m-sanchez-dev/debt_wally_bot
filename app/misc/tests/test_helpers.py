import pytest
from app.app import app
from app.misc.exceptions import InvalidCommand
from app.misc.helpers import (
    check_message_and_split,
    get_total_from_result,
    retrieve_pinned_message_amount,
)

# Mock token for testing purposes
MOCK_TOKEN = "your_mock_token"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()

    yield client


def test_get_total_from_result():
    result = [1, 2, 3, 4, 5, 6, 7]
    assert get_total_from_result(result) == 7


def test_check_message_and_split():
    # Test case 1: Valid input
    splitted_message = ["/commando", "asunto", "cantidad"]
    assert check_message_and_split(splitted_message) == tuple(["asunto", "cantidad"])

    # Test case 2: Invalid input (missing elements)
    splitted_message = ["/commando", "asunto"]
    with pytest.raises(InvalidCommand):
        check_message_and_split(splitted_message)

    # Test case 3: Invalid input (extra elements)
    splitted_message = ["/commando", "asunto", "cantidad", "extra"]
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
