from ex00_adder import adder

def multiplier(a: int, b: int) -> int:
    """
    Multiplica dos números naturales usando desplazamientos y la función adder.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("La función solo acepta números enteros.")
    if a < 0 or b < 0:
        raise ValueError("Esta función solo acepta números naturales (positivos).")
        
    result = 0
    
    # ALGORITMO DE MULTIPLICACIÓN RUSA (PEASANT) / BITWISE: Iteramos bit a bit (máximo 32 bits para simular u32)
    for i in range(32):
        # Si el bit 'i' de 'b' es 1, sumamos 'a' desplazado 'i' veces (equivale a sumar a * 2^i)
        if (b >> i) & 1:
            result = adder(result, a << i)
            
    return result