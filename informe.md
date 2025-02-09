# Tema: Detección de similitudes entre códigos a partir de sus grafos de dependencia

## Integrantes

- Daniel Toledo Martínez
- Osvaldo Roberto Moreno Prieto

## Definiciones

Grafo de dependencias (PDG):
Tipo de un vértice: El tipo asignado por el PDG

## Antecedentes e ideas generales

En la dección de plagio de código fuente de manera general aparecen 3 enfoques principales en la literatura: detección basada en texto, análisis sintáctico y análisis semántico, donde cada una maneja un nivel de abstracción del código distinta. En este proyecto nos estaremos enfocando en el análisis semántico del código por su capacidad de ser resistente contra algunas de las estrategias de ofuscación más comunes como son:
- Copias exactas
- Adición y eliminación de comentarios, modificaciones de formato
- Reordenamiento de bloques de código, cambio en las estructuras de control, modificación en estructuras de datos (ej. cambiar un array por una lista)

El problema de modelación de la estructura sobre la cual estaremos trabajando (PDG) queda fuera del ámbito de este trabajo, por lo que nos estaremos concentrando en los algoritmos sobre esta estructura que puedan ser de interés para nuestro problema.

## Propuesta 1

Para determinar si dos códigos son copias exactas, sujetos a una serie de modificaciones de las antes mencionadas, y dado que conocemos las potencialidades de los PDG, podríamos como primer enfoque determinar si un par de grafos son isomorfos, de esta manera estaríamos encontrando similitudes estructurales.

### Problema de isomorfismo de grafos (GI)

Como enfoque para esta propuesta proponemos determinar si los grafos G y H son isomorfos

#### Definición del algoritmo

Para resolver el problema de isomorfismo de grafos vamos a estar utilizando un algoritmo basado en técnicas de refinamiento de clases de equivalencia (también conocido como coloración o etiquetado). Para ello vamos a establecer un grupo de invariantes sobre los vértices (clase, grado de entrada, grado de salida, conexiones con otras clases) y realizar un proceso de refinamiento hasta que los vértices estén correctamente distribuidos en sus respectivas clases. Dos vértices pertenecen a la misma clase siempre que sus invariantes sean iguales.

#### Pasos del algoritmo

- Paso 1 (Inicialización): Para cada vértice de G determinar sus invariantes y agrupar los vértices en clases iniciales según sus invariantes
- Paso 2 (Refinamiento): En cada iteración, refinar las clases existentes usando la información de los vecinos 
- Paso 3 (Refinamiento): Agrupar vértices con la misma etiqueta en nuavas clases
- Paso 4 (Refinamiento): Repetir a partir del paso 2 hasta que las clases ya no puedan ser refinadas (estabilización)
- Paso 5: Aplicar el mismo proceso para H
- Paso 6: Verificar coincidencia de las clases, en caso positivo, generar posibles biyecciones entre las clases

#### Complejidad temporal

Sean n el número de vértices y m el número de aristas
- (Inicialización) Calcular invariantes: O(n+m)
- (Refinamiento) Generar etiqueta para todos los vértices: O(n+m)
- (Refinamiento) Número de iteraciones: O(n) en el peor caso (las clases se dividen hasta que cada vértice esté en su propia clase)
- Total: O(n) X O(n+m) = O(2n + nm) = O(nm)
  - Para grafos densos: O($n^3$)
  - Para grafos dispersos: O($n^2$)

#### Limitaciones

- Esta solución encuentra grafos isomorfos, por tanto es débil en los casos en que ocurre cualquier adición a la lógica
- Grafos regulares: Si todos los vértices tienen el mismo grado, el refinamiento no progresa
- Grafos fuertemente simétricos: Puede que no se distingan clases, requiriendo backtracking adicional
- No es concluyente para todos los grafos: Algunos grafos no isomorfos pasan la prueba (falsos positivos), como los grafos de Cayley

El problema en cuestión es suficientemente complejo en su evaluación temporal como para dar a luz a una nueva categoría de complejidad **GI** y aunque su complejidad es polinomial, no resuelve el problema de isomorfismo para todos los casos, por lo que se combina con otras técnicas.

## Propuesta 2

Para determinar similitudes entre los códigos tenemos como propuesta determinar si un código A implementa la misma lógica que un código B. Para ello llamaremos G al PDG de A y H al PDG de B

