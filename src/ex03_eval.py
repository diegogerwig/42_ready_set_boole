def eval_formula(formula: str) -> bool:
    """
    Evalúa una fórmula booleana en notación RPN (Reverse Polish Notation).
    """
    if not isinstance(formula, str):
        raise TypeError("El input debe ser una cadena de texto (str).")
        
    stack = []
    
    for char in formula:
        # Valores admitidos (0 ó 1)
        if char == '0':
            stack.append(False)
        elif char == '1':
            stack.append(True)
            
        # Operador Unario (!)
        elif char == '!':
            if len(stack) < 1:
                raise ValueError("Formato inválido: Falta operando para '!'.")
            stack.append(not stack.pop())
            
        # Operadores Binarios (&, |, ^, >, =)
        elif char in "&|^>=":
            if len(stack) < 2:
                raise ValueError(f"Formato inválido: Faltan operandos para '{char}'.")
            
            # OJO: En RPN, el último en entrar es el operando de la DERECHA
            right = stack.pop()
            left = stack.pop()
            
            if char == '&':
                stack.append(left and right)
            elif char == '|':
                stack.append(left or right)
            elif char == '^':
                stack.append(left != right)
            elif char == '>':
                # Material Implication: False solo si T -> F. Equivale a (!A o B)
                stack.append(not left or right)
            elif char == '=':
                stack.append(left == right)
        
        # Caracteres desconocidos
        else:
            raise ValueError(f"Carácter inválido encontrado: '{char}'")
            
    # Si la fórmula es correcta, debe quedar EXACTAMENTE un valor en la pila.
    if len(stack) != 1:
        raise ValueError("Fórmula inválida: sobran o faltan operadores.")
        
    return stack[0]