import requests

from common import *
from audit_log import *

def _get(url: str) -> dict:
    """Performs the GET request on a URL

    Args:
        url (str): The URL to request

    Returns:
        dict: The response object or an error
    """
    response = requests.get(
        url,
        # NOTE: this is very insecure and not how it should be done
        headers={"apikey": "JHoerquPvpmVDiqEMHGHpLQiZ35Hm1nD"},
    )
    response.raise_for_status()
    return response.json()


def get_data(from_currency: str, to_currency: str, amount: float) -> any:
    """Get the date from the currency conversion API

    Args:
        from_currency (str): The currency to convert from
        to_currency (str): The currency to convert to
        amount (float): The value to convert

    Returns:
        any: JSON response object or a string
    """
    if not (from_currency and to_currency and amount):
        return "Error: Missing parameters"

    try:
        amount = float(amount)
    except ValueError:
        return "Error: Invalid parameters"

    if from_currency not in CURRENCY_LIST or to_currency not in CURRENCY_LIST:
        return "Error: Invalid parameters"

    if from_currency == to_currency:
        return "Error: Invalid parameters"

    data = _get(
        f"https://api.apilayer.com/exchangerates_data/convert?from={from_currency}&to={to_currency}&amount={amount}"
    )

    return data