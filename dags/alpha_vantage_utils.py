import os
import requests
from airflow.models import Variable

def get_alpha_vantage_api_key():
    """
    Retrieves the Alpha Vantage API key from Airflow Variables.
    """
    api_key = Variable.get("alpha_vantage_api_key", default_var=None)
    if not api_key:
        raise ValueError("Alpha Vantage API key not found in Airflow Variables.")
    return api_key

def retrieve_data(function: str, symbol: str, api_key: str, **kwargs) -> dict:
    """
    Retrieves data from the Alpha Vantage API.

    Args:
        function (str): The API function to call (e.g., 'DIGITAL_CURRENCY_DAILY').
        symbol (str): The symbol of the asset (e.g., 'BTC').
        api_key (str): Your Alpha Vantage API key.
        **kwargs: Additional parameters for the API call.

    Returns:
        dict: The parsed JSON response from the API.
    """
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}'
    for key, value in kwargs.items():
        url += f'&{key}={value}'

    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()

def get_crypto_daily(symbol: str, market: str = 'USD') -> dict:
    """
    Retrieves daily cryptocurrency data from Alpha Vantage.

    Args:
        symbol (str): The cryptocurrency symbol (e.g., 'BTC').
        market (str): The market to convert to (e.g., 'USD').

    Returns:
        dict: The daily cryptocurrency data.
    """
    api_key = get_alpha_vantage_api_key()
    return retrieve_data('DIGITAL_CURRENCY_DAILY', symbol, api_key, market=market)