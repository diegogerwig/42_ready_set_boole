# 🧮 Ready, Set, Boole! 

---

## 🛠️ Guía de Uso del Entorno

Este proyecto utiliza un entorno automatizado para gestionar dependencias y garantizar que las pruebas se ejecuten de forma idéntica en cualquier sistema (WSL, Linux 42, etc.).

### 1. El Script Maestro: `setup.sh`
El archivo `setup.sh` detecta automáticamente tu sistema operativo y la versión de Python más reciente disponible para configurar el entorno virtual.

| Comando | Descripción |
| :--- | :--- |
| **`bash setup.sh test`** | **(Opción por defecto)** Crea/limpia el entorno, instala dependencias y ejecuta **todos** los tests de la carpeta `tests/` en orden. |
| **`bash setup.sh venv`** | Configura el entorno y abre una terminal interactiva con el `venv` activado y el `PYTHONPATH` configurado para reconocer la carpeta `src/`. |

### 2. Ejecución Individual de Tests
Si deseas ejecutar las pruebas de un solo ejercicio de forma aislada, primero activa tu entorno virtual (puedes usar `setup.sh venv`) y ejecuta el archivo de prueba directamente:

```bash
python3 tests/test_ex00.py
```

### 3. Ejecución Manual del Código
Si quieres probar el código de un ejercicio sin ejecutar los tests, ejecuta el script correspondiente en la carpeta `src/` con los argumentos necesarios. Por ejemplo:

```bash
python3 src/ex00.py <args>

python3 src/ex00_adder.py 13 37
python3 src/ex01_multiplier.py 10 5
python3 src/ex02_gray_code.py 5
python3 src/ex03_eval.py "10&1|"
```

---

## ⚡ Guía Rápida de Operadores a Nivel de Bits

Tabla de referencia rápida con las operaciones bit a bit (*bitwise*) fundamentales:

| Operador | Símbolo | Combinaciones Básicas (Bits) | Efecto Matemático / Lógico |
| :--- | :---: | :--- | :--- |
| **AND** | `&` | `0 & 0 = 0`<br>`0 & 1 = 0`<br>`1 & 0 = 0`<br>`1 & 1 = 1` | Detectar acarreos / Intersección. |
| **OR** | `\|` | `0 \| 0 = 0`<br>`0 \| 1 = 1`<br>`1 \| 0 = 1`<br>`1 \| 1 = 1` | Juntar bits / Unión booleana. |
| **XOR** | `^` | `0 ^ 0 = 0`<br>`0 ^ 1 = 1`<br>`1 ^ 0 = 1`<br>`1 ^ 1 = 0` | Suma sin acarreo / Diferencia simétrica. |
| **L-SHIFT**| `<< n` | `001 << 1 = 010`<br>`010 << 1 = 100` | Desplazar izquierda (Multiplicar por $2^n$). |
| **R-SHIFT**| `>> n` | `100 >> 1 = 010`<br>`010 >> 1 = 001` | Desplazar derecha (Dividir entre $2^n$). |

---
---

## EX00 - Adder (Sumar a nivel de bits)

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

### 📊 Ejemplo: 5 + 3 (En binario: 101 + 011)

En cada vuelta, calculamos la suma sin llevar (`a ^ b`) y el acarreo (`(a & b) << 1`).

| Vuelta | a (Suma parcial `^`) | b (Acarreo `& << 1`) | Binario `a` | Binario `b` |
| :---: | :--- | :--- | :--- | :--- |
| **Inicio** | **5** | **3** | `0101` | `0011` |
| 1 | 6 | 2 | `0110` | `0010` |
| 2 | 4 | 4 | `0100` | `0100` |
| 3 | 0 | 8 | `0000` | `1000` |
| 4 | **8** | **0** | `1000` | `0000` |

*(Como `b` ha llegado a 0, el bucle termina y el resultado final es `a = 8`)*

---
---

## EX01 - Multiplier (Multiplicar a nivel de bits)

