# Abstract Syntax Tree (AST) for the language 
# Defines the connectives used when beliefs are expressed in propositional logic

from dataclasses import dataclass
from typing import Union

# --- AST definitions ---
from dataclasses import dataclass

@dataclass(frozen=True)
class Var:
    name: str
    def __repr__(self):
        return f'Var("{self.name}")'

@dataclass(frozen=True)
class Neg:
    expr: "AST"
    def __repr__(self):
        return f"Neg({self.expr!r})"

@dataclass(frozen=True)
class Conj:
    left: "AST"
    right: "AST"
    def __repr__(self):
        return f"Conj({self.left!r}, {self.right!r})"

@dataclass(frozen=True)
class Disj:
    left: "AST"
    right: "AST"
    def __repr__(self):
        return f"Disj({self.left!r}, {self.right!r})"

@dataclass(frozen=True)
class Impl:
    left: "AST"
    right: "AST"
    def __repr__(self):
        return f"Impl({self.left!r}, {self.right!r})"

@dataclass(frozen=True)
class Bicond:
    left: "AST"
    right: "AST"
    def __repr__(self):
        return f"Bicond({self.left!r}, {self.right!r})"

@dataclass(frozen=True)
class Paren:
    expr: "AST"
    def __repr__(self):
        return f"Paren({self.expr!r})"

AST = Union[Var, Neg, Conj, Disj, Impl, Bicond, Paren]

def pretty_print_statement(ast: AST) -> str:
    match ast:
        case Var(name):
            return name
        case Neg(expr):
            return f"!{pretty_print_statement(expr)}"
        case Conj(left, right):
            return f"{pretty_print_statement(left)} & {pretty_print_statement(right)}"
        case Disj(left, right):
            return f"{pretty_print_statement(left)} || {pretty_print_statement(right)}"
        case Impl(left, right):
            return f"{pretty_print_statement(left)} -> {pretty_print_statement(right)}"
        case Bicond(left, right):
            return f"{pretty_print_statement(left)} <-> {pretty_print_statement(right)}"
        case Paren(expr):
            return f"({pretty_print_statement(expr)})"
        case _:
            raise ValueError(f"Unknown AST node: {ast}")

print(pretty_print_statement(
    Paren(Impl(Var("A"), Disj(Var("B"), Var("C")))))
)


from enum import Enum

class Connectives(Enum):
    NEG = "!"
    CONJ = "&"
    DISJ = "||"
    IMPL = "->"
    BICOND = "<->"
