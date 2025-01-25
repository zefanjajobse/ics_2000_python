import json
from typing import List
import socket
import requests
from .config import API_URL
from .encryption import encrypt
from .model.entity_type import Entity_Type


class Command:
    def __init__(
        self,
        hub_mac: str,
        device_id: int,
        device_function: int,
        value: int | float,
        aes_key: str,
        entity_type: Entity_Type,
        device_functions: List[int | float] = [],
    ):
        self.hub_mac = hub_mac
        self.device_id = device_id
        self.device_function = device_function
        self.value = value
        self.aes_key = aes_key
        self.entity_type = entity_type
        self.device_functions = device_functions

        data_object = {}
        data_object[entity_type.value] = {
            "id": device_id,
            "function": device_function,
            "value": value,
        }

        if entity_type.value == "group":
            data_object["group"]["update_group_members"] = True
            device_functions[device_function] = value
            data_object["group"]["functions"] = device_functions

        encrypted_data = encrypt(json.dumps(data_object), aes_key)
        # data = bytes.fromhex(encrypted_data)
        header = bytearray(43)
        header[0] = 1  # set frame
        header[9:13] = (653213).to_bytes(4, byteorder="little")  # set magic
        header[2] = 128  # set type
        header[41:43] = len(encrypted_data).to_bytes(
            2, byteorder="little"
        )  # set data length
        header[29:33] = device_id.to_bytes(4, byteorder="little")  # set entityId

        # set mac
        mac_buffer = bytes.fromhex(hub_mac)
        for i in range(len(mac_buffer)):
            header[3 + i] = mac_buffer[i]

        self.total_message = bytes(header) + encrypted_data

    def send_to(self, host: str, port: int, send_timeout: int = 10000) -> None:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(send_timeout / 1000)

        try:
            client.sendto(self.total_message, (host, port))
            data, _ = client.recvfrom(1024)
        except socket.timeout:
            raise TimeoutError("Message timed out")
        finally:
            client.close()

    def send_to_cloud(self, email: str, password: str) -> None:
        params = {
            "action": "add",
            "email": email,
            "mac": self.hub_mac,
            "password_hash": password,
            "device_unique_id": "",
            "command": self.to_hex(),
        }

        response = requests.get(f"{API_URL}/command.php", params=params)

        if response.status_code != 200:
            raise Exception(f"Non 200 status returned: {response.status_code}")

    def to_hex(self) -> str:
        return self.total_message.hex()
