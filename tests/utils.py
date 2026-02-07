import sys

# Códigos de colores ANSI
GREEN = "\033[0;32m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
CYAN = "\033[0;36m"
YELLOW = "\033[1;33m"
BOLD = "\033[1m"
NC = "\033[0m"

def print_header(ex_nb, title):
    print(f"\n\n{BLUE}{'=' * 60}{NC}")
    print(f"{BLUE}{BOLD}# EX {ex_nb:02} - {title.upper()}{NC}")
    print(f"{BLUE}{'=' * 60}{NC}")

def print_result(description, result, expected):
    is_correct = (result == expected)
    
    if is_correct:
        status = f"[{GREEN} OK {NC}]"
    else:
        status = f"[{RED}FAIL{NC}]"

    content = f"{description}: {result}"
    print(f"  {YELLOW}•{NC} {content:<50} {status}")

    return is_correct

def print_final(exercise_nb, all_ok):
    ex_str = f"EX {exercise_nb:02}"
    if all_ok:
        status = f"{GREEN}✅ TODO OK{NC}"
        print(f"\n{BOLD}{ex_str}:{NC} {status}")
        print(f"{BLUE}{'-' * 60}{NC}\n")
    else:
        status = f"{RED}❌ ERRORES DETECTADOS{NC}"
        print(f"\n{BOLD}{ex_str}:{NC} {status}")
        print(f"{BLUE}{'-' * 60}{NC}\n")
        
        sys.exit(1)