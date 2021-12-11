import re
from typing import List, Tuple

# Token type
SPACE = 'SP'
L_PAR = 'L_PAR'
R_PAR = 'R_PAR'
NOT = 'NOT'
AND = 'AND'
OR = 'OR'
IMPLY = 'IMPLY'
PROP = 'PROP'
# EOF

# Terminal rules
TOKEN_RULES: List[Tuple[str, re.Pattern]] = [
    (SPACE, re.compile(r'\s+')),
    (L_PAR, re.compile(r'\(')),
    (R_PAR, re.compile(r'\)')),
    (PROP, re.compile(r'p\d+')),
]

class TokenizationError(SyntaxError):
    def __init__(self, source: str, offset: int, message: str, filename: str = None):
        self.filename = filename
        self.msg = message
        self.lineno = 0
        self.offset = offset
        self.text = source



class Token:
    type: str
    match: re.Match

    def __init__(self, type: str, match: re.Match):
        self.type = type
        self.match = match

    def __str__(self):
        return f'<{self.type} {self.match.span(0)}>"{self.match.group(0)}"'
    def __repr__(self):
        return self.__str__()


def tokenize(text: str, filename: str = None):
    tokens: List[Token] = []
    offset = 0

    while offset < len(text):
        last_match: re.Match = None
        for rule in TOKEN_RULES:
            type = rule[0]
            pattern = rule[1]
            last_match = pattern.match(text, offset)
            if last_match:
              if type != SPACE:
                tokens.append(Token(type, last_match))
              # Early exit
              break
        if last_match:
            offset = last_match.end()
            pass
        else:
            raise TokenizationError(text, offset + 1, f'Invalid token at {offset + 1}', filename=filename)

    return tokens
