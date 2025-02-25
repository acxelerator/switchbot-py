from switchbot_py.errors import SwitchbotClientError
import pytest
from switchbot_py.client import SwitchBotClient


def test_error():
    with pytest.raises(SwitchbotClientError):
        SwitchBotClient(token=None, secret=None)
    with pytest.raises(SwitchbotClientError):
        SwitchBotClient(token="", secret=None)
    with pytest.raises(SwitchbotClientError):
        SwitchBotClient(token=None, secret="")
