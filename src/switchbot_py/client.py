import base64
import hashlib
import hmac
import os
import time
import uuid

import httpx

TOKEN = os.getenv("TOKEN")
SECRET = os.getenv("SECRET")


class SwitchBotClient:
    def __init__(self, token: str, secret: str):
        self.token = token
        self.secret = secret

    def _generate_switchbot_headers(self) -> dict:
        # see: https://github.com/OpenWonderLabs/SwitchBotAPI?tab=readme-ov-file#python-3-example-code
        nonce = uuid.uuid4()
        t = int(round(time.time() * 1000))
        string_to_sign = f"{self.token}{t}{nonce}"
        string_to_sign = bytes(string_to_sign, "utf-8")
        secret = bytes(self.secret, "utf-8")
        sign = base64.b64encode(
            hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest()
        )

        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
            "charset": "utf8",
            "t": str(t),
            "sign": str(sign, "utf-8"),
            "nonce": str(nonce),
        }
        return headers

    def get(self, url: str) -> dict:
        headers = self._generate_switchbot_headers()
        response = httpx.get(url, headers=headers)
        response_body = response.json()["body"]
        return response_body

    def post(self, url: str, data: dict) -> dict:
        headers = self._generate_switchbot_headers()
        response = httpx.post(url, headers=headers, json=data)
        response_body = response.json()["body"]
        return response_body
