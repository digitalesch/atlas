from collections import defaultdict

from atlas.events.event import EventType
from atlas.events.subscription import Subscription


class ListenerRegistry:
    def __init__(self):
        # event_type -> {uuid: Subscription}
        self.registry: dict[EventType, dict[str, Subscription]] = defaultdict(dict)

    def register(self, subscription: Subscription) -> str:
        event_type = subscription.event.type
        self.registry[event_type][subscription.id] = subscription
        return subscription.id

    def unregister(self, event_type: EventType, sub_id: str):
        self.registry[event_type].pop(sub_id, None)  # O(1), no error if missing

    def get_subscribers(self, event_type: EventType):
        return self.registry[event_type].values()  # O(1) lookup, then iterate only relevant subs
