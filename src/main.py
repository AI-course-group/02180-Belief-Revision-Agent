from Lex import tokens
from parser import Parser
from logic_ast import Connectives

text = "A -> (B || C)"
tokens = tokens(text)

print("TOKENS:", tokens)

parser = Parser(tokens)
ast = parser.parse()

print("AST as string:", Connectives(ast))
print("AST object:", ast)