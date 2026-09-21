# Hito 3 — Integración Quarto v1

Estado: **implementado**.

## Objetivo

Convertir las lecciones 1.1 y 1.2 aprobadas en fuente Quarto real sin permitir que la estética predeterminada de Quarto sustituya el Design System v1.

## Regla arquitectónica

> Quarto publica y organiza. El Design System v1 decide el aspecto.

Por ello la salida HTML usa:

- `theme: none`;
- `minimal: true`;
- `toc: false`;
- `page-layout: full`;
- navegación editorial propia;
- CSS canónico en `styles/book.css`.

No se usa Bootstrap, sidebar visual, breadcrumbs ni título generado por Quarto en las páginas finales.

## Fuente canónica

- `index.qmd`
- `teoria/tema1/01-que-es-computador.qmd`
- `teoria/tema1/02-representacion.qmd`
- `styles/book.css`
- `assets/book.js`

Las versiones HTML standalone aprobadas permanecen como referencias visuales y no se eliminan.

## Publicación

El workflow renderiza el proyecto Quarto y copia únicamente `_site/` a `gh-pages/book/`.

Esto preserva intactas las rutas históricas de los gates y las versiones standalone:

- `/lesson-1-1/`
- `/lesson-1-2/`
- `/mockup-gate-*/`

## Criterio del Hito 3

La integración se considera correcta cuando:

1. `/book/` muestra un índice navegable;
2. 1.1 y 1.2 se renderizan desde `.qmd`;
3. ambas conservan el lenguaje visual aprobado;
4. el explorador de 1.2 sigue siendo interactivo;
5. el despliegue no modifica otras rutas de `gh-pages`.

Tras este hito, el resto del Tema 1 puede desarrollarse directamente en Quarto utilizando el Design System v1, sin volver al ciclo de prototipos standalone salvo que aparezca un patrón visual nuevo.
