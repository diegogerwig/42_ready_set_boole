# 🧮 Ready, Set, Boole! 

---
---

## EX00 - Adder (Sumador a nivel de bits)

### 💡 Descripción
Este ejercicio simula cómo los procesadores suman números físicamente usando un circuito llamado **Half Adder** (Medio Sumador), utilizando exclusivamente operadores bit a bit (bitwise), sin usar el operador matemático `+`.

### 🧠 Lógica
Para sumar dos números en binario, igual que en papel, sumamos las columnas y si nos pasamos (ej. $1+1$), nos "llevamos" una (acarreo o *carry*).

1. **La Suma Parcial (XOR `^`)**: 
   La operación XOR suma los bits pero ignora lo que te llevas. 
   * `1 ^ 0` es 1
   * `0 ^ 1` es 1
   * `0 ^ 0` es 0 *(No se genera acarreo)*
   * `1 ^ 1` es 0 *(Se genera acarreo)*.
2. **Detectar el Acarreo (AND `&`)**: 
   La operación AND solo da 1 cuando ambos bits son 1. Nos dice exactamente dónde ocurrió un $1+1$.
3. **Mover el Acarreo (SHIFT `<< 1`)**: 
   Lo que nos llevamos se tiene que sumar en la siguiente columna a la izquierda. Por eso desplazamos los bits del acarreo una posición con `<< 1`.

**El algoritmo repite estos pasos hasta que no haya acarreos pendientes (`b == 0`).**

---
---

## EX01 - Multiplier (Multiplicador)

### 💡 Descripción
Implementamos la multiplicación utilizando el método de **"Duplicar y Dividir"**, históricamente conocido como la **Multiplicación Rusa** o del Campesino Ruso (*Peasant Multiplication*). 

Este algoritmo es brillante porque descompone cualquier multiplicación usando solo sumas, multiplicaciones por 2 y divisiones entre 2. A nivel de bits, esto encaja a la perfección con la arquitectura de los ordenadores.

### 🧠 Lógica
Descomponemos la multiplicación de `a * b` evaluando los bits de `b`.

1. **El Bucle**: Evaluamos mientras quede algo en `b` (`b != 0`).
2. **¿Debemos sumar? (AND `& 1`)**: Comprobamos si `b` es impar mirando su último bit (`b & 1`). Si es impar, significa que el valor actual de `a` forma parte de la suma total, así que lo sumamos al `resultado` usando nuestra función `adder`.
3. **Evolución de variables**:
   * **Duplicamos `a`**: Hacemos un Shift Left (`a << 1`). Equivale a multiplicar por 2.
   * **Dividimos `b`**: Hacemos un Shift Right (`b >> 1`). Equivale a dividir entre 2 y descartar el resto.

### 📊 Ejemplo: 12 * 5
En cada paso, `a` se duplica y `b` se divide. Solo sumamos `a` al resultado cuando `b` es impar.

| Vuelta | a (Duplica) | b (Divide) | ¿b es Impar? | Suma al Resultado | Total |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Inicio** | **12** | **5** | **SÍ** | Sumo 12 | **12** |
| 1 | 24 | 2 | No | No sumo nada | 12 |
| 2 | **48** | **1** | **SÍ** | Sumo 48 | **60** |
| 3 | 96 | 0 | - | Fin del bucle | **60** |

---
---

## EX02 - Gray Code (Código Gray)

### 💡 Descripción
El Código Gray es un sistema de numeración binaria alternativo donde dos números consecutivos **solo se diferencian en un único bit**. 

Esto es fundamental en el mundo del hardware y la robótica (como en sensores de posición o *encoders*) para evitar errores de lectura. Si usáramos binario normal, al pasar de 3 (`011`) a 4 (`100`) cambiarían 3 bits a la vez, y una lectura en el momento justo del cambio podría dar cualquier valor erróneo intermedio. En Gray, solo cambia uno, garantizando estabilidad.

### 🧠 Lógica
La fórmula mágica para convertir un binario normal a Gray es muy compacta: `n ^ (n >> 1)`.

Para explicarla fácilmente, usa la regla de los **Vecinos**:
**"Cada bit del Código Gray es el resultado de comparar el bit original con su vecino de la izquierda."**

