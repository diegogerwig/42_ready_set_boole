from ex00_adder import adder
from utils import *


def run():
    print_header(0, "ADDER (Aritmética Bitwise)")

    cases = [
        # (a, b)
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
        (1, 2),
        (2, 2),
        (3, 4),
        (10, 5),
        (255, 1),
        (1001, 9999),
        (13, 37),
        # Casos de error
        (100, -1),
        (3, 4, 5),
        (3,),
        (3, "x"),
        (3, "3"),
    ]

    run_cases(
        ex_num = 0,
        funcion_a_testear = adder,
        casos = cases,
        funcion_esperada = lambda a, b: a + b,
        simbolo = "+"
    )

if __name__ == "__main__":
    run()
