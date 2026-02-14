from ex02_gray_code import gray_code
from utils import print_header, print_result, print_final, print_error

def run():
    print_header(2, "GRAY CODE")
    
    cases = [
    #   (n, expected)
        (0, 0),
        (1, 1),
        (2, 3),
        (3, 2),
        (4, 6),
        (5, 7),
        (6, 5),
        (7, 4),
        (8, 12),
        
    # --- Casos de error ---
        (-1, None),      
        ('a', None),
        (3, 4, 5),
        (3,)
    ]
    
    all_ok = True

    for case in cases:
        n = case[0] if isinstance(case, tuple) and len(case) > 0 else case
        desc = f"gray_code({n})"

        try:
            if not isinstance(case, tuple) or len(case) != 2:
                raise ValueError(f"Se esperaban 2 argumentos (n, expected), se recibió: {case}")
            
            _, expected = case

            res = gray_code(n)
            
            if not print_result(desc, res, expected):
                all_ok = False

        except ValueError as e:
            print_error(desc, "VALUE ERROR", str(e))
            
        except TypeError as e:
            print_error(desc, "TYPE ERROR", str(e))
            
        except Exception as e:
            print_error(desc, "CRASH", str(e))
            all_ok = False

    print_final(2, all_ok)

if __name__ == "__main__":
    run()