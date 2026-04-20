
from logic_ast import LPAREN, RPAREN


def t_VAR(t):
    r'[A-Z][A-Z0-9_]*'
    return t

tokens = (
    VAR,
    NEG,    # (¬)
    CONJ,   # (∧)
    DISJ,   # (∨)
    IMPL,   # (→)
    BICOND, # (↔)
    LPAREN, # (()
    RPAREN, # ())
)

t_NEG   = r'!'
t_CONJ   = r'&'
t_DISJ   = r'\|\|'
t_IMPL   = r'->'
t_BICOND = r'<->'
t_LPARENT = r'\('
t_RPARENT = r'\)'

