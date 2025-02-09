# Detección de Similitudes entre Códigos a partir de sus Grafos de Dependencia

**Autores:**  
Daniel Toledo Martínez, Osvaldo Roberto Moreno Prieto

**Fecha:**  
\(\today\)

---

## Introducción

La detección de plagio en código fuente es un área relevante en el análisis de software. Tradicionalmente existen tres enfoques principales: detección basada en texto, análisis sintáctico y análisis semántico. En este trabajo se aborda el análisis semántico, considerado más robusto frente a técnicas de ofuscación como cambios en el formato, reordenamiento de bloques de código o modificaciones en las estructuras de control y de datos.

El modelado de la estructura (PDG) se toma como dado; el foco está en los algoritmos que operan sobre esta estructura.

---

## Propuestas de Solución

A continuación se presentan distintos enfoques para determinar similitudes entre códigos utilizando sus PDG.

---

### Propuesta 1: Isomorfismo de Grafos

#### Definición del Algoritmo

Se propone utilizar técnicas de refinamiento de clases de equivalencia (o etiquetado) para determinar si dos grafos \( G \) y \( H \) (correspondientes a los PDG) son isomorfos. El algoritmo sigue estos pasos:

1. **Inicialización:**  
   Para cada vértice de \( G \), determinar sus invariantes (clase, grado de entrada, grado de salida, conexiones con otras clases) y agruparlos.

2. **Refinamiento:**  
   Refinar las clases existentes utilizando la información de los vecinos.

3. **Iteración:**  
   Repetir el refinamiento hasta alcanzar la estabilización (no se pueden refinar más las clases).

4. **Aplicación en \( H \):**  
   Realizar el mismo proceso de clasificación en el grafo \( H \).

5. **Comparación:**  
   Verificar la coincidencia de clases y determinar posibles biyecciones entre ellas.

#### Complejidad Temporal

Sean \( n \) el número de vértices y \( m \) el número de aristas:

- **Inicialización:** \( O(n + m) \)
- **Refinamiento:** Cada iteración requiere \( O(n + m) \) y, en el peor caso, se pueden efectuar \( O(n) \) iteraciones, dando un total de \( O(nm) \).
  - Para grafos densos: \( O(n^3) \)
  - Para grafos dispersos: \( O(n^2) \)

#### Limitaciones

- Es sensible a modificaciones en el código: si se agregan o alteran componentes lógicos, el refinamiento puede no progresar (caso de grafos regulares) o requerir backtracking adicional en grafos altamente simétricos.
- No es concluyente para todos los grafos; algunos grafos no isomorfos podrían pasar la prueba (falsos positivos).

---

### Propuesta 2: Isomorfismo de Subgrafos

#### Definición Formal del Problema

Dado un par de grafos \( G = (V_g, E_g) \) y \( H = (V_h, E_h) \), el problema es determinar si existe un subgrafo \( G' = (V'\_g, E'\_g) \) de \( G \) isomorfo a \( H \). Esto implica encontrar una biyección \( f: V_h \to V'\_g \) que preserve las adyacencias (y las etiquetas, si existen).

#### Demostración de NP-Completitud

1. **SIP es NP:**  
   Dada una biyección \( f \), se verifica para cada par \( u, v \in V_h \):

- Si \( \{u, v\} \in E_h \) entonces \( \{f(u), f(v)\} \in E_g \).
- Si no, \( \{f(u), f(v)\} \notin E_g \).

Esta verificación toma \( O(n^2) \).

2. **Reducción de \( k \)-Clique a SIP:**

- **Entrada:** El grafo \( G \) para \( k \)-Clique.
- **Objetivo:** Construir un grafo \( H \) que sea \( K_k \) (grafo completo de \( k \) vértices).
- Si \( G \) contiene un clique de tamaño \( k \), existe un subgrafo isomorfo a \( H \); y viceversa.

3. **NP-Completitud de \( k \)-Clique:**

- Se verifica en \( O(k^2) \) comprobando que todos los pares de vértices en una solución forman un clique.
- Se puede reducir 3-SAT a \( k \)-Clique mediante la creación de nodos para cada literal y conectándolos condicionalmente, de modo que un clique de tamaño \( k \) corresponde a una solución de 3-SAT.

#### Limitaciones

Este enfoque es computacionalmente costoso y puede resultar demasiado general para el problema específico de detección de plagio.

---

### Propuesta 3: Isomorfismo de Árboles

Dado que se asume que el PDG tiene estructura de árbol, se puede aplicar el **Algoritmo de Aho-Hopcroft-Ullman (AHU)** para determinar si dos árboles enraizados son isomorfos.

#### Definición del Algoritmo

1. **Etiquetado Inicial:**  
   Asignar a cada nodo una etiqueta preliminar basada en su tipo.

2. **Recursión:**  
   Aplicar recursivamente el proceso a los hijos de cada nodo.

3. **Ordenación y Concatenación:**  
   Ordenar lexicográficamente las etiquetas de los hijos y concatenarlas junto a la etiqueta del nodo padre para formar una nueva etiqueta.

4. **Comparación Final:**  
   Comparar las etiquetas resultantes de las raíces de ambos árboles.

#### Análisis de Complejidad Temporal

- La complejidad del algoritmo es \( O(n \log n) \), donde \( n \) es el número de nodos, teniendo en cuenta la ordenación de las etiquetas en cada nodo.

#### Correctitud

- **Teorema:** El algoritmo AHU asigna una etiqueta canónica \( f(T) \) a cada árbol \( T \) de manera que:
  \[
  f(T_1) = f(T_2) \iff T_1 \cong T_2.
  \]
- La demostración se realiza por inducción en la altura del árbol, verificando el caso base (hojas) y el paso inductivo (ordenación y concatenación de etiquetas de subárboles).

#### Limitaciones

Aunque es eficiente, este enfoque puede tener dificultades en la comparación de árboles grandes o complejos. Además, comparte la limitación de ser sensible a pequeñas modificaciones en el código.

---

### Propuesta 4: Isomorfismo de Subárboles

Para abordar cambios o adiciones en el código, se extiende el algoritmo AHU para detectar isomorfismos parciales. Se busca determinar si existe un nodo en \( G \) cuya etiqueta describe un subárbol isomorfo a un árbol objetivo \( H \).

---

## Conclusiones

Se han presentado diversos enfoques para la detección de similitudes en código analizando sus Grafos de Dependencia. La estrategia adecuada dependerá del contexto y de las modificaciones aplicadas al código, siendo el isomorfismo de árboles una opción eficiente para estructuras más sencillas, mientras que enfoques más generales (como el de subgrafos) pueden ser necesarios para casos más complejos.
