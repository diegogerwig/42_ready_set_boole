import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ex08_powerset import powerset
from utils import print_header, print_result, print_final

def run():
    print_header(8, "Powerset")
    
    all_ok = True
    
    # Caso 1: Conjunto Vacío -> [[]]
    res = powerset([])
    if not print_result("Powerset([])", res, [[]]): all_ok = False
    
    # Caso 2: Un elemento -> [[], [1]]
    res = powerset([1])
    # Ordenamos para asegurar la comparación (aunque el algoritmo es determinista)
    res.sort(key=len)
    if not print_result("Powerset([1])", res, [[], [1]]): all_ok = False
    
    # Caso 3: Verificar Cardinalidad (Tamaño 3 -> 2^3 = 8 subconjuntos)
    s = [1, 2, 3]
    res_large = powerset(s)
    expected_len = 2 ** len(s)
    
    # Mostramos el resultado visualmente
    print(f"  Subconjuntos de {s}: {res_large}")
    
    if not print_result(f"Cardinalidad de P({s})", len(res_large), expected_len):
        all_ok = False

    print_final(8, all_ok)

if __name__ == "__main__":
    run()