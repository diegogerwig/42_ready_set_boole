import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ex00_adder import adder
from utils import print_final, print_header, print_result, print_final

def run():
    print_header(0, "ADDER (Aritmética Bitwise)")
    cases = [(1, 1), (10, 5), (255, 1), (13, 37)]
    all_ok = True

    for a, b in cases:
        res = adder(a, b)
        if not print_result(f"{a} + {b}", res, a + b):
            all_ok = False

    print_final(0, all_ok)

if __name__ == "__main__":
    run()