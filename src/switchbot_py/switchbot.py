import os
from .client import SwitchBotClient
from .device import Device, DeviceDto
from .remote import InfraredRemoteDto, InfraredRemote


class SwitchBot:
    def __init__(self, token: str | None = None, secret: str | None = None):
        if token is None:
            token = os.getenv("SWITCHBOT_TOKEN")
        if secret is None:
            secret = os.getenv("SWITCHBOT_SECRET")
        self._client = SwitchBotClient(token=token, secret=secret)
        self._devices = None
        self._url = "https://api.switch-bot.com/v1.1/devices"

    def get_devices(self) -> list[Device]:
        if self._devices is None:
            self._devices = self._client.get(url=self._url)
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

    def get_device_by(self, device_id: str) -> Device | None:
        if self._devices is None:
            self._devices = self._client.get(url=self._url)
        device_dto = [DeviceDto(**d) for d in self._devices.get("deviceList", {})]
        device = [d for d in device_dto if d.device_id == device_id]
        if len(device) == 0:
            return None
        return Device.from_device_type(
            client=self._client,
            device_type=device[0].device_type,
            device_id=device[0].device_id,
            device_name=device[0].device_name,
            enable_cloud_service=device[0].enable_cloud_service,
            hub_device_id=device[0].hub_device_id,
        )

    def get_infrared_remotes(self) -> list[InfraredRemote]:
        if self._devices is None:
            self._devices = self._client.get(url=self._url)
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

    def get_infrared_remote_by(self, device_id: str) -> InfraredRemote | None:
        if self._devices is None:
            self._devices = self._client.get(url=self._url)
        infrared_remote_dto = [
            InfraredRemoteDto(**d) for d in self._devices.get("infraredRemoteList", {})
        ]
        remote = [r for r in infrared_remote_dto if r.device_id == device_id]
        if len(remote) == 0:
            return None
        return InfraredRemote.from_remote_type(
            client=self._client,
            remote_type=remote[0].remote_type,
            device_id=remote[0].device_id,
            device_name=remote[0].device_name,
            hub_device_id=remote[0].hub_device_id,
        )
