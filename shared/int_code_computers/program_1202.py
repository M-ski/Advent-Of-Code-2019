import logging as log
from typing import List

from shared.int_code_computers.operations import Operations, HaltProgram, OP_MAPPINGS


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
