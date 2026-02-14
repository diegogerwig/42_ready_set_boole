from ex04_truth_table import eval_formula_with_vars

def sat(formula: str) -> bool:
    """
    Determina si la fórmula booleana es satisfacible (SAT).
    Devuelve True si existe al menos una combinación de variables que resulte en True.
    """
    if not isinstance(formula, str):
        raise TypeError("El input debe ser un string.")
        
    if not formula:
        raise ValueError("La fórmula no puede estar vacía.")

    # 1. Obtener variables únicas y ordenarlas (A-Z)
    variables = sorted(list(set([c for c in formula if c.isalpha()])))
    n = len(variables)

    # Si no hay variables (ej: "11&"), probamos una sola vez con diccionario vacío.
    if n == 0:
        try:
            return eval_formula_with_vars(formula, {})
        except ValueError as e:
            raise ValueError(str(e))

    # 2. Probar todas las combinaciones 2^n
    for i in range(1 << n):
        var_values = {}
        # Generar combinación de bits para las variables
        for j in range(n):
            var_values[variables[j]] = bool((i >> j) & 1)
            
        # 3. Evaluar y aplicar Short-circuit (cortar si encontramos un True)
        try:
            if eval_formula_with_vars(formula, var_values):
                return True
        except ValueError as e:
            # Capturamos el error del evaluador si la fórmula tiene sintaxis inválida
            raise ValueError(str(e))
            
    # Si probamos todas las combinaciones y ninguna dio True, es una contradicción.
    return False