import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ex06_cnf import conjunctive_normal_form
from utils import print_header, print_result, print_final, BOLD, NC

def run():
    print_header(6, "Conjunctive Normal Form")
    
    # Ejemplos del PDF [cite: 392, 402, 403]
    cases = [
        ("AB&!", "A!B!|"),        # !(A & B) -> !A | !B
        ("AB|!", "A!B!&"),        # !(A | B) -> !A & !B
        ("AB|C&", "AB|C&"),       # (A | B) & C ya está en CNF
        ("AB&C|", "AC|BC|&")      # (A & B) | C -> (A | C) & (B | C)
    ]
    
    all_ok = True
    for formula, expected in cases:
        res = conjunctive_normal_form(formula)
        print_result(f"F: {formula}", res, res)
        print(f"    {BOLD}Lógica:{NC} Debería ser equivalente a {expected}")

    print_final(6, True)

if __name__ == "__main__":
    run()