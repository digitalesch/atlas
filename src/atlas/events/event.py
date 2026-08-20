from dataclasses import dataclass
from enum import Enum, auto


class EventType(Enum):
    EMIT = auto()
    SUBSCRIBE = auto()
    UNSUBSCRIBE = auto()
    ERROR = auto()
    LOG = auto()
    START_BUILD = auto()
    END_BUILD = auto()
    COMPILE_START = auto()
    COMPILE_END = auto()
    COMPILE_ERROR = auto()


@dataclass
class Event:
    type: EventType
    message: str
    payload: object | None = None
