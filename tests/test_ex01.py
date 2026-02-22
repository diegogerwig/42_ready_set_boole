from ex01_multiplier import multiplier
from utils import print_header, print_result, print_final, print_error


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
        (3, 4, 5),  # Más de 2 argumentos
        (3,),  # Un solo argumento
        (3, "x"),  # Tipos incorrectos (str)
        ("a", 2),  # Tipos incorrectos (str)
    ]

    all_ok = True

    for case in cases:
        try:
            if not isinstance(case, tuple) or len(case) != 2:
                raise ValueError(f"Se esperaban 2 argumentos, se recibió: {case}")

            a, b = case
            res = multiplier(a, b)

            if isinstance(a, int) and isinstance(b, int):
                expected = a * b
            else:
                expected = None

            if not print_result(f"{a} * {b}", res, expected):
                all_ok = False

        except ValueError as e:
            print_error(str(case), "VALUE ERROR", str(e))

        except TypeError as e:
            print_error(str(case), "TYPE ERROR", str(e))

        except Exception as e:
            print_error(str(case), "CRASH", str(e))
            all_ok = False

    print_final(1, all_ok)


if __name__ == "__main__":
    run()
