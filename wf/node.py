from abc import ABC, abstractmethod
from wf.token import *


class Node(ABC):
    token: Token

    def __init__(self, token: Token):
        self.token = token


class Expression(Node):
    """(p) or root"""

    children: List[Node] = []

class NotOp(Node):
    operand: Node

class BinaryOp(Node):
    type: str # = AND | OR | IMPLY
    lhs: Node
    rhs: Node

    def __init__(self, token: Token):
        super().__init__(token)
        self.type = token.type

class Prop(Node):
    def __init__(self, token: Token):
        super().__init__(token)