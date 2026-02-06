from ex05_nnf import to_ast, to_rpn, transform_nnf, Node

def distribute(node):
    """Aplica la regla de distributividad: A | (B & C) -> (A|B) & (A|C)"""
    if not node or node.value.isalpha() or node.value in "01" or node.value == "!":
        return node

    # Recursión primero hacia las hojas
    node.left = distribute(node.left)
    node.right = distribute(node.right)

    if node.value == '|':
        # Caso: A | (B & C)
        if node.right.value == '&':
            a, b, c = node.left, node.right.left, node.right.right
            return Node('&', distribute(Node('|', a, b)), distribute(Node('|', a, c)))
        
        # Caso: (A & B) | C
        if node.left.value == '&':
            a, b, c = node.left.left, node.left.right, node.right
            return Node('&', distribute(Node('|', a, c)), distribute(Node('|', b, c)))

    return node

def conjunctive_normal_form(formula: str) -> str:
    # 1. Convertir a NNF primero
    ast = to_ast(formula)
    nnf_ast = transform_nnf(ast)
    # 2. Distribuir para obtener CNF
    cnf_ast = distribute(nnf_ast)
    return to_rpn(cnf_ast)