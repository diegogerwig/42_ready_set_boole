import sys, os

# Configuración de path para importar de src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

try:
    from ex05_nnf import negation_normal_form
    # Importamos la función de evaluación del Ex04 para verificar la equivalencia lógica
    from ex04_truth_table import eval_formula_with_vars
    from utils import print_header, print_final, RED, CYAN, BLUE, YELLOW, NC, GREEN
except ImportError as e:
    print(f"Error de importación: {e}")
    sys.exit(1)

def is_nnf_compliant(formula: str) -> bool:
    """
    Verifica que '!' solo aparezca después de una variable (letras) o constantes (0/1).
    Regla: "every occurence of '!' must be placed after a variable"
    """
    for i, char in enumerate(formula):
        if char == '!':
            # En notación RPN, el operador va DESPUÉS del operando.
            # Verificamos qué había antes del '!'
            if i == 0: return False # No puede empezar con !
            prev = formula[i-1]
            # Solo permitimos ! si lo anterior era una variable o constante
            if not (prev.isalpha() or prev in "01"):
                return False
    return True

def are_equivalent(f1: str, f2: str) -> bool:
    """
    Comprueba si dos fórmulas tienen la misma tabla de verdad.
    """
    # Obtenemos todas las variables únicas de ambas fórmulas
    vars1 = set([c for c in f1 if c.isalpha()])
    vars2 = set([c for c in f2 if c.isalpha()])
    variables = sorted(list(vars1.union(vars2)))
    n = len(variables)
    
    # Probamos las 2^n combinaciones
    for i in range(1 << n):
        vals = {}
        for j in range(n):
            vals[variables[j]] = bool((i >> j) & 1)
        
        try:
            res1 = eval_formula_with_vars(f1, vals)
            res2 = eval_formula_with_vars(f2, vals)
            if res1 != res2:
                return False
        except ValueError:
            return False
            
    return True

def run():
    print_header(5, "Negation Normal Form (NNF)")
    
    # Lista de Casos Obligatorios
    cases = [
        # --- Basic Tests ---
        "A", 
        "A!",
        "AB&!",
        "AB|!",
        "AB>!",
        "AB=!",
        
        # --- Composition Tests ---
        "ABC||",
        "ABC||!",
        "ABC|&",
        "ABC&|",
        "ABC&|!",
        "ABC^^",
        "ABC>>"
    ]

    all_ok = True

    print(f"{CYAN}--- Verificación Lógica y de Formato ---{NC}")
    
    for formula in cases:
        try:
            # 1. Transformar
            nnf_res = negation_normal_form(formula)
            
            # 2. Verificar Formato NNF (! pegado a variables)
            valid_format = is_nnf_compliant(nnf_res)
            
            # 3. Verificar Equivalencia Lógica (Tablas de verdad idénticas)
            valid_logic = are_equivalent(formula, nnf_res)
            
            # Imprimir resultado
            # Recortamos si es muy largo para que quepa en pantalla
            display_res = (nnf_res[:25] + '..') if len(nnf_res) > 25 else nnf_res
            desc = f"NNF('{formula}') -> '{display_res}'"
            
            if valid_format and valid_logic:
                print(f"  {YELLOW}•{NC} {desc:<50} [{GREEN} OK {NC}]")
            else:
                print(f"  {YELLOW}•{NC} {desc:<50} [{RED}FAIL{NC}]")
                if not valid_format:
                    print(f"    {RED}└── El formato no es NNF (hay '!' mal colocados).{NC}")
                if not valid_logic:
                    print(f"    {RED}└── La lógica no es equivalente (tablas distintas).{NC}")
                all_ok = False
                
        except Exception as e:
            print(f"  {YELLOW}•{NC} NNF('{formula}') {RED}[CRASH]{NC}")
            print(f"    {RED}└── {e}{NC}")
            all_ok = False

    print(f"\n{CYAN}--- Pruebas de Error Controlado ---{NC}")
    
    error_cases = [
        ("", None),   # Vacío
        ("AB", None), # Faltan operadores
        ("&", None),  # Faltan operandos
        ("A+", None)  # Carácter inválido
    ]
    
    for formula, _ in error_cases:
        try:
            res = negation_normal_form(formula)
            print(f"  {YELLOW}•{NC} '{formula}' {RED}[FAIL]{NC}")
            print(f"    {RED}└── Se esperaba error, pero funcionó: {res}{NC}")
            all_ok = False
        except (ValueError, TypeError) as e:
            print(f"  {YELLOW}•{NC} '{formula}' {CYAN}[VAL ERROR OK]{NC}")
        except Exception as e:
             print(f"  {YELLOW}•{NC} '{formula}' {RED}[CRASH]{NC}")
             print(f"    {RED}└── {e}{NC}")
             all_ok = False

    print_final(5, all_ok)

if __name__ == "__main__":
    run()