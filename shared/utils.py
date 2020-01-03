from typing import Callable, List, AnyStr, TypeVar

T = TypeVar('T')


class IO:

    @staticmethod
    def read_lines(x: Callable[[List[AnyStr]], T]) -> T:
        with open('input.txt', 'r') as source:
            return x(source.readlines())

    @staticmethod
    def read_as_one_line(x: Callable[[AnyStr], T]) -> T:
        with open('input.txt', 'r') as source:
            return x(source.read())


class AtomicRef:
    data: T

    def __init__(self):
        self.data = None

    def set(self, data):
        self.data = data
