from atlas.events.listener_registry import ListenerRegistry
from atlas.events.event import Event
from atlas.modules.logger import Logger

class EventBus():
    def __init__(self, listener_registry: ListenerRegistry):
        self.listener_registry = listener_registry

    @Logger.log_publish
    def publish(self, event: Event, message: str = ""):
        for subscriber in self.listener_registry.registry:
            if subscriber.event.type == event.type:
                subscriber.callback(event)

    def unsubscribe(self):
        pass

    def subscribe(self):
        self.listener_registry.register