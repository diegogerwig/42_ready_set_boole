import sys
from ex05_nnf import to_ast, to_rpn, transform_nnf, Node


def distribute(node: Node) -> Node:
    """
    Aplica la regla de distributividad de forma puramente funcional:
    A | (B & C) -> (A | B) & (A | C)
    """
    if not node:
        return None

    # Las hojas (variables o constantes) se devuelven tal cual.
    if node.value.isalpha() or node.value in "01" or node.value == "!":
        return node

    # 1. Distribuir de abajo hacia arriba (Bottom-Up)
    left = distribute(node.left)
    right = distribute(node.right)

    if node.value == "|":
        # Caso 1: A | (B & C)
        if right and right.value == "&":
            a = left
            b = right.left
            c = right.right

            # (A | B) & (A | C)
            new_left = distribute(Node("|", a, b))
            new_right = distribute(Node("|", a, c))

            return Node("&", new_left, new_right)

        # Caso 2: (A & B) | C
        if left and left.value == "&":
            a = left.left
            b = left.right
            c = right

            # (A | C) & (B | C)
            new_left = distribute(Node("|", a, c))
            new_right = distribute(Node("|", b, c))

            return Node("&", new_left, new_right)

    return Node(node.value, left, right)


def conjunctive_normal_form(formula: str) -> str:
    """
    Transforma una fórmula a su Forma Normal Conjuntiva (CNF).
    """
    if not isinstance(formula, str):
        raise TypeError("El input debe ser un string.")

    formula = formula.upper()

    if not formula:
        raise ValueError("La fórmula no puede estar vacía.")

    try:
        ast = to_ast(formula)
        nnf_ast = transform_nnf(ast)

        cnf_ast = distribute(nnf_ast)

        return to_rpn(cnf_ast)
    except ValueError as e:
        raise ValueError(str(e))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Error: Se esperaba 1 argumento.")
        print('💡 Uso: python ex06_cnf.py "AB&!"')
        sys.exit(1)

    try:
        formula = sys.argv[1]
        res = conjunctive_normal_form(formula)
        print(f"✅ Resultado: CNF('{formula}') = {res}")

    except ValueError as e:
        print(f"❌ Error de Valor: {e}")
        sys.exit(1)
        
    except TypeError as e:
        print(f"❌ Error de Tipo: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        sys.exit(1)