import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ex09_eval_set import eval_set
from utils import print_header, print_result, print_final

def run():
    print_header(9, "Set Evaluation")
    
    all_ok = True
    
    # Definimos unos conjuntos de prueba
    # A = [0, 1, 2], B = [0, 3, 4]
    # Universo implícito U = [0, 1, 2, 3, 4]
    sets = [[0, 1, 2], [0, 3, 4]]
    
    cases = [
        ("AB&", [0]),                  # Intersección: Solo el 0 está en ambos
        ("AB|", [0, 1, 2, 3, 4]),      # Unión: Todos los elementos
        ("A!",  [3, 4]),               # Complemento de A (U - A) -> [3, 4]
        ("AB^", [1, 2, 3, 4])          # Dif. Simétrica: (A-B) U (B-A)
    ]

    for formula, expected in cases:
        res = eval_set(formula, sets)
        if not print_result(f"F='{formula}' Sets={sets}", res, expected):
            all_ok = False

    # Caso complejo: Implicación Sets=[[0,1,2], [2]] (U=[0,1,2])
    # A=[0,1,2], B=[2]
    # A > B es !A | B -> [] | [2] -> [2]
    # A ver... !A = [], !A|B = [2]. Correcto.
    sets2 = [[0, 1, 2], [2]]
    formula2 = "AB>"
    res2 = eval_set(formula2, sets2)
    if not print_result(f"F='{formula2}' Sets={sets2}", res2, [2]):
        all_ok = False

    print_final(9, all_ok)

if __name__ == "__main__":
    run()