from pydantic import BaseModel, Field

from typing import ClassVar, Type
from .client import SwitchBotClient


class DeviceDto(BaseModel):
    device_id: str = Field(alias="deviceId")
    device_name: str = Field(alias="deviceName")
    device_type: str = Field(alias="deviceType")
    enable_cloud_service: bool = Field(alias="enableCloudService")
    hub_device_id: str = Field(alias="hubDeviceId")


class Device:
    _device_type: ClassVar[str]
    _device_type_mapping: ClassVar[dict[str, Type["Device"]]] = {}

    def __init__(
        self,
        client: SwitchBotClient,
        device_id: str,
        device_type: str,
        device_name: str,
        enable_cloud_service: bool,
        hub_device_id: str,
    ):
        self._client = client
        self.device_id = device_id
        self.device_type = device_type
        self.device_name = device_name
        self.enable_cloud_service = enable_cloud_service
        self.hub_device_id = hub_device_id

    def __init_subclass__(cls):
        if cls._device_type is not None:
            cls._device_type_mapping[cls._device_type] = cls

    @classmethod
    def from_device_type(
        cls,
        client: SwitchBotClient,
        device_type: str,
        device_id: str,
        device_name: str,
        enable_cloud_service: bool,
        hub_device_id: str,
        **kwargs,
    ):
        device_cls = cls._device_type_mapping.get(device_type, Device)
        return device_cls(
            client=client,
            device_id=device_id,
            device_type=device_type,
            device_name=device_name,
            enable_cloud_service=enable_cloud_service,
            hub_device_id=hub_device_id,
            **kwargs,
        )

    def get_status(self) -> dict:
        url = f"https://api.switch-bot.com/v1.1/devices/{self.device_id}/status"
        return self._client.get(url=url)

    def __repr__(self) -> str:
        return f"Device(type={self._device_type}, name={self.device_name}, device_id={self.device_id})"


class DeviceMeterProCo2(Device):
    _device_type = "MeterPro(CO2)"


class DeviceMotionSensor(Device):
    _device_type = "Motion Sensor"


class DeviceMeter(Device):
    _device_type = "Meter"


class DeviceStripLight(Device):
    _device_type = "Strip Light"


class DeviceHubMini(Device):
    _device_type = "Hub Mini"


class DeviceHub2(Device):
    _device_type = "Hub 2"
