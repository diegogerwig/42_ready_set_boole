class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def to_ast(formula):
    stack = []
    for char in formula:
        if char.isalpha() or char in "01":
            stack.append(Node(char))
        elif char == '!':
            stack.append(Node(char, left=stack.pop()))
        else:
            r, l = stack.pop(), stack.pop()
            stack.append(Node(char, l, r))
    return stack.pop()

def to_rpn(node):
    if not node: return ""
    return to_rpn(node.left) + to_rpn(node.right) + node.value

def transform_nnf(node, negated=False):
    if node.value.isalpha() or node.value in "01":
        return Node(node.value + '!') if negated else node
    
    if node.value == '!':
        return transform_nnf(node.left, not negated)
    
    if node.value == '&':
        if not negated:
            return Node('&', transform_nnf(node.left), transform_nnf(node.right))
        return Node('|', transform_nnf(node.left, True), transform_nnf(node.right, True))
    
    if node.value == '|':
        if not negated:
            return Node('|', transform_nnf(node.left), transform_nnf(node.right))
        return Node('&', transform_nnf(node.left, True), transform_nnf(node.right, True))

    if node.value == '>': # (A > B) <=> (!A | B)
        if not negated:
            return Node('|', transform_nnf(node.left, True), transform_nnf(node.right))
        return Node('&', transform_nnf(node.left), transform_nnf(node.right, True))

    if node.value == '=': # (A = B) <=> (A & B) | (!A & !B)
        # Implementación simplificada para NNF
        nnf_pos = Node('|', Node('&', transform_nnf(node.left), transform_nnf(node.right)),
                           Node('&', transform_nnf(node.left, True), transform_nnf(node.right, True)))
        if not negated: return nnf_pos
        return transform_nnf(Node('!', nnf_pos))

def negation_normal_form(formula: str) -> str:
    ast = to_ast(formula)
    nnf_ast = transform_nnf(ast)
    return to_rpn(nnf_ast)