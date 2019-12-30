from unittest import TestCase

from shared.int_code_computers.operations import AddOperation, MultiplyOperation
from shared.int_code_computers.state import State


class TestOperations(TestCase):

    def test_add_position_mode(self):
        memory = [1, 0, 0, 3]  # memory[0] + memory[0] -> 1 + 1 -> 2
        expected_memory = [1, 0, 0, 2]
        expected_end_pointer = 0 + 4
        add_op = AddOperation()
        state = State(memory, 0)
        add_op.compute(state)
        self.assertEqual(expected_end_pointer, state.index)
        self.assertEqual(expected_memory, memory)

    def test_add_position_mode_complex(self):
        memory = [4, 5, 1, 0, 1, 5, 99]  # memory[0] + memory[1] -> 4 + 5 -> 9
        expected_memory = [4, 5, 1, 0, 1, 9, 99]
        expected_end_pointer = 2 + 4
        add_op = AddOperation()
        state = State(memory, 2)
        add_op.compute(state)
        self.assertEqual(expected_end_pointer, state.index)
        self.assertEqual(expected_memory, memory)

    def test_add_immediate_mode(self):
        memory = [11001, 5, 6, 3]  # 5 + 6 -> 11
        expected_memory = [11001, 5, 6, 11]
        expected_end_pointer = 0 + 4
        add_op = AddOperation()
        state = State(memory, 0)
        add_op.compute(state)
        self.assertEqual(expected_end_pointer, state.index)
        self.assertEqual(expected_memory, memory)

    def test_multiply_position_mode(self):
        memory = [2, 0, 3, 3]  # memory[0] x memory[3] -> 2 x 3 -> 6
        expected_memory = [2, 0, 3, 6]
        expected_end_pointer = 0 + 4
        mult_op = MultiplyOperation()
        state = State(memory, 0)
        mult_op.compute(state)
        self.assertEqual(expected_end_pointer, state.index)
        self.assertEqual(expected_memory, memory)

    def test_multiply_immediate_mode(self):
        memory = [11002, 4, 5, 3]  # 4 x 5 -> 20
        expected_memory = [11002, 4, 5, 20]
        expected_end_pointer = 0 + 4
        mult_op = MultiplyOperation()
        state = State(memory, 0)
        mult_op.compute(state)
        self.assertEqual(expected_end_pointer, state.index)
        self.assertEqual(expected_memory, memory)

    def test_multiply_mixed_mode(self):
        memory = [1002, 3, 5, 6, 99, 0, 0]  # memory[3] x 5 -> 6 x 5 -> 30
        expected_memory = [1002, 3, 5, 6, 99, 0, 30]
        expected_end_pointer = 0 + 4
        mult_op = MultiplyOperation()
        state = State(memory, 0)
        mult_op.compute(state)
        self.assertEqual(expected_end_pointer, state.index)
        self.assertEqual(expected_memory, memory)
