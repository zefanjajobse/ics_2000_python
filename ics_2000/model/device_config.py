from typing import Optional


class DeviceConfig:
    def __init__(
        self,
        model_name: str,
        disabled: Optional[bool] = None,
        on_off_function: Optional[int] = None,
        dim_function: Optional[int] = None,
        color_temperature_function: Optional[int] = None,
        max_brightness: Optional[int] = None,
        max_color_temperature: Optional[int] = None,
    ):
        self.disabled = disabled
        self.model_name = model_name
        self.on_off_function = on_off_function
        self.dim_function = dim_function
        self.color_temperature_function = color_temperature_function
        self.max_brightness = max_brightness
        self.max_color_temperature = max_color_temperature
