from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_ast import Var, Neg, Disj, Impl, pretty_print_statement
from contraction import contract, entails

# ── Helpers ──────────────────────────────────────────────────────────────────

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

PASS = "✅ PASS"
FAIL = "❌ FAIL"

def check(name: str, condition: bool):
    print(f"  {'✅ PASS' if condition else '❌ FAIL'} — {name}")

# ── Postulate Tests ───────────────────────────────────────────────────────────

def test_contraction(kb, formula):
    label = pretty_print_statement(formula)
    print(f"\nContracting φ = {label}")
    print("-" * 45)

    contracted = contract(kb, formula)
    fs_kb = formulas(kb)
    fs_contracted = formulas(contracted)

    # Inclusion: KB ÷ φ ⊆ KB
    check(
        "Inclusion       (result ⊆ KB)",
        all(f in fs_kb for f in fs_contracted)
    )

    # Vacuity: if KB doesn't entail φ, result = KB
    if not entails(fs_kb, formula):
        check(
            "Vacuity         (KB unchanged since φ not entailed)",
            sets_equal(contracted, kb)
        )
    else:
        check("Vacuity         (skipped — KB entails φ)", True)

    # Success: result does not entail φ (unless tautology)
    tautology = entails([], formula)
    if not tautology:
        check(
            "Success         (result does not entail φ)",
            not entails(fs_contracted, formula)
        )
    else:
        check("Success         (skipped — φ is a tautology)", True)

    # Extensionality: φ ↔ (φ∨φ) gives same result
    contracted_equiv = contract(kb, Disj(formula, formula))
    check(
        "Extensionality  (equiv φ gives same result)",
        semantically_equal(contracted, contracted_equiv)
    )

    # Consistency: consistent KB stays consistent after contraction
    if is_consistent(kb) and not tautology:
        check(
            "Consistency     (result is consistent)",
            is_consistent(contracted)
        )
    else:
        check("Consistency     (skipped — KB inconsistent or φ tautology)", True)


# ── Test Scenarios ────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Scenario 1: standard modus ponens KB
    kb1 = [
        (Var("A"),                  3),
        (Impl(Var("A"), Var("B")), 2),
        (Var("B"),                  1),
    ]
    print("=" * 45)
    print("KB1: A, A→B, B")
    print("=" * 45)
    test_contraction(kb1, Var("B"))                      # entailed — contracts
    test_contraction(kb1, Var("C"))                      # not entailed — vacuity
    test_contraction(kb1, Impl(Var("A"), Var("B")))      # contract the implication

    # Scenario 2: minimal base
    kb2 = [
        (Var("P"), 2),
        (Var("Q"), 1),
    ]
    print("\n" + "=" * 45)
    print("KB2: P, Q")
    print("=" * 45)
    test_contraction(kb2, Var("P"))
    test_contraction(kb2, Disj(Var("P"), Var("Q")))      # entailed disjunction

    # Scenario 3: empty base
    kb3 = []
    print("\n" + "=" * 45)
    print("KB3: (empty)")
    print("=" * 45)
    test_contraction(kb3, Var("A"))                      # vacuity — nothing to contract