from dataclasses import dataclass
from typing import Callable
import inspect

from atlas.events.event import EventType

@dataclass
class Subscription():
    event: EventType
    callback: Callable[..., None]

    def notify(self):
        caller = inspect.stack()[1].function
        print(f"[{caller}] triggered event {self.event} -> {self.callback.__name__}")
        self.callback(self.event)