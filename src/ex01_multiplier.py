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

    while b != 0:

        # METEODO DE MULTIPLICACION RUSA
        # Miramos si 'b' es IMPAR (si su último bit es 1).
        # Si es impar, significa que el valor actual de 'a' forma parte de la suma total.
        if b & 1:
            result = adder(result, a)

        # Evolución de las variables para la siguiente vuelta
        # DUPLICAMOS 'a' (Shift Left << 1 es multiplicar por 2)
        a = a << 1

        # DIVIDIMOS 'b' por la mitad (Shift Right >> 1 es división entera por 2)
        b = b >> 1

    return result
