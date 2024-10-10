from typing import Callable, Generic, List, TypeVar

TEvent = TypeVar('TEvent')

class Subscription(Generic[TEvent]):
    def __init__(self, callback: Callable[[TEvent], None]) -> None:
        self.callback: Callable[[TEvent], None] = callback

class EventSource(Generic[TEvent]):
    def __init__(self) -> None:
        self.subscriptions: List[Subscription[TEvent]] = []

    def subscribe(self, callback: Callable[[TEvent], None]) -> Subscription[TEvent]:
        subscription = Subscription(callback)
        self.subscriptions.append(subscription)
        return subscription

    def unsubscribe(self, subscription: Subscription[TEvent]) -> None:
        self.subscriptions.remove(subscription)

    def publish(self, event: TEvent) -> None:
        for subscription in self.subscriptions:
            subscription.callback(event)