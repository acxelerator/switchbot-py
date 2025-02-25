from switchbot_py.errors import SwitchbotClientError
import pytest
from switchbot_py.client import SwitchBotClient
from unittest.mock import patch, MagicMock


def test_error():
    with pytest.raises(SwitchbotClientError):
        SwitchBotClient(token=None, secret=None)
    with pytest.raises(SwitchbotClientError):
        SwitchBotClient(token="", secret=None)
    with pytest.raises(SwitchbotClientError):
        SwitchBotClient(token=None, secret="")


@patch("httpx.get")
def test_get_method(mock_get):
    # モックレスポンスの設定
    mock_response = MagicMock()
    mock_response.json.return_value = {"statusCode": 100, "body": {"test": "data"}}
    mock_get.return_value = mock_response

    # クライアントの初期化
    client = SwitchBotClient(token="test_token", secret="test_secret")

    # GETリクエストのテスト
    result = client.get(url="https://api.switch-bot.com/v1.1/test")

    # 結果の検証
    assert result == {"test": "data"}
    mock_get.assert_called_once()

    # ヘッダーの検証
    headers = mock_get.call_args[1]["headers"]
    assert headers["Authorization"] == "test_token"
    assert headers["Content-Type"] == "application/json"
    assert "sign" in headers
    assert "t" in headers
    assert "nonce" in headers


@patch("httpx.post")
def test_post_method(mock_post):
    # モックレスポンスの設定
    mock_response = MagicMock()
    mock_response.json.return_value = {"statusCode": 100, "body": {"success": True}}
    mock_post.return_value = mock_response

    # クライアントの初期化
    client = SwitchBotClient(token="test_token", secret="test_secret")

    # POSTリクエストのテスト
    test_data = {"command": "turnOn"}
    result = client.post(
        url="https://api.switch-bot.com/v1.1/devices/abc123/commands", data=test_data
    )

    # 結果の検証
    assert result == {"success": True}
    mock_post.assert_called_once()

    # ヘッダーとデータの検証
    call_args = mock_post.call_args
    headers = call_args[1]["headers"]
    assert headers["Authorization"] == "test_token"
    assert call_args[1]["json"] == test_data
