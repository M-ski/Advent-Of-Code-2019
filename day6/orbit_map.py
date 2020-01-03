from typing import List

from day6.tree import OrbitalTree, Node
import logging as log

from shared.utils import IO


class OrbitDef:
    parent: str
    this: str
    added: bool
    raw_node: Node

    def __init__(self, parent, this):
        self.parent = parent
        self.this = this
        self.added = False
        self.raw_node = Node(this)


def part_1(orbital_tree):
    orbits: List[OrbitDef] = IO.read_lines(
        lambda lines: [OrbitDef(*line.rstrip().split(")")) for line in lines]
    )
    # add all orbits starting at the root orbit
    root_orbit = next(orbit for orbit in orbits if orbit.parent == 'COM')
    root_node = orbital_tree.add_node('COM', root_orbit.this)
    add_all_orbits(lambda current_orbit_name: lambda n: n.parent == current_orbit_name, root_node, orbits)
    # then get orbital information
    log.info("Sum of orbital orders in tree %s. Expected: %s", orbital_tree.orbital_orders(), 42)


def add_all_orbits(filter_for_child, current_orbit, orbits):
    child_orbits: List[OrbitDef] = list(filter(filter_for_child(current_orbit.name), orbits))
    for child_orbit in child_orbits:
        new_node = OrbitalTree.add_node_to(child_orbit.this, current_orbit)
        child_orbit.added = True
        add_all_orbits(filter_for_child, new_node, orbits)


def part_2(orbital_tree):
    path_to_you = orbital_tree.path_to('YOU')
    log.info("path to you is %s", path_to_you)
    path_to_santa = orbital_tree.path_to('SAN')
    log.info("path to santa is %s", path_to_santa)
    pathing = set(path_to_santa).symmetric_difference(set(path_to_you))
    log.info("length of path from you to santa %s", len(pathing) - 2)


def main():
    orbital_tree = OrbitalTree()
    part_1(orbital_tree)
    part_2(orbital_tree)
    log.info(orbital_tree)


def debug():
    orbits = 'COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L'
    orbital_tree = OrbitalTree()
    for orbit in orbits.split(","):
        parent_orbit, child_orbit = orbit.split(")")
        orbital_tree.add_node(parent_orbit, child_orbit)
    log.info("Sum of orbital orders in tree %s. Expected: %s", orbital_tree.orbital_orders(), 42)
    log.info(orbital_tree)


if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    main()
