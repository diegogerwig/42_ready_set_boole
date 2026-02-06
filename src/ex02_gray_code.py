def gray_code(n: int) -> int:
    """
    Calcula el código Gray de un entero n.
    Basado en la operación n XOR (n >> 1).
    """
    return n ^ (n >> 1)