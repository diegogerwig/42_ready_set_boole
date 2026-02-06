def eval_set(formula: str, sets: list[list[int]]) -> list[int]:
    """
    Evalúa una fórmula RPN aplicando operaciones de conjuntos.
    El Universo (1) se define como la unión de todos los conjuntos de entrada.
    """
    # 1. Definir el Universo (U) con todos los elementos únicos
    universe = set()
    for s in sets:
        universe.update(s)
    
    stack = []
    
    for char in formula:
        if char.isalpha():
            # Mapeamos A->0, B->1... usando ASCII
            idx = ord(char) - ord('A')
            if 0 <= idx < len(sets):
                stack.append(set(sets[idx]))
            else:
                stack.append(set()) # Variable sin set asignado
                
        elif char == '0':
            stack.append(set()) # Conjunto vacío
            
        elif char == '1':
            stack.append(universe.copy()) # Universo
            
        elif char == '!':
            a = stack.pop()
            stack.append(universe - a) # Complemento: U \ A
            
        else:
            # Operaciones binarias
            b = stack.pop()
            a = stack.pop()
            
            if char == '&': stack.append(a & b)       # Intersección
            elif char == '|': stack.append(a | b)     # Unión
            elif char == '^': stack.append(a ^ b)     # Diferencia Simétrica
            elif char == '>': stack.append((universe - a) | b) # Implicación (!A | B)
            elif char == '=': # Equivalencia (elementos en ambos o en ninguno)
                stack.append((a & b) | ((universe - a) & (universe - b)))

    # Devolvemos lista ordenada para facilitar la comparación
    return sorted(list(stack[0])) if stack else []