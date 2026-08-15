from functools import wraps
from datetime import datetime
import inspect

from atlas.events.event import Event


class Logger:
    @staticmethod
    def teste(event: Event):
        print(f"Logging {event}")

    @staticmethod
    def log_publish(func):
        @wraps(func)
        def wrapper(self, event: Event, *args, **kwargs):
            caller = inspect.stack()[1]
            print(f"[{datetime.now()}] Publishing {event.type} for [{caller.function}]")
            result = func(self, event, *args, **kwargs)
            print(f"[{datetime.now()}] Finished {event.type}")

            return result

        return wrapper
