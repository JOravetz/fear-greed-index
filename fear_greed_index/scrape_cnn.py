"""Scrape CNN Fear and Greed Index API"""
__docformat__ = "numpy"

import requests

API_URL = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}


def _get_fear_greed_data() -> dict:
    """Fetches CNN Fear and Greed Index data from API

    Returns
    -------
    dict
        JSON response containing fear and greed index data with all indicators
    """
    response = requests.get(API_URL, headers=_HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()
