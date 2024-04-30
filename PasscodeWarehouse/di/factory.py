from typing import Type, TypeVar

from injector import Injector

injector = Injector()
T = TypeVar('T')


def get(self, interface: Type[T]) -> T:
    return injector.get(interface)



