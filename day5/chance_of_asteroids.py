from typing import List
import logging as log

from shared.int_code_computers.program import Program


def part1():
    with open('input.txt', 'r') as source:
        program_code: List[int] = list(map(int, source.read().split(",")))
    program = Program(program_code)
    program.print_instructions()
    program.run()
    program.print_instructions()


def main():
    part1()


if __name__ == '__main__':
    log.basicConfig(level=log.DEBUG)
    main()
