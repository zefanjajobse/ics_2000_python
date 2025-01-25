from typing import List, TYPE_CHECKING

from ..model.device_data import DeviceData
from ..model.entity_type import EntityType

if TYPE_CHECKING:
    from ..hub import Hub


class Entity:
    """Class used for all devices"""

    def __init__(self, hub: "Hub", device_data: DeviceData, entity_type: EntityType):
        self._hub = hub
        """Main hub"""
        self.entity_id = int(device_data.id)
        """ID"""
        self.name = device_data.data[entity_type].get("name", "")
        """Name of the device"""
        self.device_type = (
            device_data.data[entity_type].get("device", "")
            if "device" in device_data.data[entity_type]
            else entity_type
        )
        self.device_data = device_data
        self.is_group = entity_type == "group"

    def get_status(self) -> List[int]:
        return self._hub.get_device_status(self.entity_id)

    def get_hub(self) -> "Hub":
        return self._hub

    def change_status(self, device_function: int, value: int, send_local: bool) -> None:
        self._hub.change_status(
            self.entity_id, device_function, value, self.is_group, send_local
        )
