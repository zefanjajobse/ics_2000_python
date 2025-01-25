from ..model.device_data import DeviceData
from ..model.device_config import DeviceConfig
from .device import Device


class SwitchDevice(Device):
    """Class used for all switch devices"""

    def __init__(self, hub, device_data: DeviceData, device_config: DeviceConfig):
        super().__init__(hub, device_data, device_config)

        if device_config.on_off_function is None:
            raise ValueError(
                f"On/off function not defined for '{self.device_data.name}'"
            )

    def turn_on_off(self, on: bool, send_local: bool = True) -> None:
        """Change the state of the device.

        Args:
          on: new state of the device, True == on.
          send_local: Use the ip_address set on the hub to talk to the device
        """
        if self.device_config.on_off_function is None:
            return
        self.get_hub().turn_device_on_off(
            self.entity_id,
            on,
            self.device_config.on_off_function,
            self.is_group,
            send_local,
        )

    def turn_on(self, send_local: bool = True) -> None:
        """Turn on the device.

        Args:
          send_local: Use the ip_address set on the hub to talk to the device
        """
        if self.device_config.on_off_function is None:
            return
        self.get_hub().turn_device_on_off(
            self.entity_id,
            True,
            self.device_config.on_off_function,
            self.is_group,
            send_local,
        )

    def turn_off(self, send_local: bool = True) -> None:
        """Turn off the device.

        Args:
          send_local: Use the ip_address set on the hub to talk to the device
        """
        if self.device_config.on_off_function is None:
            return
        self.get_hub().turn_device_on_off(
            self.entity_id,
            False,
            self.device_config.on_off_function,
            self.is_group,
            send_local,
        )

    def get_on_status(self) -> bool:
        """Returns true if device is turned on"""
        if self.device_config.on_off_function is None:
            return False
        status = self.get_status()
        return status[self.device_config.on_off_function] == 1
