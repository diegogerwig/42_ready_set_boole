from ex00_adder import adder
from utils import *


def run():
    print_header(0, "ADDER (Aritmética Bitwise)")

    cases = [
        # ((a, b), expected)
        ((0, 0), 0),
        ((1, 0), 1),
        ((0, 1), 1),
        ((1, 1), 2),
        ((1, 2), 3),
        ((2, 2), 4),
        # Casos de error
        ((100, -1), None),
        ((3, 4.4), None),
        ((3, None), None),
        ((3, "x"), None),
        ((3, "3"), None),
    ]

    run_cases(
        ex_num = 0,
        funcion_a_testear = adder,
        casos = cases,
    )

if __name__ == "__main__":
    run()
