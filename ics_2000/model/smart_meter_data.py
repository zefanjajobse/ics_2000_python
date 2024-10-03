from typing import Union
from datetime import datetime

Precision = str


class SmartMeterData:
    def __init__(
        self,
        date: Union[datetime, str, int],
        power_consumed_low_tariff: float,
        power_consumed: float,
        power_produced_low_tariff: float,
        power_produced: float,
        gas: float,
        water: float,
    ):
        self.date = date
        self.power_consumed_low_tariff = power_consumed_low_tariff
        self.power_consumed = power_consumed
        self.power_produced_low_tariff = power_produced_low_tariff
        self.power_produced = power_produced
        self.gas = gas
        self.water = water
