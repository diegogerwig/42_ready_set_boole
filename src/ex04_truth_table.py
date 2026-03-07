import sys
from ex03_eval import eval_formula


def truth_table(formula: str):
    """
    Imprime la tabla de verdad de una fórmula RPN.
    Utiliza el evaluador del ex03_eval sustituyendo las variables por 0 o 1.
    """
    if not isinstance(formula, str):
        raise TypeError("Input debe ser string.")
    
    formula = formula.upper()

    caracteres_validos = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ01!&|^>=")
    for char in formula:
        if char not in caracteres_validos:
            raise ValueError(f"Carácter inválido en la fórmula: '{char}'")

    variables = []
    for char in formula:
        if "A" <= char <= "Z" and char not in variables:
            variables.append(char)

    dummy_formula = formula
    for v in variables:
        dummy_formula = dummy_formula.replace(v, "0")
    eval_formula(dummy_formula)

    if not variables:
        res = eval_formula(formula)
        print("|   |")
        print("|---|")
        print(f"| {int(res)} |")
        return

    header = "| " + " | ".join(variables) + " |   |"
    
    separator = "|" + "|".join(["---"] * (len(variables) + 1)) + "|"
    print(header)
    print(separator)

    n_vars = len(variables)
    total_filas = 1 << n_vars 

    for i in range(total_filas):
        bits = []
        current_formula = formula
        for j in range(n_vars - 1, -1, -1):
            bit = (i >> j) & 1
            bits.append(bit)
            var_name = variables[n_vars - 1 - j]
            current_formula = current_formula.replace(var_name, str(bit))

        resultado = eval_formula(current_formula)

        str_bits = " | ".join(str(b) for b in bits)
        print(f"| {str_bits} | {int(resultado)} |")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Error: Se esperaba 1 argumento.")
        print('💡 Uso: python ex04_truth_table.py "AB&"')
        sys.exit(1)

    try:
        formula = sys.argv[1]
        truth_table(formula)

    except ValueError as e:
        print(f"❌ Error de Valor: {e}")
        sys.exit(1)
        
    except TypeError as e:
        print(f"❌ Error de Tipo: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        sys.exit(1)