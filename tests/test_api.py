import os

import requests
from unittest.mock import patch
from fastapi.testclient import TestClient

from api.main import app
from api.stake_extrinsic_sentiment import (
    fetch_bittensor_netuid_tweets,
    fetch_chutes_sentiment,
    get_twitter_sentiment,
)

TEST_TOKEN = os.environ["API_AUTH_TOKEN"]
TEST_NETUID = os.environ["NETUID_DEFAULT"]
TEST_HOTKEY = os.environ["HOTKEY_DEFAULT"]

client = TestClient(app)


def test_tao_dividends_valid_complete():
    """Test the API with a valid token and valid complete parameters."""
    response = client.get(
        "/api/v1/tao_dividends",
        headers={"Authorization": f"Bearer {TEST_TOKEN}"},
        params={"netuid": TEST_NETUID, "hotkey": TEST_HOTKEY},
    )

    assert response.status_code == 200
    data = response.json()
    assert "netuid" in data
    assert "hotkey" in data
    assert "dividends" in data
    assert "cached" in data
    assert isinstance(data["dividends"], dict)
    assert len(data["dividends"]) == 1
    assert list(data["dividends"]) == [TEST_NETUID]
    assert len(data["dividends"][TEST_NETUID]) == 1
    assert list(data["dividends"][TEST_NETUID]) == [TEST_HOTKEY]
    assert isinstance(data["dividends"][TEST_NETUID][TEST_HOTKEY], int)
    assert isinstance(data["cached"], bool)


# Note: commented out following tests, because they take a long time and don't do much at the moment
# def test_tao_dividends_valid_netuid_missing():
#     """Test the API with a valid token and valid parameters, netuid missing."""
#     response = client.get(
#         "/api/v1/tao_dividends",
#         headers={"Authorization": f"Bearer {TEST_TOKEN}"},
#         params={"hotkey": TEST_HOTKEY},
#     )
#
#     assert response.status_code == 200
#     data = response.json()
#     assert "netuid" in data and data["netuid"] is None
#     assert "hotkey" in data
#     assert "dividends" in data
#     assert isinstance(data["dividends"], dict)
#     assert len(data["dividends"]) >= 1
#     assert all(
#         isinstance(netuid, int)
#         and isinstance(hotkey, str)
#         and isinstance(dividend, int)
#         for netuid, netuid_values in data["dividends"].items()
#         for hotkey, dividend in netuid_values.items()
#     )
#
#
# def test_tao_dividends_valid_hotkey_missing():
#     """Test the API with a valid token and valid parameters, hotkey missing."""
#     response = client.get(
#         "/api/v1/tao_dividends",
#         headers={"Authorization": f"Bearer {TEST_TOKEN}"},
#         params={"netuid": TEST_NETUID},
#     )
#
#     assert response.status_code == 200
#     data = response.json()
#     assert "netuid" in data
#     assert "hotkey" in data and data["hotkey"] is None
#     assert "dividends" in data
#     assert isinstance(data["dividends"], dict)
#     assert len(data["dividends"]) >= 1
#     assert all(
#         isinstance(netuid, int)
#         and isinstance(hotkey, str)
#         and isinstance(dividend, int)
#         for netuid, netuid_values in data["dividends"].items()
#         for hotkey, dividend in netuid_values.items()
#     )
#
#
# def test_tao_dividends_parameters_missing():
#     """Test the API with a valid token and parameters missing."""
#     response = client.get(
#         "/api/v1/tao_dividends",
#         headers={"Authorization": f"Bearer {TEST_TOKEN}"},
#         params={},
#     )
#
#     assert response.status_code == 200
#     data = response.json()
#     assert "netuid" in data and data["netuid"] is None
#     assert "hotkey" in data and data["hotkey"] is None
#     assert "dividends" in data
#     assert isinstance(data["dividends"], dict)
#     assert len(data["dividends"]) >= 1
#     assert all(
#         isinstance(netuid, int)
#         and isinstance(hotkey, str)
#         and isinstance(dividend, int)
#         for netuid, netuid_values in data["dividends"].items()
#         for hotkey, dividend in netuid_values.items()
#     )


def test_tao_dividends_missing_token():
    """Test the API without an Authorization token (should return 401)."""
    response = client.get(
        "/api/v1/tao_dividends",
        params={"netuid": 1, "hotkey": "test_hotkey"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing token"


def test_tao_dividends_invalid_token():
    """Test the API with an invalid token (should return 401)."""
    response = client.get(
        "/api/v1/tao_dividends",
        headers={"Authorization": "Bearer wrong_token"},
        params={"netuid": 1, "hotkey": "test_hotkey"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing token"


def test_tao_dividends_trade_false():
    """Test the API with the trade parameter set to False."""
    response = client.get(
        "/api/v1/tao_dividends",
        headers={"Authorization": f"Bearer {TEST_TOKEN}"},
        params={"netuid": TEST_NETUID, "hotkey": TEST_HOTKEY, "trade": False},
    )

    assert response.status_code == 200
    data = response.json()
    assert "stake_tx_triggered" in data
    assert data["stake_tx_triggered"] is False


def test_tao_dividends_trade_true():
    """Test the API with the trade parameter set to True."""
    response = client.get(
        "/api/v1/tao_dividends",
        headers={"Authorization": f"Bearer {TEST_TOKEN}"},
        params={"netuid": TEST_NETUID, "hotkey": TEST_HOTKEY, "trade": True},
    )

    assert response.status_code == 200
    data = response.json()
    assert "stake_tx_triggered" in data
    assert data["stake_tx_triggered"] is True


@patch("requests.post")
def test_fetch_bittensor_netuid_tweets(mock_post):
    """Test fetching tweets with a mocked response."""
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = [
        {"text": "Bittensor is amazing!"},
        {"text": "Netuid 18 is the future!"},
    ]

    tweets = fetch_bittensor_netuid_tweets(18)
    assert isinstance(tweets, list)
    assert len(tweets) == 2
    assert "text" in tweets[0]


@patch("requests.post")
def test_fetch_chutes_sentiment(mock_post):
    """Test fetching sentiment with a mocked LLM response."""
    mock_post.return_value.status_code = 200
    mock_post.return_value.text = (
        'data: {"choices": [{"delta": {"content": "85"}}]}\ndata: [DONE]'
    )

    sentiment = fetch_chutes_sentiment("Bittensor is great!")
    assert isinstance(sentiment, int)
    assert -100 <= sentiment <= 100


@patch("api.stake_extrinsic_sentiment.fetch_bittensor_netuid_tweets")
@patch("api.stake_extrinsic_sentiment.fetch_chutes_sentiment")
def test_get_twitter_sentiment(mock_sentiment, mock_tweets):
    """Test sentiment analysis from Twitter data."""
    mock_tweets.return_value = [{"text": "Bittensor is amazing!"}]
    mock_sentiment.return_value = 90

    sentiment = get_twitter_sentiment(18)
    assert isinstance(sentiment, int)
    assert sentiment == 90
