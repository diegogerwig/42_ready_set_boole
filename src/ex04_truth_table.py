def eval_formula_with_vars(formula: str, var_values: dict) -> bool:
    stack = []
    for char in formula:
        if char in "01":
            stack.append(char == '1')
        elif char.isalpha():
            stack.append(var_values[char])
        elif char == '!':
            stack.append(not stack.pop())
        else:
            right = stack.pop()
            left = stack.pop()
            if char == '&': stack.append(left and right)
            elif char == '|': stack.append(left or right)
            elif char == '^': stack.append(left != right)
            elif char == '>': stack.append(not left or right)
            elif char == '=': stack.append(left == right)
    return stack[0]

def print_truth_table(formula: str):
    # Obtener variables únicas y ordenarlas alfabéticamente 
    variables = sorted(list(set([c for c in formula if c.isalpha()])))
    n = len(variables)
    
    # Imprimir cabecera [cite: 308]
    header = " | ".join(variables) + " | = |"
    print(header)
    print("-" * len(header))
    
    # Generar 2^n combinaciones (de 1 a 0 como en el ejemplo del PDF) [cite: 311-318]
    for i in range(1 << n):
        # Creamos los valores para esta fila (usando bits para iterar combinaciones)
        # El ejemplo del PDF empieza con 1s, así que invertimos el rango o ajustamos la lógica
        combination = [(i >> (n - 1 - j)) & 1 == 0 for j in range(n)]
        var_values = dict(zip(variables, combination))
        
        # Evaluar
        res = eval_formula_with_vars(formula, var_values)
        
        # Imprimir fila
        row = " | ".join(["1" if val else "0" for val in combination])
        print(f" {row} | {1 if res else 0} |")