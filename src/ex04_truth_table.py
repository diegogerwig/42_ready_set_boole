def eval_formula_with_vars(formula: str, var_values: dict) -> bool:
    """
    Evalúa una fórmula RPN sustituyendo las variables por sus valores booleanos.
    """
    if not isinstance(formula, str):
        raise TypeError("El input debe ser una cadena de texto (str).")

    if not isinstance(var_values, dict):
        raise TypeError("var_values debe ser un diccionario.")

    stack = []

    for char in formula:
        # Valores admitidos (0 ó 1)
        if char == "0":
            stack.append(False)
        elif char == "1":
            stack.append(True)

        # Variables (A-Z)
        elif char.isalpha():
            # Asumimos que var_values ya contiene la variable (se prepara antes)
            stack.append(var_values[char])

        # Operador Unario (!)
        elif char == "!":
            if len(stack) < 1:
                raise ValueError("Falta operando para '!'")
            stack.append(not stack.pop())

        # Operadores Binarios
        elif char in "&|^>=":
            if len(stack) < 2:
                raise ValueError(f"Faltan operandos para '{char}'")
            right = stack.pop()
            left = stack.pop()

            if char == "&":
                stack.append(left and right)
            elif char == "|":
                stack.append(left or right)
            elif char == "^":
                stack.append(left != right)
            elif char == ">":
                stack.append(not left or right)
            elif char == "=":
                stack.append(left == right)

        else:
            raise ValueError(f"Carácter desconocido: {char}")

    if len(stack) != 1:
        raise ValueError("Fórmula inválida: El resultado no es único.")

    return stack[0]


def print_truth_table(formula: str):
    """
    Imprime la tabla de verdad de una fórmula RPN.
    """
    if not isinstance(formula, str):
        raise TypeError("Input debe ser string.")

    # Extraer variables únicas y ordenarlas (A, B, C...)
    # Usamos set() para quitar duplicados y sorted() para orden alfabético
    variables = sorted(list(set([c for c in formula if c.isalpha()])))
    n = len(variables)

    # Validar antes de empezar
    # Hacemos una prueba rápida con todo a False para ver si la fórmula explota
    try:
        dummy_map = {v: False for v in variables}
        eval_formula_with_vars(formula, dummy_map)
    except ValueError as e:
        print(f"Error en la fórmula: {e}")
        return

    # Imprimir Cabecera
    if n > 0:
        header = "| " + " | ".join(variables) + " | = |"
    else:
        header = "| = |"  # Caso sin variables ("10&")

    print(header)
    print("|---" * (n + 1) + "|")

    # Generar 2^n combinaciones
    # Iteramos desde 0 hasta 2^n - 1 (Ej: 00, 01, 10, 11)
    for i in range(1 << n):
        current_vars = {}
        row_str = "|"

        # Mapeamos los bits del número 'i' a las variables
        for j in range(n):
            # (n - 1 - j) invierte el orden para que la primera variable sea el bit más significativo
            # Esto genera el orden estándar: 00, 01, 10, 11
            val = (i >> (n - 1 - j)) & 1
            current_vars[variables[j]] = bool(val)
            row_str += f" {val} |"

        # Evaluar la fórmula con los valores actuales de las variables
        try:
            res = eval_formula_with_vars(formula, current_vars)
            res_int = 1 if res else 0
            row_str += f" {res_int} |"
            print(row_str)
        except ValueError:
            print(f"| Error en fila {i} |")
