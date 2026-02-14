from ex05_nnf import negation_normal_form
from ex04_truth_table import eval_formula_with_vars 
from utils import print_header, print_result, print_final, RED, CYAN, BLUE, YELLOW, NC, GREEN

def check_nnf_logic(original, result):
    """
    Verifica 2 cosas:
    1. Formato: '!' solo puede estar delante de variables (o constantes).
    2. Lógica: La tabla de verdad de 'original' y 'result' debe ser idéntica.
    """
    # VERIFICAR FORMATO NNF
    for i, char in enumerate(result):
        if char == '!':
            if i == 0: return False, "Empieza por '!'"
            prev = result[i-1]
            if not (prev.isalpha() or prev in "01"):
                return False, f"'!' después de '{prev}' (no permitido)"

    # VERIFICAR EQUIVALENCIA LÓGICA
    # Extraemos variables de ambas fórmulas
    vars_set = set([c for c in original if c.isalpha()] + [c for c in result if c.isalpha()])
    variables = sorted(list(vars_set))
    n = len(variables)
    
    # Probamos todas las combinaciones (Tablas de verdad)
    for i in range(1 << n):
        values = {}
        for j in range(n):
            values[variables[j]] = bool((i >> j) & 1)
        
        res_orig = eval_formula_with_vars(original, values)
        res_new = eval_formula_with_vars(result, values)
        
        if res_orig != res_new:
            return False, f"Difieren para {values}"
            
    return True, "OK"

def run():
    print_header(5, "NEGATION NORMAL FORM (NNF)")
    
    cases = [
    #   (formula, expected)
    #   expected = String exacto O True (para validación lógica automática)
        
        ('A', 'A'),
        ('A!', 'A!'),
        ('AB&!', 'A!B!|'),       # !(A & B) -> !A | !B
        ('AB|!', 'A!B!&'),       # !(A | B) -> !A & !B
        ('AB>!', 'AB!&'),        # !(A > B) -> A & !B
        ('AB=!', 'A!B!|AB|&'),   # !(A = B) -> (!A|!B) & (A|B) (XOR logic)

        ('ABC||', True),
        ('ABC||!', True),
        ('ABC|&', True),
        ('ABC&|', True),
        ('ABC&|!', True),
        ('ABC^^', True),      
        ('ABC>>', True),
        
    # --- Casos de error ---
        ("", None),             # Vacío
        ("AB", None),           # Falta operador
        ("&", None),            # Faltan operandos
        ("A+", None)            # Carácter inválido
    ]
    
    all_ok = True

    for case in cases:
        try:
            formula, expected = case

            res = negation_normal_form(formula)
            
            # Esperamos Error (None)
            if expected is None:
                print(f"  {YELLOW}•{NC} '{formula}' {RED}[FAIL]{NC}")
                print(f"    {RED}└── Se esperaba un error, pero devolvió: {res}{NC}")
                all_ok = False

            # Verificación Automática (True)
            elif expected is True:
                is_valid, msg = check_nnf_logic(formula, res)
                
                # Recortamos el string si es muy largo para que no ensucie la terminal
                disp_res = (res[:30] + '...') if len(res) > 30 else res
                desc = f"NNF('{formula}') -> {disp_res}"
                
                if is_valid:
                    print(f"  {YELLOW}•{NC} {desc:<60} [{GREEN} OK {NC}]")
                else:
                    print(f"  {YELLOW}•{NC} {desc:<60} [{RED}FAIL{NC}]")
                    print(f"    {RED}└── {msg}{NC}")
                    all_ok = False

            # Comparación Exacta de String
            else:
                if not print_result(f"NNF('{formula}')", res, expected):
                    all_ok = False

        except (ValueError, TypeError) as e:
            if expected is None:
                desc = f"Formula '{formula}'"
                print(f"  {YELLOW}•{NC} {desc:<50} [{CYAN}VAL ERROR{NC}]")
                print(f"    {BLUE}└── {e}{NC}")
            else:
                print(f"  {YELLOW}•{NC} Formula '{formula}' {CYAN}[CRASH]{NC}")
                print(f"    {BLUE}└── {e}{NC}")
                all_ok = False
                
        except Exception as e:
            print(f"  {YELLOW}•{NC} Formula '{formula}' {CYAN}[UNKNOWN CRASH]{NC}")
            print(f"    {BLUE}└── {e}{NC}")
            all_ok = False

    print_final(5, all_ok)

if __name__ == "__main__":
    run()