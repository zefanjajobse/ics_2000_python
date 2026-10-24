import enum
from typing import Literal, Union


class Entity_Type(enum.Enum):
    Module = "module"
    Group = "group"
    Scene = "scene"


EntityType = Literal["module", "group", "scene"]
