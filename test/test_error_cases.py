from unittest.mock import patch

import pytest

from switchbot_py.errors import SwitchBotAPIError
from switchbot_py.switchbot import SwitchBot


def test_invalid_token():
    with patch("switchbot_py.switchbot.SwitchBotClient") as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.get.side_effect = SwitchBotAPIError("Invalid token")

        switchbot = SwitchBot(token="invalid_token", secret="test_secret")
        with pytest.raises(SwitchBotAPIError):
            switchbot.get_devices()


def test_network_error():
    with patch("switchbot_py.switchbot.SwitchBotClient") as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.get.side_effect = ConnectionError("Network error")

        switchbot = SwitchBot(token="test_token", secret="test_secret")
        with pytest.raises(ConnectionError):
            switchbot.get_devices()


def test_invalid_device_type():
    with patch("switchbot_py.switchbot.SwitchBotClient") as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.get.return_value = {
            "deviceList": [
                {
                    "deviceId": "device1",
                    "deviceName": "不明なデバイス",
                    "deviceType": "UnknownType",
                    "enableCloudService": True,
                    "hubDeviceId": "",
                }
            ]
        }

        switchbot = SwitchBot(token="test_token", secret="test_secret")
        devices = switchbot.get_devices()
        assert len(devices) == 1
        assert devices[0].device_type == "UnknownType"
