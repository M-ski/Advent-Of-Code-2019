import logging as log
from typing import List

from shared.int_code_computers.program import Program


def part_1(data: List[int]):
    # part 1: get the output before the rocket's computer caught fire
    data[1] = 95  # noun
    data[2] = 7  # verb
    log.info('Part 1: Constructing program with data: %s', data)
    p: Program = Program(data)
    p.print_instructions()
    p.run()
    log.info('Part 1: Program final output: %s', p.state.at(0))


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
