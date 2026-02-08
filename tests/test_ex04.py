from ex04_truth_table import print_truth_table
from utils import print_header, print_final, RED, CYAN, BLUE, YELLOW, GREEN, NC

def run():
    print_header(4, "TRUTH TABLE")
    
    cases = [
    #   Formula, Expected Success (True = Print Table, None = Error)
        ('A', True),
        ('A', False),  # FOrZAR FAIL de prueba
        ('A!', True),
        ('AB|', True),
        ('AB&', True),
        ('AB^', True),
        ('AB>', True),
        ('AB=', True),
        ('AA=', True),

        ('ABC==', True),
        ('AB>C>', True),
        ('AB>A>A>', True), # Pierce's Law

        # --- Casos de Error ---
        ("", None),         # Vacío
        ("AB", None),       # Faltan operadores (stack > 1 al final)
        ("A+", None),       # Carácter inválido
        (123, None)         # Tipo inválido
    ]
    
    all_ok = True

    for case in cases:
        formula, expected = case
        
        # Decoración visual para separar las tablas
        if expected is True:
            print(f"\n{CYAN}┌──────────────────────────────────────────┐{NC}")
            print(  f"{CYAN}│ Testing Formula: {YELLOW}{str(formula):<24}{CYAN}│{NC}")
            print(  f"{CYAN}└──────────────────────────────────────────┘{NC}")

        try:
            # Intentamos ejecutar la función
            # NOTA: Como la función imprime a stdout, aquí solo capturamos si explota o no.
            print_truth_table(formula)
            
            if expected is None:
                # Si esperábamos error y NO falló -> MAL
                print(f"  {YELLOW}•{NC} '{formula}' {RED}[FAIL]{NC}")
                print(f"    {BLUE}└── Se esperaba un error, pero la función se ejecutó.{NC}")
                all_ok = False
            else:
                # Si esperábamos tabla y salió bien -> BIEN
                # (La verificación visual de la tabla es responsabilidad del usuario)
                print(f"{GREEN}  [OK] Tabla generada sin errores.{NC}")

        except (ValueError, TypeError) as e:
            if expected is None:
                # Si esperábamos error y falló -> BIEN
                print(f"  {YELLOW}•{NC} '{formula}' {CYAN}[VAL ERROR OK]{NC}")
                print(f"    {BLUE}└── {e}{NC}")
            else:
                # Si esperábamos tabla y falló -> MAL
                print(f"  {YELLOW}•{NC} Formula '{formula}' {CYAN}[CRASH]{NC}")
                print(f"    {BLUE}└── {e}{NC}")
                
        except Exception as e:
            print(f"  {YELLOW}•{NC} Formula '{formula}' {CYAN}[UNKNOWN CRASH]{NC}")
            print(f"    {BLUE}└── {e}{NC}")

    print_final(4, all_ok)

if __name__ == "__main__":
    run()