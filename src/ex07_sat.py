import sys
from ex03_eval import eval_formula


def sat(formula: str) -> bool:
    """
    Determina si la fórmula booleana es satisfacible (SAT).
    Devuelve True si existe al menos una combinación de variables que resulte en True.
    """
    if not isinstance(formula, str):
        raise TypeError("El input debe ser un string.")

    formula = formula.upper()

    if not formula:
        raise ValueError("La fórmula no puede estar vacía.")

    caracteres_validos = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ01!&|^>=")
    for char in formula:
        if char not in caracteres_validos:
            raise ValueError(f"Carácter inválido en la fórmula: '{char}'")

    # 1. Obtener variables únicas respetando el orden de aparición
    variables = []
    for char in formula:
        if "A" <= char <= "Z" and char not in variables:
            variables.append(char)
            
    n = len(variables)

    # Si no hay variables (ej: "11&"), probamos una sola vez.
    if n == 0:
        return eval_formula(formula)

    # Validamos la sintaxis de la fórmula antes de iterar simulando que todo es "0"
    # Si falta algún operando, el evaluador lanzará el error aquí y nos ahorramos el bucle
    dummy_formula = formula
    for v in variables:
        dummy_formula = dummy_formula.replace(v, "0")
    eval_formula(dummy_formula)

    # 2. Probar todas las combinaciones 2^n
    for i in range(1 << n):
        current_formula = formula
        
        # Generar combinación de bits para las variables y sustituir en el string
        for j in range(n - 1, -1, -1):
            bit = (i >> j) & 1
            var_name = variables[n - 1 - j]
            current_formula = current_formula.replace(var_name, str(bit))

        # 3. Evaluar y aplicar Short-circuit (cortar y devolver True si encontramos un 1)
        if eval_formula(current_formula):
            return True

    # Si probamos todas las combinaciones y ninguna dio True, es una contradicción.
    return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Error: Se esperaba 1 argumento.")
        print('💡 Uso: python ex07_sat.py "AB&"')
        sys.exit(1)

    try:
        formula = sys.argv[1]
        res = sat(formula)
        print(f"✅ Resultado: sat('{formula}') = {res}")

    except ValueError as e:
        print(f"❌ Error de Valor: {e}")
        sys.exit(1)
        
    except TypeError as e:
        print(f"❌ Error de Tipo: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        sys.exit(1)