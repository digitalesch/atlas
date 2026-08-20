import uuid
from collections.abc import Callable
from dataclasses import dataclass, field

from atlas.events.event import Event


@dataclass
class Subscription:
    event: Event
    callback: Callable[..., None]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
