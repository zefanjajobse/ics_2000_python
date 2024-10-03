from .model.device_config import DeviceConfig


API_URL = "https://trustsmartcloud2.com/ics2000_api"
device_configs: dict[int, DeviceConfig] = {
    1: DeviceConfig(
        model_name="APC3-2300R KAKU 443MHz Smartplug",
        on_off_function=0,
    ),
    2: DeviceConfig(  # DeviceType 2 uses 0 to 15 for dim values
        model_name="KAKU dimmable",
        on_off_function=0,
        dim_function=1,
        max_brightness=15,
    ),
    3: DeviceConfig(
        disabled=True,
        model_name="Actuator",
    ),
    4: DeviceConfig(
        disabled=True,
        model_name="Trust wireless motion detector for outdoor use",
    ),
    5: DeviceConfig(
        disabled=True,
        model_name="Contact sensor",
    ),
    6: DeviceConfig(
        disabled=True,
        model_name="ACDB 7000A doorbell",
    ),
    7: DeviceConfig(
        disabled=True,
        model_name="1 Channel wall control",
    ),
    8: DeviceConfig(
        disabled=True,
        model_name="2 Channel wall control",
    ),
    9: DeviceConfig(
        disabled=True,
        model_name="1 Channel remote control",
    ),
    10: DeviceConfig(
        disabled=True,
        model_name="2 Channel remote control",
    ),
    11: DeviceConfig(
        disabled=True,
        model_name="3 Channel remote control",
    ),
    12: DeviceConfig(
        disabled=True,
        model_name="16 Channel remote control AYCT-102",
    ),
    13: DeviceConfig(
        disabled=True,
        model_name="Wall mounted remote control AYCT_202",
    ),
    14: DeviceConfig(
        disabled=True,
        model_name="Ambient light sensor",
    ),
    15: DeviceConfig(
        disabled=True,
        model_name="Dusk sensor",
    ),
    16: DeviceConfig(
        disabled=True,
        model_name="ARC Remote",
    ),
    17: DeviceConfig(
        disabled=True,
        model_name="ARC Contact sensor",
    ),
    18: DeviceConfig(
        disabled=True,
        model_name="ARC Motion sensor",
    ),
    19: DeviceConfig(
        disabled=True,
        model_name="ARC Smoke sensor",
    ),
    20: DeviceConfig(
        disabled=True,
        model_name="ARC Siren",
    ),
    21: DeviceConfig(
        disabled=True,
        model_name="ACDB 7000B Doorbell",
    ),
    22: DeviceConfig(
        disabled=True,
        model_name="AWMT Buil-in wall switch",
    ),
    23: DeviceConfig(
        disabled=True,
        model_name="Somfy Actuator",
    ),
    24: DeviceConfig(
        model_name="KAKU dimmable lightbulb",
        on_off_function=0,
        dim_function=1,
        max_brightness=15,
    ),
    25: DeviceConfig(
        disabled=True,
        model_name="AGST 8800 KAKU 1 button wireless wall switch",
    ),
    26: DeviceConfig(
        disabled=True,
        model_name="AGST 8802 KAKU 2 button wireless wall switch",
    ),
    27: DeviceConfig(
        disabled=True,
        model_name="BREL Actuator",
    ),
    28: DeviceConfig(
        disabled=True,
        model_name="Contact sensor 2",
    ),
    29: DeviceConfig(
        disabled=True,
        model_name="ARC Keychain remote",
    ),
    30: DeviceConfig(
        disabled=True,
        model_name="ARC Action button",
    ),
    31: DeviceConfig(
        disabled=True,
        model_name="ARC Rotary dimmer",
    ),
    32: DeviceConfig(
        disabled=True,
        model_name="Unkown Zigbee device",
    ),
    33: DeviceConfig(  # 0 for onOff not working, maybe this,
        model_name="Zigbee (ledvance) smart plug",
        on_off_function=3,
    ),
    34: DeviceConfig(  # not tested
        model_name="Dimmable",
        on_off_function=3,
        dim_function=4,
    ),
    35: DeviceConfig(
        model_name="Zigbee RGB Light",
    ),
    36: DeviceConfig(
        model_name="Zigbee (ledvance) dimmable with color temperature",
        on_off_function=3,
        dim_function=4,
        color_temperature_function=9,
    ),
    37: DeviceConfig(
        disabled=True,
        model_name="Zigbee multi purpose dimmer",
    ),
    38: DeviceConfig(
        disabled=True,
        model_name="Zigbee lock",
    ),
    39: DeviceConfig(
        disabled=True,
        model_name="Zigbee light link remote",
    ),
    40: DeviceConfig(
        model_name="KAKU dimmable lightbulb",
        on_off_function=3,
        dim_function=4,
    ),
    41: DeviceConfig(  # same as 33
        model_name="Zigbee (ledvance) smart plug",
        on_off_function=3,
    ),
    42: DeviceConfig(
        disabled=True,
        model_name="Zigbee lekkage sensor",
    ),
    43: DeviceConfig(
        disabled=True,
        model_name="KAKU wireless smoke detector ZSDR-850",
    ),
    44: DeviceConfig(
        disabled=True,
        model_name="Carbon monoxide sensor",
    ),
    45: DeviceConfig(
        disabled=True,
        model_name="Zigbee temperature and humidity sensor",
    ),
    46: DeviceConfig(
        disabled=True,
        model_name="Zigbee light group",
    ),
    47: DeviceConfig(
        disabled=True,
        model_name="Zigbee fire angel sensor",
    ),
    48: DeviceConfig(
        model_name="KAKU group with dimmable lightbulb",
        on_off_function=3,
        dim_function=4,
    ),
    238: DeviceConfig(disabled=True, model_name="P1 Module"),
    240: DeviceConfig(disabled=True, model_name="Alarm Module"),
    241: DeviceConfig(disabled=True, model_name="IPCam Module"),
    242: DeviceConfig(disabled=True, model_name="Geofencing Module"),
    243: DeviceConfig(disabled=True, model_name="System Module"),
}
