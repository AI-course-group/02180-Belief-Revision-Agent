from __future__ import annotations
from logic_ast import AST, Var, Impl, pretty_print_statement
from resolution import resolution


def entails(formulas: list[AST], statement: AST) -> bool:
    return resolution(formulas, statement)


def expand(
    belief_base: list[tuple[AST, int]],
    formula: AST,
    priority: int = 0,
) -> list[tuple[AST, int]]:
    # just add the formula to the belief base with a given priority
    # if we already know it, don't bother adding it again
    formulas = [f for f, _ in belief_base]

    if entails(formulas, formula):
        return belief_base

    # skip duplicates
    if any(f == formula for f in formulas):
        return belief_base

    return belief_base + [(formula, priority)]


def revise(
    belief_base: list[tuple[AST, int]],
    formula: AST,
    priority: int = 0,
) -> list[tuple[AST, int]]:
    # revision = contract the opposite first, then expand
    # this way the new formula doesn't contradict what's already in the base
    # KB * phi = (KB / neg phi) + phi
    from contraction import contract
    from logic_ast import Neg

    contracted = contract(belief_base, Neg(formula))
    return expand(contracted, formula, priority)



if __name__ == "__main__":
    from logic_ast import Neg

    def print_kb(kb):
        for f, p in kb:
            print(f"  [{p}] {pretty_print_statement(f)}")

    def expand_and_report(kb, formula, priority):
        label = pretty_print_statement(formula)
        kb_new = expand(kb, formula, priority=priority)

        before_labels = [(pretty_print_statement(f), p) for f, p in kb]
        after_labels  = [(pretty_print_statement(f), p) for f, p in kb_new]

        if entails([f for f, _ in kb], formula):
            print(f"  {label} is already entailed -> vacuity, KB unchanged")
        else:
            print(f"  {label} is not entailed -> added at priority {priority}")

        added   = [x for x in after_labels if x not in before_labels]
        removed = [x for x in before_labels if x not in after_labels]

        if added:
            print(f"  [DEBUG] Actually added:   {added}")
        if removed:
            print(f"  [DEBUG] Actually removed: {removed}")
        if not added and not removed:
            print(f"  [DEBUG] KB unchanged (confirmed)")

        return kb_new
    def revise_and_report(kb, formula, priority):
        label = pretty_print_statement(formula)
        neg_label = pretty_print_statement(Neg(formula))
        print(f"  Revising with {label} (priority {priority})")

        before_labels = {pretty_print_statement(f) for f, _ in kb}
        kb_new = revise(kb, formula, priority=priority)
        after_labels = {pretty_print_statement(f) for f, _ in kb_new}

        removed = before_labels - after_labels
        added = after_labels - before_labels

        if removed:
            print(f"  [DEBUG] Removed: {sorted(removed)}")
        if added:
            print(f"  [DEBUG] Added:   {sorted(added)}")
        if not removed and not added:
            print(f"  [DEBUG] KB unchanged")

        # Consistency check
        formulas = [f for f, _ in kb_new]
        if entails(formulas, formula) and entails(formulas, Neg(formula)):
            print(f"  [WARNING] KB is inconsistent after revision!")
        else:
            print(f"  [DEBUG] KB is consistent after revision (confirmed)")

        return kb_new

    # ── STEP 0 ──────────────────────────────────────────
    kb = [
        (Var("A"),                 3),
        (Impl(Var("A"), Var("B")), 2),
    ]
    print("=" * 40)
    print("STEP 0 - Initial belief base:")
    print("=" * 40)
    print_kb(kb)

    # ── STEP 1 ──────────────────────────────────────────
    print("\n" + "=" * 40)
    print("STEP 1 - expand(KB, C, priority=1)")
    print("=" * 40)
    kb = expand_and_report(kb, Var("C"), priority=1)
    print_kb(kb)

    # ── STEP 2 ──────────────────────────────────────────
    print("\n" + "=" * 40)
    print("STEP 2 - expand(KB, B, priority=5)")
    print("=" * 40)
    kb = expand_and_report(kb, Var("B"), priority=5)
    print_kb(kb)

    # ── STEP 3 ──────────────────────────────────────────
    print("\n" + "=" * 40)
    print("STEP 3 - revise(KB, !A, priority=4)")
    print("=" * 40)
    kb = revise_and_report(kb, Neg(Var("A")), priority=4)
    print_kb(kb)