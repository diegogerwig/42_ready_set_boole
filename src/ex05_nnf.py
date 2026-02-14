class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def to_ast(formula: str) -> Node:
    """Convierte una fórmula RPN en un Árbol de Sintaxis Abstracta (AST)."""
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
    if not node.left and not node.right:
        return node.value
    if node.left and not node.right:
        return to_rpn(node.left) + node.value
    return to_rpn(node.left) + to_rpn(node.right) + node.value

def transform_nnf(node: Node, negated=False) -> Node:
    """Aplica las leyes de De Morgan para bajar la negación a las hojas."""
    
    # 1. Caso Base A: Hojas normales (Variables/Constantes como 'A')
    if len(node.value) == 1 and (node.value.isalpha() or node.value in "01"):
        return Node(node.value + '!') if negated else node
        
    # 1. Caso Base B: Hojas temporales ya negadas (ej: 'A!')
    # (Ocurre durante la expansión de = y ^)
    if len(node.value) == 2 and node.value[1] == '!':
        # Si venimos negados, se cancela la negación !!A -> A
        return Node(node.value[0]) if negated else node
    
    # 2. Doble Negación explícita en el árbol: !!A -> A
    if node.value == '!':
        return transform_nnf(node.left, not negated)
    
    # 3. AND
    if node.value == '&':
        if negated:
            return Node('|', transform_nnf(node.left, True), transform_nnf(node.right, True))
        return Node('&', transform_nnf(node.left, False), transform_nnf(node.right, False))
    
    # 4. OR
    if node.value == '|':
        if negated:
            return Node('&', transform_nnf(node.left, True), transform_nnf(node.right, True))
        return Node('|', transform_nnf(node.left, False), transform_nnf(node.right, False))

    # 5. Implicación: A > B -> !A | B
    if node.value == '>':
        if not negated:
            return Node('|', transform_nnf(node.left, True), transform_nnf(node.right, False))
        return Node('&', transform_nnf(node.left, False), transform_nnf(node.right, True))

    # 6. Equivalencia: A = B -> (A & B) | (!A & !B)
    if node.value == '=':
        term1 = Node('&', transform_nnf(node.left, False), transform_nnf(node.right, False))
        term2 = Node('&', transform_nnf(node.left, True), transform_nnf(node.right, True))
        expansion = Node('|', term1, term2)
        if not negated: return expansion
        
        # Si está negado, forzamos la transformación de la expansión
        dummy = Node('!', left=expansion)
        return transform_nnf(dummy, False)

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
    """Transforma una fórmula a su Forma Normal Negativa (NNF)."""
    if not isinstance(formula, str):
        raise TypeError("El input debe ser un string.")
        
    try:
        ast = to_ast(formula)
        nnf_ast = transform_nnf(ast)
        return to_rpn(nnf_ast)
    except ValueError as e:
        raise ValueError(str(e))