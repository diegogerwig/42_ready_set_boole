import sys


def map_to_curve(x: int, y: int) -> float:
    """
    Mapea coordenadas 2D (x, y) a un único valor entre 0.0 y 1.0 (Z-order curve).
    """
    if not isinstance(x, int) or not isinstance(y, int):
        raise TypeError("Las coordenadas deben ser números enteros.")
    if x < 0 or y < 0:
        raise ValueError("Las coordenadas no pueden ser negativas.")
    if x > 0xFFFF or y > 0xFFFF:
        raise ValueError("Coordenadas demasiado grandes (máximo 65535).")

    res_int = 0
    # 1. Entrelazamos los 16 bits de 'x' e 'y' en un entero de 32 bits
    for i in range(16):
        bit_x = (x >> i) & 1
        bit_y = (y >> i) & 1

        res_int |= bit_x << (2 * i)
        res_int |= bit_y << (2 * i + 1)

    # 2. Normalizamos el entero a un float entre 0.0 y 1.0
    # El valor máximo posible con 32 bits es 0xFFFFFFFF (4294967295)
    max_val = float(0xFFFFFFFF)
    
    return res_int / max_val


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("❌ Error: Se esperaban 2 argumentos (x e y).")
        print("💡 Uso: python ex10_curve.py 2 3")
        sys.exit(1)

    try:
        x_arg = int(sys.argv[1])
        y_arg = int(sys.argv[2])
        
        resultado = map_to_curve(x_arg, y_arg)
        print(f"✅ Resultado: map_to_curve({x_arg}, {y_arg}) = {resultado:.10f}")

    except ValueError as e:
        if "invalid literal" in str(e):
            print("❌ Error de Valor: Los argumentos deben ser números enteros.")
        else:
            print(f"❌ Error de Valor: {e}")
        sys.exit(1)
        
    except TypeError as e:
        print(f"❌ Error de Tipo: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        sys.exit(1)