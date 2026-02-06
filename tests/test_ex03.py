import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ex03_eval import eval_formula
from utils import print_header, print_result, print_final

def run():
    print_header(3, "BOOLEAN EVALUATION (RPN)")
    # Casos del PDF [cite: 269-274]
    cases = [("10&", False), ("10|", True), ("11>", True), ("10=", False), ("1011||=", True)]
    all_ok = True
    for formula, exp in cases:
        res = eval_formula(formula)
        if not print_result(formula, res, exp): all_ok = False
    print_final(3, all_ok)

if __name__ == "__main__":
    run()