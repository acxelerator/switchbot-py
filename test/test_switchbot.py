from unittest.mock import patch
from switchbot_py.switchbot import SwitchBot
from switchbot_py.device import Device


def test_get_devices():
    with patch("switchbot_py.switchbot.SwitchBotClient") as mock_client:
        # クライアントのモック設定
        mock_instance = mock_client.return_value
        mock_instance.get.return_value = {
            "deviceList": [
                {
                    "deviceId": "device1",
                    "deviceName": "テスト機器1",
                    "deviceType": "Hub",
                    "enableCloudService": True,
                    "hubDeviceId": "",
                },
                {
                    "deviceId": "device2",
                    "deviceName": "テスト機器2",
                    "deviceType": "Meter",
                    "enableCloudService": True,
                    "hubDeviceId": "device1",
                },
            ]
        }

        # SwitchBotインスタンスの作成とテスト
        switchbot = SwitchBot(token="test_token", secret="test_secret")
        devices = switchbot.get_devices()

        # 結果の検証
        assert len(devices) == 2
        assert isinstance(devices[0], Device)
        assert devices[0].device_id == "device1"
        assert devices[1].device_name == "テスト機器2"

        # キャッシュのテスト - 2回目の呼び出しではAPIが呼ばれないはず
        mock_instance.get.reset_mock()
        devices = switchbot.get_devices()
        assert len(devices) == 2
        mock_instance.get.assert_not_called()


def test_get_device_by():
    with patch("switchbot_py.switchbot.SwitchBotClient") as mock_client:
        # クライアントのモック設定
        mock_instance = mock_client.return_value
        mock_instance.get.return_value = {
            "deviceList": [
                {
                    "deviceId": "device1",
                    "deviceName": "テスト機器1",
                    "deviceType": "Hub",
                    "enableCloudService": True,
                    "hubDeviceId": "",
                },
                {
                    "deviceId": "device2",
                    "deviceName": "テスト機器2",
                    "deviceType": "Meter",
                    "enableCloudService": True,
                    "hubDeviceId": "device1",
                },
            ]
        }

        # SwitchBotインスタンスの作成とテスト
        switchbot = SwitchBot(token="test_token", secret="test_secret")

        # 存在するデバイスの取得
        device = switchbot.get_device_by(device_id="device2")
        assert device is not None
        assert device.device_id == "device2"
        assert device.device_name == "テスト機器2"

        # 存在しないデバイスの取得
        device = switchbot.get_device_by(device_id="non_existent")
        assert device is None


def test_environment_variables():
    with (
        patch("os.getenv") as mock_getenv,
        patch("switchbot_py.switchbot.SwitchBotClient") as mock_client,
    ):
        # 環境変数のモック
        mock_getenv.side_effect = lambda key: {
            "SWITCHBOT_TOKEN": "env_token",
            "SWITCHBOT_SECRET": "env_secret",
        }.get(key)

        # SwitchBotインスタンスの作成
        switchbot = SwitchBot()  # 引数なしで環境変数から取得

        # 正しいトークンとシークレットでクライアントが初期化されたか確認
        mock_client.assert_called_once_with(token="env_token", secret="env_secret")
