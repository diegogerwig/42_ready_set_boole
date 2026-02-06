import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ex04_truth_table import print_truth_table
from utils import print_header, print_final

def run():
    print_header(4, "TRUTH TABLE")
    formula = "AB&C|" # (A ∧ B) ∨ C [cite: 302-304]
    print(f"Generating table for: {formula}\n")
    print_truth_table(formula)
    # Este test es visual, comparamos con pág 21 [cite: 308-318]
    print_final(4, True)

if __name__ == "__main__":
    run()