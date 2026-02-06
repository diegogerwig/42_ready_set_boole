import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

try:
    from ex10_curve import map_coords
    from utils import print_header, print_result, print_final
except ImportError as e:
    print(f"Error importando: {e}")
    sys.exit(1)

def run():
    print_header(10, "Curve (Hilbert Map)")
    
    all_ok = True
    
    # (x, y), valor_esperado
    cases = [
        ((0, 0), 0.0),
        ((65535, 0), 1.0)
    ]
    
    for (x, y), expected in cases:
        res = map_coords(x, y)
        res_str = f"{res:.6f}"
        
        # 1. Validación Numérica (con tolerancia epsilon)
        # Usamos 1e-5 para ser flexibles con la precisión de punto flotante
        is_close = abs(res - expected) < 0.00001
        
        # 2. Preparación Visual
        # Si está cerca, hacemos que la cadena 'expected' coincida con 'res'
        # para que print_result nos de el OK verde.
        if is_close:
            expected_str = res_str
        else:
            expected_str = f"{expected:.6f}"
        
        # 3. Imprimir resultado
        desc = f"Map({x}, {y})"
        if not print_result(desc, res_str, expected_str):
            all_ok = False
    
    # Prueba de rango
    val = map_coords(12345, 54321)
    in_range = 0.0 <= val <= 1.0
    if not print_result("Rango [0, 1] (random)", in_range, True):
        all_ok = False

    print_final(10, all_ok)

if __name__ == "__main__":
    run()