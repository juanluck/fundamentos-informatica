# Lección 1.2 — estado final del prototipo

Estado: **Hito 1 listo para revisión global**.

Referencia visual: página central del mockup aprobado «LECCIÓN 1.2 · ¿Cómo representa la información?».

## Decisiones congeladas

- Puerta A: estructura y retícula.
- Puerta B: Source Serif 4 como serif editorial y Caveat solo para anotaciones manuscritas.
- Puerta C: papel crema, tinta azul-negruzca, terracota, melocotón pálido y ámbar para el estado encendido.
- D1: figura Estado 0 / Estado 1.
- D2: figura 1 / 2 / 3 bits y regla `2^n`.
- D3: composición del explorador.
- D4: fórmula inversa y anotación final.
- E1: explorador interactivo real.

## Geometría final

- Escritorio: `width: min(92vw, 720px)`.
- Tablet/portátil: se mantiene el máximo de 720 px con margen exterior reducido.
- Móvil ≤ 620 px: lienzo al 100 %, sin sombra exterior.
- Ajuste adicional ≤ 440 px para conservar legibilidad y evitar desbordamientos.

## Interactividad

El explorador conserva 3 bits como estado inicial del mockup. El control permite 1–4 bits y recalcula:

- las combinaciones binarias completas;
- el total `2^n`;
- el exponente mostrado;
- el texto accesible anunciado por lector de pantalla.

El límite de 4 bits es deliberado para mostrar todas las combinaciones sin destruir la composición editorial.

## Accesibilidad y robustez

- control `range` nativo, operable con teclado;
- etiqueta asociada al control;
- estado dinámico anunciado mediante `output aria-live="polite"`;
- SVG con etiquetas accesibles;
- foco visible;
- reducción de movimiento respetada;
- variante terracota más oscura reservada al texto pequeño para mejorar contraste;
- CSS final autocontenido: no depende de los estilos de gates anteriores.

## Anchuras de control

La composición se ha preparado explícitamente para comprobar:

- 1440 px: lienzo editorial centrado de 720 px;
- 1024 px: misma escala editorial, márgenes exteriores menores;
- 390 px: flujo móvil de una columna para figuras complejas, manteniendo dos estados en paralelo.

## Lo que no se hace todavía

- integración con Quarto;
- navegación del libro;
- extracción definitiva del Design System v1;
- aplicación a otras lecciones.

Esos pasos comienzan únicamente después de la revisión global de esta versión final de 1.2.
