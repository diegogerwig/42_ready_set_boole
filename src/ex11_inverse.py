import sys


def inverse_curve(n: float) -> tuple[int, int]:
    """
    Deshace el mapeo de la Z-order curve.
    Recibe un valor entre 0.0 y 1.0 y devuelve las coordenadas (x, y) originales.
    """
    if not isinstance(n, (float, int)):
        raise TypeError("El valor de entrada debe ser un número (float).")
    if not (0.0 <= n <= 1.0):
        raise ValueError("El valor de entrada debe estar entre 0.0 y 1.0.")

    # 1. Deshacemos la normalización para recuperar el entero de 32 bits original.
    # Usamos round() para evitar problemas minúsculos de precisión de punto flotante.
    max_val = float(0xFFFFFFFF)
    res_int = round(n * max_val)

    x = 0
    y = 0

    # 2. Desentrelazamos los bits.
    for i in range(16):
        # El bit de 'x' estaba en las posiciones pares (2i)
        bit_x = (res_int >> (2 * i)) & 1
        x |= (bit_x << i)

        # El bit de 'y' estaba en las posiciones impares (2i + 1)
        bit_y = (res_int >> (2 * i + 1)) & 1
        y |= (bit_y << i)

    return x, y


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Error: Se esperaba 1 argumento (un float entre 0 y 1).")
        print("💡 Uso: python ex11_inverse.py 0.45")
        sys.exit(1)

    try:
        n_arg = float(sys.argv[1])
        
        resultado = inverse_curve(n_arg)
        print(f"✅ Resultado: inverse_curve({n_arg}) = {resultado}")

    except ValueError as e:
        if "could not convert string to float" in str(e):
            print("❌ Error de Valor: El argumento debe ser un número con decimales.")
        else:
            print(f"❌ Error de Valor: {e}")
        sys.exit(1)
        
    except TypeError as e:
        print(f"❌ Error de Tipo: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        sys.exit(1)