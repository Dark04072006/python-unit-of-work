from enum import Enum, auto


class ObjectState(Enum):
    CLEAN = auto()
    NEW = auto()
    DIRTY = auto()
    REMOVED = auto()
