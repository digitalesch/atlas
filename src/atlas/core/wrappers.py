import inspect
from datetime import UTC, datetime

from atlas.events.event import Event, EventType
from atlas.events.event_bus import EventBus
from atlas.events.subscription import Subscription


def subscribe(event_type: EventType, message: str = ""):
    def decorator(func):
        func._subscribe_event = Event(event_type, message)  # tag the function
        return func

    return decorator


def auto_register(cls):
    original_init = cls.__init__
    cls._instance_count = 0

    def wrapped_init(self, event_bus: EventBus, *args, **kwargs):
        cls._instance_count += 1
        if cls._instance_count > 1:
            raise RuntimeError(f"{cls.__name__} should only be instantiated once")

        if original_init is not object.__init__:
            original_init(self, event_bus, *args, **kwargs)

        self.event_bus = event_bus

        for name in dir(cls):
            attr = getattr(self, name)
            if callable(attr) and hasattr(attr, "_subscribe_event"):
                event_bus.listener_registry.register(
                    Subscription(event=attr._subscribe_event, callback=attr)
                )

    cls.__init__ = wrapped_init
    return cls


def log_publish(func):
    def wrapper(self, event: Event, *args, **kwargs):
        caller = inspect.stack()[1]
        print(f"[{datetime.now(UTC)}] Publishing {event.type} for [{caller.function}]")
        result = func(self, event, *args, **kwargs)
        print(f"[{datetime.now(UTC)}] Finished {event.type}")

        return result

    return wrapper
