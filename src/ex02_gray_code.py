import sys


def gray_code(n: int) -> int:
    """
    Calcula el código Gray de un entero n.
    El código Gray es un sistema de numeración binaria donde dos números consecutivos difieren en solo un bit.
    """
    if not isinstance(n, int):
        raise TypeError("La función solo acepta números enteros.")

    if n < 0:
        raise ValueError("Esta función solo acepta números naturales (positivos).")

    original = n

    # Movemos los bits una posición a la derecha SHIFT RIGHT (>> 1) para obtener el vecino a la izquierda.
    vecino_izquierda = n >> 1

    # Comparación (XOR)
    # XOR detecta cambios: pone un 1 si los bits son DIFERENTES.
    # 1 vs 0 -> 1
    # 0 vs 1 -> 1
    # 1 vs 1 -> 0
    # 0 vs 0 -> 0
    codigo_gray = original ^ vecino_izquierda

    return codigo_gray


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Error: Se esperaba 1 argumento.")
        print("💡 Uso: python ex02_gray_code.py <num>")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        
        res = gray_code(n)
        print(f"✅ Resultado: gray_code({n}) = {res}")

    except ValueError as e:
        if "invalid literal" in str(e):
            print("❌ Error: El argumento por terminal debe ser un número válido.")
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)
        
    except TypeError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"💥 Error: {e}")
        sys.exit(1)