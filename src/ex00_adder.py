def adder(a: int, b: int) -> int:
    if a < 0 or b < 0:
        raise ValueError("Esta función solo acepta números naturales (positivos).")
    
    while b != 0:
        
        # PASO A: Suma Parcial (Sin acarreo)
        # La operación XOR (^) suma los bits: 1+0=1, 0+1=1, 0+0=0, 1+1=0
        suma_parcial = a ^ b
        
        # PASO B: Calcular el Acarreo (Carry)
        # La operación AND (&) detecta dónde hay dos unos (1+1).
        acarreo_crudo = a & b
        
        # PASO C: Mover el Acarreo
        # La operación LEFT SHIFT (<<) mueve el acarreo a la columna de la IZQUIERDA.
        acarreo_listo = acarreo_crudo << 1
        
        # Actualizamos las variables para la siguiente vuelta:
        # 'a' se convierte en la suma parcial acumulada.
        # 'b' se convierte en el acarreo que falta por sumar.
        a = suma_parcial
        b = acarreo_listo
        
    return a