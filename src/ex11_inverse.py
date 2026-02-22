def reverse_map(n: float) -> tuple[float, float]:
    """
    Mapea un valor n en el rango continuo [0, 1] a coordenadas (x, y) de 16-bits.
    Es la función inversa exacta de map_coords (Curva de Hilbert).
    """
    if not isinstance(n, (float, int)):
        raise TypeError("El valor debe ser numérico (float).")

    if n < 0.0 or n > 1.0:
        raise ValueError("El valor de la curva debe estar en el rango [0.0, 1.0].")

    # 1. Desnormalizamos el float [0, 1] a un entero de 32 bits.
    # Usamos 'round' en lugar de 'int()' para evitar errores de precisión
    # (por ejemplo, que 4294967295.0 se trunque a 4294967294)
    d = round(n * 4294967295)

    x = 0
    y = 0
    s = 1

    # 2. Iteramos de "abajo hacia arriba" (Fine -> Coarse)
    # Reconstruyendo las coordenadas desde el nivel 1 hasta el 32768
    while s < 65536:
        # Extraemos los 2 bits correspondientes al nivel actual
        rx = 1 & (d // 2)
        ry = 1 & (d ^ rx)

        # Invertimos la rotación y el volteo del cuadrante
        if ry == 0:
            if rx == 1:
                x = s - 1 - x
                y = s - 1 - y
            # Swap x, y
            x, y = y, x

        # Acumulamos la posición en el cuadrante actual
        x += s * rx
        y += s * ry

        # Pasamos a los siguientes 2 bits para el nivel superior
        d //= 4
        s *= 2

    return float(x), float(y)
