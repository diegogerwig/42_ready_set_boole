import sys
from ex03_eval import eval_formula


def truth_table(formula: str):
    """
    Imprime la tabla de verdad de una fórmula RPN respetando el espaciado y tabulación.
    Utiliza el evaluador del ex03_eval sustituyendo las variables por 0 o 1.
    """
    if not isinstance(formula, str):
        raise TypeError("Input debe ser string.")

    # Validamos que todos los caracteres sean válidos antes de hacer nada
    caracteres_validos = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ01!&|^>=")
    for char in formula:
        if char not in caracteres_validos:
            raise ValueError(f"Carácter inválido en la fórmula: '{char}'")

    # Buscamos variables únicas (letras mayúsculas) manteniendo el orden de aparición
    variables = []
    for char in formula:
        if "A" <= char <= "Z" and char not in variables:
            variables.append(char)

    # Validar la fórmula antes de imprimir la tabla para evitar tablas a medias
    dummy_formula = formula
    for v in variables:
        dummy_formula = dummy_formula.replace(v, "0")
    eval_formula(dummy_formula)

    # Si no hay variables, evaluamos la fórmula y la imprimimos directamente
    if not variables:
        res = eval_formula(formula)
        print("|   |")
        print("|---|")
        print(f"| {int(res)} |")
        return

    # Imprimir Cabecera con espacios correctos: | A | B |   |
    header = "| " + " | ".join(variables) + " |   |"
    
    # Imprimir Separador: |---|---|---|
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
            # Reemplazamos temporalmente la variable por su valor ('0' o '1') para evaluarla
            current_formula = current_formula.replace(var_name, str(bit))

        # Le pasamos la fórmula ya sustituida (ej: "10&") a nuestra función del ex03
        resultado = eval_formula(current_formula)

        # Imprimir la fila formateada con espacios: | 0 | 0 | 0 |
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