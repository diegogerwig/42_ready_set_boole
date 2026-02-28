from ex02_gray_code import gray_code
from utils import *


def run():
    print_header(2, "GRAY CODE")

    cases = [
        # ((n), expected)
        ((0), 0),
        ((1), 1),
        ((2), 3),
        ((3), 2),
        ((4), 6),
        ((5), 7),
        ((6), 5),
        ((7), 4),
        ((8), 12),
        # Casos de error
        ((-1), None),
        (("a"), None),
        ((3, 4, 5), None),  # Demasiados argumentos
        ((), None),         # Sin argumentos
    ]

    run_cases(
        ex_num=2,
        funcion_a_testear=gray_code,
        casos=cases,
    )


if __name__ == "__main__":
    run()