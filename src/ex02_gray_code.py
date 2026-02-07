def gray_code(n: int) -> int:
    """
    Calcula el código Gray de un entero n.
    El código Gray es un sistema de numeración binaria donde dos números consecutivos difieren en solo un bit."""
    if not isinstance(n, int):
        raise TypeError("La función solo acepta números enteros.")
    if n < 0:
        raise ValueError("Esta función solo acepta números naturales (positivos).")
        
    # LÓGICA BITWISE
    return n ^ (n >> 1)