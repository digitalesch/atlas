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

    def debug(self):
        for event_type, subscriptions in self.registry.items():

            if not subscriptions:
                continue

            print(f"\n{event_type.name}")

            for subscription in subscriptions.values():
                callback = subscription.callback

                if hasattr(callback, "__self__"):
                    # Bound method
                    owner = callback.__self__.__class__.__name__
                    name = callback.__name__

                else:
                    # Regular function
                    owner = callback.__qualname__.split(".")[0]
                    name = callback.__name__

                print(f"  -> {owner}.{name} " f"[{subscription.id}]")
