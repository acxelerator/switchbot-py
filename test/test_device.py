from unittest.mock import patch

from switchbot_py.device import Device


def test_device_status():
    with patch("switchbot_py.switchbot.SwitchBotClient") as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.get.return_value = {
            "statusCode": 100,
            "body": {
                "deviceId": "device1",
                "deviceType": "Meter",
                "temperature": 25.5,
                "humidity": 60,
            },
        }

        device = Device(
            client=mock_instance,
            device_id="device1",
            device_name="テストメーター",
            device_type="Meter",
            hub_device_id="hub1",
        )

        status = device.get_status()
        assert status["temperature"] == 25.5
        assert status["humidity"] == 60


def test_device_control():
    with patch("switchbot_py.switchbot.SwitchBotClient") as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.post.return_value = {"statusCode": 100, "message": "success"}

        device = Device(
            client=mock_instance,
            device_id="device1",
            device_name="テストプラグ",
            device_type="Plug",
            hub_device_id="hub1",
        )

        # turn_on のテスト
        response = device.turn_on()
        assert response["statusCode"] == 100
        mock_instance.post.assert_called_with(
            f"/v1.1/devices/{device.device_id}/commands",
            {"command": "turnOn", "parameter": "default", "commandType": "command"},
        )

        # モックをリセット
        mock_instance.post.reset_mock()

        # turn_off のテスト
        response = device.turn_off()
        assert response["statusCode"] == 100
        mock_instance.post.assert_called_with(
            f"/v1.1/devices/{device.device_id}/commands",
            {"command": "turnOff", "parameter": "default", "commandType": "command"},
        )
