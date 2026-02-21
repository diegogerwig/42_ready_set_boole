from ex09_eval_set import eval_set
from utils import *

def run():
    print_header(9, "SET EVALUATION")
    
    cases = [
    #   (Formula, Sets, Expected)
        ('A', [[]], []),
        ('A!', [[]], []),
        ('A', [[42]], [42]),
        ('A!', [[42]], []),
        ('A!B&', [[1, 2, 3], [2, 3, 4]], [4]),
        ('AB|', [[0, 1, 2], []], [0, 1, 2]),
        ('AB&', [[0, 1, 2], []], []),
        ('AB&', [[0, 1, 2], [0]], [0]),
        ('AB&', [[0, 1, 2], [42]], []),
        ('AB^', [[0, 1, 2], [0]], [1, 2]),
        ('AB>', [[0], [1, 2]], [1, 2]),
        ('AB>', [[0], [0, 1, 2]], [0, 1, 2]),
        
        ('ABC||', [[], [], []], []),
        ('ABC||', [[0], [1], [2]], [0, 1, 2]),
        ('ABC||', [[0], [0], [0]], [0]),
        ('ABC&&', [[0], [0], []], []),
        ('ABC&&', [[0], [0], [0]], [0]),
        ('ABC^^', [[0], [0], [0]], [0]),
        ('ABC>>', [[0], [0], [0]], [0]),

    # --- Casos de error ---
        ("", [[0]], None),             # Fórmula vacía
        ("AB", [[0], [1]], None),      # Sobran operandos
        ("&", [[0], [1]], None),       # Faltan operandos
        ("A+", [[0]], None)            # Carácter inválido
    ]
    
    all_ok = True

    for case in cases:
        formula, input_sets, expected = case
        
        sets_str = str(input_sets)
        disp_sets = (sets_str[:20] + '..') if len(sets_str) > 20 else sets_str
        desc = f"eval_set('{formula}', {disp_sets})"
        
        try:
            res = eval_set(formula, input_sets)
            
            if expected is None:
                content = f"{desc}: {res}"
                print(f" {YELLOW}•{NC} {content:<{PAD_LENGTH}} [{RED}FAIL{NC}]")
                print(f"    {RED}└── Se esperaba un error, pero devolvió: {res}{NC}")
                all_ok = False
            else:
                if not print_result(desc, res, expected):
                    all_ok = False

        except (ValueError, TypeError) as e:
            if expected is None:
                print_error(desc, "VAL ERROR", str(e))
            else:
                print_error(desc, "CRASH", str(e))
                all_ok = False
                
        except Exception as e:
            print_error(desc, "UNKNOWN CRASH", str(e))
            all_ok = False

    print_final(9, all_ok)

if __name__ == "__main__":
    run()