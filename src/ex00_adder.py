def adder(a: int, b: int) -> int:
    """
    Suma dos números naturales usando solo operaciones bit a bit.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("La función solo acepta números enteros.")

    if a < 0 or b < 0:
        raise ValueError("Esta función solo acepta números naturales (positivos).")

    while b != 0:

        # Suma Parcial (Sin acarreo): La operación XOR (^) suma los bits:
        #   1 vs 0 -> 1
        #   0 vs 1 -> 1
        #   1 vs 1 -> 0
        #   0 vs 0 -> 0
        suma_parcial = a ^ b

        # Calcular el Acarreo (Carry): La operación AND (&) detecta dónde hay dos unos (1+1).
        # La operación AND (&) detecta dónde hay dos unos (1+1).
        acarreo = a & b

        # Mover el Acarreo: La operación LEFT SHIFT (<<) mueve el acarreo a la columna de la IZQUIERDA.
        acarreo_desp = acarreo << 1

        # Actualizamos las variables para la siguiente vuelta:
        # 'a' se convierte en la suma parcial acumulada.
        # 'b' se convierte en el acarreo que falta por sumar.
        a = suma_parcial
        b = acarreo_desp

    return a
