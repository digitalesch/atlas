from atlas.events.subscription import Subscription

class ListenerRegistry:
    def __init__(self):
        self.registry: list[Subscription] = []

    def register(self, subscription: Subscription):
        for existing in self.registry:
            if (existing.event.type == subscription.event.type
                    and existing.callback == subscription.callback):
                return  # already registered, skip silently (or log a warning)
        self.registry.append(subscription)