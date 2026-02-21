from ex08_powerset import powerset
from utils import *

def compare_powersets(res: list[list[int]], expected: list[list[int]]) -> bool:
    """
    Compara dos conjuntos potencia ignorando el orden de los subconjuntos 
    y el orden de los elementos dentro de ellos.
    """
    if not isinstance(res, list): return False
    
    # Ordenamos cada subconjunto internamente, y luego ordenamos la lista principal
    res_sorted = sorted([sorted(list(sub)) for sub in res])
    exp_sorted = sorted([sorted(list(sub)) for sub in expected])
    
    return res_sorted == exp_sorted

def run():
    print_header(8, "POWERSET (CONJUNTO POTENCIA)")
    
    cases = [
    #   (Input, Expected_Output)
        ([], [[]]),
        ([0], [[], [0]]),
        ([0, 1], [[], [0], [1], [0, 1]]),
        ([0, 1, 2], [
            [], [0], [1], [2], 
            [0, 1], [1, 2], [0, 2], 
            [0, 1, 2]
        ]),
        
        ([1, 1], [[], [1]]), 
        
    # --- Casos de error ---
        (None, None),
        ("123", None) # String en vez de lista
    ]
    
    all_ok = True

    for case in cases:
        input_set, expected = case
        input_str = str(input_set) if input_set is not None else "None"
            
        try:
            res = powerset(input_set)
            
            # Formateo visual (Recortamos si es muy largo)
            disp_res = (str(res)[:40] + '...') if len(str(res)) > 40 else str(res)
            content = f"powerset({input_str}): {disp_res}"
            
            if expected is None:
                print(f" {YELLOW}•{NC} {content:<{PAD_LENGTH}} [{RED}FAIL{NC}]")
                print(f"    {RED}└── Se esperaba un error, pero devolvió: {res}{NC}")
                all_ok = False

            else:
                # Calculamos 'n' (ignorando duplicados como en un Set real)
                n = len(set(input_set))
                expected_len = 2 ** n
                
                # Verificación Doble: Coincidencia + Cardinalidad 2^n
                is_correct = compare_powersets(res, expected)
                is_right_size = len(res) == expected_len
                
                if is_correct and is_right_size:
                    # Incluimos en la impresión que la cardinalidad coincide
                    print(f" {YELLOW}•{NC} {content:<{PAD_LENGTH}} [{GREEN} OK {NC}] (n={expected_len})")
                else:
                    print(f" {YELLOW}•{NC} {content:<{PAD_LENGTH}} [{RED}FAIL{NC}]")
                    if not is_right_size:
                        print(f"    {RED}└── Cardinalidad incorrecta. Esperada: {expected_len}, Obtenida: {len(res)}{NC}")
                    if not is_correct:
                        print(f"    {RED}└── Los subconjuntos no coinciden con lo esperado.{NC}")
                        print(f"    {RED}    Esperado: {expected}{NC}")
                    all_ok = False

        except (ValueError, TypeError) as e:
            content = f"powerset({input_str})"
            if expected is None:
                print_error(content, "TYPE ERROR", str(e))
            else:
                print_error(content, "CRASH", str(e))
                all_ok = False
                
        except Exception as e:
            content = f"powerset({input_str})"
            print_error(content, "UNKNOWN CRASH", str(e))
            all_ok = False

    print_final(8, all_ok)

if __name__ == "__main__":
    run()