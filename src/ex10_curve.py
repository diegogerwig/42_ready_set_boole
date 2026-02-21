def map_coords(x: int, y: int) -> float:
    """
    Mapea coordenadas (x, y) de 16-bits a un valor continuo en el rango [0, 1] 
    usando la Curva de Hilbert. El espacio total es de 2^16 x 2^16 = 2^32 celdas.
    """
    if not isinstance(x, int) or not isinstance(y, int):
        raise TypeError("Las coordenadas x e y deben ser enteros.")
        
    if x < 0 or x > 65535 or y < 0 or y > 65535:
        raise ValueError("Las coordenadas deben estar en el rango [0, 65535] (16-bits).")

    d = 0
    s = 1 << 15  # Empezamos con la mitad del tamaño máximo (32768)
    
    # Iteramos desde el bit más significativo hasta el bit 0
    while s > 0:
        # Verificamos en qué cuadrante de tamaño 's' caen las coordenadas actuales
        rx = 1 if (x & s) > 0 else 0
        ry = 1 if (y & s) > 0 else 0
        
        # Fórmula matemática de la curva de Hilbert para acumular distancia
        d += s * s * ((3 * rx) ^ ry)
        
        # Rotar y voltear el cuadrante si caemos en la región inferior
        if ry == 0:
            if rx == 1:
                x = s - 1 - x
                y = s - 1 - y
            # Intercambiar x, y
            x, y = y, x
            
        s //= 2
        
    # Normalizamos el entero de 32 bits resultante a un float en [0.0, 1.0]
    # Dividimos por el máximo valor posible (2^32 - 1)
    return d / 4294967295