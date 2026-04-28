from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_ast import Var, Neg, Disj, Impl, Conj, Bicond, pretty_print_statement
from contraction import entails
from revision import revise


p = Var("p")
q = Var("q")
r = Var("r")
s = Var("s")
t = Var("t")

p1 = Var("p1")
p2 = Var("p2")
p3 = Var("p3")

def print_case(title, formulas, statement, result):
    print("\n" + "="*50)
    print(title)
    print("Premises:", [pretty_print_statement(f) for f in formulas])
    print("Conclusion:", pretty_print_statement(statement))
    print("Result:", result)
    print("="*50)


# ── Exercise 1 ────────────────────────────────────────

# Exercise 1 no 3
formulas = [Conj(p, q)]
statement = Bicond(p, q)
result = entails(formulas, statement)
print_case("Exercise 1 no 3: p ∧ q ⊨ p ↔ q", formulas, statement, result)

# Exercise 1 no 4
formulas = [Bicond(p, q)]
statement = Conj(p, q)
result = entails(formulas, statement)
print_case("Exercise 1 no 4: p ↔ q ⊨ p ∧ q", formulas, statement, result)

# Exercise 1 no 5
formulas = [Bicond(p, q)]
statement = Conj(Neg(p), q)
result = entails(formulas, statement)
print_case("Exercise 1 no 5: p ↔ q ⊨ ¬p ∧ q", formulas, statement, result)

# Exercise 1 no 6
left = Conj(
    Disj(p, q),
    Disj(Neg(r), Disj(Neg(s), t))
)

right = Conj(
    Disj(Disj(p, q), r),
    Impl(
        Disj(q, Disj(Neg(r), s)),
        t
    )
)

result = entails([left], right)
print_case("Exercise 1 no 6", [left], right, result)

# Exercise 1 no 7
formula = Conj(
    Disj(p, q),
    Neg(Impl(p, q))
)

false_formula = Conj(p, Neg(p))

result = not entails([formula], false_formula)
print("\n" + "="*50)
print("Exercise 1 no 7: (p ∨ q) ∧ ¬(p → q) is satisfiable")
print("Formula:", pretty_print_statement(formula))
print("Result:", result)
print("="*50)

# Exercise 1 no 8
formula = Conj(
    Bicond(p, q),
    Disj(Neg(p), q)
)

result = not entails([formula], false_formula)
print("\n" + "="*50)
print("Exercise 1 no 8: (p ↔ q) ∧ (¬p ∨ q) is satisfiable")
print("Formula:", pretty_print_statement(formula))
print("Result:", result)
print("="*50)

# Exercise 1 no 9
formula1 = Bicond(Bicond(p, q), r)
formula2 = Bicond(p, q)

print("\n" + "="*50)
print("Exercise 1 no 9:")
print("Formula 1:", pretty_print_statement(formula1))
print("Formula 2:", pretty_print_statement(formula2))
print("Conclusion: They do NOT have the same number of models")
print("="*50)


# ── Exercise 5 ────────────────────────────────────────
# Helper: check tautology and satisfiability for a formula.
#
#   Tautology  : [] ⊨ φ          (entailed with NO premises)
#   Satisfiable: φ does NOT entail ⊥  (i.e. φ ∧ ¬φ is not derivable)
#                equivalently: not entails([φ], false_formula)

def print_ex5(number, formula):
    contradiction = Conj(p, Neg(p))         # canonical ⊥
    is_tautology    = entails([], formula)
    is_satisfiable  = not entails([formula], contradiction)
    
    print("\n" + "="*50)
    print(f"Exercise 5 no {number}: {pretty_print_statement(formula)}")
    print(f"  Tautology   : {is_tautology}")
    print(f"  Satisfiable : {is_satisfiable}")
    print("="*50)



print_ex5(1, Disj(p, Neg(p)))


print_ex5(2, Conj(p, Neg(p)))


print_ex5(3, Impl(Conj(p, q), p))


print_ex5(4, Impl(Conj(p, q), Neg(p)))


print_ex5(5, Impl(Impl(Conj(p1, p2), p3), Impl(p2, Impl(p1, p3))))


print_ex5(6,
    Impl(
        Conj(
            Impl(Conj(p, q), s),
            Impl(Conj(p, q), t)
        ),
        Impl(Conj(p, q), Conj(s, t))
    )
)