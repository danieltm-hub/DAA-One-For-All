# Detección de Similitudes entre Códigos mediante Grafos de Dependencia

El objetivo de este proyecto es desarrollar algoritmos eficientes para detectar similitudes entre códigos fuente a través del análisis de sus **Grafos de Dependencia (PDG)**. Este enfoque permite identificar plagio o reutilización de código, incluso cuando se aplican técnicas de ofuscación como cambios en el formato, reordenamiento de bloques o modificaciones en las estructuras de control.

## Propuestas de Solución

Se exploran varias técnicas para abordar el problema desde diferentes perspectivas:

### 1. **Isomorfismo de Grafos**

- Determina si dos grafos son isomorfos, lo que implica que los códigos tienen la misma estructura lógica.
- Utiliza técnicas de refinamiento de clases de equivalencia para comparar nodos y aristas.
- Complejidad: $ O(n^3) $ para grafos densos.
- Limitaciones: Sensible a adiciones en la lógica y grafos con alta simetría.

### 2. **Isomorfismo de Subgrafos**

- Verifica si un subgrafo de un PDG es isomorfo a otro, indicando que una parte del código implementa la misma lógica.
- Demostración de NP-completitud mediante reducción desde el problema $ k $-Clique.
- Limitaciones: Computacionalmente costoso para grafos grandes.

### 3. **Isomorfismo de Árboles (Algoritmo AHU)**

- Aplica el algoritmo de Aho-Hopcroft-Ullman (AHU) para comparar árboles enraizados.
- Asigna etiquetas únicas a cada nodo basadas en su estructura y la de sus hijos.
- Complejidad: $ O(n \log n) $.
- Ventajas: Eficiente para estructuras jerárquicas como PDGs simplificados.
- Limitaciones: No robusto frente a adiciones en el código.

### 4. **Isomorfismo de Subgrafos en Árboles No Ordenados**

- Extiende el problema de isomorfismo de subárboles a subgrafos en árboles no ordenados.
- Utiliza emparejamientos bipartitos y el algoritmo de Hopcroft-Karp para verificar biyecciones entre nodos.
- Complejidad: $ O(n*{T_2} \cdot k*{T*1} \cdot k*{T*2} \cdot \sqrt{k*{T_2}}) $.
- Ventajas: Más general que el isomorfismo de subárboles.

### 5. **Tree Edit Distance (TED)**

- Mide la distancia mínima para transformar un árbol en otro mediante operaciones como inserciones, eliminaciones y renombramientos.
- Relacionado con el problema del Máximo Subárbol Común (MCS).
- Complejidad: NP-hard.
- Aplicaciones: Comparación de proximidad entre estructuras de código.

## Análisis Temporal

Cada propuesta incluye un análisis detallado de su complejidad temporal, destacando las ventajas y limitaciones computacionales de cada enfoque.
