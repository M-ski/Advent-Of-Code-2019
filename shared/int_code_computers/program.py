import logging as log
from typing import List

from shared.int_code_computers.operations import Operation, OperationFactory
from shared.int_code_computers.state import State


class Program:
    logger = log.getLogger('Program')
    op_factory = OperationFactory()
    # Instance mappings
    state: State

    def __init__(self, program_instructions: List[int]):
        self.state = State(program_instructions)
        self.__populate_operations()

    def run(self) -> int:
        op = self.__resolve_op()
        while op.should_program_continue():
            op.compute(self.state)
            op = self.__resolve_op()

        return self.state.memory[0]

    def __resolve_op(self):
        return self.op_factory.resolve(self.state)

    def print_instructions(self) -> None:
        self.__populate_operations()
        Program.logger.info('--- Program ---')
        Program.logger.info('%s', str(self.__operations)
                            .replace("], ", "]\n", -1).replace("[[", "[\n[", 1).replace("]]", "]\n]", -1))
        Program.logger.info('---   ---   ---')

    def __populate_operations(self) -> None:
        self.__operations = []
        try :
            self.__add_op_code_pos(self.op_factory.resolve(self.state, 0), 0)
        except RuntimeError:
            self.__operations = [['Error occurred when analysing state, raw state:'], self.state.memory]

    def __add_op_code_pos(self, current_op: Operation, index: int) -> None:
        next_op_start = current_op.next_op_start(index)
        next_op = self.op_factory.resolve(self.state, next_op_start)
        self.__operations.append(self.state.memory[index: next_op_start: 1])
        if next_op.should_program_continue():
            self.__add_op_code_pos(next_op, next_op_start)
        else:
            self.__operations.append(self.state.memory[index::])

    def __repr__(self) -> str:
        return f"{self.state}"
