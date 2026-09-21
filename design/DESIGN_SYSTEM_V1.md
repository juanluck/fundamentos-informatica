# Design System v1 — Fundamentos de Informática

Estado: **derivado de la Lección 1.2 aprobada**.

Esta versión convierte las decisiones visuales ya aceptadas en reglas reutilizables. No redefine el estilo: lo documenta para poder aplicarlo al resto del libro.

## 1. Principio rector

El resultado debe sentirse como **un libro ilustrado adaptado a la web**, no como una web de documentación decorada.

Regla de control: antes de introducir un recurso visual, preguntar si cumple una función editorial o pedagógica concreta. Si solo añade apariencia de interfaz, se elimina.

## 2. Lienzo y retícula

- Fondo exterior: gris cálido `#E9E4DB`.
- Papel: crema `#FBF7EF`.
- Ancho en escritorio: `min(92vw, 720px)`.
- Entre 621 y 1024 px: `min(94vw, 720px)`.
- Hasta 620 px: `100%`, sin marco exterior.
- Padding escritorio: `22px 32px 16px 62px`.
- En móvil: aproximadamente `18px` laterales.
- Una sola columna editorial principal.
- Sin sidebar, breadcrumbs ni chrome de framework.

## 3. Tipografía

Familias permitidas:

1. **Source Serif 4**: toda la voz editorial, títulos, cuerpo, cifras, fórmulas y etiquetas ordinarias.
2. **Caveat**: solo anotaciones manuscritas puntuales.

Roles de referencia:

- Cabecera de página: 11 px, regular.
- Kicker: 15 px, 700, mayúsculas, tracking ligero.
- Título principal: 56 px, 800, `line-height: .91`, tracking negativo.
- Entradilla: 20 px, regular.
- Título de sección: 22 px, 700.
- Cuerpo: 16.5 px, `line-height: 1.24`.
- Pie: 10.5 px.
- Nota manuscrita: 22–24 px.

En móvil se reduce el título mediante `clamp`, no se cambia la familia ni la jerarquía.

## 4. Paleta funcional

- `--paper: #FBF7EF` — papel.
- `--ink: #132A3A` — tinta principal azul-negruzca.
- `--accent: #C45432` — terracota para líneas, masas y énfasis gráficos.
- `--accent-text: #A9452A` — terracota más oscuro para texto pequeño con mejor contraste.
- `--soft: #F4E5D5` — melocotón pálido para bandas y fondos pedagógicos.
- `--amber: #E3A23E` — reservado a estados de activación/encendido cuando tenga significado.
- `--line: #D7CABB` — líneas editoriales y bordes discretos.

El color no se usa para decorar arbitrariamente. Debe codificar jerarquía, relación o estado.

## 5. Ritmo vertical

Escala práctica derivada de la 1.2:

- 7–10 px: separación interna corta.
- 12–18 px: separación entre etiqueta y contenido visual.
- 22–30 px: separación entre bloques de una sección.
- 36–50 px: respiración de apertura/cabecera.

Las secciones se separan con espacio, no con contenedores genéricos.

## 6. Patrones editoriales aprobados

### Cabecera mínima
Dos referencias pequeñas, una a cada lado.

### Apertura de lección
Kicker → título grande → pregunta/entradilla → regla terracota corta.

### Sección textual
Título numerado + párrafo breve. La explicación debe preceder a la formalización.

### Figura integrada
La figura entra en el flujo de lectura. Puede usar fondo `--soft` cuando ayude a agrupar, pero no se convierte automáticamente en una tarjeta.

### Comparación en columnas
Usada cuando existen entidades comparables y la comparación es el mensaje.

### Banda de formalización
Fondo `--soft`, borde discreto y fórmula/regla en una sola masa horizontal.

### Anotación editorial
Caveat, ligera rotación en escritorio, sin apariencia de post-it genérico.

### Resultado protagonista
Una cifra o expresión puede adquirir escala grande cuando sea el resultado conceptual principal.

### Pie mínimo
Línea superior fina, nombre del libro y número de página.

## 7. Figuras

Prioridad obligatoria:

1. recurso docente original reutilizable;
2. redibujo fiel del recurso original;
3. figura nueva basada explícitamente en el recurso original;
4. figura completamente nueva solo cuando el material fuente no resuelve la necesidad.

Preferir SVG nativo para diagramas conceptuales. Mantenerlos editables, nítidos y semánticos.

No usar iconos decorativos, ilustraciones genéricas de stock ni infografías educativas sin correspondencia con el material.

## 8. Interactividad

La interactividad aparece solo cuando permite comprender algo que una figura estática explica peor.

Reglas:

- HTML nativo antes que widgets complejos.
- Estado inicial coherente con la figura de referencia.
- Operable por teclado.
- Foco visible.
- Actualizaciones relevantes anunciadas a lectores de pantalla.
- Respetar `prefers-reduced-motion`.
- No añadir botones, menús o animaciones que no tengan función pedagógica.

## 9. Responsive

Puntos de control obligatorios:

- 1440 px: referencia editorial principal.
- 1024 px: mantener composición de escritorio siempre que no comprima la lectura.
- 390 px: una columna, figuras reordenadas sin perder relaciones.

Breakpoints base:

- `<= 1024px` ajustes suaves de lienzo.
- `<= 620px` composición móvil.
- `<= 440px` correcciones para móviles estrechos.

## 10. Semántica y estilo

La estructura HTML describe significado, no apariencia. Roles previstos:

- apertura de lección;
- sección;
- figura;
- comparación;
- concepto/regla;
- anotación;
- ejercicio;
- solución;
- recurso/vídeo.

Un nuevo rol semántico puede reutilizar un patrón visual existente. No debe inventarse un patrón visual nuevo si uno aprobado ya sirve.

## 11. Regla de escalado

La 1.2 es la referencia canónica. Las nuevas lecciones pueden variar en contenido y figuras, pero no deben alterar sin necesidad:

- ancho del papel;
- familias tipográficas;
- paleta;
- jerarquía de apertura;
- ritmo editorial;
- lenguaje de figuras;
- comportamiento responsive.

Si una lección exige una solución nueva, se documenta primero la necesidad y se comprueba si puede resolverse reutilizando uno de los patrones anteriores.

## 12. Quarto

Quarto sigue fuera de esta fase. Primero se demuestra que el sistema funciona en al menos dos lecciones independientes. Después se integra en Quarto haciendo que Quarto obedezca al diseño, nunca al revés.
