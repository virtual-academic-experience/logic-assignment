import sys
from wf.token import *
from wf.node import *
from typing import List

class ParsingError(SyntaxError):
    def __init__(self, source: str, token: Token, message: str, filename: str = None):
        self.filename = filename
        self.msg = message
        self.lineno = 0
        self.offset = token.match.span(0)[0] + 1
        self.text = source


def parseTree(text: str, tokens: List[Token], filename: str = None):
    root = Expression(None)
    stack: List[Expression] = [root]
    token_index: int = 0
    token: Node = None

    def pop():
        # )
        nonlocal stack 
        if len(stack) == 1:
            raise ParsingError(text, token, 'Unbalanced right parentheses', filename=filename)
        return stack.pop()

    def push(n: Expression(token)):
        nonlocal stack
        stack.push(n)

    def peek() -> Expression:
        nonlocal stack
        return stack[len(stack) - 1]

    def appendChild(n: Node):
        peek().children.append(n)

    def removeLastChild() -> Node:
        return peek().children.pop()
    
    def consume_token():
        nonlocal token_index
        token_index += 1

    while token_index < len(tokens):
        token = tokens[token_index]

        if token.type == R_PAR:
            # Right parenthesis, pop stack
            pop()
        elif token.type == L_PAR:
            # TODO
            # push()
            pass
        elif token.type == NOT:
            neg_node = NotOp(token)
            appendChild(neg_node)
            # TODO: look ahead, next token must be a Prop or Expression
            # neg_node.oprand = parse_next_token_if_legal
            # consume_token()

        elif token.type == AND or token.type == OR or token.type == IMPLY: 
            # &p1
            # p0 & p1
            #    ^
            try:
                # Fetch last child
                last_node = removeLastChild()
                # Create a new binary op
                binary_op = BinaryOp(token)
                appendChild(binary_op)
                # Left hand side
                binary_op.lhs = last_node
                # TODO: look ahead, next token must be a Prop or Expression
                # binary_op.rhs = ?
            except IndexError:
                # Missing lhs
                raise ParsingError(text, token, 'Missing left operand', filename=filename)
        elif token.type == PROP:
            p = Prop(token)
            appendChild(p)
        elif token.type == EOF:
            if len(stack) > 1:
                # Stack not empty, more left parenthesis than right ones
                raise ParsingError(text, token, 'Unblanced left parentheses', filename=filename)

        consume_token()

    return root


def parse(text: str, filename: str = None):
    # Tokenization
    tokens = tokenize(text, filename=filename)
    print(f"Tokens: {tokens}")

    # Parsing
    ast = parseTree(text, tokens, filename=filename)

    return ast


if __name__ == "__main__":
    filename = sys.argv[1]
    try:
        f = open(filename, 'r')
        text = f.read()
        print(f"Parsing: {text}")
        print(parse(text, filename=filename))
    except FileNotFoundError as e:
        print(e)
