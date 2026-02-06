import sys
import os

# Añadir 'src' al path para poder importar los ejercicios
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

try:
    from ex00_adder import adder
    
    print(">>> Validando Ejercicio 00: Adder")
    
    # Casos de prueba basados en el comportamiento esperado [cite: 152]
    assert adder(1, 1) == 2, "Error: 1 + 1 debería ser 2"
    assert adder(10, 5) == 15, "Error: 10 + 5 debería ser 15"
    assert adder(0, 42) == 42, "Error con el cero"
    
    print("✅ Todos los casos de Adder pasaron correctamente.")

except ImportError:
    print("❌ Error: No se pudo encontrar src/ex00_adder.py")
except Exception as e:
    print(f"❌ Fallo en el test: {e}")