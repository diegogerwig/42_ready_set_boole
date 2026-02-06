def map_coords(x: int, y: int) -> float:
    """
    Mapea coordenadas (x, y) de 16-bits a un valor [0, 1] usando la Curva de Hilbert.
    Espacio total: 2^16 x 2^16 = 2^32 celdas.
    """
    d = 0
    s = 1 << 15  # Empezamos con la mitad del tamaño (32768)
    
    # Iteramos desde el bit más significativo hasta el 0
    while s > 0:
        rx = 1 if (x & s) > 0 else 0
        ry = 1 if (y & s) > 0 else 0
        
        # Fórmula mágica de Hilbert para acumular distancia:
        # Añade s*s * ((3 * rx) ^ ry)
        d += s * s * ((3 * rx) ^ ry)
        
        # Rotar/Voltear cuadrante si es necesario
        if ry == 0:
            if rx == 1:
                x = s - 1 - x
                y = s - 1 - y
            
            # Swap x, y
            x, y = y, x
            
        s //= 2
        
    # Normalizamos el entero de 32 bits resultante a un float [0, 1]
    # Dividimos por el máximo valor posible (2^32 - 1)
    return d / 4294967295.0