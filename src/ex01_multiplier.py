from ex00_adder import adder

def multiplier(a: int, b: int) -> int:
    """
    Multiplica dos números usando desplazamientos y tu función adder.
    Complejidad máxima permitida: O(1) (para un entero de tamaño fijo como u32).
    """
    result = 0
    # Iteramos sobre los bits de 'b' (asumiendo 32 bits como indica el PDF)
    for i in range(32):
        # Si el bit i-ésimo de 'b' está encendido
        if (b >> i) & 1:
            # Sumamos 'a' desplazado 'i' posiciones al resultado
            result = adder(result, a << i)
    return result