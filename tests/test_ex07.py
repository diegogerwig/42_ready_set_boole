import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ex07_sat import sat
from utils import print_header, print_result, print_final

def run():
    print_header(7, "SAT (Satisfiability)")
    
    # Casos basados en lógica estándar y el PDF [cite: 438-442]
    cases = [
        ("AB|", True),     # A OR B -> Satisfacible (basta que uno sea 1)
        ("AB&", True),     # A AND B -> Satisfacible (si A=1, B=1)
        ("AA!&", False),   # A AND !A -> Contradicción (Nunca es verdad)
        ("AA!|", True)     # A OR !A -> Tautología (Siempre es verdad)
    ]
    
    all_ok = True
    for formula, expected in cases:
        res = sat(formula)
        if not print_result(f"Sat({formula})", res, expected):
            all_ok = False

    print_final(7, all_ok)

if __name__ == "__main__":
    run()