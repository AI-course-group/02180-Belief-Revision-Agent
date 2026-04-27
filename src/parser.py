from logic_ast import AST, Bicond, Conj, Disj, Impl, Neg, Var, Paren


class ParseError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def parse(tokens: list[str]) -> AST:
    ast, next_index = parse_bicond(tokens, 0)

    if next_index != len(tokens):
        raise ParseError(f"Unexpected tokens after valid expression at index {next_index}")

    return ast


# Lowest precedence: biconditional
def parse_bicond(tokens: list[str], i: int) -> tuple[AST, int]:
    left, i = parse_impl(tokens, i)

    while i < len(tokens) and tokens[i] == "<->":
        right, i = parse_impl(tokens, i + 1)
        left = Bicond(left, right)

    return left, i


# Implication
def parse_impl(tokens: list[str], i: int) -> tuple[AST, int]:
    left, i = parse_disj(tokens, i)

    while i < len(tokens) and tokens[i] == "->":
        right, i = parse_disj(tokens, i + 1)
        left = Impl(left, right)

    return left, i


# Disjunction
def parse_disj(tokens: list[str], i: int) -> tuple[AST, int]:
    left, i = parse_conj(tokens, i)

    while i < len(tokens) and tokens[i] == "|":
        right, i = parse_conj(tokens, i + 1)
        left = Disj(left, right)

    return left, i


# Conjunction
def parse_conj(tokens: list[str], i: int) -> tuple[AST, int]:
    left, i = parse_neg(tokens, i)

    while i < len(tokens) and tokens[i] == "&":
        right, i = parse_neg(tokens, i + 1)
        left = Conj(left, right)

    return left, i


# Negation
def parse_neg(tokens: list[str], i: int) -> tuple[AST, int]:
    if i >= len(tokens):
        raise ParseError("Unexpected end of input")

    if tokens[i] == "!":
        expr, next_i = parse_neg(tokens, i + 1)
        return Neg(expr), next_i

    return parse_atom(tokens, i)


# Variables and parenthesized expressions
def parse_atom(tokens: list[str], i: int) -> tuple[AST, int]:
    if i >= len(tokens):
        raise ParseError("Unexpected end of input")

    token = tokens[i]

    if token == "(":
        expr, next_i = parse_bicond(tokens, i + 1)

        if next_i >= len(tokens) or tokens[next_i] != ")":
            raise ParseError("Expected closing parenthesis")

        return Paren(expr), next_i + 1

    if token not in {"(", ")", "!", "&", "|", "->", "<->"}:
        return Var(token), i + 1

    raise ParseError(f"Unexpected token at index {i}: {token}")