# tests/utils.py
GREEN = "\033[0;32m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
CYAN = "\033[0;36m"
YELLOW = "\033[1;33m"
BOLD = "\033[1m"
NC = "\033[0m"

def print_header(ex_nb, title):
    print(f"\n\n{BLUE}{'=' * 40}{NC}")
    print(f"{BLUE}{BOLD}# EX {ex_nb:02} - {title.upper()}{NC}")
    print(f"{BLUE}{'=' * 40}{NC}")

def print_result(description, result, expected):
    is_correct = (result == expected)
    status = f"{GREEN}OK{NC}" if is_correct else f"{RED}FAIL{NC}"
    print(f"  {YELLOW}•{NC} {description}: {result} [{status}]")
    return is_correct

def print_final(exercise_nb, all_ok):
    ex_str = f"EX {exercise_nb:02}"
    status = f"{GREEN}✅ TODO OK{NC}" if all_ok else f"{RED}❌ ERRORES DETECTADOS{NC}"
    print(f"\n{BOLD}{ex_str}:{NC} {status}")
    print(f"{BLUE}{'-' * 40}{NC}")