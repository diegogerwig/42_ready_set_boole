from ex10_curve import map_to_curve
from utils import *


def run():
    print_header(10, "MAP TO CURVE (MORTON CODE / Z-ORDER)")

    MAX_VAL = float(0xFFFFFFFF)

    def wrapper_curve(x, y):
        res = map_to_curve(x, y)
        
        if not (0.0 <= res <= 1.0):
            return f"FAIL: El resultado {res} no está entre 0 y 1."
            
        return f"{res:.15f}"

    cases = [
        # ((Values X, Y), Expected_Output)
        ((0, 0), f"{0.0:.15f}"),
        ((1, 0), f"{(1.0 / MAX_VAL):.15f}"),
        ((0, 1), f"{(2.0 / MAX_VAL):.15f}"),
        ((1, 1), f"{(3.0 / MAX_VAL):.15f}"),
        ((2, 0), f"{(4.0 / MAX_VAL):.15f}"),
        ((0, 2), f"{(8.0 / MAX_VAL):.15f}"),
        ((2, 2), f"{(12.0 / MAX_VAL):.15f}"),
        ((3, 3), f"{(15.0 / MAX_VAL):.15f}"),
        ((65535, 65535), f"{1.0:.15f}"), 
        
        # Casos de error
        ((-1, 0), None),
        ((0, -1), None),
        (("1", 0), None),
        ((65536, 0), None),
    ]


    run_cases(
        ex_num=10,
        funcion_a_testear=wrapper_curve,
        casos=cases,
    )


if __name__ == "__main__":
    run()