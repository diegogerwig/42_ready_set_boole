import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ex01_multiplier import multiplier

print("--- EJECUTANDO EX01: MULTIPLIER ---")
cases = [(2, 2), (10, 5), (12, 12), (7, 8), (0, 42)]
all_ok = True

for a, b in cases:
    expected = a * b
    res = multiplier(a, b)
    is_correct = (res == expected)
    if not is_correct: all_ok = False
    
    status = "OK" if is_correct else f"ERROR (esperado {expected})"
    print(f"Operación: {a} * {b} = {res} -> {status}")

if all_ok:
    print("\n✅ Todo OK")
else:
    print("\n❌ Se encontraron errores")