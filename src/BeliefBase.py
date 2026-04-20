from __future__ import annotations
from logic_ast import AST, Var, Neg, Conj, Disj, Impl, Bicond, Connectives
from cnf import formula_to_clauses

class BeliefBase:
    def __init__(self):
        self.beliefbase: list[tuple[AST, int]] = []  # (formula, priority)
        self.clauses: set[frozenset] = set()

    def expand(self, formula: AST, priority: int = 0):
        self.beliefbase.append((formula, priority))
        self.clauses |= formula_to_clauses(formula)

    def get(self) -> tuple[list[tuple[AST, int]], set[frozenset]]:
        return self.beliefbase, self.clauses

    def display(self):
        print("Belief Base:")
        print("=" * 30)
        if not self.beliefbase:
            print("  (empty)")
        else:
            for formula, priority in sorted(self.beliefbase, key=lambda x: -x[1]):
                print(f"  [{priority}] {Connectives(formula)}")
        print("\nCNF Clauses:")
        for clause in self.clauses:
            literals = " v ".join(Connectives(l) for l in clause)
            print(f"  {{{literals}}}")
        print("=" * 30)


# --- Test ---
if __name__ == "__main__":
    bb = BeliefBase()
    bb.expand(Impl(Var("A"), Var("B")), priority=1)
    bb.expand(Disj(Var("B"), Var("C")), priority=2)

    bb.display()

    beliefbase, clauses = bb.get()
    print("\nRaw belief base:", beliefbase)
    print("Raw clauses:", clauses)