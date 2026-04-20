from logic_ast import AST, Bicond, Conj, Disj, Impl, Neg, Var, Paren
from logic_ast import pretty_print_statement 

# Error handling for parsing 
class ParseError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


# Parsing logic statements into ASTs
def parse(tokens: list[str]) -> AST:
    ast, next_index = parse_expr(tokens, 0)

    if next_index != len(tokens):
        raise ParseError(f"Unexpected tokens after valid expression at index {next_index}")

    return ast

# Makes the expression into an AST, and returns the AST along with the index of the next token to parse
def parse_expr(tokens: list[str], i: int) -> tuple[AST, int]:
    if i >= len(tokens):
        raise ParseError("Unexpected end of input")

    token = tokens[i]

    if token not in {"(", ")", "!", "&", "||", "->", "<->"}:
        return Var(token), i + 1

    # Negation has the highest precedence, so we check for it first
    if token == "!":
        expr, next_i = parse_expr(tokens, i + 1)
        return Neg(expr), next_i

    # Then we check for parentheses, which can contain any expression, including binary operations
    if token == "(":
        left, i = parse_expr(tokens, i + 1)

        if i >= len(tokens):
            raise ParseError("Expected operator or closing parenthesis")

        
        if tokens[i] == ")":
            return Paren(left), i + 1

        
        op = tokens[i]
        i += 1

        right, i = parse_expr(tokens, i)

        if i >= len(tokens) or tokens[i] != ")":
            raise ParseError("Expected closing parenthesis")

    # Now we have the left and right expressions, and the operator, so we can construct the appropriate AST node
        if op == "&":
            node = Conj(left, right)
        elif op == "||":
            node = Disj(left, right)
        elif op == "->":
            node = Impl(left, right)
        elif op == "<->":
            node = Bicond(left, right)
        else:
            raise ParseError(f"Expected binary operator, got {op}")

        return Paren(node), i + 1

    raise ParseError(f"Unexpected token at index {i}: {token}")

#ast = parse(["(", "A", "->", "(", "B", "||", "C", ")", ")"])
#print(pretty_print_statement(ast))
print(parse(["(", "A", "->", "(", "B", "||", "C", ")", ")"]))
