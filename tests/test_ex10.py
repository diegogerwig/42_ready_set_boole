import random

from ex10_curve import map_coords
from utils import *

def run():
    print_header(10, "CURVE (HILBERT MAP)")

    cases = [
    #   (x, y), expected
        ((0, 0), 0.0),                  # Principio de la curva
        ((65535, 0), 1.0),              # Final de la curva
        
    # --- Casos de error ---
        ((-1, 0), None),                # Fuera de rango (negativo)
        ((0, 65536), None),             # Fuera de rango (exceso)
        (("0", 0), None),               # Tipo inválido
        ((44.4, 555.5), None),          # Valores no enteros
    ]
    
    all_ok = True

    for case in cases:
        coords, expected = case
        x, y = coords
        desc = f"map_coords({x}, {y})"
        
        try:
            res = map_coords(x, y)
            
            if expected is None:
                content = f"{desc}: {res}"
                print(f" {YELLOW}•{NC} {content:<{PAD_LENGTH}} [{RED}FAIL{NC}]")
                print(f"    {RED}└── Se esperaba un error, pero devolvió un valor.{NC}")
                all_ok = False
            else:
                # Usamos una tolerancia pequeña para evitar errores de precisión de float
                is_close = abs(res - expected) < 1e-6
                
                res_str = f"{res:.6f}"
                expected_str = res_str if is_close else f"{expected:.6f}"
                
                if not print_result(desc, res_str, expected_str):
                    all_ok = False

        except (ValueError, TypeError) as e:
            if expected is None:
                print_error(desc, "VAL/TYPE ERROR", str(e))
            else:
                print_error(desc, "CRASH", str(e))
                all_ok = False
                
        except Exception as e:
            print_error(desc, "UNKNOWN CRASH", str(e))
            all_ok = False

    # --- PRUEBA DE UNICIDAD Y RANGO MASIVA ---
    print(f"\n{CYAN}--- Pruebas Dinámicas (Unicidad y Rango [0, 1]) ---{NC}")
    
    visited_values = set()
    test_count = 10000
    is_unique = True
    is_in_range = True
    
    # Probamos una muestra grande de coordenadas aleatorias
    for _ in range(test_count):
        rx = random.randint(0, 65535)
        ry = random.randint(0, 65535)
        val = map_coords(rx, ry)
        
        if val in visited_values:
            is_unique = False
        visited_values.add(val)
        
        if not (0.0 <= val <= 1.0):
            is_in_range = False
            
    desc_range = f"Rango verificado [0, 1] en {test_count} iteraciones"
    desc_unique = f"Unicidad verificada en {test_count} iteraciones"
    
    if not print_result(desc_range, is_in_range, True): all_ok = False
    if not print_result(desc_unique, is_unique, True): all_ok = False

    print_final(10, all_ok)

if __name__ == "__main__":
    run()