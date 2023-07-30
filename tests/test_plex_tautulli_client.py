from unittest.mock import patch, Mock
from src.plex_tautulli_client import Plex


@patch("plex_tautulli_client.requests.get")
def test_check_if_alive(mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {
        "response": {"result": "success", "data": {"connected": True}}
    }
    mock_get.return_value = mock_resp
    plex = Plex()
    assert plex.check_if_alive() is True


@patch("plex_tautulli_client.requests.get")
def test_check_if_alive_fail(mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {
        "response": {"result": "failure", "message": "Error message"}
    }
    mock_get.return_value = mock_resp
    plex = Plex()
    assert plex.check_if_alive() is False


@patch("plex_tautulli_client.requests.get")
def test_get_activity(mock_get):
    mock_resp = Mock()
    data = {"stream_count": 5, "total_bandwidth": 10, "sessions": "some_data"}
    mock_resp.json.return_value = {
        "response": {
            "result": "success",
            "data": data,
        }
    }
    mock_get.return_value = mock_resp
    plex = Plex()
    assert plex.get_activity() == ["5", "10", "some_data"]


@patch("plex_tautulli_client.requests.get")
def test_get_activity_fail(mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {
        "response": {"result": "failure", "message": "Error message"}
    }
    mock_get.return_value = mock_resp
    plex = Plex()
    assert plex.get_activity() is False


@patch("plex_tautulli_client.requests.get")
def test_check_for_update(mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {
        "response": {"result": "success", "data": {"update_available": True}}
    }
    mock_get.return_value = mock_resp
    plex = Plex()
    assert plex.check_for_update() is True


@patch("plex_tautulli_client.requests.get")
def test_check_for_update_fail(mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {
        "response": {"result": "failure", "message": "Error message"}
    }
    mock_get.return_value = mock_resp
    plex = Plex()
    assert plex.check_for_update() is False
