from ex07_sat import sat
from utils import *


def run():
    print_header(7, "SAT (SATISFIABILITY)")

    cases = [
        # ((formula), expected)
        (("A",), True),
        (("A!",), True),
        (("AA|",), True),
        (("AA&",), True),
        (("AA!&",), False),
        (("AA^",), False),
        (("AB^",), True),
        (("AB=",), True),
        (("AA>",), True),
        (("AA!>",), True),
        (("ABC||",), True),
        (("AB&A!B!&&",), False),
        (("ABCDE&&&&",), True),
        (("AAA^^",), True),
        (("ABCDE^^^^",), True),
        
        # Casos de error
        (("",), None),
        (("AB",), None),
        (("&",), None),
        (("A+",), None),
    ]

    run_cases(
        ex_num=7,
        funcion_a_testear=sat,
        casos=cases,
    )


if __name__ == "__main__":
    run()