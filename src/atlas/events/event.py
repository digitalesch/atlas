from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    EMIT = 1
    SUBSCRIBE = 2
    UNSUBSCRIBE = 3
    ERROR = 4
    LOG = 5
    START_BUILD = 6
    END_BUILD = 7


@dataclass
class Event:
    type: EventType
    message: str
