import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ex04_truth_table import print_truth_table

print("--- EJECUTANDO EX04: TRUTH TABLE ---")
formula = "AB&C|"
print(f"Fórmula: {formula} (Equivalente a (A ∧ B) ∨ C)\n")

print_truth_table(formula)

# Verificación manual del estado final
print("\n✅ Tabla generada. Compara con los valores del PDF (pág. 21).")