from ex02_gray_code import gray_code
from utils import RED, print_header, print_result, print_final, CYAN, BLUE, YELLOW, NC

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
        
        # --- Casos que provocarán errores ---
        (-1, None),      
        ('a', None)     
        ]
    
    all_ok = True

    for case in cases:
        try:

            if len(case) != 2:
                raise ValueError(f"Formato inválido: {case}")
            
            n, expected = case

            res = gray_code(n)
            
            if not print_result(f"gray_code({n})", res, expected):
                all_ok = False

        except ValueError as e:
            desc = f"gray_code({n})"
            
            # 2. Imprimimos ALINEADO a 50 caracteres (igual que print_result)
            # Usamos RED para el tag de error y el mensaje, igual que Ex 01
            print(f"  {YELLOW}•{NC} {desc:<50} [{CYAN}VAL ERROR{NC}]")
            print(f"    {BLUE}└── {e}{NC}")
            
        except TypeError as e:
            desc = f"gray_code({n})"
            print(f"  {YELLOW}•{NC} {desc:<50} [{CYAN}TYPE ERR{NC}]")
            print(f"    {BLUE}└── {e}{NC}")
            
        except Exception as e:
            desc = f"gray_code({n})"
            print(f"  {YELLOW}•{NC} {desc:<50} [{CYAN}CRASH{NC}]")
            print(f"    {BLUE}└── {e}{NC}")

    print_final(2, all_ok)

if __name__ == "__main__":
    run()