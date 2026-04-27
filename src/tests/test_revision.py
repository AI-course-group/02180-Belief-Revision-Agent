from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_ast import Var, Neg, Disj, Impl, pretty_print_statement
from contraction import entails
from revision import revise

# ── Helpers ───────────────────────────────────────────────────────────────────

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
    print(f"  {'✅ PASS' if condition else '❌ FAIL'} — {name}")

# ── Postulate Tests ───────────────────────────────────────────────────────────

def test_revision(kb, formula, priority=0):
    label = pretty_print_statement(formula)
    print(f"\nRevising with φ = {label}")
    print("-" * 45)

    revised = revise(kb, formula, priority)
    fs_revised = formulas(revised)

    # Success: φ is entailed after revision
    check(
        "Success         (φ entailed after revision)",
        entails(fs_revised, formula)
    )

    # Inclusion: KB * φ ⊆ KB + φ
    from expansion import expand
    expanded = expand(kb, formula, priority)
    fs_expanded = formulas(expanded)
    check(
        "Inclusion       (result ⊆ KB + φ)",
        all(f in fs_expanded for f in fs_revised)
    )

    # Consistency: result should be consistent (unless φ itself is contradictory)
    phi_consistent = not entails([formula], Neg(formula))
    if phi_consistent:
        check(
            "Consistency     (result is consistent)",
            is_consistent(revised)
        )
    else:
        check("Consistency     (skipped — φ is contradictory)", True)

    # Levi identity: KB * φ = (KB ÷ ¬φ) + φ
    from contraction import contract
    levi = revise(kb, formula, priority)
    contracted_neg = contract(kb, Neg(formula))
    from expansion import expand
    levi_manual = expand(contracted_neg, formula, priority)
    check(
        "Levi identity   (KB*φ = (KB÷¬φ)+φ)",
        semantically_equal(levi, levi_manual)
    )

    # Extensionality: φ ↔ (φ∨φ) gives same revision
    revised_equiv = revise(kb, Disj(formula, formula), priority)
    check(
        "Extensionality  (equiv φ gives same result)",
        semantically_equal(revised, revised_equiv)
    )


# ── Test Scenarios ────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Scenario 1: revise with contradicting belief
    kb1 = [
        (Var("A"),                  3),
        (Impl(Var("A"), Var("B")), 2),
        (Var("B"),                  1),
    ]
    print("=" * 45)
    print("KB1: A, A→B, B")
    print("=" * 45)
    test_revision(kb1, Neg(Var("A")), priority=4)       # contradicts A
    test_revision(kb1, Var("C"),      priority=1)       # consistent addition

    # Scenario 2: minimal base
    kb2 = [
        (Var("P"), 2),
        (Var("Q"), 1),
    ]
    print("\n" + "=" * 45)
    print("KB2: P, Q")
    print("=" * 45)
    test_revision(kb2, Neg(Var("P")), priority=3)
    test_revision(kb2, Impl(Var("P"), Var("Q")), priority=2)

    # Scenario 3: empty base
    kb3 = []
    print("\n" + "=" * 45)
    print("KB3: (empty)")
    print("=" * 45)
    test_revision(kb3, Var("A"), priority=1)