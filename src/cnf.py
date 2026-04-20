from __future__ import annotations
from logic_ast import AST, Var, Not, Conjunction, Disjunction, Implies, Biconditional

# --- Fully recursive CNF conversion ---
def formula_to_clauses(ast: AST) -> set[frozenset]:
    """
    Recursively converts a formula to a set of CNF clauses.
    Each clause is a frozenset of literals (Var or Not(Var)).
    """
    match ast:
        # Base cases — already a literal
        case Var():
            return {frozenset([ast])}
        case Not(Var()):
            return {frozenset([ast])}

        # Conjunction — each side becomes its own set of clauses
        case Conjunction(left, right):
            return formula_to_clauses(left) | formula_to_clauses(right)

        # Disjunction — cross-product merge of both sides
        case Disjunction(left, right):
            left_clauses = formula_to_clauses(left)
            right_clauses = formula_to_clauses(right)
            return {
                frozenset(l | r)
                for l in left_clauses
                for r in right_clauses
            }

        # Eliminate Implies recursively
        case Implies(left, right):
            return formula_to_clauses(Disjunction(Not(left), right))

        # Eliminate Biconditional recursively
        case Biconditional(left, right):
            return formula_to_clauses(Conjunction(
                Disjunction(Not(left), right),
                Disjunction(left, Not(right))
            ))

        # Push negations inward (NNF)
        case Not(Not(expr)):
            return formula_to_clauses(expr)

        case Not(Conjunction(left, right)):
            # De Morgan: ¬(A ∧ B) → (¬A ∨ ¬B)
            return formula_to_clauses(Disjunction(Not(left), Not(right)))

        case Not(Disjunction(left, right)):
            # De Morgan: ¬(A ∨ B) → (¬A ∧ ¬B)
            return formula_to_clauses(Conjunction(Not(left), Not(right)))

        case Not(Implies(left, right)):
            # ¬(A → B) → (A ∧ ¬B)
            return formula_to_clauses(Conjunction(left, Not(right)))

        case Not(Biconditional(left, right)):
            # ¬(A ↔ B) → (A ∧ ¬B) ∨ (¬A ∧ B)
            return formula_to_clauses(Disjunction(
                Conjunction(left, Not(right)),
                Conjunction(Not(left), right)
            ))

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

    # Negate the statement — proof by refutation
    clauses |= formula_to_clauses(Not(statement))

    return clauses


# --- Test ---
if __name__ == "__main__":
    from logic_ast import Connectives

    kb = [Implies(Var("A"), Var("B")), Var("A")]
    statement = Var("B")

    clauses = cnf(kb, statement)
    print("Clauses for resolution (KB ∪ {¬B}):")
    for clause in clauses:
        print(f"  {{{', '.join(Connectives(l) for l in clause)}}}")