class DeviceData:
    def __init__(
        self,
        home_id: str,
        id: str,
        name: str,
        device: int,
        isGroup: bool,
        status: dict[str, dict[str, int]],
        data: dict[str, dict[str, int]],
    ):
        self.home_id = home_id
        self.id = id
        self.name = name
        self.device = device
        self.isGroup = isGroup
        self.status = status
        self.data = data
