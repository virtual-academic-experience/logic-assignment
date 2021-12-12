from abc import ABC, abstractmethod
from wf.token import *
from typing import Callable


class Node(ABC):
    token: Token

    def __init__(self, token: Token):
        self.token = token

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.token or ""}' 
    def __repr__(self) -> str:
        return self.__str__()

NodeVisitor = Callable[[Node], None]

class Walkable(Node):
    @abstractmethod
    def walk(self, visit: NodeVisitor, level: int = 0):
        pass

def format_tree(root: Walkable) -> str:
    lines: List[str] = []
    def visit(n: Node, level: int):
        lines.append(f'{"  " * level}{n}') 
    root.walk(visit)

    return '\n'.join(lines)

class Expression(Walkable):
    """(p) or root"""

    children: List[Node]

    def __init__(self, token: Token):
        super().__init__(token)
        self.children = []

    def walk(self, visit: NodeVisitor, level: int = 0):
        visit(self, level)
        for child in self.children:
            child.walk(visit, level + 1)
        

class NotOp(Walkable):
    operand: Walkable

    def walk(self, visit: NodeVisitor, level: int = 0):
        visit(self, level)
        self.operand.walk(visit, level + 1)

class BinaryOp(Walkable):
    type: str # = AND | OR | IMPLY
    lhs: Walkable
    rhs: Walkable

    def __init__(self, token: Token):
        super().__init__(token)
        self.type = token.type

    def walk(self, visit: NodeVisitor, level: int = 0):
        visit(self, level)
        self.lhs.walk(visit, level + 1)
        self.rhs.walk(visit, level + 1)

class Prop(Walkable):
    def __init__(self, token: Token):
        super().__init__(token)

    def walk(self, visit: NodeVisitor, level: int = 0):
        visit(self, level)