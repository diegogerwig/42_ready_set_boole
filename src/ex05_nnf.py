class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def to_ast(formula: str) -> Node:
    """
    Convierte una fórmula RPN en un Árbol de Sintaxis Abstracta (AST).
    """
    stack = []
    for char in formula:
        if char.isalpha() or char in "01":
            stack.append(Node(char))
        elif char == '!':
            if not stack: raise ValueError("Falta operando para '!'")
            stack.append(Node(char, left=stack.pop()))
        elif char in "&|^>=":
            if len(stack) < 2: raise ValueError(f"Faltan operandos para '{char}'")
            r, l = stack.pop(), stack.pop()
            stack.append(Node(char, l, r))
        else:
            raise ValueError(f"Carácter inválido: {char}")
            
    if len(stack) != 1:
        raise ValueError("Fórmula inválida ( sobran/faltan operadores )")
        
    return stack.pop()

def to_rpn(node: Node) -> str:
    """Convierte el AST de vuelta a string RPN (Post-order traversal)"""
    if not node: return ""
    # Si es hoja (variable/número)
    if not node.left and not node.right:
        return node.value
    # Si es operador unario (!)
    if node.left and not node.right:
        return to_rpn(node.left) + node.value
    # Operadores binarios
    return to_rpn(node.left) + to_rpn(node.right) + node.value

def transform_nnf(node: Node, negated=False) -> Node:
    """
    Aplica las leyes de De Morgan y transformaciones para bajar la negación a las hojas.
    """
    # 1. Caso Base: Hojas (Variables/Constantes)
    if node.value.isalpha() or node.value in "01":
        # Si venimos negados, añadimos '!' al nodo final
        return Node(node.value + '!') if negated else node
    
    # 2. Doble Negación: !!A -> A
    if node.value == '!':
        # Invertimos el estado de 'negated' y procesamos el hijo
        return transform_nnf(node.left, not negated)
    
    # 3. Leyes de De Morgan: !(A & B) -> !A | !B
    if node.value == '&':
        if negated:
            # Cambiamos & por | y negamos los hijos
            return Node('|', transform_nnf(node.left, True), transform_nnf(node.right, True))
        return Node('&', transform_nnf(node.left, False), transform_nnf(node.right, False))
    
    # 4. Leyes de De Morgan: !(A | B) -> !A & !B
    if node.value == '|':
        if negated:
            return Node('&', transform_nnf(node.left, True), transform_nnf(node.right, True))
        return Node('|', transform_nnf(node.left, False), transform_nnf(node.right, False))

    # 5. Implicación: A > B -> !A | B
    if node.value == '>':
        if not negated:
            return Node('|', transform_nnf(node.left, True), transform_nnf(node.right, False))
        # Negado: !(A > B) -> !(!A | B) -> A & !B
        return Node('&', transform_nnf(node.left, False), transform_nnf(node.right, True))

    # 6. Equivalencia: A = B -> (A & B) | (!A & !B)
    if node.value == '=':
        # Construimos la expansión estándar
        term1 = Node('&', transform_nnf(node.left, False), transform_nnf(node.right, False))
        term2 = Node('&', transform_nnf(node.left, True), transform_nnf(node.right, True))
        expansion = Node('|', term1, term2)
        
        if not negated: return expansion
        # Si está negado, transformamos la expansión negada (recursion)
        # !( (A&B) | (!A&!B) ) ...
        # Nota: Podríamos hardcodear la expansión negada, pero recursar es más seguro
        # Creamos un nodo dummy '!' sobre la expansión y lo transformamos
        dummy = Node('!', left=expansion)
        return transform_nnf(dummy, False) # Reiniciamos negación sobre el nuevo árbol

    # 7. XOR: A ^ B -> (!A & B) | (A & !B)
    if node.value == '^':
        term1 = Node('&', transform_nnf(node.left, True), transform_nnf(node.right, False))
        term2 = Node('&', transform_nnf(node.left, False), transform_nnf(node.right, True))
        expansion = Node('|', term1, term2)
        
        if not negated: return expansion
        dummy = Node('!', left=expansion)
        return transform_nnf(dummy, False)

    return node

def negation_normal_form(formula: str) -> str:
    """
    Transforma una fórmula a su Forma Normal Negativa (NNF).
    Solo se permiten &, | y ! (este último solo junto a variables).
    """
    if not isinstance(formula, str):
        raise TypeError("El input debe ser un string.")
        
    try:
        ast = to_ast(formula)
        nnf_ast = transform_nnf(ast)
        return to_rpn(nnf_ast)
    except ValueError as e:
        # Re-lanzamos para que los tests lo capturen limpio
        raise ValueError(str(e))