import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ex02_gray_code import gray_code

print("--- EJECUTANDO EX02: GRAY CODE ---")
# Valores y resultados esperados del PDF 
expected_map = {
    0: 0, 1: 1, 2: 3, 3: 2, 4: 6, 5: 7, 6: 5, 7: 4, 8: 12
}
all_ok = True

for n, expected in expected_map.items():
    res = gray_code(n)
    is_correct = (res == expected)
    if not is_correct: all_ok = False
    
    status = "OK" if is_correct else f"ERROR (esperado {expected})"
    print(f"Entrada: {n} -> Gray Code: {res} -> {status}")

if all_ok:
    print("\n✅ Todo OK")
else:
    print("\n❌ Se encontraron errores")