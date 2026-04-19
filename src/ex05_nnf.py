import sys


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def to_ast(formula: str) -> Node:
    """Convierte una fórmula RPN en un Árbol de Sintaxis Abstracta (AST)."""
    stack = []
    for char in formula:
        if char.isalpha():
            stack.append(Node(char))
        elif char == "!":
            if not stack:
                raise ValueError("Falta operando para '!'")
            stack.append(Node(char, left=stack.pop()))
        elif char in "&|^>=":
            if len(stack) < 2:
                raise ValueError(f"Faltan operandos para '{char}'")
            right, left = stack.pop(), stack.pop()
            stack.append(Node(char, left, right))
        else:
            raise ValueError(f"Carácter inválido: {char}")

    if len(stack) != 1:
        raise ValueError("Fórmula inválida (sobran/faltan operadores)")

    return stack.pop()


def to_rpn(node: Node) -> str:
    """Convierte el AST de vuelta a string RPN (Post-order traversal)"""
    if not node:
        return ""
    if not node.left and not node.right:
        return node.value
    if node.left and not node.right:
        return to_rpn(node.left) + node.value
    return to_rpn(node.left) + to_rpn(node.right) + node.value


def traducir_operadores(node: Node) -> Node:
    """Paso 1: Convierte >, =, ^ en combinaciones de &, |, !"""
    if not node: 
        return None
        
    # Si es una hoja (letra), la devolvemos tal cual
    if not node.left and not node.right: 
        return node

    # Primero traducimos las ramas de abajo (Post-order)
    izq = traducir_operadores(node.left)
    der = traducir_operadores(node.right)

    # Si ya es un operador básico, lo dejamos igual
    if node.value in "!&|":
        return Node(node.value, izq, der)

    # Traducciones directas de los libros de matemáticas:
    # A > B  ==  !A | B
    if node.value == ">":
        return Node("|", Node("!", left=izq), der)

    # A = B  ==  (A & B) | (!A & !B)
    if node.value == "=":
        parte1 = Node("&", izq, der)
        parte2 = Node("&", Node("!", left=izq), Node("!", left=der))
        return Node("|", parte1, parte2)

    # A ^ B  ==  (!A & B) | (A & !B)
    if node.value == "^":
        parte1 = Node("&", Node("!", left=izq), der)
        parte2 = Node("&", izq, Node("!", left=der))
        return Node("|", parte1, parte2)


def aplicar_de_morgan(node: Node, negated=False) -> Node:
    """Paso 2: Empuja las negaciones hacia las hojas."""
    if not node: 
        return None

    # 1. Si es una hoja (letra)
    if not node.left and not node.right:
        if negated:
            return Node(node.value + "!") # Le pegamos la negación
        return node

    # 2. Doble negación (!!A -> A)
    if node.value == "!":
        return aplicar_de_morgan(node.left, not negated)

    # 3. AND
    if node.value == "&":
        if negated: # !(A & B) -> !A | !B
            return Node("|", aplicar_de_morgan(node.left, True), aplicar_de_morgan(node.right, True))
        return Node("&", aplicar_de_morgan(node.left, False), aplicar_de_morgan(node.right, False))

    # 4. OR
    if node.value == "|":
        if negated: # !(A | B) -> !A & !B
            return Node("&", aplicar_de_morgan(node.left, True), aplicar_de_morgan(node.right, True))
        return Node("|", aplicar_de_morgan(node.left, False), aplicar_de_morgan(node.right, False))


def negation_normal_form(formula: str) -> str:
    """Transforma una fórmula a su Forma Normal Negativa (NNF)."""
    if not isinstance(formula, str):
        raise TypeError("El input debe ser un string.")

    formula = formula.upper()

    try:
        arbol_original = to_ast(formula)
        
        # 1. Limpiamos el árbol de operadores complejos
        arbol_traducido = traducir_operadores(arbol_original)
        
        # 2. Aplicamos De Morgan para bajar las negaciones
        arbol_nnf = aplicar_de_morgan(arbol_traducido, False)
        
        return to_rpn(arbol_nnf)
        
    except ValueError as e:
        raise ValueError(str(e))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Error: Se esperaba 1 argumento.")
        print('💡 Uso: python ex05_nnf.py "AB&!"')
        sys.exit(1)

    try:
        formula = sys.argv[1]
        res = negation_normal_form(formula)
        print(f"✅ Resultado: NNF('{formula}') = {res}")

    except ValueError as e:
        print(f"❌ Error de Valor: {e}")
        sys.exit(1)
        
    except TypeError as e:
        print(f"❌ Error de Tipo: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        sys.exit(1)