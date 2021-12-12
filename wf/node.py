from abc import ABC, abstractmethod
from wf.token import *
from typing import Callable

# p0, p1, ..., pn
EvalContext = List[bool]


class Node(ABC):
    token: Token

    def __init__(self, token: Token):
        self.token = token

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.token or ""}'

    def __repr__(self) -> str:
        return self.__str__()

    @abstractmethod
    def eval(self, context: EvalContext) -> bool:
        pass


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

    def eval(self, context: EvalContext):
        # Should only have one child
        child = self.children[0]
        return child.eval(context)


class NotOp(Walkable):
    operand: Walkable

    def walk(self, visit: NodeVisitor, level: int = 0):
        visit(self, level)
        self.operand.walk(visit, level + 1)

    def eval(self, context: EvalContext):
        return not self.operand.eval(context)


class BinaryOp(Walkable):
    type: str  # = AND | OR | IMPLY
    lhs: Walkable
    rhs: Walkable

    def __init__(self, token: Token):
        super().__init__(token)
        self.type = token.type

    def walk(self, visit: NodeVisitor, level: int = 0):
        visit(self, level)
        self.lhs.walk(visit, level + 1)
        self.rhs.walk(visit, level + 1)

    def eval(self, context: EvalContext):
        type = self.token.type
        lhs = self.lhs
        rhs = self.rhs

        if type == AND:
            return lhs.eval(context) and rhs.eval(context)
        if type == OR:
            return lhs.eval(context) or rhs.eval(context)
        if type == IMPLY:
            return not lhs.eval(context) or rhs.eval(context)


class Prop(Walkable):
    index: int
    def __init__(self, token: Token):
        super().__init__(token)
        self.index = int(token.match.group(1))
        

    def walk(self, visit: NodeVisitor, level: int = 0):
        visit(self, level)
    
    def eval(self, context: EvalContext):
        return context[self.index]
