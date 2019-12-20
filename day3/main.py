import logging as log
from enum import Enum
from functools import reduce
from time import time_ns
from typing import List, Tuple, Optional


class Direction(Enum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'


class Coordinate:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def get_distance_from_another(self, another):
        return abs(self.x - another.x) + abs(self.y - another.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "(x: {}, y: {})".format(self.x, self.y)


class Segment:
    logger = log.getLogger('Segment')
    __vertical_directions = [Direction.UP, Direction.DOWN]
    __horizontal_directions = [Direction.LEFT, Direction.RIGHT]
    direction: Direction
    length: int
    start: Coordinate
    starting_position_along_line: int
    end: Coordinate

    def __init__(self, direction: Direction, length: int, starting_coord: Coordinate, starting_position_on_line: int):
        Segment.logger.debug('Creating new segment with direction: %s, length: %s, starting coord: %s',
                             direction, length, starting_coord)
        self.direction = Direction(direction)
        self.length = length
        self.start = starting_coord
        self.starting_position_along_line = starting_position_on_line
        if self.direction == Direction.UP:
            self.end = Coordinate(0 + starting_coord.x, 1 * self.length + starting_coord.y)
        if self.direction == Direction.DOWN:
            self.end = Coordinate(0 + starting_coord.x, -1 * self.length + starting_coord.y)
        if self.direction == Direction.RIGHT:
            self.end = Coordinate(1 * self.length + starting_coord.x, 0 + starting_coord.y)
        if self.direction == Direction.LEFT:
            self.end = Coordinate(-1 * self.length + starting_coord.x, 0 + starting_coord.y)

    def intersect(self, another) -> Tuple[bool, Optional[Coordinate], Optional[int]]:
        # check if a vertical line intersects with another horizontal line
        if self.direction in Segment.__vertical_directions and another.direction in Segment.__horizontal_directions \
                and min(self.start.y, self.end.y) <= another.start.y <= max(self.start.y, self.end.y) \
                and min(another.start.x, another.end.x) <= self.start.x <= max(another.start.x, another.end.x):
            coordinate = Coordinate(self.start.x, another.start.y)
            combined_distance_to_intercept = self.get_combined_distance_to_intercept(another, coordinate)
            return True, coordinate, combined_distance_to_intercept
        # check if a horizontal line intersects with another vertical line
        elif self.direction in Segment.__horizontal_directions and another.direction in Segment.__vertical_directions \
                and min(self.start.x, self.end.x) <= another.start.x <= max(self.start.x, self.end.x) \
                and min(another.start.y, another.end.y) <= self.start.y <= max(another.start.y, another.end.y):
            coordinate = Coordinate(another.start.x, self.start.y)
            combined_distance_to_intercept = self.get_combined_distance_to_intercept(another, coordinate)
            return True, coordinate, combined_distance_to_intercept
        # otherwise, check if they're vertical and overlapping
        elif self.direction in Segment.__vertical_directions and another.direction in Segment.__vertical_directions:
            if self.start.x == another.start.x:
                coordinate = Coordinate(self.start.x, min([self.start.y, another.start.y, self.end.y, another.end.y]))
                combined_distance_to_intercept = self.get_combined_distance_to_intercept(another, coordinate)
                return True, coordinate, combined_distance_to_intercept
            else:
                return False, None, None
        # and penultimately, check if they're both horizontal and overlapping
        # elif self.direction in Segment.__horizontal_directions and another.direction in Segment.__horizontal_directions:
        #     if self.start.y == another.start.y:
        #         coordinate = Coordinate(self.start.y, min([self.start.x, another.start.x, self.end.x, another.end.x]))
        #         combined_distance_to_intercept = self.get_combined_distance_to_intercept(another, coordinate)
        #         return True, coordinate, combined_distance_to_intercept
        #     else:
        #         return False, None, None
        # finally, generic case of no intercept
        else:
            return False, None, None

    def get_combined_distance_to_intercept(self, another, coordinate):
        return coordinate.get_distance_from_another(self.start) + self.starting_position_along_line + \
               coordinate.get_distance_from_another(another.start) + another.starting_position_along_line

    def __str__(self):
        return "(start: {}, end: {}, direction: {}, length: {})".format(
            self.start, self.end, self.direction, self.length)


class Line:
    logger = log.getLogger('Line')
    relative_pathing: List[Coordinate]
    segments: List[Segment]
    __path: str

    def __init__(self, path_str: str):
        self.__path = path_str
        self.relative_pathing = [Coordinate(0, 0)]
        self.segments = []
        Line.logger.info('Creating Line from paths: %s', path_str)
        line_length = 0
        for path in path_str.split(","):
            segment = Segment(Direction(path[0]), int(path[1::]), self.relative_pathing[-1], line_length)
            self.segments.append(segment)
            self.relative_pathing.append(segment.end)
            line_length = line_length + segment.length

    def get_intercepts(self, another) -> List[Tuple[Coordinate, int]]:
        intercepts = []
        for seg1 in self.segments:
            for seg2 in another.segments:
                intercept_present, coord, length_of_line_till_intercept = seg1.intersect(seg2)
                if intercept_present:
                    Line.logger.debug("Found the intercept %s (length: %s) for:\n * seg: %s \n * and: %s",
                                      coord, length_of_line_till_intercept, seg1, seg2)
                    intercepts.append((coord, length_of_line_till_intercept))
        if intercepts[0][0].x == 0 and intercepts[0][0].y == 0:
            intercepts.pop(0)
        return intercepts

    def intercepts(self, another):
        Line.logger.debug('Seeing if line %s intercepts with line %s', self.__path, another.__path)
        has_intercepts = len(self.get_intercepts(another)) > 0
        Line.logger.debug('Does Line %s intersect with Line %s? Result: %s',
                          self.__path, another.__path, has_intercepts)
        return has_intercepts


def main():
    log.basicConfig(level=log.INFO)
    t1 = time_ns()
    with open('input.txt', 'r') as source:
        path_defs = source.readlines()
    l1 = Line(path_defs[0])
    l2 = Line(path_defs[1])
    intercepts = l1.get_intercepts(l2)
    min_distance_2 = min(map(lambda x: abs(x.x + x.y), [x[0] for x in intercepts]))
    log.info("Min intercept between l1 & l3: %s", min_distance_2)
    log.info("Min combined distance to an intercept: %s", reduce(lambda a, b: a if a[1] < b[1] else b, intercepts)[1])
    t2 = time_ns()
    log.info("Run took :%ss", (t2 - t1) / 1e9)


def debug_help():
    log.basicConfig(level=log.DEBUG)
    s1 = Segment(Direction.UP, 5, Coordinate(0, 0), 1)
    s2 = Segment(Direction.RIGHT, 5, Coordinate(-2, 2), 1)
    s3 = Segment(Direction.LEFT, 6, Coordinate(6, -2), 1)
    s4 = Segment(Direction.UP, 7, Coordinate(-1, -1), 1)
    z1 = s1.intersect(s2)  # true (0,2)
    z2 = s1.intersect(s3)  # false
    z3 = s2.intersect(s4)  # true (-1, 2)
    z4 = s2.intersect(s3)  # false
    z4 = s2.intersect(s3)  # false

    l1 = Line("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51")
    l2 = Line("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")
    intercepts = l1.get_intercepts(l2)

    min_distance_2 = min(map(lambda x: abs(x.x + x.y), [x[0] for x in intercepts]))
    log.info("Min intercept between l1 & l3: %s", min_distance_2)
    log.info("Min combined distance to an intercept: %s", reduce(lambda a, b: a if a[1] < b[1] else b, intercepts)[1])


if __name__ == '__main__':
    main()
