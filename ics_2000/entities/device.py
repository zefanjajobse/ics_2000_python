from typing import TYPE_CHECKING
from .entity import Entity
from ..model.device_data import DeviceData
from ..model.device_config import DeviceConfig

if TYPE_CHECKING:
    from ..hub import Hub


class Device(Entity):
    def __init__(
        self, hub: "Hub", device_data: DeviceData, device_config: DeviceConfig
    ):
        super().__init__(
            hub, device_data, "group" in device_data.data and "group" or "module"
        )
        self.device_config = device_config
        """List of device functions"""
        self.disabled = (
            device_config.disabled if device_config.disabled is not None else False
        )
        """If the device can be changed"""
