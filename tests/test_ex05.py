import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ex05_nnf import negation_normal_form
# Añadimos BOLD y NC a la importación
from utils import print_header, print_result, print_final, BOLD, NC 

def run():
    print_header(5, "Negation Normal Form")
    
    cases = [
        ("AB&!", "A!B!|"),
        ("AB|!", "A!B!&"),
        ("AB>", "A!B|"),
        ("AB&!C!|", "A!B!|C!|")
    ]
    
    all_ok = True
    for formula, expected in cases:
        res = negation_normal_form(formula)
        print_result(f"F: {formula}", res, res) 
        print(f"    {BOLD}Lógica:{NC} Debería ser similar a {expected}")

    print_final(5, True)

if __name__ == "__main__":
    run()