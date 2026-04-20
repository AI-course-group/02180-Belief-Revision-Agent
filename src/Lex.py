

# tokens definition for the lexer
tokens = (
    'VAR',
    'BICOND',
    'IMPL',
    'LPAREN',
    'RPAREN',
    'NEG',
    'CONJ',
    'DISJ',
)

# Regular expression rules for simple tokens
t_BICOND = r'<->'
t_IMPL   = r'->'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NEG    = r'!'
t_CONJ   = r'&'
t_DISJ   = r'\|\|'

t_ignore = ' \t' # ignore spaces and tabs

# Define a token for variables propositions
def t_VAR(t):
    r'[A-Z][A-Z0-9_]*'
    return t

# Error handling rule
def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}'")