import sys


def map_to_curve(x: int, y: int) -> float:
    """
    Mapea coordenadas 2D (x, y) a un único valor entre 0.0 y 1.0 (Z-order curve).
    Versión simplificada mediante manipulación de cadenas (strings).
    """
    if not isinstance(x, int) or not isinstance(y, int):
        raise TypeError("Las coordenadas deben ser números enteros.")
    if x < 0 or y < 0:
        raise ValueError("Las coordenadas no pueden ser negativas.")
    if x > 0xFFFF or y > 0xFFFF:
        raise ValueError("Coordenadas demasiado grandes (máximo 65535).")

    # 1. Convertimos los números a texto binario asegurando que tengan 16 letras
    # El formato "016b" rellena con ceros a la izquierda hasta llegar a 16.
    # Ejemplo: x=1 se convierte en "0000000000000001"
    str_x = f"{x:016b}"
    str_y = f"{y:016b}"

    # 2. Creamos un texto vacío para nuestro número entrelazado
    str_res = ""

    # 3. Entrelazamos letra por letra (La Cremallera)
    for i in range(16):
        # En la Curva Z, los bits de Y van primero (impares) y luego los de X (pares)
        str_res += str_y[i] + str_x[i]

    # 4. Convertimos el texto binario gigante de vuelta a un número entero
    res_int = int(str_res, 2)

    # 5. Normalizamos dividiendo por el valor máximo (32 bits todos a 1)
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
        print(f"✅ Resultado: map_to_curve({x_arg}, {y_arg}) = {resultado:.15f}")

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