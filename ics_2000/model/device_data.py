from typing import Dict


class DeviceData:
    def __init__(
        self,
        home_id: str,
        id: str,
        name: str,
        device: int,
        isGroup: bool,
        status: Dict[str, Dict[str, int]],
        data: Dict[str, Dict[str, int]],
    ):
        self.home_id = home_id
        self.id = id
        self.name = name
        self.device = device
        self.isGroup = isGroup
        self.status = status
        self.data = data
