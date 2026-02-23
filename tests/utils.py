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

def run_cases(ex_num: int, funcion_a_testear, casos: list, funcion_esperada=None, simbolo=""):
    """
    Motor genérico para ejecutar casos de prueba, atrapar errores y formatear la salida.
    """
    all_ok = True

    for case in casos:
        try:
            # 1. Aseguramos que los argumentos se puedan desempaquetar
            if not isinstance(case, tuple):
                case = (case,)
                
            # 2. Llamamos a tu función con los argumentos desempaquetados (*case)
            res = funcion_a_testear(*case)

            # 3. Calculamos el resultado esperado (si nos pasaron una función de referencia y no hay letras)
            expected = None
            if funcion_esperada and all(isinstance(arg, int) for arg in case):
                expected = funcion_esperada(*case)

            # 4. Generamos la descripción (ej: "3 + 4" o "gray_code(5)")
            if len(case) == 2 and simbolo:
                desc = f"{case[0]} {simbolo} {case[1]}"
            else:
                desc = f"{funcion_a_testear.__name__}{case}"

            # 5. Comparamos
            if not print_result(desc, res, expected):
                all_ok = False

        except ValueError as e:
            print_error(str(case), "VALUE ERROR", str(e))
            
        except TypeError as e:
            print_error(str(case), "TYPE ERROR", str(e))
            
        except Exception as e:
            print_error(str(case), "CRASH", str(e))
            all_ok = False

    print_final(ex_num, all_ok)