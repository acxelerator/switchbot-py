from pydantic import BaseModel, Field
from typing import ClassVar, Type
from .client import SwitchBotClient


class InfraredRemoteDto(BaseModel):
    device_id: str = Field(alias="deviceId")
    device_name: str = Field(alias="deviceName")
    remote_type: str = Field(alias="remoteType")
    hub_device_id: str = Field(alias="hubDeviceId")


class InfraredRemote:
    _remote_type: ClassVar[str]
    _remote_type_mapping: ClassVar[dict[str, Type["InfraredRemote"]]] = {}

    def __init__(
        self,
        client: SwitchBotClient,
        device_id: str,
        remote_type: str,
        device_name: str,
        hub_device_id: str,
    ):
        self._client = client
        self.remote_type = remote_type
        self.device_id = device_id
        self.device_name = device_name
        self.hub_device_id = hub_device_id

    def __init_subclass__(cls):
        if cls._remote_type is not None:
            cls._remote_type_mapping[cls._remote_type] = cls

    @classmethod
    def from_remote_type(
        cls,
        client: SwitchBotClient,
        remote_type: str,
        device_id: str,
        device_name: str,
        hub_device_id: str,
    ):
        device_cls = cls._remote_type_mapping.get(remote_type, InfraredRemote)
        return device_cls(
            client=client,
            remote_type=remote_type,
            device_id=device_id,
            device_name=device_name,
            hub_device_id=hub_device_id,
        )

    def __repr__(self) -> str:
        return f"Remote(type={self._remote_type}, name={self.device_name}, device_id={self.device_id})"


class RemoteAirConditioner(InfraredRemote):
    _remote_type = "Air Conditioner"


class RemoteLight(InfraredRemote):
    _remote_type = "Light"


class RemoteDiyTv(InfraredRemote):
    _remote_type = "DIY TV"
