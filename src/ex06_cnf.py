import sys

# Importamos las herramientas de nuestra cadena de montaje del EX05
from ex05_nnf import Node, to_ast, to_rpn, traducir_operadores, aplicar_de_morgan


def aplicar_distributiva(nodo: Node) -> Node:
    """
    Paso 3 (CNF): Aplica la propiedad distributiva para forzar los OR (|) hacia abajo
    y subir los AND (&) hacia la raíz.
    """
    if not nodo:
        return None

    # Primero, procesamos los hijos (Post-orden)
    nodo.left = aplicar_distributiva(nodo.left)
    nodo.right = aplicar_distributiva(nodo.right)

    # Si el nodo actual es un OR (|), revisamos si alguno de sus hijos es un AND (&)
    if nodo.value == "|":
        
        # Caso 1: El hijo izquierdo es un AND -> (A & B) | C  ==>  (A | C) & (B | C)
        if nodo.left and nodo.left.value == "&":
            A = nodo.left.left
            B = nodo.left.right
            C = nodo.right
            
            # Volvemos a aplicar distributiva por si se generan nuevos conflictos
            nueva_rama_izq = aplicar_distributiva(Node("|", A, C))
            nueva_rama_der = aplicar_distributiva(Node("|", B, C))
            return Node("&", nueva_rama_izq, nueva_rama_der)

        # Caso 2: El hijo derecho es un AND -> A | (B & C)  ==>  (A | B) & (A | C)
        elif nodo.right and nodo.right.value == "&":
            A = nodo.left
            B = nodo.right.left
            C = nodo.right.right
            
            nueva_rama_izq = aplicar_distributiva(Node("|", A, B))
            nueva_rama_der = aplicar_distributiva(Node("|", A, C))
            return Node("&", nueva_rama_izq, nueva_rama_der)

    return nodo


def conjunctive_normal_form(formula: str) -> str:
    """Transforma una fórmula a su Forma Normal Conjuntiva (CNF)."""
    if not isinstance(formula, str):
        raise TypeError("El input debe ser un string.")

    formula = formula.upper()

    try:
        # FASE 1: Texto a Árbol
        arbol_original = to_ast(formula)
        
        # FASE 2: NNF (Usando nuestras herramientas limpias del ex05)
        arbol_traducido = traducir_operadores(arbol_original)
        arbol_nnf = aplicar_de_morgan(arbol_traducido, False)
        
        # FASE 3: Aplicar ley distributiva para forzar el CNF
        arbol_cnf = aplicar_distributiva(arbol_nnf)
        
        # FASE 4: Árbol a Texto
        return to_rpn(arbol_cnf)
        
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