from typing import List


class State:
    memory: List[int]
    mem_length: int
    index: int
    operations: List[List[int]]  # formatted operation sets

    def __init__(self, memory: List[int], start_index=0):
        self.memory = memory
        self.mem_length = len(memory)
        self.index = start_index

    def assign(self, at: int, data: int):
        self.memory[at] = data

    def at(self, index: int) -> int:
        return self.memory[index]

    def current_op(self) -> int:
        return self.at(self.index)

    def is_in_memory(self, loc_to_check: int) -> int:
        return 0 <= loc_to_check < self.mem_length

    def increase_index(self, op_length: int):
        self.index = self.index + op_length

    def __repr__(self):
        return f"State: index: {self.index}. current operation: {self.current_op()}." \
               f"\n *All instructions: {self.memory}"

