import sys


def inverse_curve(n: float) -> tuple[int, int]:
    """
    Deshace el mapeo de la Z-order curve.
    Recibe un valor entre 0.0 y 1.0 y devuelve las coordenadas (x, y) originales.
    Versión simplificada mediante manipulación de cadenas (strings).
    """
    if not isinstance(n, (float, int)):
        raise TypeError("El valor de entrada debe ser un número (float).")
    if not (0.0 <= n <= 1.0):
        raise ValueError("El valor de entrada debe estar entre 0.0 y 1.0.")

    # 1. Deshacemos la normalización para recuperar el entero gigante de 32 bits.
    max_val = float(0xFFFFFFFF)
    res_int = round(n * max_val)

    # 2. Convertimos el número a texto binario, forzando que tenga exactamente 32 letras
    # El formato "032b" rellena con ceros a la izquierda si hiciera falta.
    str_res = f"{res_int:032b}"

    # 3. Desentrelazamos las letras (Abrimos la cremallera) usando Slicing [inicio:fin:salto]
    # Empezamos en la letra 0 y damos saltos de 2 en 2 para sacar la Y
    str_y = str_res[0::2]
    
    # Empezamos en la letra 1 y damos saltos de 2 en 2 para sacar la X
    str_x = str_res[1::2]

    # 4. Convertimos los textos binarios de 16 letras de vuelta a números normales
    x = int(str_x, 2)
    y = int(str_y, 2)

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