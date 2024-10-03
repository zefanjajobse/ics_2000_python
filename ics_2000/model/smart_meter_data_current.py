from typing import List


class SmartMeterDataCurrent:
    def __init__(
        self,
        power_consumed_low_tariff: float,
        power_consumed: float,
        power_produced_low_tariff: float,
        power_produced: float,
        current_consumption: float,
        current_production: float,
        gas: float,
        raw_data_array: List[float],
    ):
        self.power_consumed_low_tariff = power_consumed_low_tariff
        self.power_consumed = power_consumed
        self.power_produced_low_tariff = power_produced_low_tariff
        self.power_produced = power_produced
        self.current_consumption = current_consumption
        self.current_production = current_production
        self.gas = gas
        self.raw_data_array = raw_data_array
