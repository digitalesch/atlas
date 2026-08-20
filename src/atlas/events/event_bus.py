from atlas.events.event import Event, EventType
from atlas.events.listener_registry import ListenerRegistry
from atlas.events.subscription import Subscription


class EventBus:
    def __init__(self, listener_registry: ListenerRegistry):
        self.listener_registry = listener_registry

    # @Logger.log_publish
    def publish(self, event: Event, message: str = ""):
        for subscriber in self.listener_registry.get_subscribers(event.type):
            subscriber.callback(event)

    def unsubscribe(self, event_type: EventType, sub_id: str):
        self.listener_registry.unregister(
            event_type=event_type, sub_id=sub_id
        )  # O(1), simple, no event_type needed

    def subscribe(self, subscription: Subscription):
        self.listener_registry.register(subscription)
