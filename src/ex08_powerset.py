import sys


def powerset(s: list[int]) -> list[list[int]]:
    """
    Calcula el conjunto potencia de un conjunto de enteros.
    Complejidad temporal y espacial: O(2^n).
    """
    if not isinstance(s, (list, set, tuple)):
        raise TypeError("El input debe ser un iterable (lista, conjunto, tupla).")

    # 1. Un conjunto real no tiene duplicados.
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


if __name__ == "__main__":
    try:
        input_set = [int(arg) for arg in sys.argv[1:]]
        res = powerset(input_set)
        print(f"✅ Resultado: powerset({input_set}) = {res}")

    except ValueError:
        print("❌ Error de Valor: Todos los argumentos deben ser números enteros.")
        print("💡 Uso: python ex08_powerset.py 0 1 2 ...")
        sys.exit(1)
        
    except TypeError as e:
        print(f"❌ Error de Tipo: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        sys.exit(1)