1.  **`n`**: Tomamos el número original.
2.  **`n >> 1`**: Creamos una copia desplazada a la derecha. Esto alinea visualmente cada bit con su vecino superior.
3.  **`^` (XOR)**: Comparamos ambas versiones.
    * Si el bit y su vecino son **iguales** (0 y 0, ó 1 y 1) -> **0**.
    * Si el bit y su vecino son **diferentes** (0 y 1, ó 1 y 0) -> **1**.

### 📊 Ejemplo: Convertir 6 a Gray
Queremos convertir el 6 (binario `110`).

```text
Binario (6):       1   1   0
                   |   |   |
                   |   |   |  
Vecino (6>>1):     0   1   1   (SHIFT RIGHT)
                   ---------   
Gray (5):          1   0   1   (XOR)
```

### 📊 Valores de 0 a 8

Aplicando la fórmula a los valores obligatorios (0-8) para demostrar que coinciden con la tabla del enunciado:

* **0:** `0 ^ 0` = **0**
* **1:** `1 ^ 0` = **1**
* **2:** `2 ^ 1` *(10 ^ 01)* = `11` → **3**
* **3:** `3 ^ 1` *(11 ^ 01)* = `10` → **2**
* **4:** `4 ^ 2` *(100 ^ 010)* = `110` → **6**
* **5:** `5 ^ 2` *(101 ^ 010)* = `111` → **7**
* **6:** `6 ^ 3` *(110 ^ 011)* = `101` → **5**
* **7:** `7 ^ 3` *(111 ^ 011)* = `100` → **4**
* **8:** `8 ^ 4` *(1000 ^ 0100)* = `1100` → **12**

---
---


## EX03 - Boolean Evaluation (RPN)

### 💡 Descripción
Evaluamos fórmulas booleanas escritas en **RPN (Reverse Polish Notation)**.
En esta notación, el operador va *después* de los números (ej. `10&` en vez de `1&0`). Esto es genial para los ordenadores porque **elimina la necesidad de paréntesis**.

### 🧠 Lógica
Imagina una pila de platos vacía (`stack`).

1.  Recorremos la cadena carácter por carácter.
2.  **Si vemos un número (0 o 1):** Lo ponemos encima de la pila.
3.  **Si vemos un operador (&, |, >, =):**
    * Sacamos los **dos** platos de arriba (`pop`).
    * Hacemos la operación matemática con ellos.
    * Ponemos el resultado (el nuevo plato) en la pila.
4.  **Si vemos un negador (!):** Sacamos solo **un** plato, le cambiamos el valor, y lo devolvemos.

Al final, si la fórmula es correcta, **solo debe quedar un plato** en la pila. Ese es el resultado final.

### 📊 Ejemplo: `10&1|` (Equivale a `(1 AND 0) OR 1`)

| Carácter | Acción | Estado de la Pila `[]` |
| :--- | :--- | :--- |
| **1** | Empuja True | `[True]` |
| **0** | Empuja False | `[True, False]` |
| **&** | Saca dos (`T`, `F`) -> Calcula `T & F` = `F` -> Empuja | `[False]` |
| **1** | Empuja True | `[False, True]` |
| **\|** | Saca dos (`F`, `T`) -> Calcula `F \| T` = `T` -> Empuja | `[True]` |

**Resultado Final:** `True`.

### 🔑 Claves de los Operadores
* `&` (AND): Ambos deben ser verdaderos.
* `|` (OR): Basta que uno sea verdadero.
* `^` (XOR): Deben ser **diferentes**.
* `=` (EQUIV): Deben ser **iguales**.
* `>` (IMPLICACIÓN): La única forma de que sea falso es `True > False`. En el resto de casos es verdadero.

---
---

## EX04 - Truth Table (Tabla de Verdad)

### 💡 Descripción
Una tabla de verdad es una representación visual que muestra **todos los posibles resultados** de una fórmula booleana para todas las combinaciones posibles de sus variables de entrada. 

Si una fórmula tiene `n` variables únicas (por ejemplo, A, B y C son 3 variables), la tabla tendrá exactamente $2^n$ filas de combinaciones posibles.

