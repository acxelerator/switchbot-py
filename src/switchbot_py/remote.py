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
    _funcs_to_attach: ClassVar[list[str]] = []

    def __init__(
        self,
        client: SwitchBotClient,
        device_id: str,
        remote_type: str,
        device_name: str | None = None,
        hub_device_id: str | None = None,
    ):
        self._client = client
        self.remote_type = remote_type
        self.device_id = device_id
        self.device_name = device_name
        self.hub_device_id = hub_device_id
        # attach required functions
        for func in self._funcs_to_attach:
            setattr(self, func[1:], getattr(self, func))

    def __init_subclass__(cls):
        if cls._remote_type is not None:
            cls._remote_type_mapping[cls._remote_type] = cls

    @classmethod
    def from_remote_type(
        cls,
        client: SwitchBotClient,
        remote_type: str,
        device_id: str,
        device_name: str | None = None,
        hub_device_id: str | None = None,
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

    def _command(
        self,
        command: str,
        command_type: str | None = None,
        parameter: str | None = None,
    ) -> dict:
        url = f"https://api.switch-bot.com/v1.1/devices/{self.device_id}/commands"
        data = {"command": command}
        if command_type:
            data.update({"commandType": command_type})
        if parameter:
            data.update({"parameter": parameter})
        res = self._client.post(url, data=data)
        return res

    def _turn_on(self):
        self._command(command="turnOn")

    def _turn_off(self):
        self._command(command="turnOff")


class RemoteAirConditioner(InfraredRemote):
    _remote_type = "Air Conditioner"
    _funcs_to_attach = ["_turn_off"]

    def _turn_on_air_conditioner(self, temperature: int, mode: int, fan: int):
        res = self._command(
            command="setAll",
            command_type="command",
            parameter=f"{temperature},{mode},{fan},on",
        )
        return res

    def turn_on_with_cool(self, temperature: int):
        return self._turn_on_air_conditioner(temperature=temperature, mode=2, fan=1)

    def turn_on_with_hot(self, temperature: int):
        return self._turn_on_air_conditioner(temperature=temperature, mode=5, fan=1)


class RemoteLight(InfraredRemote):
    _remote_type = "Light"
    _funcs_to_attach = ["_turn_on", "_turn_off"]


class RemoteDiyTv(InfraredRemote):
    _remote_type = "DIY TV"
    _funcs_to_attach = ["_turn_on", "_turn_off"]
