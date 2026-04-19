import sys
from ex03_eval import eval_formula


def truth_table(formula: str):
    """
    Imprime la tabla de verdad de una fórmula RPN.
    Utiliza el evaluador del ex03_eval sustituyendo las variables por 0 o 1.
    """
    if not isinstance(formula, str):
        raise TypeError("Input debe ser string.")
    
    formula = formula.upper()

    caracteres_validos = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ!&|^>=")
    for char in formula:
        if char not in caracteres_validos:
            raise ValueError(f"Carácter inválido en la fórmula: '{char}'")

    variables = []
    for char in formula:
        if "A" <= char <= "Z" and char not in variables:
            variables.append(char)

    header = "| " + " | ".join(variables) + " |   |"
    separator = "|" + "|".join(["---"] * (len(variables) + 1)) + "|"

    n_vars = len(variables)
    
    total_filas = 2 ** n_vars

    for i in range(total_filas):
        
        # Convertir la fila actual (i) en binario paso a paso
        numero_actual = i
        bits_al_reves = []
        
        # Dividimos entre 2 y guardamos el resto (0 o 1)
        for _ in range(n_vars):
            resto = numero_actual % 2
            bits_al_reves.append(str(resto))
            numero_actual = numero_actual // 2
            
        # Como el método matemático saca los bits de derecha a izquierda, 
        # le damos la vuelta a la lista para que queden en el orden correcto.
        bits_ordenados = []
        for bit in reversed(bits_al_reves):
            bits_ordenados.append(bit)

        # Sustituir las letras de la fórmula por los bits
        formula_bits = formula
        
        for indice in range(n_vars):
            letra = variables[indice]
            numero = bits_ordenados[indice]
            
            # Cambiamos esa letra por su número correspondiente
            formula_bits = formula_bits.replace(letra, numero)

        resultado_booleano = eval_formula(formula_bits)

        if resultado_booleano == True:
            resultado_final = "1"
        else:
            resultado_final = "0"

        if i == 0:
            print(header)
            print(separator)

        texto_de_bits = " | ".join(bits_ordenados)
        
        print(f"| {texto_de_bits} | {resultado_final} |")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Error: Se esperaba 1 argumento.")
        print('💡 Uso: python ex04_truth_table.py "AB&"')
        sys.exit(1)

    try:
        formula = sys.argv[1]
        truth_table(formula)

    except ValueError as e:
        print(f"❌ Error de Valor: {e}")
        sys.exit(1)
        
    except TypeError as e:
        print(f"❌ Error de Tipo: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        sys.exit(1)