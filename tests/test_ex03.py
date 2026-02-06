import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ex03_eval import eval_formula

print("--- EJECUTANDO EX03: BOOLEAN EVALUATION ---")
# Casos de prueba del PDF [cite: 269-274]
cases = [
    ("10&", False),
    ("10|", True),
    ("11>", True),
    ("10=", False),
    ("1011||=", True)
]
all_ok = True

for formula, expected in cases:
    res = eval_formula(formula)
    is_correct = (res == expected)
    if not is_correct: all_ok = False
    print(f"Fórmula: {formula:10} | Resultado: {str(res):5} | {'OK' if is_correct else 'ERROR'}")

if all_ok:
    print("\n✅ Todo OK")
else:
    print("\n❌ Se encontraron errores")