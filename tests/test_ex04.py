import io
from contextlib import redirect_stdout

from ex04_truth_table import truth_table
from ex03_eval import eval_formula
from utils import *


def verify_printed_table(formula: str, output: str) -> tuple[bool, str]:
    """
    Parsea y verifica la tabla matemáticamente independientemente de los espacios.
    """
    variables = []
    for char in formula:
        if "A" <= char <= "Z" and char not in variables:
            variables.append(char)

    lines = output.strip().split("\n")
    data_rows_found = 0

    for line in lines:
        # Ignoramos la cabecera, los separadores y la línea final vacía
        if "---" in line or not line.strip() or "=" in line or line.endswith("||"):
            continue
            
        parts = [p.strip() for p in line.split("|") if p.strip().isdigit()]
        if not parts:
            continue

        values = list(map(int, parts))
        printed_result = bool(values[-1])
        inputs = values[:-1]

        if len(inputs) != len(variables):
            return False, f"Estructura incorrecta en fila: {line}"

        # Sustituimos las variables (A, B) por sus valores (0, 1) en el string
        formula_verificacion = formula
        for var, val in zip(variables, inputs):
            formula_verificacion = formula_verificacion.replace(var, str(val))
            
        try:
            calculated_result = eval_formula(formula_verificacion)
        except Exception:
            return False, "Error interno evaluando fórmula de verificación"

        if calculated_result != printed_result:
            var_values = {var: bool(val) for var, val in zip(variables, inputs)}
            return (
                False,
                f"Error matemático. Entrada {var_values} -> "
                f"Tu Output: {int(printed_result)} != Real: {int(calculated_result)}"
            )

        data_rows_found += 1

    if data_rows_found == 0 and len(variables) > 0:
        return False, "No se encontraron datos en la tabla impresa."

    return True, ""


def run():
    print_header(4, "TRUTH TABLE")

    def print_truth_table(formula):
        f = io.StringIO()
        with redirect_stdout(f):
            truth_table(formula)
        output = f.getvalue()
        
        is_valid, msg = verify_printed_table(formula, output)
        if not is_valid:
            print(f"    {RED}└── {msg}{NC}")
            return False
            
        print(f"\n{CYAN}┌──────────────────────────────────────────┐{NC}")
        print(f"{CYAN}│ Tabla de verdad: {YELLOW}{str(formula):<24}{CYAN}│{NC}")
        print(f"{CYAN}└──────────────────────────────────────────┘{NC}")
        print(output.strip())
        print() 

        return True

    cases = [
        # ((formula), expected)
        (("A",), True),
        (("A!",), True),
        (("AB|",), True),
        (("AB&",), True),
        (("AB^",), True),
        (("AB>",), True),
        (("AB=",), True),
        (("AA=",), True),
        (("ABC==",), True),
        (("AB>C>",), True),
        (("AB>A>A>",), True),
        # Casos de Error
        (("ABC====",), None),
        (("",), None),
        (("AB",), None),
        (("A+",), None),
        ((123,), None),
        (("A1="), None),
    ]

    run_cases(
        ex_num=4,
        funcion_a_testear=print_truth_table,
        casos=cases,
    )


if __name__ == "__main__":
    run()