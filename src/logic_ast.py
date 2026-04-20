# Abstract Syntax Tree (AST) for the language 
# Defines the connectives used when beliefs are expressed in propositional logic

from dataclasses import dataclass
from typing import Union

# --- AST definitions ---

@dataclass(frozen=True)
class Var:
    name: str

@dataclass(frozen=True)
class Not:
    expr: "AST"

@dataclass(frozen=True)
class Conjunction:
    left: "AST"
    right: "AST"

@dataclass(frozen=True)
class Disjunction:
    left: "AST"
    right: "AST"

@dataclass(frozen=True)
class Implies:
    left: "AST"
    right: "AST"

@dataclass(frozen=True)
class Biconditional:
    left: "AST"
    right: "AST"

@dataclass(frozen=True)
class LPAREN:
    pass

@dataclass(frozen=True)
class RPAREN:
    pass

AST = Union[Var, Not, Conjunction, Disjunction, Implies, Biconditional, LPAREN, RPAREN]

def Connectives(ast: AST) -> str:
    match ast:
        case Var(name):
            return name
        case Not(expr):
            return f"!({Connectives(expr)})"
        case Conjunction(left, right):
            return f"({Connectives(left)} & {Connectives(right)})"
        case Disjunction(left, right):
            return f"({Connectives(left)} || {Connectives(right)})"
        case Implies(left, right):
            return f"({Connectives(left)} -> {Connectives(right)})"
        case Biconditional(left, right):
            return f"({Connectives(left)} <-> {Connectives(right)})"
        case LPAREN():
            return "("
        case RPAREN():
            return ")"


print(Connectives(Implies(Var("A"), Disjunction(Var("B"), Var("C")))))