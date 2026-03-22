from ex11_inverse import inverse_curve
from ex10_curve import map_to_curve 
from utils import *


def run():
    print_header(11, "INVERSE CURVE (REVERSE Z-ORDER)")

    MAX_VAL = float(0xFFFFFFFF)

    cases = [
        # ((float_value,), (expected_x, expected_y))
        ((0.0,), (0, 0)),
        (((1.0 / MAX_VAL),), (1, 0)),
        (((2.0 / MAX_VAL),), (0, 1)),
        (((3.0 / MAX_VAL),), (1, 1)),
        (((4.0 / MAX_VAL),), (2, 0)),
        (((8.0 / MAX_VAL),), (0, 2)),
        (((12.0 / MAX_VAL),), (2, 2)),
        (((15.0 / MAX_VAL),), (3, 3)),
        ((1.0,), (0xFFFF, 0xFFFF)), 
        
        # Casos de error
        ((-0.1,), None),
        ((1.1,), None),
        (("0.5",), None),
    ]

    run_cases(
        ex_num=11,
        funcion_a_testear=inverse_curve,
        casos=cases,
    )


if __name__ == "__main__":
    run()