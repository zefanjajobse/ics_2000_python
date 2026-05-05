from ..model import device_data
from ..model.device_config import DeviceConfig
from .device import Device


class BlindDevice(Device):
    def __init__(self, hub, device_data: device_data.DeviceData, device_config: DeviceConfig):
        super().__init__(hub, device_data, device_config)

        if device_config.index_open is None:
            raise ValueError(
                f"index_open not defined for '{self.device_data.name}'"
            )
        if device_config.index_close is None:
            raise ValueError(
                f"index_close not defined for '{self.device_data.name}'"
            )
        if device_config.index_my is None:
            raise ValueError(
                f"index_my not defined for '{self.device_data.name}'"
            )

    def open(self, send_local: bool = False) -> None:
        """Turn off the device.

        Args:
          send_local: Use the ip_address set on the hub to talk to the device
          send_local set to false, because it triggers a time out.
        """
        if self.device_config.index_open is None:
            return

        self.get_hub().change_status(
            self.entity_id,
            self.device_config.index_open,
            0,
            self.is_group,
            send_local,
        )

    def close(self, send_local: bool = False) -> None:
        """Turn off the device.

        Args:
          send_local: Use the ip_address set on the hub to talk to the device
          send_local set to false, because it triggers a timeout.
        """
        if self.device_config.index_close is None:
            return

        self.get_hub().change_status(
            self.entity_id,
            self.device_config.index_close,
            0,
            self.is_group,
            send_local,
        )
    def stop(self, send_local: bool = False) -> None:
        """Turn off the device.

        Args:
          send_local: Use the ip_address set on the hub to talk to the device
          send_local set to false, because it triggers a timeout.
        """
        if self.device_config.index_my is None:
            return

        self.get_hub().change_status(
            self.entity_id,
            self.device_config.index_my,
            0,
            self.is_group,
            send_local,
        )
