import sys

GREEN = "\033[0;32m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
CYAN = "\033[0;36m"
YELLOW = "\033[1;33m"
BOLD = "\033[1m"
NC = "\033[0m"

PAD_LENGTH = 70


def print_header(ex_nb, title):
    print(f"\n{BLUE}{'=' * 80}{NC}")
    print(f"{BLUE}{BOLD}# EX {ex_nb:02} - {title.upper()}{NC}")
    print(f"{BLUE}{'=' * 80}{NC}")


def print_result(description, result, expected):
    is_correct = result == expected

    if is_correct:
        status = f"[{GREEN} OK {NC}]"
    else:
        status = f"[{RED}FAIL{NC}]"

    content = f"{description}: {result}"
    print(f" {YELLOW}•{NC} {content:<{PAD_LENGTH}} {status}")

    return is_correct


def print_error(description, error_type, error_msg):
    status = f"[{CYAN}{error_type}{NC}]"

    print(f" {YELLOW}•{NC} {description:<{PAD_LENGTH}} {status}")
    print(f"   {BLUE}└── {error_msg}{NC}")


def print_final(exercise_nb, all_ok):
    ex_str = f"EX {exercise_nb:02}"
    if all_ok:
        status = f"{GREEN}✅ TODO OK{NC}"
        print(f"\n{BOLD}{ex_str}:{NC} {status}")
        print(f"{BLUE}{'-' * 80}{NC}\n")
    else:
        status = f"{RED}❌ ERRORES DETECTADOS{NC}"
        print(f"\n{BOLD}{ex_str}:{NC} {status}")
        print(f"{BLUE}{'-' * 80}{NC}\n")
        sys.exit(1)
