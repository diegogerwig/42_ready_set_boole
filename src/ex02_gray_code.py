def gray_code(n: int) -> int:
    """
    Calcula el código Gray de un entero n.
    El código Gray es un sistema de numeración binaria donde dos números consecutivos difieren en solo un bit.
    """
    if not isinstance(n, int):
        raise TypeError("La función solo acepta números enteros.")
    
    if n < 0:
        raise ValueError("Esta función solo acepta números naturales (positivos).")
        
    original = n
    
    # Movemos los bits una posición a la derecha SHIFT RIGHT (>> 1) para obtener el vecino a la izquierda.
    vecino_izquierda = n >> 1
    
    # COMPARACIÓN (XOR)
    # XOR detecta cambios: pone un 1 si los bits son DIFERENTES.
    # 1 vs 0 -> 1
    # 0 vs 1 -> 1
    # 1 vs 1 -> 0
    # 0 vs 0 -> 0
    # Resultado:         1 0 1  (5 en Gray)
    codigo_gray = original ^ vecino_izquierda
    
    return codigo_gray