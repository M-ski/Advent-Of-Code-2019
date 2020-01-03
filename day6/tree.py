from typing import Any, Optional, List, TypeVar, Callable
import logging as log

from shared.utils import AtomicRef

T = TypeVar('T')


class NoNodeFoundException(RuntimeError):

    def __init__(self, error_msg):
        super().__init__(error_msg)


class Node:
    children: List[Any]
    name: str
    orbital_order: int

    def __init__(self, name, orbital_order=0):
        self.children = []
        self.name = name
        self.orbital_order = orbital_order

    def add(self, child):
        self.children.append(child)

    def has_children(self) -> bool:
        return len(self.children) > 0

    def __repr__(self):
        return f'name: {self.name}, order: {self.orbital_order}, has children(?): {self.has_children()}'


class OrbitalTree:
    root: Node
    __logger = log.getLogger("OrbitalTree")

    def __init__(self, centre_of_mass='COM'):
        self.root = Node(centre_of_mass, 0)

    @staticmethod
    def add_node_to(child_node_name: str, parent_node: Node) -> Node:
        node = OrbitalTree.construct_node_from_parent(child_node_name, parent_node)
        parent_node.add(node)
        return node

    @staticmethod
    def construct_node_from_parent(child_node_name: str, parent_node: Node) -> Node:
        return Node(child_node_name, parent_node.orbital_order + 1)

    def add_node(self, parent_name: str, child_name: str) -> Node:
        self.__logger.debug("Adding child_name: %s on to parent_name: %s", child_name, parent_name)
        if self.root.name == parent_name:
            return OrbitalTree.add_node_to(child_name, self.root)
        parent_node: Node = self.find(parent_name)
        if parent_node is None:
            raise NoNodeFoundException("Could not add a node, parent not found")
        else:
            return OrbitalTree.add_node_to(child_name, parent_node)

    def __traverse(self, node: Node, accessor_fn: Callable[[Node], T], collector_fn: Callable[[T], None]) -> None:
        collector_fn(accessor_fn(node))
        for child in node.children:
            if child.has_children():
                self.__traverse(child, accessor_fn, collector_fn)
            else:
                collector_fn(accessor_fn(child))

    def find(self, node_name: str) -> Optional[Node]:
        collector = AtomicRef()
        self.__traverse(self.root, lambda n: n, lambda val: collector.set(val) if val.name == node_name else None)
        return collector.data

    def path_to(self, search_node_name: str) -> List[Node]:
        node = self.find(search_node_name)
        if node is None:
            raise NoNodeFoundException(f'Could not find node: {search_node_name}')
        path_to: List[Node] = [node]
        is_not_at_root = node.name != 'COM'
        while is_not_at_root:
            child_name = node.name
            collector = AtomicRef()
            self.__traverse(self.root, lambda n: n,
                            lambda val: [collector.set(val) for n in val.children if n.name == node.name])
            node = collector.data
            is_not_at_root = node.name != 'COM'
            self.__logger.debug('Parent of %s is %s, at root: %s', child_name, node.name, is_not_at_root)
            path_to.append(node)
        return list(reversed(path_to))

    def orbital_orders(self) -> int:
        node = self.root
        orbital_orders = []
        self.__traverse(node, lambda n: n.orbital_order, lambda val: orbital_orders.append(val))
        return sum(orbital_orders)
