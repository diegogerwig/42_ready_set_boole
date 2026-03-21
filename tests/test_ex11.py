import random

from ex11_inverse import reverse_map
from ex10_curve import map_coords
from utils import *


def run():
    print_header(11, "INVERSE (HILBERT UNMAP)")

    cases = [
        #   (n, expected_coords_as_floats)
        (0.0, (0.0, 0.0)),
        (1.0, (65535.0, 0.0)),
        # --- Casos de error ---
        (-0.5, None),  # Fuera de rango (inferior)
        (1.5, None),  # Fuera de rango (superior)
        ("0.5", None),  # Tipo inválido
    ]

    all_ok = True

    for case in cases:
        n, expected = case
        desc = f"reverse_map({n})"

        try:
            res = reverse_map(n)

            if expected is None:
                content = f"{desc}: {res}"
                print(f" {YELLOW}•{NC} {content:<{PAD_LENGTH}} [{RED}FAIL{NC}]")
                print(f"    {RED}└── Se esperaba un error, pero devolvió un valor.{NC}")
                all_ok = False
            else:
                if not print_result(desc, res, expected):
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

    # --- PRUEBAS DE IDA Y VUELTA (ROUND-TRIP) ---
    print(f"\n{CYAN}--- Pruebas de Bidireccionalidad (Round-Trip) ---{NC}")
    print(f"{CYAN}    Fórmula: reverse_map(map_coords(x, y)) == (x, y){NC}\n")

    test_count = 10000
    round_trip_success = True

    # Probamos coordenadas aleatorias masivas
    for _ in range(test_count):
        original_x = random.randint(0, 65535)
        original_y = random.randint(0, 65535)

        # 1. Mapear (2D -> 1D)
        d = map_coords(original_x, original_y)

        # 2. Desmapear (1D -> 2D)
        recovered_x, recovered_y = reverse_map(d)

        # 3. Comprobar exactitud
        if recovered_x != original_x or recovered_y != original_y:
            round_trip_success = False
            failed_case = (original_x, original_y)
            failed_d = d
            failed_recovered = (recovered_x, recovered_y)
            break

    desc_rt = f"Round-Trip verificado en {test_count} puntos aleatorios"

    if round_trip_success:
        print_result(desc_rt, True, True)
    else:
        print(f" {YELLOW}•{NC} {desc_rt:<{PAD_LENGTH}} [{RED}FAIL{NC}]")
        print(
            f"    {RED}└── Fallo en {failed_case} -> cur:{failed_d} -> rev:{failed_recovered}{NC}"
        )
        all_ok = False

    print_final(11, all_ok)


if __name__ == "__main__":
    run()



