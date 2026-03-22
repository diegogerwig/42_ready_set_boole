import io
from contextlib import redirect_stdout

from ex06_cnf import conjunctive_normal_form
from ex05_nnf import to_ast
from ex04_truth_table import truth_table
from utils import *


def get_truth_table_string(formula: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        truth_table(formula)
    return f.getvalue()


def check_cnf_structure(ast_node):
    """
    Verifica la regla CNF: Ningún operador '&' puede estar debajo de un '|'.
    """
    def check_no_and(node):
        if not node:
            return True
        if node.value == "&":
            return False
        return check_no_and(node.left) and check_no_and(node.right)

    def check_cnf(node):
        if not node:
            return True
        if node.value == "|":
            if not check_no_and(node.left) or not check_no_and(node.right):
                return False
        return check_cnf(node.left) and check_cnf(node.right)

    return check_cnf(ast_node)


def run():
    print_header(6, "CONJUNCTIVE NORMAL FORM (CNF)")

    def wrapper_cnf(formula):
        res_cnf = conjunctive_normal_form(formula)

        tabla_orig = get_truth_table_string(formula)
        tabla_cnf = get_truth_table_string(res_cnf)
        tablas_iguales = (tabla_orig == tabla_cnf)

        max_len = 28
        disp_orig = (formula[:max_len-3] + "...") if len(formula) > max_len else formula
        disp_cnf = (res_cnf[:max_len-3] + "...") if len(res_cnf) > max_len else res_cnf

        print(f"\n{CYAN}┌──────────────────────────────────────────────────┐{NC}")
        print(f"{CYAN}│ Fórmula original : {YELLOW}{disp_orig:<30}{CYAN}│{NC}")
        print(f"{CYAN}│ CNF generada     : {YELLOW}{disp_cnf:<30}{CYAN}│{NC}")
        print(f"{CYAN}│ Tablas de verdad : {GREEN if tablas_iguales else RED}{'IDÉNTICAS ✓' if tablas_iguales else 'DIFERENTES ✗':<30}{CYAN}│{NC}")
        print(f"{CYAN}└──────────────────────────────────────────────────┘{NC}")

        if tablas_iguales:
            print(tabla_orig.strip())
            print()
            print(tabla_cnf.strip())
        else:
            print(f"{RED}--- Tabla Original ({formula}) ---{NC}")
            print(tabla_orig.strip())
            print()
            print(f"\n{RED}--- Tabla CNF Fallida ({disp_cnf}) ---{NC}")
            print(tabla_cnf.strip())
            
        print() 

        if not tablas_iguales:
            return "FAIL: La lógica cambió (tablas diferentes)"

        for i, char in enumerate(res_cnf):
            if char == "!":
                if i == 0 or not (res_cnf[i-1].isalpha() or res_cnf[i-1] in "01"):
                    return f"FAIL: Símbolo '!' mal posicionado después de '{res_cnf[i-1]}'"

        try:
            ast_res = to_ast(res_cnf)
            if not check_cnf_structure(ast_res):
                return "FAIL: Regla CNF rota (Hay un '&' operando dentro de un '|')"
        except Exception as e:
            return f"FAIL: Error parseando AST del resultado: {e}"

        return res_cnf

    user_cases = [
        (("A",), True),
        (("A!",), True),
        (("AB&!",), True),
        (("AB|!",), True),
        (("AB>!",), True),
        (("AB=!",), True),
        (("ABC||",), True),
        (("ABC||!",), True),
        (("ABC|&",), True),
        (("ABC&|",), True),
        (("ABC&|!",), True),
        (("ABC^^",), True),
        (("ABC>>",), True),
        
        # Casos de error
        (("",), None),
        (("AB",), None),
        (("&",), None),
        (("A+",), None),
    ]

    cases_for_engine = []
    for args, expected in user_cases:
        if expected is True:
            try:
                expected = conjunctive_normal_form(args[0])
            except Exception:
                pass
        cases_for_engine.append((args, expected))

    run_cases(
        ex_num=6,
        funcion_a_testear=wrapper_cnf,
        casos=cases_for_engine,
    )


if __name__ == "__main__":
    run()