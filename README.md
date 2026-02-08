# 🧮 Ready, Set, Boole! 

---
---

## EX00 - Adder (Sumador a nivel de bits)

### 💡 El Concepto
Este ejercicio simula cómo los procesadores suman números físicamente usando un circuito llamado **Half Adder** (Medio Sumador), utilizando exclusivamente operadores bit a bit (bitwise), sin usar el operador matemático `+`.

### 🧠 La Lógica Paso a Paso
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

### 💡 El Concepto
Implementamos la multiplicación utilizando el método de **"Duplicar y Dividir"**, históricamente conocido como la **Multiplicación Rusa** o del Campesino Ruso (*Peasant Multiplication*). 

Este algoritmo es brillante porque descompone cualquier multiplicación usando solo sumas, multiplicaciones por 2 y divisiones entre 2. A nivel de bits, esto encaja a la perfección con la arquitectura de los ordenadores.

### 🧠 La Lógica Paso a Paso
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

### 💡 El Concepto
El Código Gray es un sistema de numeración binaria alternativo donde dos números consecutivos **solo se diferencian en un único bit**. 

Esto es fundamental en el mundo del hardware y la robótica (como en sensores de posición o *encoders*) para evitar errores de lectura. Si usáramos binario normal, al pasar de 3 (`011`) a 4 (`100`) cambiarían 3 bits a la vez, y una lectura en el momento justo del cambio podría dar cualquier valor erróneo intermedio. En Gray, solo cambia uno, garantizando estabilidad.

### 🧠 La Lógica Paso a Paso
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

---

## EX03 - Boolean Evaluation (RPN)

### 💡 El Concepto
Evaluamos fórmulas booleanas escritas en **RPN (Reverse Polish Notation)**.
En esta notación, el operador va *después* de los números (ej. `10&` en vez de `1&0`). Esto es genial para los ordenadores porque **elimina la necesidad de paréntesis**.

### 🧠 La Lógica Paso a Paso
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
| **|** | Saca dos (`F`, `T`) -> Calcula `F | T` = `T` -> Empuja | `[True]` |

**Resultado Final:** `True`.

### 🔑 Claves de los Operadores
* `&` (AND): Ambos deben ser verdaderos.
* `|` (OR): Basta que uno sea verdadero.
* `^` (XOR): Deben ser **diferentes**.
* `=` (EQUIV): Deben ser **iguales**.
* `>` (IMPLICACIÓN): La única forma de que sea falso es `True > False`. En el resto de casos es verdadero.

---
---

