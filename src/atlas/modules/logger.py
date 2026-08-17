from atlas.events.event import Event


class Logger:

    @staticmethod
    def teste(event: Event):
        print(f"[Logger] {event.type.name}: {event.message}")
