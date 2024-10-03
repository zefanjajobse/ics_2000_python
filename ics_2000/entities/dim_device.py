from ..model.device_data import DeviceData
from .switch_device import SwitchDevice
from ..model.device_config import DeviceConfig


class DimDevice(SwitchDevice):
    def __init__(self, hub, device_data: DeviceData, device_config: DeviceConfig):
        super().__init__(hub, device_data, device_config)

        if device_config.dim_function is None:
            raise ValueError(f"Dim function not defined for '{self.device_data.name}'")

    def dim(self, dim_level: int, send_local: bool = True) -> None:
        return self.get_hub().dim_device(
            self.entity_id,
            self.device_config.dim_function,
            dim_level,
            self.is_group,
            send_local,
        )

    def get_dim_level(self) -> int:
        status = self.get_hub().get_device_status(self.entity_id)
        return status[self.device_config.dim_function]
