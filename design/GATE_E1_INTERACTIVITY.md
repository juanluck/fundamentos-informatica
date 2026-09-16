# Puerta E1 — Interactividad del explorador

Estado: implementada para validación.

Base congelada: Puerta D4.

## Alcance

Se convierte únicamente el explorador estático en un componente funcional manteniendo su composición visual aprobada.

- `<input type="range">` real.
- Rango inicial: 1–4 bits.
- Estado inicial: 3 bits.
- Se regeneran todas las combinaciones binarias para el número de bits seleccionado.
- Se actualizan simultáneamente el contador, el total `2^n` y el exponente mostrado.
- Máximo 16 combinaciones para conservar la densidad editorial del bloque y mostrar siempre todas las posibilidades sin scroll interno.
- Actualización accesible mediante regiones con `aria-live`.

## No cambia

No se añaden botones, menús, animaciones, tarjetas nuevas ni controles adicionales. D1–D4, retícula, tipografía y paleta permanecen congeladas.

## Criterio

La interacción debe sentirse como si el elemento estático del mockup hubiese cobrado vida, no como un widget ajeno insertado en la página.
