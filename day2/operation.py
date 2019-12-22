import logging as log
from abc import abstractmethod
from typing import Tuple, List, Mapping, Optional


class Operation:
    # Constants
    logger = log.getLogger('Operations')
    op_code = -1
    op_length = -1

    def __init__(self):
        self.validate()
        pass

    @classmethod
    def validate(cls):
        if cls.op_code == -1 or cls.op_length == -1:
            raise RuntimeError("Extending class did not update the op_code or op_length")

    @classmethod
    def get_op_code(cls):
        return cls.op_code

    @abstractmethod
    def compute(self, raw_operations: List[int], index: int) -> Optional[int]:
        pass

    def __get_prog_el_at(self, raw_operations: List[int], index) -> int:
        return raw_operations[index]

    def __get_values_from_prog_at(self, raw_operations: List[int], index) -> Tuple[int, int]:
        return (
            self.__get_prog_el_at(raw_operations, self.__get_prog_el_at(raw_operations, index + 1)),
            self.__get_prog_el_at(raw_operations, self.__get_prog_el_at(raw_operations, index + 2))
        )


class AddOperation(Operation):
    op_code = 1
    op_length = 4

    def compute(self, raw_operations: List[int], index: int) -> Optional[int]:
        (val1, val2) = self.__get_values_from_prog_at(raw_operations, index)
        result_index = self.__get_prog_el_at(raw_operations, index + 3)
        Operation.logger.debug('Adding value: %s to %s into position %s', val1, val2, result_index)
        raw_operations[result_index] = val1 + val2
        return index + AddOperation.op_length


class MultiplyOperation(Operation):
    op_code = 2
    op_length = 4

    def compute(self, raw_operations: List[int], index: int) -> Optional[int]:
        (val1, val2) = self.__get_values_from_prog_at(raw_operations, index)
        result_index = self.__get_prog_el_at(raw_operations, index + 3)
        Operation.logger.debug('Multiplying value: %s with %s into position %s', val1, val2, result_index)
        raw_operations[result_index] = val1 * val2
        return index + self.op_length


class HaltOperation(Operation):
    op_code = 99
    op_length = 1

    def compute(self, raw_operations: List[int], index: int) -> Optional[int]:
        Operation.logger.info("End of program reached, final index was: %s", index)
        return None


class OperationFactory:
    logger = log.getLogger('OperationFactory')

    mappings: List[Tuple[str, Operation]]

    def __init__(self):
        self.mappings = [op for op in {str(op.get_op_code()): op for op in Operation.__subclasses__()}.items()]
        if self.mappings != len(Operation.__subclasses__()):
            raise RuntimeError("Operation Factory found a non-unique op_code in extending classes of Operation")

    def resolve(self, op_code: int, index: int) -> Operation:
        op = [op[1] for op in self.mappings if str(op_code).endswith(op[0])][0]
        if op is None:
            self.logger.error('Something went wrong. Op code was not valid. Current position: %s, Op code was: %s',
                          index, op_code)
            raise RuntimeError(f"Could not find operation with op_code {op_code}")
        return op