### 🧠 Lógica
El reto principal es generar todas esas combinaciones de True/False dinámicamente sin saber de antemano cuántas variables habrá.

1.  **Identificar Variables**: Escaneamos la fórmula y extraemos todas las letras únicas. Las ordenamos alfabéticamente (ej: `['A', 'B']`). La cantidad de letras nos da la `n`.
2.  **El Contador Binario**: En lugar de hacer bucles anidados complicados, usamos un simple contador que va desde `0` hasta `(2^n) - 1`.
    * Si tenemos 2 variables (A y B), el contador va de 0 a 3.
    * En binario, esto es: `00`, `01`, `10`, `11`. ¡Estas son exactamente las combinaciones que necesitamos!
3.  **Extracción de Bits**: Para cada fila, leemos los bits del número actual usando un desplazamiento a la derecha (`>>`). Si el bit es `1`, la variable es `True`; si es `0`, es `False`.
4.  **Evaluación RPN**: Con las variables mapeadas (ej. `A=False, B=True`), usamos el mismo evaluador de pila (stack) que construimos en el EX03 para calcular el resultado final de esa fila y lo imprimimos.

### 📊 Ejemplo: `AB|` (A OR B)
Variables detectadas: `A`, `B` ($n = 2$). Total de filas: $2^2 = 4$.

| i (Decimal) | Bits | A | B | `AB|` (Resultado) |
| :---: | :---: | :---: | :---: | :---: |
| 0 | `00` | 0 | 0 | **0** |
| 1 | `01` | 0 | 1 | **1** |
| 2 | `10` | 1 | 0 | **1** |
| 3 | `11` | 1 | 1 | **1** |

---
---

## EX05 - Negation Normal Form (NNF)

### 💡 Descripción
La Forma Normal Negativa (NNF) es una manera de reescribir una fórmula lógica con una regla estricta: **el operador de negación (`!`) solo puede aplicarse directamente a variables**. No puede haber negaciones aplicadas a paréntesis o a grupos de operaciones.

Es como "empujar" las negaciones hacia adentro hasta que tocan fondo.

### 🧠 Lógica
Dado que modificar una cadena RPN directamente con expresiones regulares es frágil, la forma correcta y matemática de hacerlo es usando un **Árbol de Sintaxis Abstracta (AST)**.

1.  **Parsear a Árbol (AST):** Convertimos la cadena RPN en una estructura de nodos jerárquicos. 
    * Por ejemplo, `AB&!` se convierte en un nodo `!` en la raíz, que tiene como hijo un nodo `&`, el cual tiene como hojas a `A` y `B`.
2.  **Transformar (Recursión):** Recorremos el árbol desde la raíz hacia las hojas, aplicando las reglas lógicas para bajar el `!`.
    * **Doble Negación:** `!!A` se convierte simplemente en `A`.
    * **Leyes de De Morgan:** * `!(A & B)` se transforma en `!A | !B`. (La AND se vuelve OR y la negación se divide).
        * `!(A | B)` se transforma en `!A & !B`. (La OR se vuelve AND).
    * **Implicación y Equivalencia:** Transformamos operaciones complejas a básicas. Por ejemplo, `A > B` se reescribe como `!A | B`.
3.  **Serializar a RPN:** Una vez que el árbol está en formato NNF, lo recorremos en "post-orden" (izquierda, derecha, raíz) para reconstruir la cadena RPN final.

### 📊 Ejemplo: `AB&!` (equivale a `!(A & B)`)

| Estado | Fórmula Visual | Explicación |
| :--- | :--- | :--- |
| **Original** | `!(A & B)` | La negación afecta a toda la operación AND. |
| **De Morgan**| `!A | !B` | Invertimos `&` por `|` y bajamos la negación a las variables. |
| **Final RPN**| `A!B!|` | Ya cumple con NNF (los `!` están junto a las letras). |

---
---

## EX06 - Conjunctive Normal Form (CNF)

### 💡 Descripción
La Forma Normal Conjuntiva (CNF) es un formato estandarizado donde una fórmula se representa como un gran **AND de ORs**. 
Es decir, son cláusulas (agrupaciones unidas por `|`) que se unen todas juntas mediante `&`. 

