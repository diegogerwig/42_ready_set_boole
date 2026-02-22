def eval_set(formula: str, sets: list[list[int]]) -> list[int]:
    """
    Evalúa una fórmula RPN aplicando operaciones de conjuntos.
    El Universo (1) se define como la unión de todos los conjuntos de entrada.
    """
    if not isinstance(formula, str):
        raise TypeError("La fórmula debe ser un string.")
    if not isinstance(sets, list):
        raise TypeError("Los sets deben ser una lista de listas.")

    # 1. Definir el Universo (U) con todos los elementos únicos
    universe = set()
    for s in sets:
        universe.update(s)

    stack = []

    for char in formula:
        if char.isalpha() and char.isupper():
            # Mapeamos A->0, B->1... usando ASCII
            idx = ord(char) - ord("A")
            if 0 <= idx < len(sets):
                stack.append(set(sets[idx]))
            else:
                stack.append(set())  # Variable sin set asignado (vacío)

        elif char == "0":
            stack.append(set())  # Conjunto vacío

        elif char == "1":
            stack.append(universe.copy())  # Universo

        elif char == "!":
            if not stack:
                raise ValueError("Falta operando para '!'")
            a = stack.pop()
            stack.append(universe - a)  # Complemento: U \ A

        elif char in "&|^>=":
            if len(stack) < 2:
                raise ValueError(f"Faltan operandos para '{char}'")
            b = stack.pop()
            a = stack.pop()

            if char == "&":
                stack.append(a & b)  # Intersección
            elif char == "|":
                stack.append(a | b)  # Unión
            elif char == "^":
                stack.append(a ^ b)  # Diferencia Simétrica
            elif char == ">":
                stack.append((universe - a) | b)  # Implicación (!A | B)
            elif char == "=":  # Equivalencia (elementos en ambos o en ninguno)
                stack.append((a & b) | ((universe - a) & (universe - b)))
        else:
            raise ValueError(f"Carácter inválido: {char}")

    if len(stack) != 1:
        raise ValueError("Fórmula inválida (sobran operandos o faltan operadores)")

    # Devolvemos lista ordenada para facilitar la comparación y legibilidad
    return sorted(list(stack[0]))
