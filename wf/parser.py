import sys
import traceback
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

    def push(n: Expression):
        nonlocal stack
        stack.append(n)

    def peek() -> Expression:
        nonlocal stack
        return stack[len(stack) - 1]

    def appendChild(n: Node):
        top = peek()
        top.children.append(n)

    def removeLastChild() -> Node:
        return peek().children.pop()
    
    def consume_token():
        nonlocal token_index
        token_index += 1
    def open_expr(t: Token, should_append: bool = False) -> Expression:
        # Create a new sub expression
        sub_expr = Expression(t)
        # Append child 
        should_append and appendChild(sub_expr)
        # Push stack
        push(sub_expr)
        return sub_expr
    def close_expr():
        # Right parenthesis, pop stack
        pop()

    def look_ahead() -> Token:
        nonlocal token_index
        return tokens[token_index + 1]

    def look_ahead_for_operand() -> Node:
        next_token = look_ahead()

        if next_token.type == PROP:
            return Prop(next_token)
        if next_token.type == L_PAR:
            return open_expr(next_token) 

        raise ParsingError(text, next_token, f'Unexpected token type {next_token.type} (Invalid operand)', filename=filename)


    while token_index < len(tokens):
        token = tokens[token_index]

        if token.type == R_PAR:
            close_expr()
        elif token.type == L_PAR:
            open_expr(token, True)
        elif token.type == NOT:
            neg_node = NotOp(token)
            appendChild(neg_node)
            # Look ahead, next token must be a Prop or Expression
            neg_node.operand = look_ahead_for_operand()
            consume_token()

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
                # Look ahead, next token must be a Prop or Expression
                binary_op.rhs = look_ahead_for_operand()
                consume_token()

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
        with open(filename, 'r') as f:
            text = f.read()
            print(f"Parsing: {text}")
            root = parse(text, filename=filename)
            print(format_tree((root)))

    except FileNotFoundError as e:
        print(e)
    except SyntaxError as e:
        print(f'{e} offset={e.offset}')
        traceback.print_exception(SyntaxError, e, None)
