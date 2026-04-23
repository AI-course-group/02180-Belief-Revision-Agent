from __future__ import annotations

from logic_ast import AST, Neg, pretty_print_statement
from contraction import contract
from expansion import expand


def revise(
    belief_base: list[tuple[AST, int]],
    formula: AST,
    priority: int = 0,
) -> list[tuple[AST, int]]:
    """
    Revise a belief base with a new formula using Levi identity:

        KB * phi = (KB / !phi) + phi

    We first contract away beliefs that force the negation of the new
    information, then expand the belief base with the new formula.
    """
    contracted = contract(belief_base, Neg(formula))
    return expand(contracted, formula, priority)


if __name__ == "__main__":
    from logic_ast import Impl, Var

    kb = [
        (Var("A"), 3),
        (Impl(Var("A"), Var("B")), 2),
        (Var("B"), 1),
    ]

    print("Before revision:")
    for belief, weight in kb:
        print(f"  [{weight}] {pretty_print_statement(belief)}")

    revised = revise(kb, Neg(Var("B")), priority=4)

    print("\nAfter revising with !B:")
    for belief, weight in revised:
        print(f"  [{weight}] {pretty_print_statement(belief)}")
