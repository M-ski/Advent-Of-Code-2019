import logging as log
from typing import List
from unittest import TestCase

from shared.int_code_computers.program import Program


class TestProgram1201(TestCase):

    def setUp(self):
        super().setUp()
        log.basicConfig(level=log.DEBUG)

    def test_simple_addition_program(self):
        log.info('Running simple addition test')
        program_code: List[int] = [1, 0, 0, 0, 99]
        expected_mutated_code: List[int] = [2, 0, 0, 0, 99]
        p: Program = Program(program_code)
        p.run()
        # this program once run will mutate the el at pos 0 from 1 to 2:
        self.assertEqual(2, p.state.at(0))
        # and sanity check the entire output
        self.assertEqual(expected_mutated_code, p.state.memory)

    def test_simple_multiplication_program(self):
        log.info('Running simple multiplication test')
        program_code: List[int] = [2, 3, 0, 3, 99]
        expected_mutated_code: List[int] = [2, 3, 0, 6, 99]
        p: Program = Program(program_code)
        p.run()
        # this program multiplies 2 by 3, and inserts that as position 3:
        self.assertEqual(6, p.state.at(3))
        # and sanity check the entire output
        self.assertEqual(expected_mutated_code, p.state.memory)

    def test_simple_multiplication_and_halt_program(self):
        log.info('Running simple multiplication with a halt before the end of the program data array test')
        program_code: List[int] = [2, 4, 4, 5, 99, 0]
        expected_mutated_code: List[int] = [2, 4, 4, 5, 99, 9801]
        p: Program = Program(program_code)
        p.run()
        # this program squares position 4 and stores it in pos 5 (after the program halt) = 99^2 = 9801:
        self.assertEqual(9801, p.state.at(5))
        # and sanity check the entire output
        self.assertEqual(expected_mutated_code, p.state.memory)

    def test_multiple_operations_and_fake_halt(self):
        log.info('Running program with multipe operations and fake halt')
        program_code: List[int] = [1, 1, 1, 4, 99, 5, 6, 0, 99]
        expected_mutated_code: List[int] = [30, 1, 1, 4, 2, 5, 6, 0, 99]
        p: Program = Program(program_code)
        p.run()
        # this program first changes a halt to a multiplication at pos 4, then set 5*6 at pos 0:
        self.assertEqual(2, p.state.at(4))
        self.assertEqual(30, p.state.at(0))
        # and sanity check the entire output
        self.assertEqual(expected_mutated_code, p.state.memory)

    def test_puzzle_example(self):
        program_code: List[int] = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
        expected_mutated_code: List[int] = [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
        p: Program = Program(program_code)
        p.run()
        # and sanity check the entire output
        self.assertEqual(expected_mutated_code, p.state.memory)

    def test_avoid_file_reading(self):
        program_code = [1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 6, 1, 19, 1, 5, 19, 23, 2, 6, 23, 27, 1, 27,
                        5, 31, 2, 9, 31, 35, 1, 5, 35, 39, 2, 6, 39, 43, 2, 6, 43, 47, 1, 5, 47, 51, 2, 9, 51, 55, 1, 5,
                        55, 59, 1, 10, 59, 63, 1, 63, 6, 67, 1, 9, 67, 71, 1, 71, 6, 75, 1, 75, 13, 79, 2, 79, 13, 83,
                        2, 9, 83, 87, 1, 87, 5, 91, 1, 9, 91, 95, 2, 10, 95, 99, 1, 5, 99, 103, 1, 103, 9, 107, 1, 13,
                        107, 111, 2, 111, 10, 115, 1, 115, 5, 119, 2, 13, 119, 123, 1, 9, 123, 127, 1, 5, 127, 131, 2,
                        131, 6, 135, 1, 135, 5, 139, 1, 139, 6, 143, 1, 143, 6, 147, 1, 2, 147, 151, 1, 151, 5, 0, 99,
                        2, 14, 0, 0]
        program_code[1] = 12
        program_code[2] = 2
        p: Program = Program(program_code)
        p.run()
        log.info(p.state)
        self.assertEqual(4484226, p.state.at(0))

    def test_avoid_file_reading_part_2(self):
        program_code = [1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 6, 1, 19, 1, 5, 19, 23, 2, 6, 23, 27, 1, 27,
                        5, 31, 2, 9, 31, 35, 1, 5, 35, 39, 2, 6, 39, 43, 2, 6, 43, 47, 1, 5, 47, 51, 2, 9, 51, 55, 1, 5,
                        55, 59, 1, 10, 59, 63, 1, 63, 6, 67, 1, 9, 67, 71, 1, 71, 6, 75, 1, 75, 13, 79, 2, 79, 13, 83,
                        2, 9, 83, 87, 1, 87, 5, 91, 1, 9, 91, 95, 2, 10, 95, 99, 1, 5, 99, 103, 1, 103, 9, 107, 1, 13,
                        107, 111, 2, 111, 10, 115, 1, 115, 5, 119, 2, 13, 119, 123, 1, 9, 123, 127, 1, 5, 127, 131, 2,
                        131, 6, 135, 1, 135, 5, 139, 1, 139, 6, 143, 1, 143, 6, 147, 1, 2, 147, 151, 1, 151, 5, 0, 99,
                        2, 14, 0, 0]
        program_code[1] = 56
        program_code[2] = 96
        p: Program = Program(program_code)
        p.run()
        log.info(p.state)
        self.assertEqual(19690720, p.state.at(0))
