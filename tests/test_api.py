import os

from fastapi.testclient import TestClient

from api.main import app

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
    assert isinstance(data["dividends"], dict)
    assert len(data["dividends"]) == 1
    assert list(data["dividends"]) == [TEST_NETUID]
    assert len(data["dividends"][TEST_NETUID]) == 1
    assert list(data["dividends"][TEST_NETUID]) == [TEST_HOTKEY]
    assert isinstance(data["dividends"][TEST_NETUID][TEST_HOTKEY], int)


def test_tao_dividends_valid_netuid_missing():
    """Test the API with a valid token and valid parameters, netuid missing."""
    response = client.get(
        "/api/v1/tao_dividends",
        headers={"Authorization": f"Bearer {TEST_TOKEN}"},
        params={"hotkey": TEST_HOTKEY},
    )

    assert response.status_code == 200
    data = response.json()
    assert "netuid" in data and data["netuid"] is None
    assert "hotkey" in data
    assert "dividends" in data
    assert isinstance(data["dividends"], dict)
    assert len(data["dividends"]) >= 1
    assert all(
        isinstance(netuid, int)
        and isinstance(hotkey, str)
        and isinstance(dividend, int)
        for netuid, netuid_values in data["dividends"].items()
        for hotkey, dividend in netuid_values.items()
    )


def test_tao_dividends_valid_hotkey_missing():
    """Test the API with a valid token and valid parameters, hotkey missing."""
    response = client.get(
        "/api/v1/tao_dividends",
        headers={"Authorization": f"Bearer {TEST_TOKEN}"},
        params={"netuid": TEST_NETUID},
    )

    assert response.status_code == 200
    data = response.json()
    assert "netuid" in data
    assert "hotkey" in data and data["hotkey"] is None
    assert "dividends" in data
    assert isinstance(data["dividends"], dict)
    assert len(data["dividends"]) >= 1
    assert all(
        isinstance(netuid, int)
        and isinstance(hotkey, str)
        and isinstance(dividend, int)
        for netuid, netuid_values in data["dividends"].items()
        for hotkey, dividend in netuid_values.items()
    )


def test_tao_dividends_parameters_missing():
    """Test the API with a valid token and parameters missing."""
    response = client.get(
        "/api/v1/tao_dividends",
        headers={"Authorization": f"Bearer {TEST_TOKEN}"},
        params={},
    )

    assert response.status_code == 200
    data = response.json()
    assert "netuid" in data and data["netuid"] is None
    assert "hotkey" in data and data["hotkey"] is None
    assert "dividends" in data
    assert isinstance(data["dividends"], dict)
    assert len(data["dividends"]) >= 1
    assert all(
        isinstance(netuid, int)
        and isinstance(hotkey, str)
        and isinstance(dividend, int)
        for netuid, netuid_values in data["dividends"].items()
        for hotkey, dividend in netuid_values.items()
    )


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
