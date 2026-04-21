from Lex import tokens
from parser import parse
# from logic_ast import Connectives

text = "A -> (B || C)"
tokens = tokens(text)

print("TOKENS:", tokens)

ast = parse(tokens)

print(ast)
# print("AST as string:", Connectives(ast))
# print("AST object:", ast)