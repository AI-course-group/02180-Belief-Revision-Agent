from __future__ import annotations

from logic_ast import AST, pretty_print_statement
from parser import parse, ParseError
from contraction import contract
from expansion import expand
from revision import revise


def tokenize(formula: str) -> list[str]:
    tokens = []
    i = 0

    while i < len(formula):
        ch = formula[i]

        if ch.isspace():
            i += 1
            continue

        if ch == "(":
            tokens.append("(")
            i += 1
            continue

        if ch == ")":
            tokens.append(")")
            i += 1
            continue

        if ch == "!":
            tokens.append("!")
            i += 1
            continue

        if ch == "&":
            tokens.append("&")
            i += 1
            continue

        if ch == "|":
            tokens.append("|")
            i += 1
            continue

        if formula[i:i+3] == "<->":
            tokens.append("<->")
            i += 3
            continue

        if formula[i:i+2] == "->":
            tokens.append("->")
            i += 2
            continue

        if ch.isalpha():
            start = i
            i += 1
            while i < len(formula) and (formula[i].isalnum() or formula[i] == "_"):
                i += 1
            tokens.append(formula[start:i])
            continue

        raise SyntaxError(f"Illegal character: {ch}")

    return tokens


def split_formulas(text: str) -> list[str]:
    """
    Split formulas separated by commas, ignoring commas inside parentheses.
    Example:
    "A, B & C, (D | E)" -> ["A", "B & C", "(D | E)"]
    """
    parts = []
    current = []
    depth = 0

    for ch in text:
        if ch == "(":
            depth += 1
            current.append(ch)
        elif ch == ")":
            depth -= 1
            current.append(ch)
        elif ch == "," and depth == 0:
            piece = "".join(current).strip()
            if piece:
                parts.append(piece)
            current = []
        else:
            current.append(ch)

    last = "".join(current).strip()
    if last:
        parts.append(last)

    return parts


def parse_formula(text: str) -> AST:
    tokens = tokenize(text)
    return parse(tokens)


def parse_formula_list(text: str) -> list[AST]:
    formulas = split_formulas(text)
    return [parse_formula(f) for f in formulas]


def print_belief_base(belief_base: list[tuple[AST, int]]) -> None:
    print("\nCurrent belief base:")

    if not belief_base:
        print("{}")
        return

    print("{")
    for formula, priority in belief_base:
        print(f"  [{priority}] {pretty_print_statement(formula)}")
    print("}")


def main() -> None:
    belief_base: list[tuple[AST, int]] = []

    while True:
        print_belief_base(belief_base)

        print("\nChoose an option:")
        print("1. Expansion")
        print("2. Contraction")
        print("3. Revision")
        print("4. Reset belief base")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                user_input = input(
                    "Enter formula(s) to expand with, separated by commas:\n> "
                )
                formulas = parse_formula_list(user_input)

                for formula in formulas:
                    belief_base = expand(belief_base, formula)

            elif choice == "2":
                user_input = input("Enter one formula to contract by:\n> ").strip()
                formula = parse_formula(user_input)
                belief_base = contract(belief_base, formula)

            elif choice == "3":
                user_input = input("Enter one formula to revise by:\n> ").strip()
                formula = parse_formula(user_input)
                
                priority = int(input("Enter priority:\n> "))
                belief_base = revise(belief_base, formula, priority)

            elif choice == "4":
                belief_base = []
                print("\nBelief base has been reset.")

            elif choice == "5":
                print("Goodbye.")
                break

            else:
                print("Invalid choice. Please choose 1, 2, 3, 4, or 5.")

        except (SyntaxError, ParseError, ValueError) as e:
            print(f"\nInput error: {e}")


if __name__ == "__main__":
    main()