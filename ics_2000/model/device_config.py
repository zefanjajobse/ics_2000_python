from typing import Optional


class DeviceConfig:
    def __init__(
        self,
        model_name: str,
        disabled: bool | None = None,
        on_off_function: int | None = None,
        dim_function: int | None = None,
        color_temperature_function: int | None = None,
        max_brightness: int | None = None,
        max_color_temperature: int | None = None,
        index_open: int | None = None,
        index_close: int | None = None,
        index_my: int | None = None,
    ):
        self.disabled = disabled
        self.model_name = model_name
        self.on_off_function = on_off_function
        self.dim_function = dim_function
        self.color_temperature_function = color_temperature_function
        self.max_brightness = max_brightness
        self.max_color_temperature = max_color_temperature
        self.index_open = index_open
        self.index_close = index_close
        self.index_my = index_my
