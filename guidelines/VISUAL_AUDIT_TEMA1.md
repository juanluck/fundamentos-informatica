# Auditoría visual — Tema 1, material fuente L1.1 y L1.2

Documento de trabajo para reconstruir el Tema 1. Esta auditoría **no decide qué contenido entra o sale del libro**. Registra cómo se utiliza visualmente el material fuente y cómo se traslada al prototipo web.

Fuente principal revisada: `Tema 1 - Resumen - Ejercicios` (Google Slides).

## L1.1 — Definiciones básicas

### Diapositivas 4–7

**Observación**

Son diapositivas de alta dependencia visual: gran parte de su significado reside en imágenes y asociaciones espaciales; la extracción de texto devuelve prácticamente solo el título.

**Decisión de prototipo**

No trasladarlas como capturas. Reconstruir su función mediante una apertura visual donde varias formas de información (texto, imagen y sonido) convergen en una codificación y terminan en patrones procesables por el computador.

**Recurso creado**

`assets/tema1/informacion-computador.svg`

### Diapositiva 9 — Leyenda de Sissa

**Observación**

La historia se utiliza para dar intuición sobre potencias de dos y crecimiento exponencial antes de los ejercicios.

**Decisión de prototipo**

Mantener la idea y redibujarla con la identidad gráfica del libro. El tablero no es decoración: debe hacer visible la duplicación.

**Recurso creado**

`assets/tema1/sissa.svg`

### Diapositivas 10–19 — bits, potencias de 2 y codificación

**Observación**

La presentación utiliza revelado progresivo de respuestas: número de bits, número de símbolos y asignación de patrones.

**Decisión de prototipo**

No agruparlo todo en una tabla estática. Usar:
- figura progresiva 1/2/3 bits;
- pequeño explorador interactivo web;
- ejercicios inmediatamente después de la explicación;
- solución plegable.

**Recursos creados**

- `assets/tema1/crecimiento-bits.svg`
- widget `bit-explorer` en `assets/components.js`

### Diapositivas 20–24 — 100 Megas y 1 GByte

**Observación**

Ejercicio contextual que obliga a distinguir bits/bytes y relacionar velocidad, tiempo y cantidad de información.

**Decisión de prototipo**

Conservar el problema, pero situarlo después de introducir visualmente el byte y la distinción `b`/`B`.

**Recurso creado**

`assets/tema1/byte.svg` y composición comparativa `Mb/s ≠ MB/s`.

## L1.2 — Unidades funcionales

### Diapositivas 26–36 — construcción CPU/memoria

**Observación**

La explicación depende de una secuencia visual: aparece CPU, longitud de palabra, memoria, posiciones y contenidos. El valor pedagógico está en la **construcción progresiva**, no en una única figura final.

**Decisión**

No implementado todavía en la primera iteración visual. Para la nueva lección 1.3 se conservará la secuencia como varios estados o una interacción paso a paso.

### Diapositivas 37–38 — bus de datos y bus de direcciones

**Observación**

Es uno de los recursos visuales más importantes del Tema 1. Distingue dos funciones que los estudiantes suelen confundir y conecta el ancho del bus de direcciones con $2^n=m$.

**Decisión**

Reservado para la nueva lección 1.4. Se redibujará como secuencia:
1. CPU + memoria;
2. «¿dónde?» → bus de direcciones;
3. «¿qué contenido?» → bus de datos;
4. relación entre bits de dirección y número de posiciones.

### Diapositivas 39–41

**Observación**

Continúan apoyándose en recursos gráficos con muy poco texto extraíble.

**Decisión**

Revisarlas de nuevo durante la implementación de 1.3–1.4, evitando convertirlas en explicación puramente textual.

## Criterio adoptado

El prototipo visual de 1.1–1.2 no intenta imitar el aspecto de PowerPoint. **Conserva el papel pedagógico de sus imágenes y secuencias**, pero las convierte en recursos nativos de la web: SVG escalable, composición responsive e interacción pequeña cuando aporta comprensión.
