import logging as log
from typing import List

from day2.Operations import Operations, HaltProgram, OP_MAPPINGS


class Program:
    logger = log.getLogger('Program')
    # Instance mappings
    memory: List[int]  # the original un-formatted operations
    __op_code_positions: List[int]  # position of each "operation" start
    __operations: List[List[int]]  # formatted operation sets

    def __init__(self, program_instructions: List[int]):
        arr = program_instructions
        self.memory = arr
        self.__op_code_positions = self.__get_op_code_positions()
        self.__populate_operations()

    def run(self) -> int:
        try:
            for op_index in self.__get_op_code_positions():
                self.__print_current_op(op_index)
                operation = OP_MAPPINGS.get(self.memory[op_index], Operations.unrecognised_op_instr)
                operation(self.memory, op_index)
        except HaltProgram:
            self.print_instructions()
            Program.logger.info("Program completed")
        return self.memory[0]

    def print_instructions(self, index: int = None) -> None:
        self.__populate_operations()
        Program.logger.info('--- Program ---')
        Program.logger.info('%s', str(self.__operations)
                            .replace("], ", "]\n", -1).replace("[[", "[\n[", 1).replace("]]", "]\n]", -1))
        if index:
            self.__print_current_op(index)
        Program.logger.info('---   ---   ---')

    def __print_current_op(self, index) -> None:
        Program.logger.debug('Current instruction: %s', self.memory[index:index + Operations.OP_LENGTH:1])

    def __get_op_code_positions(self) -> List[int]:
        return list(range(0, len(self.memory), Operations.OP_LENGTH))

    def __populate_operations(self) -> None:
        self.__operations = [self.memory[self.__op_code_positions[i]:self.__op_code_positions[i + 1]]
                             for i in range(0, len(self.__op_code_positions) - 1)]

    def __str__(self) -> str:
        return "Original instructions: %s".format(self.memory)


def part_1(data: List[int]):
    # part 1: get the output before the rocket's computer caught fire
    data[1] = 95  # noun
    data[2] = 7  # verb
    log.info('Part 1: Constructing program with data: %s', data)
    p: Program = Program(data)
    p.print_instructions()
    p.run()
    log.info('Part 1: Program final output: %s', p.memory[0])


def part_2(data: List[int]):
    hoped_for_value: int = 19690720
    result_found = False
    # hoped_for_value: int = 34551522
    for noun in range(100):
        if result_found:
            break
        for verb in range(100):
            test_data = data.copy()
            test_data[1:3] = [noun, verb]
            result: int = Program(test_data).run()
            log.info('-------------------------------------------------------------------')
            if result == hoped_for_value:
                result_found = True
                log.info('Found values to look for in part 2. Noun: %s, Verb: %s', noun, verb)
                log.info('Calculated result of part 2 question: %s', 100 * noun + verb)
                break
            else:
                log.info('Attempted Noun:%s, Verb:%s - program did not yield hoped for value', noun, verb)


def main():
    # load the program data
    with open('input.txt', 'r') as source:
        data: List[int] = list(map(int, source.readline().split(",")))
    part_1(data.copy())
    part_2(data.copy())


if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    main()
