# Política de autoría Quarto: Markdown primero

## Regla general

El contenido del libro se escribe en Markdown/Quarto siempre que sea posible. El diseño se expresa mediante clases CSS aplicadas a fenced divs y spans de Pandoc. El HTML crudo se reserva para componentes que Markdown/Quarto no puede expresar con fidelidad o funcionalidad suficiente.

## Orden de preferencia

1. Markdown semántico: títulos, párrafos, listas, enlaces, énfasis, tablas, matemáticas, imágenes.
2. Fenced divs/spans de Quarto para aplicar clases del sistema visual.
3. Componentes externos incluidos con `{{< include ... >}}` para figuras SVG complejas o widgets.
4. HTML crudo solo dentro de esos componentes cuando sea necesario.
5. JavaScript siempre fuera de las lecciones `.qmd` salvo la referencia mínima al recurso.

## Restricción visual

Esta refactorización no autoriza cambios de diseño. Las lecciones 1.1 y 1.2 aprobadas siguen siendo la referencia visual. El objetivo es desacoplar contenido y presentación sin modificar su apariencia.

## Patrón de una lección

- YAML mínimo.
- Un contenedor `.sheet` mediante fenced div.
- Contenido textual en Markdown.
- Clases visuales mediante atributos Pandoc.
- Ilustraciones complejas en `components/`.
- Comportamiento en `assets/*.js`.
- Apariencia en `styles/*.css`.

## Componentes extraídos en esta primera refactorización

- `components/tema1/_computer-figure.qmd`
- `components/tema1/_states-figure.qmd`
- `components/tema1/_bit-explorer.qmd`

La misma política se aplicará al resto del libro una vez comprobada la equivalencia visual de 1.1 y 1.2.
