import logging as log
from typing import Tuple, List


class Operations:
    # Constants
    OP_CODE_ADDITION: int = 1
    OP_CODE_MULTIPLY: int = 2
    OP_CODE_HALT: int = 99
    OP_CODES: List[int] = [OP_CODE_ADDITION, OP_CODE_MULTIPLY, OP_CODE_HALT]
    OP_LENGTH: int = 4

    @staticmethod
    def __get_prog_el_at(raw_operations: List[int], index) -> int:
        return raw_operations[index]

    @staticmethod
    def __get_values_from_prog_at(raw_operations: List[int], index) -> Tuple[int, int]:
        return (
            Operations.__get_prog_el_at(raw_operations, Operations.__get_prog_el_at(raw_operations, index + 1)),
            Operations.__get_prog_el_at(raw_operations, Operations.__get_prog_el_at(raw_operations, index + 2))
        )

    @staticmethod
    def add(raw_operations: List[int], index: int) -> None:
        (val1, val2) = Operations.__get_values_from_prog_at(raw_operations, index)
        result_index = Operations.__get_prog_el_at(raw_operations, index + 3)
        log.debug('Adding value: %s to %s into position %s', val1, val2, result_index)
        raw_operations[result_index] = val1 + val2

    @staticmethod
    def multiply(raw_operations: List[int], index: int) -> None:
        (val1, val2) = Operations.__get_values_from_prog_at(raw_operations, index)
        result_index = Operations.__get_prog_el_at(raw_operations, index + 3)
        log.debug('Multiplying value: %s with %s into position %s', val1, val2, result_index)
        raw_operations[result_index] = val1 * val2

    @staticmethod
    def halt(raw_operations: List[int], index: int) -> None:
        log.info("End of program reached, final index was: %s", index)
        raise RuntimeError("Halt Encountered")

    @staticmethod
    def unrecognised_op_instr(raw_operations: List[int], i) -> None:
        log.error('Something went wrong. Op code was not as expected. Current position: %s, next 4 bits: %s',
                  i, raw_operations[i:i + Operations.OP_LENGTH:1])
        raise RuntimeError("Unexpected Operation")
