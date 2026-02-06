import sys
import os

# Añadir la carpeta src al path para poder importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from ex00_adder import adder
except ImportError:
    adder = None

def wait_for_user():
    print("\n" + "="*40)
    input("Presiona ENTER para continuar con el siguiente test...")
    print("="*40 + "\n")

def test_ex00():
    print(">>> Probando Ejercicio 00: Adder")
    if adder is None:
        print("Error: No se encontró src/ex00_adder.py")
        return

    test_cases = [
        (1, 1, 2),
        (10, 5, 15),
        (255, 1, 256),
        (0, 0, 0),
        (4096, 4096, 8192)
    ]

    for a, b, expected in test_cases:
        result = adder(a, b)
        status = "✅ OK" if result == expected else f"❌ ERROR (obtenido: {result})"
        print(f"  {a} + {b} = {result} {status}")

def main():
    print("=== READY, SET, BOOLE! - SUITE DE TESTS ===\n")

    # Test Ejercicio 00
    test_ex00()
    wait_for_user()

    # Aquí irás añadiendo los demás:
    # test_ex01()
    # wait_for_user()

    print("Todos los tests disponibles han finalizado.")

if __name__ == "__main__":
    main()