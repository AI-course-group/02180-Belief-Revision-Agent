from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_ast import Var, Neg, Disj, Impl, pretty_print_statement
from contraction import entails
from expansion import expand

# Helpers 

def formulas(kb):
    return [f for f, _ in kb]

def sets_equal(kb1, kb2):
    return set(formulas(kb1)) == set(formulas(kb2))

def semantically_equal(kb1, kb2):
    fs1 = formulas(kb1)
    fs2 = formulas(kb2)

    return (
        all(entails(fs1, f2) for f2 in fs2)
        and
        all(entails(fs2, f1) for f1 in fs1)
    )

def is_consistent(kb):
    fs = formulas(kb)
    if not fs:
        return True
    for f, _ in kb:
        if entails(fs, f) and entails(fs, Neg(f)):
            return False
    return True

def check(name: str, condition: bool):
    print(f"  {'PASS' if condition else ' FAIL'} — {name}")

# Postulate Tests

def test_expansion(kb, formula, priority=0):
    label = pretty_print_statement(formula)
    print(f"\nExpanding with Phi = {label}")
    print("-" * 45)

    expanded = expand(kb, formula, priority)
    fs_kb = formulas(kb)
    fs_expanded = formulas(expanded)

    # Success: Phi is entailed after expansion
    check(
        "Success         (Phi entailed after expansion)",
        entails(fs_expanded, formula)
    )

    # Inclusion: KB Subsetequals KB + Phi
    check(
        "Inclusion       (KB Subsetequals result)",
        all(f in fs_expanded for f in fs_kb)
    )

    # Vacuity: if Phi already entailed, KB unchanged
    if entails(fs_kb, formula):
        check(
            "Vacuity         (KB unchanged since Phi already entailed)",
            sets_equal(expanded, kb)
        )
    else:
        check("Vacuity         (skipped — Phi not already entailed)", True)

    # Consistency
    phi_consistent = not entails([formula], Neg(formula))
    if is_consistent(kb) and phi_consistent:
        check(
            "Consistency     (result is consistent)",
            is_consistent(expanded)
        )
    else:
        check("Consistency     (skipped — KB or Phi inconsistent)", True)

    # Extensionality: Phi <-> (Phi ∨ Phi) gives same expansion
    expanded_equiv = expand(kb, Disj(formula, formula), priority)
    check(
        "Extensionality  (equiv Phi gives same result)",
        semantically_equal(expanded, expanded_equiv)
    )


# Test Scenarios

if __name__ == "__main__":

    # Scenario 1: standard KB
    kb1 = [
        (Var("A"),                  3),
        (Impl(Var("A"), Var("B")), 2),
        (Var("B"),                  1),
    ]
    print("=" * 45)
    print("KB1: A, A→B, B")
    print("=" * 45)
    test_expansion(kb1, Var("C"), priority=1)
    test_expansion(kb1, Var("B"), priority=5)
    test_expansion(kb1, Var("D"), priority=4)

    # Scenario 2: minimal base
    kb2 = [
        (Var("P"), 2),
        (Var("Q"), 1),
    ]
    print("\n" + "=" * 45)
    print("KB2: P, Q")
    print("=" * 45)
    test_expansion(kb2, Impl(Var("P"), Var("Q")), priority=3)
    test_expansion(kb2, Var("R"), priority=2)

    # Scenario 3: empty base
    kb3 = []
    print("\n" + "=" * 45)
    print("KB3: (empty)")
    print("=" * 45)
    test_expansion(kb3, Var("A"), priority=1)