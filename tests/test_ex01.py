from ex01_multiplier import multiplier
from utils import *


def run():
    print_header(1, "MULTIPLIER (Aritmética Bitwise)")

    cases = [
        #   ((a, b), expected)
        ((0, 0), 0),
        ((1, 0), 0),
        ((0, 1), 0),
        ((1, 1), 1),
        ((1, 2), 2),
        ((2, 2), 4),
        # --- Casos de error ---
        ((-5, 10), None),
        ((10, -5), None),
        ((3, 4, 5), None),  # Más de 2 argumentos
        ((3,), None),       # Un solo argumento
        ((3, "x"), None),   # Tipos incorrectos (str)
        (("a", 2), None),   # Tipos incorrectos (str)
    ]

    run_cases(
        ex_num=1,
        funcion_a_testear=multiplier,
        casos=cases,
        # # Usamos b=None para evitar el error si se pasa un solo argumento en los casos de error
        # custom_desc_func=lambda a, b=None: f"{a} * {b}" if b is not None else str(a)
    )


if __name__ == "__main__":
    run()