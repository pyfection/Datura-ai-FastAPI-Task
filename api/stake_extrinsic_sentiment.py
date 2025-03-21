import json
import os
from datetime import date, timedelta

import requests

from dotenv import load_dotenv

load_dotenv()

DATURA_API_KEY = os.environ.get("DATURA_API_KEY")
CHUTES_API_KEY = os.environ.get("CHUTES_API_KEY")


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


def fetch_chutes_sentiment(text: str) -> int:
    """Return a sentiment based on the given text between -100 (very bad) and 100 (very good)."""
    base = "Return a sentiment score between -100 and +100 (only the score and nothing else) for the following data:"
    url = "https://llm.chutes.ai/v1/chat/completions"
    headers = {
        "Authorization": f"BEARER {CHUTES_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "unsloth/Llama-3.2-3B-Instruct",
        "messages": [{"role": "user", "content": f"{base}\n{text}"}],
        "stream": True,
        "max_tokens": 1024,
        "temperature": 0.5,
    }
    response = requests.post(url, json=payload, headers=headers)

    # Note: response doesn't give a JSON for some reason, which is why I put this workaround.
    lines = response.text.split("data: ")
    content = []
    for line in lines:
        line = line.strip()
        if not line or line == "[DONE]":
            continue
        data = json.loads(line)
        choices = data["choices"]
        content.append("".join([c["delta"]["content"] for c in choices]))
    return int("".join(content))


if __name__ == "__main__":
    # tweets = fetch_bittensor_netuid_tweets(18)
    # for tweet in tweets:
    #     print(tweet["text"])
    #     break
    print(fetch_chutes_sentiment("I'm OK today"))
