# Fundamentos de Informática — maqueta Quarto

Prototipo de maquetación para el futuro libro de Fundamentos de Informática.

## Estado actual

Esta rama valida la identidad visual, los componentes editoriales y su comportamiento web/PDF antes de trabajar con contenido real de la asignatura.

La prioridad de diseño es la **web**, manteniendo una futura salida PDF coherente y apta tanto para pantalla como para impresión.

## Previsualización local

Con Quarto instalado:

```bash
quarto preview
```

Para renderizar solo la versión web:

```bash
quarto render --to html
```

Para generar todos los formatos configurados:

```bash
quarto render
```

## GitHub Pages

El workflow `.github/workflows/publish.yml` renderiza la salida HTML y la publica en la rama `gh-pages` cuando hay cambios en `main` o en `maqueta-quarto-v01`.

## Archivos principales

- `_quarto.yml`: configuración del libro.
- `sandbox.qmd`: galería de componentes.
- `styles/book.scss`: identidad visual web.
- `assets/components.js`: interacción de soluciones plegables.
- `filters/components.lua`: generación semántica de etiquetas, títulos y dificultad.
- `guidelines/COMPONENTS.md`: contrato de componentes.
- `guidelines/STYLE_GUIDE.md`: decisiones visuales actuales.
