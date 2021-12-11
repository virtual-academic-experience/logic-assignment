import sys
from wf.token import *
from typing import List


def parseTree(text: str, token: List[Token], filename: str = None):
    pass


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
