# Puerta D3 — Figura «Explorador interactivo»

Estado: **en validación**. Parte de D2 aprobada y no modifica ninguna decisión previa.

## Alcance

Se sustituye únicamente el placeholder del bloque **3. Explorador interactivo** por una reconstrucción estática fiel al mockup aprobado.

No se modifica:
- la retícula;
- la tipografía;
- la paleta;
- las figuras D1 y D2;
- la fórmula inversa;
- el contenido textual;
- el comportamiento responsive general.

No se introduce JavaScript todavía.

## Referencia visual

El mockup muestra dos masas horizontales:

1. **Panel izquierdo**
   - fila superior: etiqueta «Número de bits:», valor `3` y deslizador;
   - debajo: ocho combinaciones de tres bits en dos filas de cuatro.

2. **Panel derecho**
   - etiqueta «Total de combinaciones:»;
   - número `8` grande en terracota;
   - pequeños rayos de énfasis alrededor del número;
   - fórmula `(2³)` debajo.

## Decisiones

- Se mantiene el fondo melocotón pálido ya aprobado en C.
- El deslizador es estático y sitúa visualmente el selector en `3`.
- Las combinaciones son celdas editoriales, no botones.
- El `8` es la masa visual dominante del panel derecho.
- Los rayos de énfasis se dibujan con trazos simples en terracota, sin iconos ni efectos nuevos.

## Criterio de aprobación

D3 se aprueba si la composición reproduce de forma reconocible el explorador del mockup y no parece todavía un widget de aplicación web genérico.
