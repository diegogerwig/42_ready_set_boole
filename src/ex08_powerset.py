def powerset(s: list[int]) -> list[list[int]]:
    """
    Calcula el conjunto potencia de s.
    Complejidad espacial: O(2^n).
    """
    # Empezamos con el conjunto vacío
    power_set = [[]]
    
    for elem in s:
        # Para cada elemento del conjunto original, duplicamos los subconjuntos
        # existentes y les añadimos el nuevo elemento.
        new_subsets = [subset + [elem] for subset in power_set]
        power_set.extend(new_subsets)
        
    return power_set