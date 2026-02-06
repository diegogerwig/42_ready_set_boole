from ex04_truth_table import eval_formula_with_vars

def sat(formula: str) -> bool:
    """
    Determina si la fórmula es satisfacible (SAT).
    Devuelve True si existe al menos una combinación de variables que resulte en True.
    Complejidad máxima: O(2^n).
    """
    # 1. Obtener variables únicas (A-Z)
    variables = sorted(list(set([c for c in formula if c.isalpha()])))
    n = len(variables)

    # 2. Probar todas las combinaciones 2^n
    # Si n=0 (fórmula sin variables como "11&"), probamos una sola vez.
    limit = 1 << n if n > 0 else 1
    
    for i in range(limit):
        # Generar combinación de bits para las variables
        combination = [(i >> (n - 1 - j)) & 1 == 0 for j in range(n)]
        var_values = dict(zip(variables, combination))
        
        # 3. Evaluar. Si encontramos un True, cortamos (Short-circuit)
        if eval_formula_with_vars(formula, var_values):
            return True
            
    return False