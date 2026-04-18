from ex03_eval import eval_formula
from utils import *


def run():
    print_header(3, "BOOLEAN EVALUATION (RPN)")

    cases = [
        # ((formula), expected)
        (("0!"), True),
        (("1!"), False),
        (("00|"), False),
        (("10|"), True),
        (("01|"), True),
        (("11|"), True),
        (("10&"), False),
        (("11&"), True),
        (("11^"), False),
        (("10^"), True),
        (("00>"), True),
        (("01>"), True),
        (("10>"), False),
        (("11>"), True),
        (("00="), True),
        (("11="), True),
        (("10="), False),
        (("01="), False),
        (("11&0|"), True),
        (("10&1|"), True),
        (("11&1|"), True),
        (("11&1|1^"), False),
        (("01&1|1="), True),
        (("01&1&1&"), False),
        (("0111&&&"), False),
        # Casos de Error
        ((""), None),        # Vacío
        (("1&"), None),      # Falta operando
        (("11"), None),      # Sobra operando (falta operador)
        (("12&"), None),     # Carácter inválido ('2')
        (("ABC"), None),     # Basura
        (("01 &"), None),    # Sobra espacio
    ]

    run_cases(
        ex_num=3,
        funcion_a_testear=eval_formula,
        casos=cases,
    )


if __name__ == "__main__":
    run()