### 💡 Descripción
Implementamos la multiplicación utilizando el método de **"Duplicar y Dividir"**, históricamente conocido como la **Multiplicación Rusa** o del Campesino Ruso (*Peasant Multiplication*). 

Este algoritmo es brillante porque descompone cualquier multiplicación usando solo sumas, multiplicaciones por 2 y divisiones entre 2. A nivel de bits, esto encaja a la perfección con la arquitectura de los ordenadores.

### 🧠 Lógica
Descomponemos la multiplicación de `a * b` evaluando los bits de `b`.

1. **El Bucle**: Evaluamos mientras quede algo en `b` (`b != 0`).
2. **¿Debemos sumar? (AND `& 1`)**: Comprobamos si `b` es impar mirando su último bit (`b & 1`). Si es impar, significa que el valor actual de `a` forma parte de la suma total, así que lo sumamos al `resultado` usando nuestra función `adder`.
3. **Evolución de variables**:
   * **Duplicamos `a`**: Hacemos un LEFT SHIFT (`a << 1`). Equivale a multiplicar por 2.
   * **Dividimos `b`**: Hacemos un RIGHT SHIFT (`b >> 1`). Equivale a dividir entre 2 y descartar el resto.

### 📊 Ejemplo: 12 * 5
En cada paso, `a` se duplica y `b` se divide. Solo sumamos `a` al resultado cuando `b` es impar.

| Vuelta | a (Duplica) | b (Divide) | ¿b es Impar? | Suma al Resultado | Total |
| :---: | :--- | :--- | :--- | :--- | :--- |
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
La fórmula para convertir un binario normal a Gray es muy compacta: `n ^ (n >> 1)`.

Usa la regla de los **Vecinos**:
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
Vecino (6>>1):     0   1   1   (RIGHT SHIFT )
                   ---------   
