import os
from datetime import date, timedelta

import requests


DATURA_API_KEY = os.environ.get("DATURA_API_KEY")


def fetch_bittensor_netuid_tweets(netuid: int) -> list[dict]:
    url = "https://apis.datura.ai/twitter"
    headers = {"Authorization": DATURA_API_KEY, "Content-Type": "application/json"}
    today = date.today()
    payload = {
        "query": f"Bittensor netuid {netuid}",
        "blue_verified": False,
        "start_date": (today - timedelta(days=7)).isoformat(),
        "end_date": today.isoformat(),
        "is_image": False,
        "is_quote": False,
        "is_video": False,
        "lang": "en",
        "min_likes": 0,
        "min_replies": 0,
        "min_retweets": 0,
        "sort": "Top",
        "count": 10,
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.status_code)  # ToDo: raise proper error message if not 200
    return response.json()
