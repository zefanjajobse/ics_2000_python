from datetime import datetime
import json
import requests

from ics_2000.exceptions import InvalidAuthException, InvalidHomeException, InvalidMacOrAuthException, NoHomeSelectedException
from .command import Command
from .encryption import decrypt
from .config import API_URL, device_configs
from .entities.color_temperature_device import ColorTemperatureDevice
from .entities.device import Device
from .entities.dim_device import DimDevice
from .entities.switch_device import SwitchDevice
from .model.device_config import DeviceConfig
from .model.device_data import DeviceData
from .model.entity_type import Entity_Type


class Hub:
    """KlikAanKlikUit ICS-2000 Control Station connection info


    Attributes:
        email: Email address of the account connected to the ICS-2000
        password: Password of the account connected to the ICS-2000
    """

    def __init__(self, email: str, password: str):
        self.homes = []
        self.devices: list[
            Device | DimDevice | SwitchDevice | ColorTemperatureDevice
        ] = []
        """List of available devices within the authenticated home"""
        self.aes_key: str | None = None
        """Authentication key"""
        self.mac: str | None = None
        """MAC-Address of the KlikAanKlikUit ICS-2000"""
        self.home_name: str | None = None
        """Name of the home given within KlikAanKlikUit"""
        self.home_id: str | None = None
        """ID of the home"""
        self.email = email
        """Email address of the account connected to the ICS-2000"""
        self.password = password
        """Password of the account connected to the ICS-2000"""
        self.local_address: str | None = None
        """Local IP address when you want to control it locally"""
        self.device_statuses: dict[int, list[int]] = {}
        """Statuses of the devices"""
        self.update_date = datetime.min
        """When the device statuses were last updated"""

    def login(self) -> dict[str, str]:
        """Logs in to the account given"""
        self.homes = []
        response = requests.post(
            f"{API_URL}/account.php",
            {
                "action": "login",
                "email": self.email,
                "password_hash": self.password,
                "device_unique_id": "android",
                "platform": "",
                "mac": "",
            },
        )

        if response.status_code != 200:
            if response.status_code == 401:
                raise InvalidAuthException("Incorrect username or password")
            raise InvalidAuthException(response.content)

        data = response.json()
        if data is not None:
            self.homes = data.get("homes", [])
        return dict([(home.get("home_id"), home.get("home_name"))for home in self.homes])

    def select_home(self, home_id: str) -> None:
        home = next(home for home in self.homes if home.get("home_id") == home_id)
        if home is None:
            raise InvalidHomeException()
        self.aes_key = home.get("aes_key", "")
        self.mac = home.get("mac", "")
        self.home_id = home.get("home_id")
        self.home_name = home.get("home_name")

    def get_raw_devices_data(self, decrypt_data, decrypt_status) -> list:
        if self.aes_key is None or self.mac is None:
            raise InvalidMacOrAuthException()

        device_info = requests.post(
            f"{API_URL}/gateway.php",
            {
                "action": "sync",
                "email": self.email,
                "mac": self.mac,
                "password_hash": self.password,
                "home_id": "",
            },
        )
        data = []
        for device in device_info.json():
            current_device = self.format_device_data(
                device, decrypt_data, decrypt_status
            )
            current_device["isGroup"] = "group" in current_device.keys()

            if (
                "module" in current_device["data"].keys()
                and "info" in current_device["data"]["module"].keys()
                and any(i > 0 for i in current_device["data"]["module"]["info"])
            ):
                data.append(current_device)

            if "group" in current_device["data"].keys():
                current_device["data"]["module"] = current_device["data"]["group"]
                del current_device["data"]["group"]
                data.append(current_device)

        return data

    def get_devices(
        self,
    ) -> list[Device | DimDevice | SwitchDevice | ColorTemperatureDevice]:
        """Gets all devices connected to the hub"""
        if self.home_id is None:
            raise NoHomeSelectedException()

        entities = self.get_raw_devices_data(True, False)
        for device in entities:
            device_data = DeviceData(
                home_id=self.home_id,
                name=device["data"]["module"]["name"],
                id=device["data"]["module"]["id"],
                device=device["data"]["module"]["device"],
                isGroup=device.get("isGroup", False),
                status=device.get("status", {}),
                data=device.get("data", {}),
            )
            device_config = device_configs[device_data.device]
            if device_config is None:
                self.devices.append(
                    SwitchDevice(
                        self,
                        device_data,
                        DeviceConfig(
                            model_name="Unknown device type", on_off_function=0
                        ),
                    )
                )
            elif device_config.color_temperature_function is not None:
                self.devices.append(
                    ColorTemperatureDevice(self, device_data, device_config)
                )

            elif device_config.dim_function is not None:
                self.devices.append(DimDevice(self, device_data, device_config))

            elif device_config.on_off_function is not None:
                self.devices.append(SwitchDevice(self, device_data, device_config))
            else:
                self.devices.append(Device(self, device_data, device_config))
        return self.devices

    def create_command(
        self,
        device_id: int,
        device_function: int,
        value: int | float,
        entity_type: Entity_Type,
    ) -> Command:
        if self.aes_key is None or self.mac is None:
            raise InvalidMacOrAuthException()

        device_functions: list[int | float] = []

        # if entity_type == Entity_Type.Group:
        #     device_functions = self.device_statuses.get(device_id, [])

        return Command(
            self.mac,
            device_id,
            device_function,
            value,
            self.aes_key,
            entity_type,
            device_functions,
        )

    def turn_device_on_off(
        self,
        device_id: int,
        on: bool,
        on_function: int,
        is_group: bool,
        send_local: bool,
    ) -> None:
        """Change to the enabled state of the device"""
        command = self.create_command(
            device_id,
            on_function,
            1 if on else 0,
            Entity_Type.Group if is_group else Entity_Type.Module,
        )
        return self.send_command(command, send_local)

    def send_command(self, command: Command, send_local):
        if send_local:
            return self.send_command_to_hub(command, 2012)
        else:
            return self.send_command_to_cloud(command)

    def send_command_to_hub(self, command: Command, port):
        if self.local_address is None:
            raise ValueError("Local address is not set")

        if not isinstance(port, int):
            raise ValueError("Port needs to be an integer")

        command.send_to(self.local_address, port)

    def send_command_to_cloud(self, command: Command):
        command.send_to_cloud(self.email, self.password)

    def get_device_status(self, device_id: int) -> list[int]:
        current_date = datetime.now()
        update_date = self.update_date
        self.update_date = datetime.now()

        date_difference = (current_date - update_date).total_seconds() * 1000

        if date_difference >= 2000 or len(self.device_statuses) == 0:
            self.updating = True
            self.get_all_device_statuses()
            self.updating = False

        # # Wait till the new data is fetched
        # while self.updating:
        #     await asyncio.sleep(0.1)

        return self.device_statuses.get(device_id, [])

    def get_raw_device_statuses(
        self, decrypt_data: bool, decrypt_status: bool
    ) -> list[dict]:
        device_ids = [int(device.entity_id) for device in self.devices]
        ids_string = json.dumps(device_ids)

        params = {
            "action": "get-multiple",
            "email": self.email,
            "mac": self.mac,
            "password_hash": self.password,
            "home_id": "",
            "entity_id": ids_string,
        }
        status_list = requests.post(
            f"{API_URL}/entity.php",
            params,
        ).json()

        if len(status_list) == 0:
            print(params)
            raise Exception(
                f"Unknown error while fetching device statuses, response json: {status_list}"
            )
        return [
            self.format_device_data(d, decrypt_data, decrypt_status)
            for d in status_list
        ]

    def format_device_data(
        self, data: dict, decrypt_data: bool, decrypt_status: bool
    ) -> dict:
        if self.aes_key is None or self.mac is None:
            raise InvalidMacOrAuthException()

        if decrypt_data:
            data["data"] = json.loads(decrypt(data.get("data", ""), self.aes_key))
        if decrypt_status and data.get("status", None) is not None:
            data["status"] = json.loads(decrypt(data.get("status", ""), self.aes_key))
        return data

    def get_all_device_statuses(self):
        status_list = self.get_raw_device_statuses(False, True)
        for device in status_list:
            json_status = device["status"]
            if "module" in json_status.keys():
                self.device_statuses[device["id"]] = json_status["module"]["functions"]
            elif "group" in json_status.keys():
                self.device_statuses[device["id"]] = json_status["group"]["functions"]
            else:
                Exception("Module or group data not found")

    def change_status(
        self,
        device_id: int,
        device_function: int,
        value: int,
        is_group: bool,
        send_local: bool,
    ):
        command = self.create_command(
            device_id,
            device_function,
            value,
            Entity_Type.Group if is_group else Entity_Type.Module,
        )
        return self.send_command(command, send_local)

    def dim_device(
        self,
        device_id: int,
        dim_function: int,
        dim_level: int,
        is_group: bool,
        send_local: bool,
    ):
        if dim_level < 0 or dim_level > 255:
            raise ValueError(f"Dim level {dim_level} is negative or greater than 255")

        command = self.create_command(
            device_id,
            dim_function,
            dim_level,
            Entity_Type.Group if is_group else Entity_Type.Module,
        )
        return self.send_command(command, send_local)

    def change_color_temperature(
        self,
        device_id: int,
        color_temp_function: int,
        color_temperature: float,
        is_group: bool,
        send_local: bool,
    ):
        if color_temperature < 0 or color_temperature > 600:
            raise ValueError(
                f"Color temperature {color_temperature} is negative or greater than 600"
            )

        command = self.create_command(
            device_id,
            color_temp_function,
            color_temperature,
            Entity_Type.Group if is_group else Entity_Type.Module,
        )
        return self.send_command(command, send_local)

    def generate_devices_json(self, decrypt_data: bool, decrypt_status: bool):
        if not self.aes_key or not self.mac:
            # print('MAC or AES key is null, so logging in!')
            self.login()

        devices = self.get_raw_devices_data(decrypt_data, decrypt_status)
        with open("devices.json", "w") as f:
            json.dump(devices, f, indent=2)

    def generate_device_statuses_json(self, decrypt_data: bool, decrypt_status: bool):
        if not self.aes_key or not self.mac:
            # print('MAC or AES key is null, so logging in!')
            self.login()
            self.get_devices()

        devices = self.get_raw_device_statuses(decrypt_data, decrypt_status)
        with open("statuses.json", "w") as f:
            json.dump(devices, f, indent=2)

    def get_p1_entity_id(self):
        raw_devices_data = self.get_raw_devices_data(True, False)
        p1_entity = next(
            (
                d
                for d in raw_devices_data
                if d.get("data", {}).get("module", {}).get("name") == "P1 Module"
            ),
            None,
        )
        return p1_entity.get("id") if p1_entity else None
