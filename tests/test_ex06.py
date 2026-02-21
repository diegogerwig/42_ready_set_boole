from ex06_cnf import conjunctive_normal_form
from ex05_nnf import to_ast
from ex04_truth_table import eval_formula_with_vars
from utils import *

def check_cnf_logic(original, result):
    """Verifica Formato NNF, Formato CNF y Equivalencia Lógica."""
    
    # 1. VERIFICAR FORMATO NNF ('!' solo tras variables)
    for i, char in enumerate(result):
        if char == '!':
            if i == 0: return False, "Empieza por '!'"
            prev = result[i-1]
            if not (prev.isalpha() or prev in "01"):
                return False, f"'!' después de '{prev}' (no permitido)"

    # 2. VERIFICAR FORMATO CNF
    # Regla: Ningún operador '&' puede estar debajo de un operador '|' en el AST.
    try:
        ast = to_ast(result)
        
        def check_no_and(node):
            if not node: return True
            if node.value == '&': return False
            return check_no_and(node.left) and check_no_and(node.right)
            
        def check_cnf(node):
            if not node: return True
            if node.value == '|':
                if not check_no_and(node.left) or not check_no_and(node.right):
                    return False
            return check_cnf(node.left) and check_cnf(node.right)
            
        if not check_cnf(ast):
            return False, "Regla CNF rota (Hay un '&' operando dentro de un '|')"
            
    except Exception as e:
        return False, f"Error parseando resultado CNF: {e}"

    # 3. VERIFICAR EQUIVALENCIA LÓGICA (Tabla de verdad)
    vars_set = set([c for c in original if c.isalpha()] + [c for c in result if c.isalpha()])
    variables = sorted(list(vars_set))
    n = len(variables)
    
    for i in range(1 << n):
        values = {}
        for j in range(n):
            values[variables[j]] = bool((i >> j) & 1)
        
        try:
            res_orig = eval_formula_with_vars(original, values)
            res_new = eval_formula_with_vars(result, values)
            if res_orig != res_new:
                return False, f"Lógica rota para {values}"
        except Exception:
            return False, "Error evaluando fórmula internamente"
            
    return True, "OK"

def run():
    print_header(6, "CONJUNCTIVE NORMAL FORM (CNF)")
    
    cases = [
    #   (formula, expected value)
        ('A', True),
        ('A!', True),
        ('AB&!', True),
        ('AB|!', True),
        ('AB>!', True),
        ('AB=!', True),

        ('ABC||', True),
        ('ABC||!', True),
        ('ABC|&', True),
        ('ABC&|', True),
        ('ABC&|!', True),
        ('ABC^^', True),
        ('ABC>>', True),
        
    # --- Casos de error ---
        ("", None),
        ("AB", None),
        ("&", None),
        ("A+", None)
    ]
    
    all_ok = True

    for case in cases:
        try:
            formula, expected = case
            res = conjunctive_normal_form(formula)
            desc = f"CNF('{formula}')"
            
            # Esperamos Error (None)
            if expected is None:
                content = f"{desc}: {res}"
                print(f" {YELLOW}•{NC} {content:<{PAD_LENGTH}} [{RED}FAIL{NC}]")
                print(f"    {RED}└── Se esperaba un error, pero devolvió: {res}{NC}")
                all_ok = False

            # Verificación Automática (True)
            elif expected is True:
                is_valid, msg = check_cnf_logic(formula, res)
                
                disp_res = (res[:40] + '...') if len(res) > 40 else res
                content = f"{desc}: {disp_res}"
                
                if is_valid:
                    print(f" {YELLOW}•{NC} {content:<{PAD_LENGTH}} [{GREEN} OK {NC}]")
                else:
                    print(f" {YELLOW}•{NC} {content:<{PAD_LENGTH}} [{RED}FAIL{NC}]")
                    print(f"    {RED}└── {msg}{NC}")
                    all_ok = False

            # Comparación Exacta de String
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

    print_final(6, all_ok)

if __name__ == "__main__":
    run()