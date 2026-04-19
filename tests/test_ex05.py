import io
from contextlib import redirect_stdout

from ex05_nnf import negation_normal_form
from ex04_truth_table import truth_table
from utils import *


def get_truth_table_string(formula: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        truth_table(formula)
    return f.getvalue()


def run():
    print_header(5, "NEGATION NORMAL FORM (NNF)")

    def nnf(formula):
        res_nnf = negation_normal_form(formula)

        tabla_orig = get_truth_table_string(formula)
        tabla_nnf = get_truth_table_string(res_nnf)
        tablas_iguales = (tabla_orig == tabla_nnf)

        print(f"\n{CYAN}┌─────────────────────────────────────────────────┐{NC}")
        print(f"{CYAN}│ Fórmula original : {YELLOW}{formula:<30}{CYAN}│{NC}")
        print(f"{CYAN}│ NNF generada     : {YELLOW}{res_nnf:<30}{CYAN}│{NC}")
        print(f"{CYAN}│ Tablas de verdad : {GREEN if tablas_iguales else RED}{'IDÉNTICAS ✓' if tablas_iguales else 'DIFERENTES ✗':<30}{CYAN}│{NC}")
        print(f"{CYAN}└──────────────────────────────────────────────────┘{NC}")

        if tablas_iguales:
            print(tabla_orig.strip())
            print()
            print(tabla_nnf.strip())
        else:
            print(f"{RED}--- Tabla Original ({formula}) ---{NC}")
            print(tabla_orig.strip())
            print()
            print(f"\n{RED}--- Tabla NNF Fallida ({res_nnf}) ---{NC}")
            print(tabla_nnf.strip())
            
        print()

        if not tablas_iguales:
            return "FAIL: La lógica cambió (tablas diferentes)"

        for i, char in enumerate(res_nnf):
            if char == "!":
                if i == 0 or not (res_nnf[i-1].isalpha() or res_nnf[i-1] in "01"):
                    return f"FAIL: Símbolo '!' mal posicionado después de '{res_nnf[i-1]}'"

        return res_nnf

    cases = [
        # ((formula), expected)
        (("A",), "A"),
        (("A!",), "A!"),
        (("AB&!",), "A!B!|"),  # !(A & B) -> !A | !B
        (("AB|!",), "A!B!&"),  # !(A | B) -> !A & !B
        (("AB>!",), "AB!&"),   # !(A > B) -> A & !B
        (("AB=!",), "A!B!|AB|&"),  # !(A = B) -> (!A|!B) & (A|B)
        (("AB>",), "A!B|"),
        (("AB=",), "AB&A!B!&|"),
        (("AB|C&!",), "A!B!&C!|"),
        (("ABC||",), "ABC||"),
        (("ABC||!",), "A!B!C!&&"),
        (("ABC|&",), "ABC|&"),
        (("ABC&|",), "ABC&|"),
        (("ABC&|!",), "A!B!C!|&"),
        (("ABC^^",), "A!B!C&BC!&|&ABC!|B!C|&&|"),
        (("ABC>>",), "A!B!C||"),
        
        # Casos de error
        (("",), None),     
        (("AB",), None),   
        (("&",), None),    
        (("A+",), None),   
    ]

    cases_for_engine = []
    for args, expected in cases:
        if expected is True:
            try:
                expected = negation_normal_form(args[0])
            except Exception:
                pass
        cases_for_engine.append((args, expected))

    run_cases(
        ex_num=5,
        funcion_a_testear=nnf,
        casos=cases_for_engine,
    )


if __name__ == "__main__":
    run()