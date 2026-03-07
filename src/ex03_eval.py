import sys


def eval_formula(formula: str) -> bool:
    """
    Evalúa una fórmula booleana en notación RPN (Reverse Polish Notation).
    """
    if not isinstance(formula, str):
        raise TypeError("El input debe ser una cadena de texto (str).")

    stack = []

    for char in formula:
        # Valores admitidos (0 ó 1)
        if char == "0":
            stack.append(False)
        elif char == "1":
            stack.append(True)

        # Operador Unario (!)
        elif char == "!":
            if len(stack) < 1:
                raise ValueError("Formato inválido: Falta operando para '!'.")
            
            # El operador '!' invierte el valor lógico:
            # True  → False
            # False → True
            stack.append(not stack.pop())

        # Operadores Binarios (&, |, ^, >, =)
        elif char in "&|^>=":
            if len(stack) < 2:
                raise ValueError(f"Formato inválido: Faltan operandos para '{char}'.")

            # OJO: En RPN, el último en entrar es el operando de la DERECHA
            right = stack.pop()
            left = stack.pop()

            if char == "&":
                # AND lógico: solo es True si ambos operandos son True.
                stack.append(left and right)

            elif char == "|":
                # OR lógico: es True si al menos uno de los operandos es True.
                stack.append(left or right)

            elif char == "^":
                # XOR lógico: es True si los operandos son distintos.
                stack.append(left != right)

            elif char == ">":
                # Implicación material (A → B):
                # Solo es falsa cuando A es True y B es False.
                stack.append(not left or right)

            elif char == "=":
                # Equivalencia lógica: True si ambos operandos tienen el mismo valor.
                stack.append(left == right)

        # Caracteres desconocidos
        else:
            raise ValueError(f"Carácter inválido encontrado: '{char}'")

    # Si la fórmula es correcta, debe quedar EXACTAMENTE un valor en la pila.
    if len(stack) != 1:
        raise ValueError("Fórmula inválida: sobran o faltan operadores.")

    return stack[0]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Error: Se esperaba 1 argumento.")
        print('💡 Uso: python ex03_eval.py "10&1|"')
        sys.exit(1)

    try:
        formula = sys.argv[1]
        
        res = eval_formula(formula)
        print(f"✅ Resultado: eval_formula('{formula}') = {res}")

    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
        
    except TypeError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"💥 Error: {e}")
        sys.exit(1)
