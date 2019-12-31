from unittest import TestCase

from shared.int_code_computers.operations import AddOperation, MultiplyOperation, JumpIfTrueOperation, \
    JumpIfFalseOperation
from shared.int_code_computers.program import Program
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
        memory = [1101, 5, 6, 3]  # 5 + 6 -> 11
        expected_memory = [1101, 5, 6, 11]
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
        memory = [1102, 4, 5, 3]  # 4 x 5 -> 20
        expected_memory = [1102, 4, 5, 20]
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

    def test_jump_if_true_position_mode(self):
        #         0, 1, 2,  3, 4
        memory = [5, 1, 4, 99, 100]
        expected_memory = [5, 1, 4, 99, 100]  # we don't expect any modification of the memory
        expected_end_pointer = 0 + 100
        operation = JumpIfTrueOperation()
        state = State(memory, 0)
        operation.compute(state)
        self.assertEqual(expected_end_pointer, state.index)
        self.assertEqual(expected_memory, state.memory)

    def test_jump_if_true_immediate_mode(self):
        #           0, 1, 2
        memory = [1105, -1, 100]
        expected_memory = [1105, -1, 100]  # we don't expect any modification of the memory
        expected_end_pointer = 0 + 100
        operation = JumpIfTrueOperation()
        state = State(memory, 0)
        operation.compute(state)
        self.assertEqual(expected_end_pointer, state.index)
        self.assertEqual(expected_memory, state.memory)

    def test_jump_if_true_should_not_jump_immediate_mode(self):
        #           0, 1, 2
        memory = [1105, 0, 100]
        expected_memory = [1105, 0, 100]  # we don't expect any modification of the memory
        expected_end_pointer = 0 + 3
        operation = JumpIfTrueOperation()
        state = State(memory, 0)
        operation.compute(state)
        self.assertEqual(expected_end_pointer, state.index)
        self.assertEqual(expected_memory, state.memory)

    def test_jump_if_true_intg_test(self):
        #         0, 1, 2,  3,   4, 5,   6, 7, 8, 8, 10, 11,12,13, 14
        memory = [1, 0, 0, 12, 105, 99, 14, 2, 0, 0, 13, 99, 0, 0, 11]
        expected_pos_12 = 2  # we want the addition to work
        expected_pos_13 = 0  # we don't want the multiplication to happen (jump if true should work)
        program = Program(memory)
        program.run()
        end_state = program.state
        self.assertEqual(expected_pos_12, end_state.at(12))
        self.assertEqual(expected_pos_13, end_state.at(13))

    def test_jump_if_false_position_mode(self):
        #         0, 1, 2, 3,  4,   5
        memory = [6, 5, 4, 99, 100, 0]
        expected_memory = [6, 5, 4, 99, 100, 0]  # we don't expect any modification of the memory
        expected_end_pointer = 0 + 100
        operation = JumpIfFalseOperation()
        state = State(memory, 0)
        operation.compute(state)
        self.assertEqual(expected_end_pointer, state.index)
        self.assertEqual(expected_memory, state.memory)

    def test_jump_if_false_immediate_mode(self):
        #           0, 1, 2
        memory = [1106, 0, 100]
        expected_memory = [1106, 0, 100]  # we don't expect any modification of the memory
        expected_end_pointer = 0 + 100
        operation = JumpIfFalseOperation()
        state = State(memory, 0)
        operation.compute(state)
        self.assertEqual(expected_end_pointer, state.index)
        self.assertEqual(expected_memory, state.memory)

    def test_jump_if_false_should_not_jump_immediate_mode(self):
        #           0, 1, 2
        memory = [1106, -1, 100]
        expected_memory = [1106, -1, 100]  # we don't expect any modification of the memory
        expected_end_pointer = 0 + 3
        operation = JumpIfFalseOperation()
        state = State(memory, 0)
        operation.compute(state)
        self.assertEqual(expected_end_pointer, state.index)
        self.assertEqual(expected_memory, state.memory)