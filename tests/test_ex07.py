from ex07_sat import sat
from utils import *


def run():
    print_header(7, "SAT (SATISFIABILITY)")

    cases = [
        #   (formula, expected value)
        ("A", True),
        ("A!", True),
        ("AA|", True),
        ("AA&", True),
        ("AA!&", False),
        ("AA^", False),
        ("AB^", True),
        ("AB=", True),
        ("AA>", True),
        ("AA!>", True),
        ("ABC||", True),
        ("AB&A!B!&&", False),
        ("ABCDE&&&&", True),
        ("AAA^^", True),
        ("ABCDE^^^^", True),
        # --- Casos de error ---
        ("", None),
        ("AB", None),
        ("&", None),
        ("A+", None),
    ]

    all_ok = True

    for case in cases:
        try:
            formula, expected = case
            res = sat(formula)
            desc = f"sat('{formula}')"

            if expected is None:
                content = f"{desc}: {res}"
                print(f" {YELLOW}•{NC} {content:<{PAD_LENGTH}} [{RED}FAIL{NC}]")
                print(f"    {RED}└── Se esperaba un error, pero devolvió: {res}{NC}")
                all_ok = False

            else:
                if not print_result(desc, res, expected):
                    all_ok = False

        except (ValueError, TypeError) as e:
            desc = f"Formula '{formula}'"
            if expected is None:
                print_error(desc, "VAL ERROR", str(e))
            else:
                print_error(desc, "CRASH", str(e))
                all_ok = False

        except Exception as e:
            desc = f"Formula '{formula}'"
            print_error(desc, "UNKNOWN CRASH", str(e))
            all_ok = False

    print_final(7, all_ok)


if __name__ == "__main__":
    run()
