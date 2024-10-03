from typing import List
from ..model.device_data import DeviceData
from ..model.entity_type import EntityType


class Entity:
    def __init__(self, hub, device_data: DeviceData, entity_type: EntityType):
        self._hub = hub
        self.entity_id = int(device_data.id)
        self.name = device_data.data[entity_type].get("name", "")
        self.device_type = (
            device_data.data[entity_type].get("device", "")
            if "device" in device_data.data[entity_type]
            else entity_type
        )
        self.device_data = device_data
        self.is_group = entity_type == "group"

    def get_status(self) -> List[int]:
        return self._hub.get_device_status(self.entity_id)

    def get_hub(self):
        return self._hub

    def change_status(self, device_function: int, value: int, send_local: bool) -> None:
        self._hub.change_status(
            self.entity_id, device_function, value, self.is_group, send_local
        )
