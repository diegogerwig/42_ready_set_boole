import sys
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


if __name__ == "__main__":
    # 1. Verificamos que haya exactamente 2 argumentos (sys.argv[0] es el nombre del script)
    if len(sys.argv) != 3:
        print("❌ Error: Se esperaban 2 argumentos.")
        print("💡 Uso: python ex01_multiplier.py <num1> <num2>")
        sys.exit(1)

    try:
        # 2. Convertimos el texto de la terminal a enteros
        a = int(sys.argv[1])
        b = int(sys.argv[2])
        
        # 3. Llamamos a la función matemática
        res = multiplier(a, b)
        print(f"✅ Resultado: {a} * {b} = {res}")

    except ValueError as e:
        # Atrapa si el usuario escribe letras (falla el int()) o si pasa negativos (falla el multiplier())
        if "invalid literal" in str(e):
            print("❌ Error: Los argumentos por terminal deben ser números válidos.")
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)
        
    except TypeError as e:
        # Atrapa si la función se queja de los tipos
        print(f"❌ Error: {e}")
        sys.exit(1)
        
    except Exception as e:
        # Por si ocurre algo catastrófico e inesperado
        print(f"💥 Error: {e}")
        sys.exit(1)