from ex03_eval import eval_formula
from utils import print_header, print_result, print_final, print_error, RED, CYAN, BLUE, YELLOW, NC

def run():
    print_header(3, "BOOLEAN EVALUATION (RPN)")
    
    cases = [
    #   (formula, expected)
        ('0!', True),
        ('1!', False),
        ('00|', False),
        ('10|', True),
        ('01|', True),
        ('11|', True),
        ('10&', False),
        ('11&', True),
        ('11^', False),
        ('10^', True),
        ('00>', True),
        ('01>', True),
        ('10>', False),
        ('11>', True),
        ('00=', True),
        ('11=', True),
        ('10=', False),
        ('01=', False),

        ('11&0|', True),
        ('10&1|', True),
        ('11&1|', True),
        ('11&1|1^', False),
        ('01&1|1=', True),
        ('01&1&1&', False),
        ('0111&&&', False),
        
    # --- Casos de Error ---
        ("", None),         # Vacío
        ("1&", None),       # Falta operando
        ("11", None),       # Sobra operando (falta operador)
        ("12&", None),      # Carácter inválido ('2')
        ("ABC", None)       # Basura
    ]
    
    all_ok = True

    for case in cases:
        try:
            formula, expected = case
            res = eval_formula(formula)
            
            if expected is None:
                desc = f"Formula '{formula}'"
                print(f"  {YELLOW}•{NC} {desc:<70} [{RED}FAIL{NC}]")
                print(f"    {RED}└── Se esperaba un error, pero devolvió: {res}{NC}")
                all_ok = False
            else:
                # Verificación de resultado correcto
                if not print_result(f"Formula '{formula}'", res, expected):
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

    print_final(3, all_ok)

if __name__ == "__main__":
    run()