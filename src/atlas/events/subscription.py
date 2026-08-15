import uuid
from dataclasses import dataclass, field
from typing import Callable
import inspect

from atlas.events.event import EventType


@dataclass
class Subscription:
    event: EventType
    callback: Callable[..., None]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def notify(self):
        caller = inspect.stack()[1].function
        print(f"[{caller}] triggered event {self.event} -> {self.callback.__name__}")
        self.callback(self.event)
