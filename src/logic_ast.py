# Abstract Syntax Tree (AST) for the language 
# Defines the connectives used when beliefs are expressed in propositional logic

from dataclasses import dataclass
from typing import Union

# --- AST definitions ---

@dataclass(frozen=True)
class Var:
    name: str

@dataclass(frozen=True)
class Neg:
    expr: "AST"

@dataclass(frozen=True)
class Conj:
    left: "AST"
    right: "AST"

@dataclass(frozen=True)
class Disj:
    left: "AST"
    right: "AST"

@dataclass(frozen=True)
class Impl:
    left: "AST"
    right: "AST"

@dataclass(frozen=True)
class Bicond:
    left: "AST"
    right: "AST"

AST = Union[Var, Neg, Conj, Disj, Impl, Bicond]

def Connectives(ast: AST) -> str:
    match ast:
        case Var(name):
            return name
        case Neg(expr):
            return f"!({Connectives(expr)})"
        case Conj(left, right):
            return f"({Connectives(left)} & {Connectives(right)})"
        case Disj(left, right):
            return f"({Connectives(left)} || {Connectives(right)})"
        case Impl(left, right):
            return f"({Connectives(left)} -> {Connectives(right)})"
        case Bicond(left, right):
            return f"({Connectives(left)} <-> {Connectives(right)})"


print(Connectives(Impl(Var("A"), Disj(Var("B"), Var("C")))))