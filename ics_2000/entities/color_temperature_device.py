from typing import TYPE_CHECKING
from ..model.device_data import DeviceData
from .dim_device import DimDevice
from ..model.device_config import DeviceConfig

if TYPE_CHECKING:
    from ..hub import Hub


class ColorTemperatureDevice(DimDevice):
    """Class used for color changeable, dimmable devices"""

    def __init__(
        self, hub: "Hub", device_data: DeviceData, device_config: DeviceConfig
    ):
        super().__init__(hub, device_data, device_config)

        if device_config.color_temperature_function is None:
            raise ValueError(
                f"Color temperature function not defined for '{self.device_data.name}'"
            )

    def change_color_temperature(
        self, color_temperature: float, send_local: bool = True
    ) -> None:
        if self.device_config.color_temperature_function is None:
            return

        return self.get_hub().change_color_temperature(
            self.entity_id,
            self.device_config.color_temperature_function,
            color_temperature,
            self.is_group,
            send_local,
        )

    def get_color_temperature(self) -> float:
        if self.device_config.color_temperature_function is None:
            return 0

        status = self.get_hub().get_device_status(self.entity_id)
        return status[self.device_config.color_temperature_function]
