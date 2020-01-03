from typing import List
import logging as log

from shared.int_code_computers.program import Program
from shared.utils import IO


def part1():
    program_code: List[int] = IO.read_as_one_line(lambda line: list(map(int, line.split(","))))
    program = Program(program_code)
    program.print_instructions()
    program.run()
    program.print_instructions()


def main():
    part1()


if __name__ == '__main__':
    log.basicConfig(level=log.DEBUG)
    main()
