from __future__ import annotations
from logic_ast import AST, Var, Neg, Conj, Disj, Impl, Bicond, Connectives
from resolution import resolution

# --- Check if a set of formulas entails a statement ---
def entails(formulas: list[AST], statement: AST) -> bool:
    if not formulas:
        return False
    return resolution(formulas, statement)

# --- Compute remainder sets ---
# KB ⊥ φ = all maximal subsets of KB that do NOT entail φ
def remainder_sets(belief_base: list[AST], formula: AST) -> list[list[AST]]:
    """
    A remainder set is a maximal subset of the belief base that
    does not entail the formula being contracted.
    Maximal means: you cannot add any more beliefs back in
    without entailing φ again.
    """
    remainders = []

    # Try every subset of the belief base
    n = len(belief_base)
    for i in range(2**n):
        subset = [belief_base[j] for j in range(n) if (i >> j) & 1]

        # Skip if this subset entails φ
        if entails(subset, formula):
            continue

        # Check maximality — can we add any excluded belief without entailing φ?
        excluded = [belief_base[j] for j in range(n) if not (i >> j) & 1]
        is_maximal = all(
            entails(subset + [b], formula)
            for b in excluded
        )

        if is_maximal:
            remainders.append(subset)

    return remainders

# --- Selection function based on priority ---
# Picks the remainder sets with the highest total priority
def select(
    remainders: list[list[AST]],
    belief_base: list[tuple[AST, int]]
) -> list[list[AST]]:
    """
    From all remainder sets, select the best ones based on
    the priority order of the belief base.
    Higher priority = more important = prefer subsets that keep them.
    """
    if not remainders:
        return []

    # Build a priority lookup
    priority_map = {formula: priority for formula, priority in belief_base}

    def score(remainder: list[AST]) -> int:
        return sum(priority_map.get(f, 0) for f in remainder)

    max_score = max(score(r) for r in remainders)
    return [r for r in remainders if score(r) == max_score]

# --- Partial meet contraction ---
def contract(
    belief_base: list[tuple[AST, int]],
    formula: AST
) -> list[tuple[AST, int]]:
    """
    Partial meet contraction: KB ÷ φ
    Returns the new belief base after contracting by formula.

    AGM postulates satisfied:
    - Inclusion:    result ⊆ KB
    - Vacuity:      if KB doesn't entail φ, result = KB
    - Success:      result does not entail φ (unless φ is a tautology)
    - Extensionality: logically equivalent φ give same result
    """
    formulas = [f for f, p in belief_base]

    # Vacuity postulate — if KB doesn't entail φ, nothing to do
    if not entails(formulas, formula):
        return belief_base

    # Compute remainder sets
    remainders = remainder_sets(formulas, formula)

    # If no remainders found, contract to empty
    if not remainders:
        return []

    # Select best remainders using priority
    selected = select(remainders, belief_base)

    # Partial meet = intersection of selected remainders
    if not selected:
        return []

    intersection = set(selected[0])
    for r in selected[1:]:
        intersection &= set(r)

    # Rebuild with original priorities
    priority_map = {f: p for f, p in belief_base}
    return [(f, priority_map[f]) for f in intersection]


# --- Test ---
if __name__ == "__main__":
    kb = [
        (Var("A"),              3),
        (Impl(Var("A"), Var("B")), 2),
        (Var("B"),              1),
    ]

    print("Before contraction:")
    for f, p in kb:
        print(f"  [{p}] {Connectives(f)}")

    contracted = contract(kb, Var("B"))

    print("\nAfter contracting B:")
    for f, p in contracted:
        print(f"  [{p}] {Connectives(f)}")