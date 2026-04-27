from __future__ import annotations
from logic_ast import AST, Paren, Var, Neg, Conj, Disj, Impl, Bicond, pretty_print_statement

# --- Fully recursive CNF conversion ---
def formula_to_clauses(ast: AST) -> set[frozenset]:
    """
    Recursively converts a formula to a set of CNF clauses.
    Each clause is a frozenset of literals (Var or Not(Var)).
    """
    match ast:
        case Var():
            return {frozenset([ast])}
        case Neg(Var()):
            return {frozenset([ast])}

        # Conjunction: each side becomes its own set of clauses
        case Conj(left, right):
            return formula_to_clauses(left) | formula_to_clauses(right)

        # Disjunction: cross-product merge of both sides
        case Disj(left, right):
            left_clauses = formula_to_clauses(left)
            right_clauses = formula_to_clauses(right)
            return {
                frozenset(l | r)
                for l in left_clauses
                for r in right_clauses
            }

        # Eliminate Impl recursively
        case Impl(left, right):
            return formula_to_clauses(Disj(Neg(left), right))

        # Eliminate Bicond recursively
        case Bicond(left, right):
            return formula_to_clauses(Conj(
                Disj(Neg(left), right),
                Disj(left, Neg(right))
            ))

        # Push negations inward (NNF)
        case Neg(Neg(expr)):
            return formula_to_clauses(expr)

        case Neg(Conj(left, right)):
            return formula_to_clauses(Disj(Neg(left), Neg(right)))

        case Neg(Disj(left, right)):
            return formula_to_clauses(Conj(Neg(left), Neg(right)))

        case Neg(Impl(left, right)):
            return formula_to_clauses(Conj(left, Neg(right)))
        
        case Paren(expr):
            return formula_to_clauses(expr)  # unwrap parentheses
        
        case Neg(Paren(expr)):
            return formula_to_clauses(Neg(expr))  # unwrap then negate

        case Neg(Bicond(left, right)):
            return formula_to_clauses(Disj(
                Conj(left, Neg(right)),
                Conj(Neg(left), right)
            ))
        case _:
            raise ValueError(f"Unknown AST node: {ast}")

# --- Main entry point called by resolution.py ---
def cnf(belief_base: list[AST], statement: AST) -> set[frozenset]:
    """
    Takes a belief base (list of formulas) and a statement to check entailment for.
    Returns KB ∪ {¬statement} as a flat set of CNF clauses,
    ready for the resolution loop.
    """
    clauses = set()

    for formula in belief_base:
        clauses |= formula_to_clauses(formula)

    # Negate the statement - proof by refutation
    clauses |= formula_to_clauses(Neg(statement))

    return clauses


# --- Test ---
if __name__ == "__main__":
    from logic_ast import pretty_print_statement

    kb = [Impl(Var("A"), Var("B")), Var("A")]
    statement = Var("B")

    clauses = cnf(kb, statement)
    print("Clauses for resolution (KB ∪ {¬B}):")
    for clause in clauses:
        print(f"  {{{', '.join(pretty_print_statement(l) for l in clause)}}}")