Gray (5):          1   0   1   (XOR)
```

### 📊 Valores de 0 a 16

Aplicando la fórmula a los primeros 16 valores para demostrar que coinciden con la secuencia del Código Gray. Para mayor claridad, se muestran todas las operaciones en formato de 5 bits:

| Decimal (`n`) | Fórmula (`n ^ n>>1`) | Operación Binaria | Resultado Binario | Gray (Decimal) |
| :---: | :---: | :--- | :---: | :---: |
| **0** | `0 ^ 0` | `00000 ^ 00000` | `00000` | **0** |
| **1** | `1 ^ 0` | `00001 ^ 00000` | `00001` | **1** |
| **2** | `2 ^ 1` | `00010 ^ 00001` | `00011` | **3** |
| **3** | `3 ^ 1` | `00011 ^ 00001` | `00010` | **2** |
| **4** | `4 ^ 2` | `00100 ^ 00010` | `00110` | **6** |
| **5** | `5 ^ 2` | `00101 ^ 00010` | `00111` | **7** |
| **6** | `6 ^ 3` | `00110 ^ 00011` | `00101` | **5** |
| **7** | `7 ^ 3` | `00111 ^ 00011` | `00100` | **4** |
| **8** | `8 ^ 4` | `01000 ^ 00100` | `01100` | **12** |
| **9** | `9 ^ 4` | `01001 ^ 00100` | `01101` | **13** |
| **10** | `10 ^ 5` | `01010 ^ 00101` | `01111` | **15** |
| **11** | `11 ^ 5` | `01011 ^ 00101` | `01110` | **14** |
| **12** | `12 ^ 6` | `01100 ^ 00110` | `01010` | **10** |
| **13** | `13 ^ 6` | `01101 ^ 00110` | `01011` | **11** |
| **14** | `14 ^ 7` | `01110 ^ 00111` | `01001` | **9** |
| **15** | `15 ^ 7` | `01111 ^ 00111` | `01000` | **8** |
| **16** | `16 ^ 8` | `10000 ^ 01000` | `11000` | **24** |

[Convertidor Decimal a Gray](https://tools.namlabs.com/decimal-gray/)

---
---


## EX03 - Boolean Evaluation (RPN)

### 💡 Descripción
Evaluamos fórmulas booleanas escritas en **RPN (Reverse Polish Notation)**.
En esta notación, el operador va *después* de los números (ej. `10&` en vez de `1&0`). Esto es genial para los ordenadores porque **elimina la necesidad de paréntesis**.

### 🔑 Claves de los Operadores
* `0` (FALSE)
* `1` (TRUE)
* `!` (NEGATION): El valor contrario.
* `&` (AND): Ambos deben ser verdaderos.
* `|` (OR): Basta que uno sea verdadero.
* `^` (XOR): Deben ser **diferentes**.
* `>` (IMPLICACIÓN): La única forma de que sea falso es `True > False`. En el resto de casos es verdadero.
* `=` (EQUIV): Deben ser **iguales**.

### 🧠 Lógica
Imagina una pila de platos vacía (`stack`).

1.  Recorremos la cadena carácter por carácter.
2.  **Si vemos un número (0 o 1):** Lo ponemos encima de la pila.
3.  **Si vemos un operador (&, |, ^, >, =):**
    * Sacamos los **dos** platos de arriba (`pop`).
    * Hacemos la operación matemática con ellos.
    * Ponemos el resultado (el nuevo plato) en la pila.
4.  **Si vemos un negador (!):** Sacamos solo **un** plato, le cambiamos el valor, y lo devolvemos.

El primer valor que extraemos es el operando de la derecha; el segundo, es el operando de la izquierda.

Al final, si la fórmula es correcta, **solo debe quedar un plato** en la pila. Ese es el resultado final.

### 📊 Ejemplo: `10&1|` (Equivale a `(1 AND 0) OR 1`)

| Carácter | Acción | STACK |
| :---: | :--- | :--- |
| **`1`** | `PUSH` de `True` | `[` `True` `]` |
| **`0`** | `PUSH` de `False` | `[` `True`, `False` `]` |
| **`&`** | `POP` de dos (`True`, `False`) → Calcula `True & False` = `False` → `PUSH` de `False` | `[` `False` `]` |
| **`1`** | `PUSH` de `True` | `[` `False`, `True` `]` |
| **`\|`** | `POP` de dos (`False`, `True`) → Calcula <code>False &#124; True</code> = `True` → `PUSH` de `True` | `[` `True` `]` |

**Resultado Final:** `True`

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

| Combinación | Bits | A | B | <code>AB&#124;</code> (Resultado) |
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
Dado que modificar una cadena RPN directamente con manipulaciones de texto es frágil y muy complejo, la forma matemática y profesional de resolverlo es usando un **Árbol de Sintaxis Abstracta (AST)**, dividiendo el proceso en 4 fases exactas:

1.  **Parsear a Árbol (AST Abstract Syntax Tree):** Convertimos la cadena RPN en una estructura de nodos jerárquicos. Esto nos permite saber con precisión matemática qué operandos pertenecen a la rama izquierda y derecha de cada operador.
2.  **Eliminar Operadores Complejos:** Destruimos los operadores matemáticos avanzados (`>`, `=`, `^`) y los sustituimos por sus equivalentes básicos (`&`, <code>&#124;</code>, `!`).
3.  **Aplicar De Morgan (Recursión):** Recorremos el árbol de arriba a abajo empujando los `!` hacia las ramas inferiores. Si la orden es negar, los `&` giran a <code>&#124;</code> (y viceversa), hasta que la negación se pega a las hojas (variables) o se anula por doble negación.
4.  **Serializar a RPN (Recorrido en Post-orden):** Para aplastar el árbol de vuelta a una línea de texto plano y que sea un RPN válido, aplicamos la regla estricta del **Post-orden**. En cada nodo que visitamos, hacemos estas tres cosas en este orden exacto:
    * **1º Izquierda:** Leemos todo el sub-árbol del hijo izquierdo.
    * **2º Derecha:** Leemos todo el sub-árbol del hijo derecho.
    * **3º Raíz:** Nos imprimimos a nosotros mismos (el operador).
    * *(Esto garantiza que los ingredientes/operandos siempre se impriman antes que la instrucción/operador).*

### 📖 Reglas Estrictas de Traducción Matemática
El algoritmo se basa en un diccionario estricto de equivalencias lógicas que el árbol aplica automáticamente:

**Traducción de Operadores Complejos**
* **Implicación (`>`):** `A > B` ➔ <code>!A &#124; B</code>
* **Equivalencia (`=`):** `A = B` ➔ <code>(A & B) &#124; (!A & !B)</code>
* **XOR (`^`):** `A ^ B` ➔ <code>(!A & B) &#124; (A & !B)</code>

**Leyes de De Morgan y Negación**
* **Inversión de AND:** `!(A & B)` ➔ <code>!A &#124; !B</code>
* **Inversión de OR:** <code>!(A &#124; B)</code> ➔ `!A & !B`
* **Doble Negación:** `!!A` ➔ `A`

### 📊 Ejemplo Práctico: `AB>!` (equivale a `!(A > B)`)
El siguiente ejemplo muestra cómo una fórmula fluye a través de nuestra cadena de montaje, traduciendo una implicación y luego bajando la negación a las hojas.

| Fase | Función Ejecutada | Estado del Árbol | Explicación |
| :--- | :--- | :--- | :--- |
| **0. Inicio** | - | `!(A > B)` | La negación afecta a toda la implicación. |
| **1. Traducción**| `traducir_operadores` | <code>!(!A &#124; B)</code> | El operador `>` se traduce como <code>!A &#124; B</code>. |
| **2. De Morgan**| `aplicar_de_morgan` | `!!A & !B` | El `!` principal baja: el <code>&#124;</code> gira a `&`, `A` recibe un segundo `!`, `B` se niega. |
| **3. Limpieza**| `aplicar_de_morgan` | `A & !B` | La doble negación `!!A` se anula dejando la `A` limpia. |
| **4. Salida**| `to_rpn` | **`AB!&`** | Aplastamos el árbol usando Post-orden: Izquierda (`A`) + Derecha (`B!`) + Raíz (`&`). |

---
---

## EX06 - Conjunctive Normal Form (CNF)

### 💡 Descripción
La Forma Normal Conjuntiva (CNF) es un formato estandarizado donde una fórmula se representa exclusivamente como un **"AND de ORs"**. 
Es decir, son grupos de variables unidas por <code>&#124;</code> (cláusulas), y todos esos grupos se unen entre sí mediante `&`. 

Esta forma es un pilar en ciencias de la computación porque la inmensa mayoría de los solucionadores booleanos (SAT Solvers) y algoritmos de Inteligencia Artificial exigen que el input esté en este formato estricto.

### 🧠 Lógica
Para convertir cualquier fórmula a CNF, no partimos de cero, sino que construimos sobre los cimientos del NNF. Usamos nuestro **Árbol de Sintaxis Abstracta (AST)** y añadimos un paso crucial:

1.  **Reutilización de NNF (Fases 1 a 3):** Parseamos el texto a AST, eliminamos operadores complejos (`>`, `=`, `^`) y aplicamos las leyes de De Morgan para bajar todos los `!` a las hojas.
2.  **Fase 4: Aplicar Ley Distributiva:** Recorremos el árbol buscando un patrón "ilegal" en CNF: un operador OR (<code>&#124;</code>) que tenga como hijo a un operador AND (`&`). El CNF exige que los `&` estén arriba y los <code>&#124;</code> abajo. Para solucionarlo, forzamos al `&` a subir a la raíz aplicando distributividad.
3.  **Fase 5: Serializar a RPN:** Usamos nuevamente el recorrido en **Post-orden** para aplastar el árbol en texto.

*(Nota: Este algoritmo utiliza la vía algebraica expansiva. Aunque existen métodos visuales/algorítmicos para simplificar el CNF resultante, como los Mapas de Karnaugh, esta implementación prioriza la precisión estructural matemática del árbol).*

### 📖 Reglas Estrictas de Traducción Matemática
Además del diccionario lógico del NNF, nuestro árbol aplica automáticamente la **Ley Distributiva** siempre que detecta un conflicto de jerarquía:

**Distribución del OR sobre el AND:**
* **Conflicto por la Izquierda:** <code>(A & B) &#124; C</code> ➔ <code>(A &#124; C) & (B &#124; C)</code>
* **Conflicto por la Derecha:** <code>A &#124; (B & C)</code> ➔ <code>(A &#124; B) & (A &#124; C)</code>

*El árbol clona las hojas (como la `C` o la `A`) para repartirlas en las nuevas ramas, creando nodos completamente nuevos para evitar referencias cruzadas (enfoque puramente funcional).*

### 📊 Ejemplo Práctico: `AB&C|` (equivale a `(A & B) | C`)
El siguiente ejemplo muestra cómo un árbol que ya está en NNF sufre una transformación distributiva para forzar el `&` hacia la cima.

| Fase | Función Ejecutada | Estado del Árbol | Explicación |
| :--- | :--- | :--- | :--- |
| **0. Inicio** | `conjunctive_normal_form`| <code>(A & B) &#124; C</code> | El <code>&#124;</code> es la raíz. El `&` está atrapado debajo. ¡Ilegal en CNF! |
| **1. NNF**| `aplicar_de_morgan` | <code>(A & B) &#124; C</code> | La fórmula ya cumple NNF, no hay negaciones que bajar. |
| **2. Distributiva**| `aplicar_distributiva` | <code>(A &#124; C) & (B &#124; C)</code> | Detectamos el conflicto por la izquierda. El `&` sube a la raíz. Se clona la `C`. |
| **3. Salida**| `to_rpn` | **<code>AC&#124;BC&#124;&</code>** | Aplastamos el árbol usando Post-orden: <code>A &#124; C</code> + <code>B &#124; C</code> + `&`. |

---
---

## EX07 - SAT (Satisfiability)

### 💡 Descripción
El problema de satisfacibilidad booleana (SAT) es la "piedra roseta" de las Ciencias de la Computación. De hecho, fue el primer problema de la historia demostrado matemáticamente como **NP-Completo** (Teorema de Cook-Levin).

Para entender qué significa NP-Completo, **imagina un Sudoku gigante**: resolverlo desde cero puede llevarte horas de probar y borrar números (es muy difícil calcular la solución), pero si alguien te da el Sudoku ya relleno, tardas apenas unos segundos en comprobar que no hay números repetidos (es rapidísimo verificar la respuesta). 

El SAT actúa como una llave maestra universal: si algún día alguien inventara un algoritmo capaz de resolver el SAT de forma rápida sin usar la fuerza bruta, podría usar esa misma lógica para resolver instantáneamente problemas mundiales como el plegamiento de proteínas, la logística global o romper toda la criptografía bancaria.

A nuestro nivel, la pregunta que el algoritmo debe responder es directa: **¿Existe al menos una combinación de variables (`True`/`False`) que haga que esta fórmula devuelva `True`?**
* Si existe (al menos una), la fórmula es **Satisfacible** (`True`).
* Si da `False` sin importar la combinación que probemos (una contradicción lógica), es **Insatisfacible** (`False`).

### 🧠 Lógica
Existen algoritmos extremadamente complejos para resolver esto en la industria (los famosos *SAT Solvers*), pero la forma algorítmicamente correcta de abordarlo en este punto del proyecto es mediante un ataque de **Fuerza Bruta**.

1. **Identificación de Variables ($n$):** Escaneamos la fórmula para aislar las variables únicas. Esto nos indica que existen exactamente $2^n$ combinaciones posibles.
2. **Generación de Universos (Bitwise):** Usamos manipulación de bits (el operador *shift* `>>`) iterando desde $0$ hasta $(2^n)-1$ para generar todas las combinaciones de `1`s y `0`s.
3. **Evaluación:** Le inyectamos cada combinación a nuestra función `eval_formula` para resolver el árbol lógico.
4. **Optimización por Cortocircuito (Short-circuit):** No necesitamos calcular la tabla de verdad completa. En el milisegundo exacto en el que una sola evaluación nos devuelve `True`, sabemos que la respuesta global es afirmativa. **Cortamos el bucle y devolvemos `True` inmediatamente**.
5. **Veredicto Final:** Si agotamos los $2^n$ intentos sin ver ni un solo `True`, confirmamos que es matemáticamente imposible y devolvemos `False`.

### 📊 Ejemplos Prácticos

| Fórmula (RPN) | SAT | Explicación de la Lógica |
| :--- | :---: | :--- |
| <code>AB&#124;</code> | **True** | Es **satisfacible**. La operación OR (<code>&#124;</code>) solo necesita que $A$ o $B$ valgan `1`. Con la combinación $A=1, B=0$, la fórmula ya devuelve `True`. |
| `AA!&` | **False** | Es **insatisfacible** (contradicción pura). El AND (`&`) requiere que ambos lados sean verdad, pero es imposible que $A$ valga `1` y `0` (por el `!`) al mismo tiempo. |
| <code>AA!&#124;</code> | **True** | Es una **tautología** (siempre satisfacible). El OR (<code>&#124;</code>) garantiza que, si $A$ es `1`, la primera parte es verdad; y si $A$ es `0`, la negación (`!`) la hace verdad. Siempre devuelve `True`. |

---
---

## EX08 - Powerset (Conjunto Potencia)

### 💡 Descripción
En la teoría de conjuntos, el **Conjunto Potencia** de un conjunto $S$, denotado como $P(S)$, es el conjunto que contiene **absolutamente todos los subconjuntos posibles** de $S$, incluyendo el conjunto vacío (`[]`) y el propio conjunto $S$.

La regla matemática de oro aquí es la cardinalidad (el tamaño). Si tu conjunto original tiene $n$ elementos, tu conjunto potencia tendrá exactamente **$2^n$** elementos. 
* Ejemplo: Si tienes 3 elementos, habrá $2^3 = 8$ subconjuntos.

### 🧠 Lógica
El algoritmo iterativo es la forma más eficiente de resolver esto (con complejidad $O(2^n)$ real). 

En lugar de generar combinaciones complejas, usamos la lógica de **"duplicar y añadir"**:

1. **Empezamos con la base:** Nuestro conjunto potencia inicial solo contiene el conjunto vacío: `[ [] ]`.
2. **Iteramos sobre el input:** Cogemos el primer elemento del input (ej: `1`).
3. **Duplicamos lo que tenemos:** Cogemos todo lo que hay en nuestro conjunto potencia actual (`[]`), hacemos una copia, y a esa copia le inyectamos el nuevo elemento `1` -> `[1]`.
4. **Unimos:** Guardamos los originales y los nuevos: `[ [], [1] ]`.
5. **Siguiente iteración:** Cogemos el siguiente elemento (ej: `2`). Duplicamos lo que tenemos e inyectamos el `2`:
   * Copia de `[]` + `2` = `[2]`
   * Copia de `[1]` + `2` = `[1, 2]`
   * Total acumulado: `[ [], [1], [2], [1, 2] ]`.

### 📊 Ejemplo: `powerset([1, 2, 3])`

| Iteración (Elemento) | Subconjuntos Previos (A) | Nuevos (A + elemento) | Total Acumulado |
| :---: | :--- | :--- | :--- |
| **Inicio** | `[ [] ]` | - | `[ [] ]` |
| **1** | `[ [] ]` | `[ [1] ]` | `[ [], [1] ]` |
| **2** | `[ [], [1] ]` | `[ [2], [1, 2] ]` | `[ [], [1], [2], [1, 2] ]` |
| **3** | `[ [], [1], [2], [1, 2] ]`| `[ [3], [1, 3], [2, 3], [1, 2, 3] ]` | **Total: 8 subconjuntos** |

---
---

## EX09 - Set Evaluation (Evaluación de Conjuntos)

### 💡 Descripción
En la teoría matemática, la **Lógica Booleana** (True/False) y la **Teoría de Conjuntos** son sistemas isomorfos. Esto significa que operan bajo exactamente las mismas reglas estructurales. 

En este ejercicio, en lugar de evaluar si una variable es verdadera o falsa, evaluamos qué **elementos numéricos** (que pertenecen a esa variable) sobreviven a las operaciones lógicas.
* Un **False lógico** equivale al **Conjunto Vacío** (`[]`).
* Un **True lógico** equivale al **Universo** (la unión de todos los elementos únicos introducidos).

### 🧠 Lógica
Utilizamos el método de RPN, pero con algunas modificaciones clave:

1. **Definir el Universo:** Antes de empezar, iteramos por todas las listas de entrada y metemos todos los números en un conjunto (`set()`). Esto representará nuestro "True" absoluto.
2. **Mapeo de Variables:** Las variables (`A`, `B`, `C`...) se asocian a las listas en el orden en el que se introducen (`A` es la lista 0, `B` la 1...).
3. **Pila de Sets:** La pila (stack) ahora no guarda booleanos, guarda objetos `set()` nativos de Python.
4. **Traducción de Operadores:**
    * **`&` (AND)** -> **Intersección (`a & b`)**: Solo los números que están en ambas listas.
    * **`|` (OR)** -> **Unión (`a | b`)**: Juntamos los números de ambas listas (sin duplicados).
    * **`!` (NOT)** -> **Complemento (`U - a`)**: Restamos al Universo los números de nuestra lista `a`. (Todos los números que existen *excepto* los nuestros).
    * **`^` (XOR)** -> **Diferencia Simétrica (`a ^ b`)**: Números que están en `a` o en `b`, pero *no en ambos*.
    * **`>` (IMPLIES)** -> Usamos la equivalencia lógica `!A | B` para traducirlo a conjuntos: `(U - a) | b`.

### 📊 Ejemplo: `A!B&` con `A=[1,2,3]` y `B=[2,3,4]`

1.  **Universo (U):** `[1, 2, 3, 4]` (La combinación única de todos los elementos).
2.  Leemos `A`: Metemos en la pila `[1, 2, 3]`.
3.  Leemos `!`: Reemplazamos `A` por su complemento (U - A).
    * `[1, 2, 3, 4] - [1, 2, 3] = [4]`.
    * En la pila queda: `[4]`.
4.  Leemos `B`: Metemos en la pila `[2, 3, 4]`.
5.  Leemos `&`: Hacemos la intersección de `[4]` y `[2, 3, 4]`.
    * El único elemento en común es el `4`.
6.  **Resultado final:** `[4]`.

---
---

## EX10 - Curve (Space-Filling Curve / Hilbert Curve)

### 💡 Descripción
Imagina que tienes una pantalla cuadrada de 2D llena de píxeles, y tienes un solo hilo muy largo que debe pasar por **todos y cada uno de los píxeles** sin cruzar sobre sí mismo, hasta llenar completamente el cuadrado.

Eso es una **Curva que llena el espacio** (Space-Filling Curve). La más famosa es la **Curva de Hilbert**. 
Esta función mapea unas coordenadas `(X, Y)` en un espacio $2^{16} \times 2^{16}$ y nos dice exactamente **en qué porcentaje de recorrido** (de 0.0 a 1.0) está ese punto en la curva.

### 🧠 Justificación: ¿Por qué es Continua?
Una pregunta clásica en la evaluación es justificar su continuidad.
La curva de Hilbert es continua porque **preserva la localidad de los datos**. Esto significa que dos coordenadas `(X, Y)` que estén muy pegadas en el tablero 2D, tendrán valores `[0, 1]` extremadamente cercanos en la línea 1D.

El algoritmo lo consigue dividiendo el espacio en 4 cuadrantes grandes, luego divide cada cuadrante en otros 4, y así sucesivamente (de forma recursiva). Cuando la curva pasa de un cuadrante al siguiente, la rotación de los ejes garantiza que el salto se haga entre los píxeles limítrofes directos, por lo que **jamás da saltos bruscos ("teletransportes")**, asegurando la continuidad matemática.

### 📊 Lógica
1. **Espacio inicial:** Operamos en un tablero de $65536 \times 65536$ celdas (16 bits). El máximo valor posible del hilo sería $2^{32} - 1$ (4294967295).
2. **Desplazamiento a nivel de Bit (`s`):** Empezamos inspeccionando el cuadrante más grande (el bit 15: `s = 32768`) y vamos bajando hasta 0.
3. **Rotación:** Con los operadores bit a bit (`&`, `^`) calculamos en qué sub-cuadrante está nuestro punto. Si el recorrido requiere cambiar de dirección (para no cruzarse), aplicamos una transformación matemática intercambiando e invirtiendo `x` e `y`.
4. **Normalización:** Al terminar el bucle, tenemos una variable `d` que nos dice la posición exacta del punto en la línea (entre 0 y 4294967295). Lo dividimos entre el máximo y obtenemos un elegante `float` de 0.0 a 1.0.

* **Inicio `(0, 0)`** $\rightarrow$ Devuelve `0.0`.
* **Final `(65535, 0)`** $\rightarrow$ Devuelve `1.0`.

---
---

## EX11 - Inverse (Hilbert Unmap)

### 💡 Descripción
Si en el ejercicio anterior (Curve) convertíamos una coordenada 2D en una distancia 1D, aquí hacemos exactamente lo contrario: **dada una distancia `d` a lo largo de la Curva de Hilbert (entre 0.0 y 1.0), ¿cuáles son las coordenadas `(x, y)` exactas en la cuadrícula 2D?**

Esta operación es vital en bases de datos espaciales y gráficos por computadora porque nos permite recuperar información de ubicación bidimensional a partir de un índice unidimensional súper rápido.

### 🧠 Lógica
El algoritmo de decodificación de Hilbert funciona al revés que el de codificación. En lugar de dividir el espacio de mayor a menor, reconstruimos el punto **de menor a mayor (Fine to Coarse)**.

1. **Desnormalización:** Tomamos el `float` que va de `0.0` a `1.0` y lo multiplicamos por el máximo valor de celdas ($2^{32} - 1$). Usamos `round()` para proteger la precisión flotante de Python y obtenemos un entero de 32 bits que representa la distancia absoluta `d`.
2. **Reconstrucción Bottom-Up:** Iniciamos un bucle que representa el tamaño del cuadrante, empezando por $s = 1$ (el píxel más pequeño) y subiendo hasta $s = 32768$.
3. **Decodificación de Bits:** * Tomamos `d` y extraemos los 2 últimos bits usando lógica binaria (`rx = 1 & (d // 2)`).
    * Estos dos bits nos indican en cuál de los 4 sub-cuadrantes relativos nos encontrábamos en ese nivel de recursión.
4. **Deshacer la Rotación:** Si la curva había rotado o se había invertido en ese nivel, aplicamos la transformación geométrica opuesta (`x = s - 1 - x`, y un *swap* `x, y = y, x`).
5. **Acumular:** Desplazamos nuestras coordenadas `x` e `y` basándonos en el cuadrante actual.
6. **Subir de nivel:** Tiramos a la basura los 2 bits de distancia que acabamos de leer (`d //= 4`) y duplicamos el tamaño de nuestro lienzo (`s *= 2`).

Al terminar el ciclo, las variables `x` e `y` contienen la coordenada exacta y perfecta de 16 bits original.

### 📊 Ejemplo: Round-Trip
La evaluación de 42 requiere que verifiquemos esto matemáticamente:
`reverse_map(map_coords(x, y)) == (x, y)`

Gracias a que hemos evitado la pérdida de precisión flotante en Python usando `round()`, nuestro test genera **10,000 coordenadas aleatorias**, las codifica en `d`, las vuelve a decodificar, y garantiza un 100% de exactitud en la recuperación para cada una de ellas.