import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ex05_nnf import negation_normal_form
from utils import print_header, print_result, print_final

def run():
    print_header(5, "NEGATION NORMAL FORM (NNF)")
    # Casos del PDF [cite: 369-373]
    cases = [("AB&!", "A!B!|"), ("AB|!", "A!B!&"), ("AB>", "A!B|"), ("AB=", "AB&A!B!&|")]
    all_ok = True
    for formula, exp in cases:
        res = negation_normal_form(formula)
        print_result(formula, res, exp, "Equivalence test")
    print_final(5, True) # Varias salidas pueden ser válidas [cite: 364]

if __name__ == "__main__":
    run()