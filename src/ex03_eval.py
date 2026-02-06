def eval_formula(formula: str) -> bool:
    """
    Evalúa una fórmula booleana en notación RPN.
    Complejidad máxima: O(n)[cite: 239].
    """
    stack = []
    
    for char in formula:
        if char == '0':
            stack.append(False)
        elif char == '1':
            stack.append(True)
        elif char == '!':
            stack.append(not stack.pop())
        else:
            # Operadores binarios
            right = stack.pop()
            left = stack.pop()
            if char == '&': stack.append(left and right)       # AND
            elif char == '|': stack.append(left or right)        # OR
            elif char == '^': stack.append(left != right)        # XOR
            elif char == '>': stack.append(not left or right)   # IMPLY [cite: 331]
            elif char == '=': stack.append(left == right)       # EQUIV [cite: 333]
            
    return stack[0]