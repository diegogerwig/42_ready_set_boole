def reverse_map(n: float) -> tuple[int, int]:
    """
    Mapea un valor n en [0, 1] a coordenadas (x, y) de 16-bits.
    Inverso de la Curva de Hilbert.
    """
    # Convertimos el float [0, 1] a un entero de 32 bits
    dist = int(n * 4294967295.0)
    x = 0
    y = 0
    s = 1
    
    # Iteramos desde el nivel 1 hasta 32768 (potencias de 2)
    # Construyendo la coordenada de 'abajo hacia arriba' (Fine -> Coarse)
    while s < 65536:
        rx = 1 & (dist // 2)
        ry = 1 & (dist ^ rx)
        
        # Rotación del cuadrante si es necesario
        if ry == 0:
            if rx == 1:
                x = s - 1 - x
                y = s - 1 - y
            
            # Swap x, y
            x, y = y, x
            
        # Posicionamos las coordenadas relativas en el cuadrante actual
        x += s * rx
        y += s * ry
        
        # Pasamos al siguiente nivel de detalle (siguientes 2 bits)
        dist //= 4
        s *= 2
        
    return x, y