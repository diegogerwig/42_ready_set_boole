import sys, os

# Añadimos 'src' al path para las importaciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

try:
    from ex01_multiplier import multiplier
    from utils import print_header, print_result, print_final
except ImportError as e:
    print(f"Error de importación: {e}")
    sys.exit(1)

def run():
    # Cabecera estilizada [cite: 175]
    print_header(1, "MULTIPLIER (Aritmética Bitwise)")
    
    # Casos de prueba: a * b 
    cases = [
        (2, 2),
        (10, 5),
        (12, 12),
        (7, 8),
        (1, 0),
        (13, 1),
        (1024, 2)
    ]
    
    all_ok = True

    for a, b in cases:
        # Ejecutamos tu función
        res = multiplier(a, b)
        # El valor esperado es la multiplicación real
        expected = a * b
        
        # Mostramos el resultado usando la plantilla de utils
        if not print_result(f"{a} * {b}", res, expected):
            all_ok = False

    # Mensaje final con check verde o cruz roja
    print_final(1, all_ok)

if __name__ == "__main__":
    run()