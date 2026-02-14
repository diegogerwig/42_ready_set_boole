def powerset(s: list[int]) -> list[list[int]]:
    """
    Calcula el conjunto potencia de un conjunto de enteros.
    Complejidad temporal y espacial: O(2^n).
    """
    if not isinstance(s, (list, set, tuple)):
        raise TypeError("El input debe ser una lista o conjunto.")
        
    # 1. Un conjunto real no tiene duplicados. 
    # Filtramos manteniendo el orden original (opcional pero buena práctica)
    unique_s = []
    for x in s:
        if x not in unique_s:
            unique_s.append(x)
            
    # 2. Inicializamos el conjunto potencia con el conjunto vacío
    power_set = [[]]
    
    # 3. Construcción iterativa O(2^n)
    for elem in unique_s:
        # Por cada elemento, tomamos todos los subconjuntos que ya tenemos,
        # los duplicamos, y a esa copia le añadimos el nuevo elemento.
        new_subsets = [subset + [elem] for subset in power_set]
        
        # Unimos los viejos y los nuevos
        power_set.extend(new_subsets)
        
    return power_set