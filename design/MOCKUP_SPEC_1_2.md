# Especificación medible del mockup — Lección 1.2

Estado: **prototipo completo listo para revisión global (Hito 1)**.

La referencia visual autoritativa es la página central del mockup aprobado: **«LECCIÓN 1.2 · ¿Cómo representa la información?»**, de aproximadamente **436 × 1199 px**. Los documentos `GATE_*` conservan el historial detallado de cada etapa.

## Retícula final aprobada

- Una única columna editorial, sin sidebar, breadcrumbs ni chrome de Quarto.
- Escritorio: `width: min(92vw, 720px)`.
- Tablet/portátil: máximo 720 px con margen exterior reducido.
- Móvil ≤ 620 px: ancho 100 %, sin sombra exterior.
- Margen izquierdo visualmente mayor que el derecho, reproduciendo la composición editorial del mockup.
- No existe una cuadrícula global de cards: los contenedores aparecen únicamente cuando son parte de una figura.

## Jerarquía vertical de referencia

| Elemento | Inicio aprox. | Fin aprox. |
|---|---:|---:|
| Cabecera de página | 1 % | 2 % |
| Kicker «LECCIÓN 1.2» | 5 % | 6 % |
| Título | 7 % | 13 % |
| Pregunta introductoria | 14 % | 19 % |
| Regla corta | 21 % | 22 % |
| Sección 1: título + texto | 23 % | 30 % |
| Visual de dos estados | 31 % | 46 % |
| Sección 2: título + texto | 49 % | 54 % |
| Visual 1/2/3 bits | 56 % | 64 % |
| Regla `2^n` | 65 % | 68 % |
| Sección 3: título + texto | 70 % | 75 % |
| Explorador | 76 % | 85 % |
| Sección 4: título + texto | 87 % | 92 % |
| Fórmula inversa + nota | 93 % | 97 % |
| Pie | 98 % | 100 % |

## Tipografía aprobada

- **Source Serif 4**: tipografía editorial base para cabecera, título, cuerpo, etiquetas y matemáticas.
- **Caveat**: reservada exclusivamente para las dos anotaciones manuscritas.
- No se añaden más familias.

Jerarquía relativa, tomando el cuerpo como `1`:

- cabecera `0.72`;
- kicker `0.95`;
- título `2.7–3.0`;
- deck `1.15`;
- título de sección `1.25–1.35`;
- cuerpo `1`;
- pie `0.68`.

## Paleta aprobada

- papel crema: `#FBF7EF`;
- tinta azul-negruzca: `#132A3A`;
- terracota principal: `#C45432`;
- terracota de texto accesible: `#A9452A`;
- melocotón pálido: `#F4E5D5`;
- ámbar de estado encendido: `#E3A23E`.

La variante oscura del terracota se usa solo en texto pequeño para mejorar contraste; no introduce una función cromática nueva.

## Patrones presentes

1. Cabecera editorial mínima.
2. Título + pregunta.
3. Sección textual corta.
4. Dos estados + anotación lateral.
5. Comparación 1/2/3 bits.
6. Regla/formalización `2^n`.
7. Explorador en dos masas: control/patrones + total.
8. Fórmula inversa + anotación manuscrita.
9. Pie mínimo.

No se admiten patrones nuevos sin justificación pedagógica o aprobación explícita.

## Figuras aprobadas

### Dos estados
Interruptor y bombilla redibujados en SVG; apagado y encendido deben resultar distinguibles sin depender únicamente del color.

### 1 / 2 / 3 bits
Tres comparaciones alineadas que hacen visible `2 → 4 → 8` antes de la regla `2^n`.

### Explorador
Estado inicial de 3 bits, como en el mockup. Interactividad limitada a 1–4 bits para poder mostrar todas las combinaciones sin romper la composición editorial.

### Fórmula inversa
`n = ⌈log₂ N⌉` en banda melocotón con anotación manuscrita lateral.

## Responsive de control

Las anchuras de referencia son:

- **1440 px**: lienzo centrado de 720 px;
- **1024 px**: misma escala editorial;
- **390 px**: flujo móvil; figuras complejas pasan a una columna y los dos estados permanecen en paralelo.

## Reglas de implementación

- El prototipo final es HTML/CSS/JS independiente.
- El CSS final no importa estilos de gates anteriores.
- El control interactivo es un `input[type=range]` nativo y operable por teclado.
- Las actualizaciones dinámicas se anuncian mediante un `output` con `aria-live="polite"`.
- Se respeta `prefers-reduced-motion`.
- Quarto permanece fuera hasta la aprobación global de la lección.

## Próximo gate humano

No se solicitan más validaciones de componentes. La siguiente validación es únicamente **la lección 1.2 completa**. Tras aprobarla se extraerá el **Design System v1** y se aplicará a la lección 1.1 antes de integrar Quarto.
