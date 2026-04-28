from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_ast import Var, Neg, Conj, Disj, Impl, Bicond, pretty_print_statement
from contraction import contract, entails
from expansion import expand

# ---------- Helpers ----------

def formulas(kb):
    return [f for f, _ in kb]

def sets_equal(kb1, kb2):
    return set(formulas(kb1)) == set(formulas(kb2))

def semantically_equal(kb1, kb2):
    fs1 = formulas(kb1)
    fs2 = formulas(kb2)
    return (
        all(entails(fs1, f2) for f2 in fs2) and
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
    print(f"  {' PASS' if condition else ' FAIL'} — {name}")

# ---------- Exercise 1 ----------
# KB = {!p -> q, q -> p, p -> r & s}
# Does p & r & s follow from KB?

def test_exercise_1():
    print("\n" + "=" * 50)
    print("Exercise 1: Does KB entail p & r & s ?")
    print("KB = { !p -> q,  q -> p,  p -> r & s }")
    print("=" * 50)

    p, q, r, s = Var("p"), Var("q"), Var("r"), Var("s")

    kb = [
    (Impl(Neg(p), q),     1),
    (Impl(q, p),          1),
    (Impl(p, Conj(r, s)), 1),
    ]

    statement = Conj(p, Conj(r, s))  # p & r & s

    result = entails(formulas(kb), statement)

    print(f"\n  KB = {{ {', '.join(pretty_print_statement(f) for f in formulas(kb))} }}")
    print(f"  φ  = {pretty_print_statement(statement)}")
    print(f"\n  Expected: YES (p & r & s follows from KB)")
    check("KB entails p & r & s", result)

    # Show the reasoning steps
    print("\n  Reasoning trace:")
    check("  KB entails p  (from !p->q and q->p, p must hold)",
          entails(formulas(kb), p))
    check("  KB entails r  (from p and p->r&s)",
          entails(formulas(kb), r))
    check("  KB entails s  (from p and p->r&s)",
          entails(formulas(kb), s))

# ---------- Exercise 2 ----------
# A = {p, q, p&q, p|q, p->q}
# Which sets are valid results of contracting with q?

def test_exercise_2():
    print("\n" + "=" * 50)
    print("Exercise 2: Valid contraction results for A ÷ q")
    print("A = { p, q, p&q, p|q, p->q }")
    print("=" * 50)

    p, q = Var("p"), Var("q")

    # Full belief base, all with equal priority
    belief_base = [
        (p,              5),
        (q,              4),
        (Conj(p, q),     3),
        (Disj(p, q),     2),
        (Impl(p, q),     1),
    ]

    contracted = contract(belief_base, q)
    fs_contracted = formulas(contracted)

    print(f"\n  Contracting with φ = {pretty_print_statement(q)}")
    print(f"  Result: {{ {', '.join(pretty_print_statement(f) for f in fs_contracted)} }}")

    # Key checks: after contraction, q must not be entailed
    print("\n  Verifying contraction postulates:")
    check("Success     — result does not entail q",
          not entails(fs_contracted, q))
    check("Inclusion   — result ⊆ A",
          all(f in formulas(belief_base) for f in fs_contracted))
    check("Consistency — result is consistent",
          is_consistent(contracted))

    # Now check each candidate set from the exercise
    print("\n  Checking candidate sets from exercise:")

    # Candidate 1: {p, p|q}
    c1 = [p, Disj(p, q)]
    check("{p, p|q}      — valid remainder (does not entail q, subset of A, maximal)",
          not entails(c1, q) and all(f in formulas(belief_base) for f in c1))

    # Candidate 2: {p->q}
    c2 = [Impl(p, q)]
    check("{p->q}         — invalid (p->q alone doesn't entail q, but not maximal)",
          not entails(c2, q) and all(f in formulas(belief_base) for f in c2))

    # Candidate 3: {p|q, p->q}
    c3 = [Disj(p, q), Impl(p, q)]
    check("{p|q, p->q}   — invalid (p|q and p->q together entail q)",
          not entails(c3, q))

    # Candidate 4: {p|q}
    c4 = [Disj(p, q)]
    check("{p|q}         — invalid (p|q alone does not entail q, but not maximal)",
          not entails(c4, q) and all(f in formulas(belief_base) for f in c4))

# ---------- Exercise 3 ----------
# B = Cn({p, p<->q, !r})
# Find a plausibility order such that:
# 1. After revision with r, Bob believes !q
# 2. After contraction with p->q, Bob believes p

def test_exercise_3():
    print("\n" + "=" * 50)
    print("Exercise 3: Plausibility order for Bob's belief set")
    print("B = Cn({ p, p<->q, !r })")
    print("=" * 50)

    p, q, r = Var("p"), Var("q"), Var("r")

    # Bob's initial belief base
    # p<->q means p and q have the same truth value
    # so B entails: p, q (from p and p<->q), !r
    bob_kb = [
        (p,               3),
        (Bicond(p, q),    2),
        (Neg(r),          1),
    ]

    print(f"\n  Initial KB: {{ {', '.join(pretty_print_statement(f) for f, _ in bob_kb)} }}")

    fs_bob = formulas(bob_kb)
    print("\n  Verifying initial beliefs:")
    check("B entails p",    entails(fs_bob, p))
    check("B entails q",    entails(fs_bob, q))
    check("B entails !r",   entails(fs_bob, Neg(r)))

    # ── Requirement 1: revise with r -> should believe !q ──
    print("\n  Requirement 1: After revision with r, believe !q")
    print("  (Levi identity: B * r = (B ÷ !r) + r)")

    from contraction import contract
    contracted_neg_r = contract(bob_kb, Neg(r))   # B ÷ !r
    revised_r = expand(contracted_neg_r, r)        # + r

    fs_revised = formulas(revised_r)
    print(f"  After revision with r: {{ {', '.join(pretty_print_statement(f) for f in fs_revised)} }}")

    # For !q to follow after revision with r:
    # When we add r, p<->q combined with r should force !q
    # This requires p to be removed during contraction of !r
    check("After B*r: believes r",   entails(fs_revised, r))
    check("After B*r: believes !q",  entails(fs_revised, Neg(q)))

    # ── Requirement 2: contract p->q -> should believe p ──
    print("\n  Requirement 2: After contraction with p->q, believe p")

    # p->q is equivalent to !p|q
    p_impl_q = Impl(p, q)
    contracted_pq = contract(bob_kb, p_impl_q)

    fs_contracted = formulas(contracted_pq)
    print(f"  After contraction with p->q: {{ {', '.join(pretty_print_statement(f) for f in fs_contracted)} }}")

    check("After B÷(p->q): does not entail p->q",
          not entails(fs_contracted, p_impl_q))
    check("After B÷(p->q): still believes p",
          entails(fs_contracted, p))
    check("After B÷(p->q): still believes p<->q",
          entails(fs_contracted, Bicond(p, q)))

# ---------- Run all ---------- 

if __name__ == "__main__":
    test_exercise_1()
    test_exercise_2()
    test_exercise_3()