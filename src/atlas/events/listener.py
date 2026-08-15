from dataclasses import dataclass

from atlas.events.event import Event


@dataclass
class Listener:
    name: str
    events: list[Event]
