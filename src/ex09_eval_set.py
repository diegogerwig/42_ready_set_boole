import sys
import ast


def eval_set(formula: str, sets: list[list[int]]) -> list[int]:
    """
    Evalúa una fórmula RPN aplicando operaciones de conjuntos.
    El Universo (1) se define como la unión de todos los conjuntos de entrada.
    """
    if not isinstance(formula, str):
        raise TypeError("La fórmula debe ser un string.")
    if not isinstance(sets, list):
        raise TypeError("Los sets deben ser una lista de listas.")

    # Convertimos a mayúsculas para aceptar inputs amigables
    formula = formula.upper()

    if not formula:
        raise ValueError("La fórmula no puede estar vacía.")

    caracteres_validos = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ01!&|^>=")
    for char in formula:
        if char not in caracteres_validos:
            raise ValueError(f"Carácter inválido en la fórmula: '{char}'")

    # 1. Definir el Universo (U) con todos los elementos únicos
    universe = set()
    for s in sets:
        universe.update(s)

    stack = []

    for char in formula:
        if char.isalpha():
            # Mapeamos A->0, B->1... usando ASCII
            idx = ord(char) - ord("A")
            if 0 <= idx < len(sets):
                stack.append(set(sets[idx]))
            else:
                stack.append(set())  # Variable sin set asignado (vacío)

        elif char == "0":
            stack.append(set())  # Conjunto vacío

        elif char == "1":
            stack.append(universe.copy())  # Universo

        elif char == "!":
            if not stack:
                raise ValueError("Falta operando para '!'")
            a = stack.pop()
            stack.append(universe - a)  # Complemento: U \ A

        elif char in "&|^>=":
            if len(stack) < 2:
                raise ValueError(f"Faltan operandos para '{char}'")
            b = stack.pop()
            a = stack.pop()

            if char == "&":
                stack.append(a & b)  # Intersección
            elif char == "|":
                stack.append(a | b)  # Unión
            elif char == "^":
                stack.append(a ^ b)  # Diferencia Simétrica
            elif char == ">":
                stack.append((universe - a) | b)  # Implicación (!A | B)
            elif char == "=":  # Equivalencia
                stack.append((a & b) | ((universe - a) & (universe - b)))

    if len(stack) != 1:
        raise ValueError("Fórmula inválida (sobran operandos o faltan operadores)")

    # Devolvemos lista ordenada para facilitar la comparación y legibilidad
    return sorted(list(stack[0]))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Error: Se esperaba al menos 1 argumento.")
        print('💡 Uso: python ex09_eval_set.py "AB&" "[0, 1, 2]" "[2, 3, 4]"')
        sys.exit(1)

    try:
        formula = sys.argv[1]
        sets_args = sys.argv[2:]
        parsed_sets = [ast.literal_eval(s) for s in sets_args]
        
        res = eval_set(formula, parsed_sets)
        print(f"✅ Resultado: eval_set('{formula}', {parsed_sets}) = {res}")

    except ValueError as e:
        print(f"❌ Error de Valor: {e}")
        sys.exit(1)
        
    except TypeError as e:
        print(f"❌ Error de Tipo: {e}")
        sys.exit(1)
        
    except SyntaxError:
        print("❌ Error de Sintaxis: Asegúrate de pasar los sets como listas válidas de Python entre comillas.")
        sys.exit(1)
        
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        sys.exit(1)