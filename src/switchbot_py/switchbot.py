from .client import SwitchBotClient
from .device import Device, DeviceDto
from .remote import InfraredRemoteDto, InfraredRemote


class SwitchBot:
    def __init__(self, token: str, secret: str):
        self._client = SwitchBotClient(token=token, secret=secret)
        self._devices = None

    def devices(self) -> list[Device]:
        url = f"https://api.switch-bot.com/v1.1/devices"
        if self._devices is None:
            self._devices = self._client.get(url=url)
        device_dto = [DeviceDto(**d) for d in self._devices.get("deviceList", {})]
        return [
            Device.from_device_type(
                client=self._client,
                device_type=d.device_type,
                device_id=d.device_id,
                device_name=d.device_name,
                enable_cloud_service=d.enable_cloud_service,
                hub_device_id=d.hub_device_id,
            )
            for d in device_dto
        ]

    def infrared_remotes(self) -> list[InfraredRemote]:
        url = f"https://api.switch-bot.com/v1.1/devices"
        if self._devices is None:
            self._devices = self._client.get(url=url)
        infrared_remote_dto = [
            InfraredRemoteDto(**d) for d in self._devices.get("infraredRemoteList", {})
        ]
        return [
            InfraredRemote.from_remote_type(
                client=self._client,
                remote_type=r.remote_type,
                device_id=r.device_id,
                device_name=r.device_name,
                hub_device_id=r.hub_device_id,
            )
            for r in infrared_remote_dto
        ]