### Problema de isomorfismo de subgrafos (SIP)

Como enfoque para esta propuesta planteamos determinar si existe algún subgrafo en A isomorfo con B, esto implicaría que se implementa la misma lógica de B en un subconjuto de A, es decir, que B es parte de la solución de A.

#### Definición formal del problema:

Dado un par de grafos G=($V_g$, $E_g$) y H=($V_h$, $E_h$) existe un subgrafo G'=($V_g$', $E_g$') tal que G' es isomorfo con H. Es decir, existe una biyección *f*: $V_h$ -> $V_g$' que preserva las adyacencias.

Se debe tener en cuenta que la definición se aplica tanto para grafos dirigidos como para no dirigidos y si existen etiquetas en los vertices o aristas, estas deben preservarse. 

#### Demostración de np-completitud:

(SIP $\in$ NP) -> Dada una biyección *f*: $V_h$ -> $V_g$', se comprueban las aristas en O($n^2$).

Por cada arista verificar si:
- {u, v} $\in E_g$ 
- {f(u), f(v)} $\in E_h$

Reducción de la entrada del problema a k-clique

El problema de k-clique recibe como entrada un grafo *G* y un entero *k*
Transformación:
- G = *G*
- H = $K_k$ (Grafo completo de k vértices)

La transformación es trivial y se realiza en O($k^2$). Si G tiene un k-clique entonces existe un subgrafo isomorfo a H = $K_k$ (el propio clique). Si G contiene un subgrafo isomorfo a H = $K_k$ entonces ese subgrafo es un k-clique de G

#### Limitaciones

La solución es demasiado compleja temporalmente, además es demasiado general para nuestro problema innecesariamente.

## Propuesta 3

Las estructuras sobre las cuales estamos computando nuestro problema garantizan que el grafo sobre el que estamos trabajando es un árbol. Por este motivo podemos enfocar los algoritmos anteriores a un dominio más restringido

### Problema de isomorfismo de árboles 

Para este enfoque vamos a determinar si un par de árboles G y H son isomorfos

#### Definición del algoritmo

Para solucionar el problema de isomorfismo de árboles vamos a utilziar el algoritmo de AHU que consiste en etiquetar los vértices de forma progresiva para obtener en cada vértice una descripción uníca para él que contenga la información de sus hijos. De esta forma determinar si dos árboles son isomorfos no sería más que determinar si sus raíces tienen la misma etiqueta.

#### Pasos del algoritmo

Paso 1: Etiquetar de forma preliminar los vértices teniendo en cuenta su tipo
Paso 2: Para cada vértice se aplica el algoritmo en sus hijos (en caso de no tener conserva su etiqueta preliminar)
Paso 3: Se ordenan las nuevas etiquetas obtenidas para los hijos y se concatenan para formar la nueva etiqueta del nodo
Paso 4: Se realiza el mismo procedimiento para el otro árbol
Paso 5: Se comparan las raíces de ambos árboles

#### Complejidad temporal

**Caso base:**  
Para \( n = 1 \) (un árbol formado por una hoja), el coste es:
\[
T(1) = O(1)
\]

**Hipótesis de inducción:**  
Supongamos que para todo árbol de tamaño \( m < n \) se cumple que:
\[
T(m) \leq a \, m \log m
\]
para alguna constante \( a > 0 \)

**Paso inductivo:**  
Consideremos un árbol con \( n \) nodos cuya raíz tiene \( k \) hijos y tamaños de subárboles \( n_1, n_2, \dots, n_k \) con \( \sum_{i=1}^{k} n_i = n - 1 \). Entonces:
\[
T(n) = \sum_{i=1}^{k} T(n_i) + c_1 \, k \log k
\]
por alguna constante \( c_1 \).

Aplicando la hipótesis de inducción para cada subárbol:
\[
T(n) \leq \sum_{i=1}^{k} a \, n_i \log n_i + c_1 \, k \log k
\]

#### Correctitud


#### Limitaciones


## Notas

En el caso de la propuesta 1 se define la solución general, pero el primer paso no es necesario ya que los vértices están agrupados por la *etiqueta* que los representa
En el caso de la propuesta 2 el vértice con la *etiqueta* **Program** de B debe ser sustituido por un vértice compatible con cualquier otro para su correcto funcionamiento.