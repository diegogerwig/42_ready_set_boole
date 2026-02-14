from ex07_sat import sat
from utils import print_header, print_final, RED, CYAN, BLUE, YELLOW, NC, GREEN

def run():
    print_header(7, "SAT (SATISFIABILITY)")
    
    cases = [
    #   (formula, expected value)
        ('A', True),
        ('A!', True),
        ('AA|', True),
        ('AA&', True),
        ('AA!&', False),
        ('AA^', False),
        ('AB^', True),
        ('AB=', True),
        ('AA>', True),
        ('AA!>', True),

        ('ABC||', True),
        ('AB&A!B!&&', False),
        ('ABCDE&&&&', True),
        ('AAA^^', True),
        ('ABCDE^^^^', True),

    # --- Casos de error ---
        ("", None),
        ("AB", None),
        ("&", None),
        ("A+", None)
    ]
    
    all_ok = True

    for case in cases:
        try:
            formula, expected = case
            res = sat(formula)
            
            content = f"sat('{formula}'): {res}"
            
            if expected is None:
                print(f"  {YELLOW}•{NC} {content:<50} [{RED}FAIL{NC}]")
                print(f"    {RED}└── Se esperaba un error, pero devolvió: {res}{NC}")
                all_ok = False

            else:
                if res == expected:
                    print(f"  {YELLOW}•{NC} {content:<50} [{GREEN} OK {NC}]")
                else:
                    print(f"  {YELLOW}•{NC} {content:<50} [{RED}FAIL{NC}]")
                    print(f"    {RED}└── Esperado: {expected}{NC}")
                    all_ok = False

        except (ValueError, TypeError) as e:
            content = f"Formula '{formula}'"
            if expected is None:
                print(f"  {YELLOW}•{NC} {content:<50} [{CYAN}VAL ERROR{NC}]")
                print(f"    {BLUE}└── {e}{NC}")
            else:
                print(f"  {YELLOW}•{NC} {content:<50} [{CYAN}CRASH{NC}]")
                print(f"    {BLUE}└── {e}{NC}")
                all_ok = False
                
        except Exception as e:
            content = f"Formula '{formula}'"
            print(f"  {YELLOW}•{NC} {content:<50} [{CYAN}UNKNOWN CRASH{NC}]")
            print(f"    {BLUE}└── {e}{NC}")
            all_ok = False

    print_final(7, all_ok)

if __name__ == "__main__":
    run()