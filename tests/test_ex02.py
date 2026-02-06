import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ex02_gray_code import gray_code
from utils import print_header, print_result, print_final

def run():
    print_header(2, "GRAY CODE")
    # Casos del PDF [cite: 213-231]
    expected_map = {0:0, 1:1, 2:3, 3:2, 4:6, 5:7, 6:5, 7:4, 8:12}
    all_ok = True
    for n, exp in expected_map.items():
        res = gray_code(n)
        if not print_result(f"n={n}", res, exp): all_ok = False
    print_final(2, all_ok)

if __name__ == "__main__":
    run()