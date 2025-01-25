from typing import TYPE_CHECKING
from ..model.device_data import DeviceData
from .switch_device import SwitchDevice
from ..model.device_config import DeviceConfig

if TYPE_CHECKING:
    from ..hub import Hub


class DimDevice(SwitchDevice):
    """Class used for all dimmable devices"""

    def __init__(
        self, hub: "Hub", device_data: DeviceData, device_config: DeviceConfig
    ):
        super().__init__(hub, device_data, device_config)

        if device_config.dim_function is None:
            raise ValueError(f"Dim function not defined for '{self.device_data.name}'")

    def dim(self, dim_level: int, send_local: bool = True) -> None:
        """Change the dim level of the device.

        Args:
          dim_level: new dim level (0-255).
          send_local: Use the ip_address set on the hub to talk to the device
        """
        if self.device_config.dim_function is None:
            return

        return self.get_hub().dim_device(
            self.entity_id,
            self.device_config.dim_function,
            dim_level,
            self.is_group,
            send_local,
        )

    def get_dim_level(self) -> int:
        """Get the dim level of a device

        Returns:
        Current dim level (0-255)."""
        if self.device_config.dim_function is None:
            return 0

        status = self.get_hub().get_device_status(self.entity_id)
        return status[self.device_config.dim_function]
