import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

try:
    from ex11_inverse import reverse_map
    from ex10_curve import map_coords # Necesario para verificar el ciclo completo
    from utils import print_header, print_result, print_final
except ImportError as e:
    print(f"Error importando: {e}")
    sys.exit(1)

def run():
    print_header(11, "Inverse (Hilbert Unmap)")
    
    all_ok = True
    
    # Casos básicos teóricos
    # 0.0 -> (0, 0)
    res_start = reverse_map(0.0)
    if not print_result("Reverse(0.0)", res_start, (0, 0)): all_ok = False
    
    # Check de ida y vuelta (Round Trip)
    # Si mapeamos (42, 42) -> d -> (x, y), deberíamos recuperar (42, 42)
    original = (42, 42)
    d = map_coords(*original)
    recovered = reverse_map(d)
    
    desc = f"RoundTrip {original} -> {d:.5f} -> {recovered}"
    if not print_result(desc, recovered, original):
        all_ok = False

    # Otro caso aleatorio
    original_2 = (12345, 54321)
    d_2 = map_coords(*original_2)
    recovered_2 = reverse_map(d_2)
    
    desc_2 = f"RoundTrip {original_2}"
    if not print_result(desc_2, recovered_2, original_2):
        all_ok = False

    print_final(11, all_ok)

if __name__ == "__main__":
    run()