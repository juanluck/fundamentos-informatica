# Fundamentos de Informática — maqueta Quarto

Prototipo del futuro libro de Fundamentos de Informática construido con Quarto.

## Estado actual

La rama `maqueta-quarto-v01` contiene ya dos niveles de trabajo:

1. **sistema editorial y visual**: componentes, estilos y comportamiento web/PDF;
2. **prototipo pedagógico del Tema 1**: primer capítulo utilizado como conejillo de indias para validar la reconstrucción didáctica del material docente.

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

- `_quarto.yml`: configuración y navegación del libro.
- `teoria/01-introduccion.qmd`: prototipo completo del Tema 1.
- `sandbox.qmd`: galería de componentes.
- `styles/book.scss`: identidad visual web.
- `assets/components.js`: interacción de soluciones plegables.
- `filters/components.lua`: generación semántica de etiquetas, títulos y dificultad.
- `guidelines/PEDAGOGY.md`: contrato pedagógico del proyecto.
- `guidelines/COMPONENTS.md`: contrato de componentes.
- `guidelines/STYLE_GUIDE.md`: decisiones visuales actuales.
