# Tema 2 — Representación de la información

Fuente: **Tema 2 - Resumen - Ejercicios-con notas.pdf**, 247 páginas,
aportado el 10 de octubre de 2026. La numeración siguiente corresponde a
las páginas del PDF con notas, no a los contadores internos de las diapositivas.

Presentación de referencia verificada en Drive:
https://docs.google.com/presentation/d/1OiidO8Az93wBqBbaKmTIn3BUm2A03WjUSUU8cCBEGhc/edit

## Correspondencia

| Fuente | Páginas | Fuente Quarto | Contenido |
|---|---:|---|---|
| Apertura y recorrido | 1–4 | Portada y aperturas | Motivación y relación con Tema 1 |
| L2.0 | 5–37 | `00-sistemas-numeracion.qmd` | Posición, bases, conversiones y aritmética |
| L2.1 | 38–49 | `01-representacion.qmd` | Interpretación, redundancia y compresión |
| L2.2 | 50–81 | `02-textos.qmd` | ASCII, familias de códigos, Unicode, UTF-8 y UTF-16 |
| L2.3 | 82–107 | `03-sonidos.qmd` | Muestreo, cuantificación, PCM, códecs, transmisión |
| L2.4 | 108–152 | `04-imagenes.qmd` | Percepción, color, píxeles/vectores, formatos y compresión |
| L2.5 | 153–169 | `05-video.qmd` | Fotogramas, GOP, dependencias, tamaño y contenedores |
| L2.6 | 170–218 | `06-enteros.qmd` | Sin signo, SM, CA1, CA2, sesgo, BCD y límites |
| L2.7 | 219–246 | `07-reales.qmd` | Normalización, binary32/64, codificación y límites |
| Cierre | 247 | Síntesis y tarjetas | El contexto determina la interpretación |

`ejercicios.qmd` reúne 24 ejercicios. Conserva los problemas de texto
(75–81), sonido (103–107), imagen (131–134, 141–143, 149–152), vídeo
(163–169), CA1/CA2 (186–189, 196–199), sesgo (206–207), suma CA2
(216–218) y reales (235–242). Añade como práctica explícita ejemplos y
cuestiones presentes en las lecciones, incluidas conversiones y desbordamiento.
`tarjetas.qmd` contiene 48 tarjetas redactadas para esta adaptación: seis por
lección; no son un CSV original del profesor.

## Adaptación editorial

- Se mantienen Design System v1, ancho de papel, paleta y tipografías.
- El contenido se escribe en Markdown: encabezados, tablas, imágenes,
  listas y matemáticas. Los fenced divs aplican el diseño compartido.
- El HTML necesario se limita a `details/summary`, el componente de tarjetas
  y la navegación existente. Los diagramas se mantienen como SVG editables.
- Las revelaciones progresivas y transiciones de las diapositivas se convierten
  en explicaciones continuas, tablas de pasos o ejercicios desplegables.
- Se incorporan las precisiones de las notas: UTF-16 variable, exclusión de
  sustitutos en UTF-8, Y′ frente a luminancia, límites de Nyquist, pérdida en
  submuestreo, tamaño de paletas y diferencias entre acarreo y desbordamiento.
- La hipótesis B = 0 bytes se identifica como modelo didáctico, no como
  descripción general de los códecs. Se evita repetir afirmaciones absolutas
  sobre BMP/TIFF, visibilidad de pérdidas o tamaños de los tipos de C.
- Las tablas exhaustivas de variantes ISO 8859 y formatos de sonido se
  condensan conservando las familias y su función; el PDF íntegro acompaña
  al libro. Las cifras históricas de Photoshop se etiquetan como mediciones.
- Las animaciones RGB sucesivas se condensan en la explicación de integración
  espacial y modelos de color. No se incorporan vídeos externos no disponibles
  como archivo. Los dos laboratorios existentes se enlazan. En JPEG se sustituye únicamente
  un marcador de estado JSON no válido por un objeto vacío para corregir
  un error de inicialización; el contenido docente permanece igual.
- La escena de The Martian se resume como motivación sin reproducir su cita
  extensa ni incorporar contenido audiovisual externo.

## Figuras y procedencia

Los PNG se extraen de los objetos de imagen del PDF, sin rasterizar diapositivas
enteras ni sus notas. Se reutilizan como material docente aportado; no se
atribuye una licencia nueva a recursos cuya autoría original no figura.

| Archivo en `assets/figures/tema2/` | Procedencia |
|---|---|
| `monet-conjunto.png`, `monet-detalle.png` | Página 111, Monet, *Las amapolas* (1873) |
| `cie-cromaticidad.png` | Página 114, diagrama CIE del material |
| `componentes-ycbcr.png` | Página 116, descomposición del recurso original |
| `cisne.png`, `cisne-pixeles.png` | Página 126, fotografía y ampliación del original |
| `muybridge-secuencia.png` | Página 155, E. Muybridge (1878), obra en dominio público |
| `muestreo.svg` | Redibujo didáctico basado en las páginas 87–91; señal ilustrativa |
| `submuestreo.svg` | Redibujo del recuento de la página 139 |
| `gop.svg` | Dependencias I1/P3/B2 de las páginas 158–159 |
| `ieee754.svg` | Campos del ejemplo 53,25 de la página 225 |

## Recursos y navegación

- PDF local: `assets/media/tema2/tema2-resumen-ejercicios-con-notas.pdf`.
- Interactivos existentes: `assets/interactivos/nyquist-shannon.html` y
  `assets/interactivos/jpeg-paso-a-paso.html`.
- Se añaden once páginas a `_quarto.yml`, al índice y al menú editorial.
- La lectura secuencial enlaza ejercicios de Tema 1 → 2.0 → … → 2.7 →
  ejercicios de Tema 2 → prácticas. Tarjetas y recursos son complementarios,
  igual que en Tema 1.
- Los estilos nuevos se limitan a `.tema2-sheet`; no se rediseña Tema 1.

Las fórmulas se publican como MathML nativo mediante metadatos limitados
al Tema 2, conservando LaTeX editable en las fuentes Quarto.
