import io
from contextlib import redirect_stdout
from ex04_truth_table import print_truth_table, eval_formula_with_vars
from utils import print_header, print_final, RED, CYAN, BLUE, YELLOW, GREEN, NC

def verify_printed_table(formula: str, output: str) -> tuple[bool, str]:
    """
    Parsea y verifica la tabla. Retorna (True, "") si todo ok, o (False, "Motivo") si falla.
    """
    variables = sorted(list(set([c for c in formula if c.isalpha()])))
    lines = output.strip().split('\n')
    data_rows_found = 0
    
    for line in lines:
        if "---" in line or not line.strip(): continue
        parts = [p.strip() for p in line.split('|') if p.strip().isdigit()]
        if not parts: continue

        values = list(map(int, parts))
        printed_result = bool(values[-1])
        inputs = values[:-1]
        
        if len(inputs) != len(variables):
            return False, f"Estructura incorrecta en fila: {line}"

        var_values = {var: bool(val) for var, val in zip(variables, inputs)}
        try:
            calculated_result = eval_formula_with_vars(formula, var_values)
        except Exception:
            return False, "Error interno evaluando fórmula de verificación"

        if calculated_result != printed_result:
            return False, f"Error matemático. Entrada: {var_values} -> Tu Output: {int(printed_result)} != Real: {int(calculated_result)}"
            
        data_rows_found += 1

    if data_rows_found == 0:
        return False, "No se encontraron datos en la tabla impresa"

    return True, ""

def run():
    print_header(4, "TRUTH TABLE")
    
    cases = [
    #   (formula, expected_validity)
    #   True = Debe imprimir tabla válida | None = Debe dar error
        ('A', True),
        ('A!', True),
        ('AB|', True),
        ('AB&', True),
        ('AB^', True),
        ('AB>', True),
        ('AB=', True),
        ('AA=', True),

        ('ABC==', True),
        ('AB>C>', True),
        ('AB>A>A>', True), 
        
    # --- Casos de Error ---
        ('ABC====', None),
        ("", None),
        ("AB", None),
        ("A+", None),
        (123, None)
    ]
    
    all_ok = True

    for case in cases:
        formula, expected = case
        desc = f"Formula '{formula}'"
        
        # Capturar STDOUT y Excepciones
        f = io.StringIO()
        exception_occurred = None
        
        try:
            with redirect_stdout(f):
                print_truth_table(formula)
        except Exception as e:
            exception_occurred = e
            
        output = f.getvalue()
        
        # --- MODIFICACIÓN: IMPRIMIR LA TABLA SI SE GENERA ---
        if expected is True and output.strip():
            print(f"\n{CYAN}┌──────────────────────────────────────────┐{NC}")
            print(f"{CYAN}│ Testing Formula: {YELLOW}{str(formula):<24}{CYAN}│{NC}")
            print(f"{CYAN}└──────────────────────────────────────────┘{NC}")
            print(output) # Aquí mostramos lo que se capturó
        # ----------------------------------------------------

        is_error_printed = "Error" in output

        # Verificar Resultados con Formato ex03

        if expected is None:
            # CASO: ESPERAMOS ERROR (None)
            if exception_occurred:
                # Excepción capturada -> VAL ERROR (Como en ex03)
                print(f"  {YELLOW}•{NC} {desc:<50} [{CYAN}VAL ERROR{NC}]")
                print(f"    {BLUE}└── {exception_occurred}{NC}")
            elif is_error_printed:
                # Error impreso -> ERROR HANDLED (Variante válida de error)
                print(f"  {YELLOW}•{NC} {desc:<50} [{CYAN}ERROR MSG{NC}]")
                print(f"    {BLUE}└── La función imprimió el mensaje de error esperado.{NC}")
            else:
                # Ni excepción ni mensaje de error -> FAIL
                print(f"  {YELLOW}•{NC} {desc:<50} {RED}[FAIL]{NC}")
                print(f"    {RED}└── Se esperaba un error, pero la función continuó.{NC}")
                all_ok = False

        else: 
            # CASO: ESPERAMOS ÉXITO (True)
            if exception_occurred:
                print(f"  {YELLOW}•{NC} {desc:<50} [{CYAN}CRASH]{NC}")
                print(f"    {BLUE}└── {exception_occurred}{NC}")
                all_ok = False
            elif is_error_printed:
                print(f"  {YELLOW}•{NC} {desc:<50} {RED}[FAIL]{NC}")
                print(f"    {RED}└── La función imprimió un mensaje de error inesperado.{NC}")
                all_ok = False
            else:
                # Verificación Dinámica de la Tabla
                is_valid, msg = verify_printed_table(formula, output)
                
                if is_valid:
                    print(f"  {YELLOW}•{NC} {desc:<50} [{GREEN} OK {NC}]")
                else:
                    print(f"  {YELLOW}•{NC} {desc:<50} {RED}[FAIL]{NC}")
                    print(f"    {RED}└── {msg}{NC}")
                    all_ok = False

    print_final(4, all_ok)

if __name__ == "__main__":
    run()