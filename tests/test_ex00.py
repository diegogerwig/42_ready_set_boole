from ex00_adder import adder
from utils import print_header, print_result, print_final, RED, YELLOW, NC

def run():
    print_header(0, "ADDER (Aritmética Bitwise)")
    cases = [
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
        (1, 2),
        (2, 2),
        (3, 4), 
        (10, 5), 
        (255, 1), 
        (1001, 9999),
        (13, 37),
        # --- Casos que provocarán errores ---
        (100, -1),
        (3, 4, 5),
        (3),
        (3, 'x'),
        (3, '3')
        ]
    all_ok = True

    for case in cases:
        try:
            if len(case) != 2:
                raise ValueError(f"Se esperaban 2 argumentos, se recibieron {len(case)}")
            
            a, b = case

            res = adder(a, b)
            
            if isinstance(a, int) and isinstance(b, int):
                 expected = a + b
            else:
                 expected = None 

            if not print_result(f"{a} + {b}", res, expected):
                all_ok = False
                
        except ValueError as e:
            print(f"  {YELLOW}•{NC} {str(case):<50} [{RED}VALUE ERROR{NC}]")
            print(f"    {RED}└── {e}{NC}")
            
        except TypeError as e:
            print(f"  {YELLOW}•{NC} {str(case):<50} [{RED}TYPE ERROR{NC}]")
            print(f"    {RED}└── {e}{NC}")
            
        except Exception as e:
            print(f"  {YELLOW}•{NC} {str(case):<50} [{RED}CRASH{NC}]")
            print(f"    {RED}└── {e}{NC}")

    print_final(0, all_ok)

if __name__ == "__main__":
    run()