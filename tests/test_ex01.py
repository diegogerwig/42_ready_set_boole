from ex01_multiplier import multiplier
from utils import print_header, print_result, print_final, CYAN, BLUE, YELLOW, NC

def run():
    print_header(1, "MULTIPLIER (Aritmética Bitwise)")
    
    cases = [
    #   (a, b)
        (0, 0),
        (1, 0),
        (0, 1),    
        (1, 1),    
        (1, 2),    
        (2, 2),    
        
        (10, 5),
        (12, 12),
        (1024, 2),
        
    # --- Casos de error ---
        (-5, 10),
        (10, -5),
        ('a', 2)
    ]
    
    all_ok = True

    for case in cases:
        try:
            if len(case) != 2:
                raise ValueError(f"Formato inválido: {case}")
            
            a, b = case
            
            res = multiplier(a, b)
            
            if isinstance(a, int) and isinstance(b, int):
                expected = a * b
            else:
                expected = None

            if not print_result(f"{a} * {b}", res, expected):
                all_ok = False

        except ValueError as e:
            print(f"  {YELLOW}•{NC} {str(case):<50} [{CYAN}VAL ERROR{NC}]")
            print(f"    {BLUE}└── {e}{NC}")
            
        except TypeError as e:
            print(f"  {YELLOW}•{NC} {str(case):<50} [{CYAN}TYPE ERR{NC}]")
            print(f"    {BLUE}└── {e}{NC}")
            
        except Exception as e:
            print(f"  {YELLOW}•{NC} {str(case):<50} [{CYAN}CRASH{NC}]")
            print(f"    {BLUE}└── {e}{NC}")

    print_final(1, all_ok)

if __name__ == "__main__":
    run()