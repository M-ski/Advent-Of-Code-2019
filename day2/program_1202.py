import logging as log
from typing import List, Mapping, Callable

from day2.Operations import Operations


class Program:

    # Instance mappings
    raw_operations: List[int]  # the original un-formatted operations
    __op_code_positions: List[int]  # position of each "operation" start
    __operations: List[List[int]]  # formatted operation sets
    program_mappings: Mapping[int, Callable]  # why have else ifs when you can map ints to functions.

    def __init__(self, program_instructions: List[int]):
        arr = program_instructions
        self.raw_operations = arr
        self.__populate_operations()
        self.program_mappings = {
            Operations.OP_CODE_ADDITION: Operations.add,
            Operations.OP_CODE_MULTIPLY: Operations.multiply,
            Operations.OP_CODE_HALT: Operations.halt
        }

    def __populate_operations(self) -> None:
        self.__op_code_positions = list(range(0, len(self.raw_operations), Operations.OP_LENGTH))
        self.__operations = [self.raw_operations[self.__op_code_positions[i]:self.__op_code_positions[i + 1]]
                             for i in range(0, len(self.__op_code_positions) - 1)]

    def run(self) -> None:
        try:
            for op_index in range(0, len(self.raw_operations), Operations.OP_LENGTH):
                self.__print_current_op(op_index)
                operation = self.program_mappings.get(self.raw_operations[op_index], Operations.unrecognised_op_instr)
                operation(self.raw_operations, op_index)
                self.__populate_operations()
        except RuntimeError:
            self.print_instructions()
            log.info("Program completed")

    def print_instructions(self, index: int = None) -> None:
        log.info('--- Program ---')
        log.info('%s', str(self.__operations)
                 .replace("], ", "]\n", -1).replace("[[", "[\n[", 1).replace("]]", "]\n]", -1))
        if index:
            self.__print_current_op(index)
        log.info('---   ---   ---')

    def __print_current_op(self, index: int):
        log.info('Current instruction: %s', self.raw_operations[index:index + Operations.OP_LENGTH:1])

    def __str__(self) -> str:
        return "Original instructions: %s".format(self.raw_operations)


if __name__ == '__main__':
    # load the program data
    with open('input.txt', 'r') as source:
        data: List[int] = list(map(int, source.readline().split(",")))
    # and then mutate the state to match the rocket's computer prior to it catching fire
    data[1] = 12
    data[2] = 2
    log.basicConfig(level=log.DEBUG)
    log.info('Constructing program with data: %s', data)
    p: Program = Program(data)
    p.print_instructions()
    p.run()
    log.info('Program final output: %s', p.raw_operations)