Esta forma es extremadamente importante en ciencias de la computación porque muchos algoritmos de Inteligencia Artificial (como los solucionadores SAT que veremos en el EX07) exigen que el input esté exclusivamente en este formato.

### 🧠 Lógica
Para llegar a CNF, seguimos 2 grandes pasos:
1. **Pasar a NNF:** Reutilizamos nuestro algoritmo del EX05 para empujar todas las negaciones (`!`) hasta las variables y eliminar operaciones complejas (`>`, `=`, `^`).
2. **Aplicar Distributividad:** Si tenemos un operador OR compitiendo con un AND, el AND debe "subir" en el árbol. 
   Usamos la regla matemática: `A | (B & C)  =>  (A | B) & (A | C)`.

Para implementarlo sin romper las referencias de memoria de Python (y sin hacer trucos "sucios" como clonados profundos de objetos), utilizamos un enfoque **puramente funcional**:
* Parseamos la fórmula NNF en un árbol (AST).
* En lugar de modificar los nodos existentes para hacer el cruce distributivo, **creamos nodos completamente nuevos** en cada paso de la recursión (`Node('|', a, b)`).
* De esta forma, las hojas (`A`, `B`, `C`) pueden compartirse entre múltiples ramas sin peligro. En memoria, el resultado es un Grafo Acíclico Dirigido (DAG), ¡pero a la hora de serializarlo a RPN se lee perfectamente como un árbol expandido!

### 📊 Ejemplo: `AB&C|` (Equivale a `(A & B) | C`)

1. Al construir el árbol original NNF, la raíz es un `|`, su hijo izquierdo es un `&` (con A y B), y su hijo derecho es `C`.
2. Como detectamos el patrón prohibido `(A & B) | C` (un AND dentro de un OR), aplicamos la regla de distributividad.
3. Creamos una nueva raíz `&`. Su hijo izquierdo será el nuevo nodo `A | C` y su hijo derecho será el nuevo nodo `B | C`.
4. Al serializarlo de nuevo a RPN, esto se lee como `AC|BC|&`. ¡El `&` ha subido al final, operando sobre las cláusulas!

---
---

## EX07 - SAT (Satisfiability)

### 💡 Descripción
El problema de satisfacibilidad booleana (SAT) es la madre de todos los problemas en Ciencias de la Computación (es el primer problema demostrado como **NP-Completo**). 

La pregunta que responde es simple: **¿Existe al menos una combinación de entradas (`True`/`False`) que haga que esta fórmula devuelva `True`?**
* Si existe, la fórmula es **Satisfacible** (`True`).
* Si sin importar lo que hagamos siempre da `False` (una contradicción lógica), es **Insatisfacible** (`False`).

### 🧠 Lógica
Existen algoritmos súper complejos para resolver esto eficientemente (los famosos "SAT Solvers"), pero para este nivel, la forma más robusta es el ataque de **Fuerza Bruta**, evaluando la Tabla de Verdad completa que creamos en el EX04.

1. Identificamos cuántas variables únicas hay ($n$) para saber que existen $2^n$ combinaciones posibles.
2. Usamos el truco de manipulación de bits (shift `>>`) iterando desde $0$ hasta $(2^n)-1$ para generar todas las combinaciones imaginables.
3. Le pasamos cada combinación a la función `eval_formula` (reutilizada del EX04).
4. **Short-circuit (Cortocircuito):** ¡No necesitamos generar la tabla completa! En el mismo milisegundo en el que la función nos devuelva un `True`, sabemos que la respuesta es afirmativa, por lo que **cortamos el bucle y devolvemos `True` inmediatamente**.
5. Si agotamos los $2^n$ intentos sin ver ni un solo `True`, entonces confirmamos que es matemáticamente imposible y devolvemos `False`.

### 📊 Ejemplos

| Fórmula (RPN) | Fórmula Matemática | SAT | Razón |
| :--- | :--- | :---: | :--- |
| `AB|` | $A \lor B$ | **True** | Basta con poner A=1 para que sea verdad. |
| `AA!&` | $A \land \neg A$ | **False** | Es una contradicción pura. $A$ no puede ser 1 y 0 a la vez. |
| `AA!|`| $A \lor \neg A$ | **True** | Es una tautología. Siempre es verdad pase lo que pase. |

---
---

