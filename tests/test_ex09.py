from ex09_eval_set import eval_set
from utils import *


def run():
    print_header(9, "SET EVALUATION")

    cases = [
        # ((Formula, Sets), Expected_Output)
        (("AB&", [[0, 1, 2], [0, 3, 4]]), [0]),
        (("AB|", [[0, 1, 2], [3, 4, 5 ]]), [0, 1, 2, 3, 4, 5]),
        (("A!", [[0, 1, 2]]), []),
        (("A", [[]]), []),
        (("A!", [[]]), []),
        (("A", [[42]]), [42]),
        (("A!", [[42]]), []),
        (("A!B&", [[1, 2, 3], [2, 3, 4]]), [4]),
        (("AB|", [[0, 1, 2], []]), [0, 1, 2]),
        (("AB&", [[0, 1, 2], []]), []),
        (("AB&", [[0, 1, 2], [0]]), [0]),
        (("AB&", [[0, 1, 2], [42]]), []),
        (("AB^", [[0, 1, 2], [0]]), [1, 2]),
        (("AB>", [[0], [1, 2]]), [1, 2]),
        (("AB>", [[0], [0, 1, 2]]), [0, 1, 2]),
        (("ABC||", [[], [], []]), []),
        (("ABC||", [[0], [1], [2]]), [0, 1, 2]),
        (("ABC||", [[0], [0], [0]]), [0]),
        (("ABC&&", [[0], [0], []]), []),
        (("ABC&&", [[0], [0], [0]]), [0]),
        (("ABC^^", [[0], [0], [0]]), [0]),
        (("ABC>>", [[0], [0], [0]]), [0]),
        
        # Casos de error
        (("", [[0]]), None),         # Fórmula vacía
        (("AB", [[0], [1]]), None),  # Sobran operandos
        (("&", [[0], [1]]), None),   # Faltan operandos
        (("A+", [[0]]), None),       # Carácter inválido
    ]

    def format_desc(*args):
        formula = args[0]
        sets_str = str(args[1])
        disp_sets = (sets_str[:25] + "...") if len(sets_str) > 25 else sets_str
        return f"eval_set('{formula}', {disp_sets})"

    run_cases(
        ex_num=9,
        funcion_a_testear=eval_set,
        casos=cases,
        custom_desc_func=format_desc
    )


if __name__ == "__main__":
    run()