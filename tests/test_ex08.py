from ex08_powerset import powerset
from utils import *


def sort(ps: list[list[int]]) -> list[list[int]]:
    if not isinstance(ps, list):
        return ps
    
    def sort_criteria(sublist):
        return len(sublist), sublist
    
    internal_sorted = [sorted(list(sub)) for sub in ps]
    
    final_list = sorted(internal_sorted, key=sort_criteria)
    
    return final_list


def run():
    print_header(8, "POWERSET (CONJUNTO POTENCIA)")

    def wrapper_powerset(s):
        # Calculamos
        res = powerset(s)
        
        # Validamos tamaño matemático
        n = len(set(s))
        expected_len = 1 << n 
        
        if len(res) != expected_len:
            return f"FAIL: Cardinalidad incorrecta. Esperada {expected_len}, obtenida {len(res)}"
        
        # Devolvemos la lista agrupada por tamaño para que el test la imprima bonita
        return sort(res)

    raw_cases = [
        # ((Input,), Expected_Output)
        (([],), [[]]),
        (([0],), [[], [0]]),
        (([0, 1],), [[], [0], [1], [0, 1]]),
        (([0, 1, 2],), [[], [0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2]]),
        
        (([1, 1],), [[], [1]]), 
        
        # Casos de error
        ((None,), None),
        (("123",), None),
    ]

    cases_for_engine = []
    for args, expected in raw_cases:
        if expected is not None:
            expected = sort(expected)
        cases_for_engine.append((args, expected))

    def get_desc(s):
        s_str = str(s)
        if len(s_str) > 20:
            return f"powerset({s_str[:15]}...)"
        return f"powerset({s_str})"

    run_cases(
        ex_num=8,
        funcion_a_testear=wrapper_powerset,
        casos=cases_for_engine,
    )


if __name__ == "__main__":
    run()