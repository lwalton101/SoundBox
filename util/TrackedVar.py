from typing import Callable, Generic, TypeVar

T = TypeVar("T")

class TrackedVar(Generic[T]):
    subscribers: set[Callable[[T], None]]
    __value: T
    def __init__(self, value: T) -> None:
        self.__value = value
        self.subscribers = set()

    def subscribe(self, callback: Callable[[T], None]):
        self.subscribers.add(callback)

    def unsubscribe(self, callback: Callable[[T], None]):
        self.subscribers.remove(callback)

    def set(self, value: T):
        self.__value = value
        for subscriber in self.subscribers:
            subscriber(value)

    def get(self) -> T:
        return self.__value
