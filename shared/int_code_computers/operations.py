import logging as log
from abc import abstractmethod
from typing import List, Optional, Mapping

from shared.int_code_computers.state import State

# get_inputs constants
IMMEDIATE_MODE = 1
POSITION_MODE = 0
__LOGGER = log.getLogger('Operations-Inputs')


def get_inputs(state: State, num_inputs: int) -> List[Optional[int]]:
    full_codes: List[int] = [int(code) for code in f'{state.current_op():0{num_inputs + 1}}']
    instruction_types = full_codes[0:len(full_codes) - 2:1]
    inputs = []
    input_number = 1
    index = state.index
    __LOGGER.debug('Getting inputs for op at %s, with code: %s', state.current_op(), full_codes)
    for int_type_code in reversed(instruction_types):
        if int_type_code == POSITION_MODE and state.is_in_memory(index + input_number):
            inputs.append(state.at(state.at(index + input_number))
                          if state.is_in_memory(state.at(index + input_number))
                          else None)
        elif int_type_code == IMMEDIATE_MODE and state.is_in_memory(index + input_number):
            inputs.append(state.at(index + input_number)
                          if state.is_in_memory(index + input_number)
                          else None)
        else:
            inputs.append(None)
        input_number = input_number + 1
    return inputs


# root class for operations
class Operation:
    # Constants
    logger = log.getLogger('Operations')
    op_code = -1
    op_length = -1

    def __init__(self):
        self.validate()
        pass

    def validate(self) -> None:
        if self.op_code == -1 or self.op_length == -1:
            raise RuntimeError("Extending class did not update the op_code or op_length")

    @classmethod
    def get_op_code(cls) -> int:
        return cls.op_code

    @classmethod
    def next_op_start(cls, index: int) -> Optional[int]:
        return index + cls.op_length

    @abstractmethod
    def compute(self, state: State):
        pass

    def should_program_continue(self):
        return True


class AddOperation(Operation):
    op_code = 1
    op_length = 4

    def compute(self, state: State):
        val1, val2 = get_inputs(state, self.op_length)[0:2]
        result_index = state.at(state.index + 3)
        self.logger.debug('Adding value: %s to %s into position %s', val1, val2, result_index)
        state.assign(result_index, val1 + val2)
        state.increase_index(self.op_length)


class MultiplyOperation(Operation):
    op_code = 2
    op_length = 4

    def compute(self, state: State):
        val1, val2 = get_inputs(state, self.op_length)[0:2]
        result_index = state.at(state.index + 3)
        self.logger.debug('Multiplying value: %s with %s into position %s', val1, val2, result_index)
        state.assign(result_index, val1 * val2)
        state.increase_index(self.op_length)


class InputOperation(Operation):
    op_code = 3
    op_length = 2

    def compute(self, state: State):
        result_index = state.at(state.index + 1)
        self.logger.debug("Requesting input from user to be stored at position %s in memory", result_index)
        state.assign(result_index, int(input("Input: ")))
        state.increase_index(self.op_length)


class OutputOperation(Operation):
    __logger = log.getLogger('OutputOperation')
    op_code = 4
    op_length = 2

    def compute(self, state: State):
        result_index: int = get_inputs(state, self.op_length)[0]
        self.__logger.info("Output operation, op_ind: %s, val: %s", state.index, result_index)
        state.increase_index(self.op_length)


class JumpSupport:
    op_length = 3

    @staticmethod
    def potentially_execute_jump(logger, state: State, should_jump: bool, jump_to: int):
        if should_jump:
            logger.info('jumping from %s to %s', state.index, jump_to)
            state.index = jump_to
        else:
            logger.debug("not jumping at this point, should_jump=%s", should_jump)
            state.increase_index(JumpSupport.op_length)


class JumpIfTrueOperation(Operation):
    __logger = log.getLogger('JumpIfTrueOperation')
    op_code = 5
    op_length = 3

    def compute(self, state: State):
        should_jump, to_location = get_inputs(state, self.op_length)[0:2]
        JumpSupport.potentially_execute_jump(self.__logger, state, should_jump != 0, to_location)


class JumpIfFalseOperation(Operation):
    __logger = log.getLogger('JumpIfFalseOperation')
    op_code = 6
    op_length = 3

    def compute(self, state: State):
        should_jump, to_location = get_inputs(state, self.op_length)[0:2]
        JumpSupport.potentially_execute_jump(self.__logger, state, should_jump == 0, to_location)


class LessThanOperation(Operation):
    __logger = log.getLogger('LessThanOperation')
    op_code = 7
    op_length = 4

    def compute(self, state: State):
        val_1, val_2 = get_inputs(state, self.op_length)[0:2]
        assignment_index = state.at(state.index + 3)
        if val_1 < val_2:
            self.__logger.info("Values were less than, assigning true to %s", assignment_index)
            state.assign(assignment_index, 1)
        else:
            self.__logger.info("Values were not less than, assigning false to %s", assignment_index)
            state.assign(assignment_index, 0)
        state.increase_index(self.op_length)


class EqualsOperation(Operation):
    __logger = log.getLogger('EqualsOperation')
    op_code = 8
    op_length = 4

    def compute(self, state: State):
        val_1, val_2 = get_inputs(state, self.op_length)[0:2]
        assignment_index = state.at(state.index + 3)
        if val_1 == val_2:
            self.__logger.info("Values were equal, assigning true to %s", assignment_index)
            state.assign(assignment_index, 1)
        else:
            self.__logger.info("Values were not equal than, assigning true to %s", assignment_index)
            state.assign(assignment_index, 0)
        state.increase_index(self.op_length)


class HaltOperation(Operation):
    op_code = 99
    op_length = 1

    def compute(self, state: State):
        Operation.logger.info("End of program reached, final index was: %s", state.index)

    def should_program_continue(self):
        return False


class OperationFactory:
    logger = log.getLogger('OperationFactory')

    mappings: Mapping[str, Operation]

    def __init__(self):
        self.mappings = {str(op.get_op_code()): op() for op in Operation.__subclasses__()}
        if len(self.mappings) != len(Operation.__subclasses__()):
            raise RuntimeError("Operation Factory found a non-unique op_code in extending classes of Operation")

    def resolve(self, state: State, resolve_at_index=-1) -> Operation:
        index = state.index if resolve_at_index == -1 else resolve_at_index
        potential_op_list = [entry for entry in self.mappings.items()
                             if str(state.at(index) if state.is_in_memory(index) else 98)  # 98 is not a valid op code
                             .endswith(entry[0])]
        if len(potential_op_list) is 0:
            self.logger.error('Something went wrong: op_code was not valid. Current position: %s, op_code was: %s',
                              index, state.at(index) if state.is_in_memory(index) else None)
            raise RuntimeError("Could not find operation with op_code " +
                               f"{state.at(index) if state.is_in_memory(index) else None}")
        return potential_op_list[0][1]
