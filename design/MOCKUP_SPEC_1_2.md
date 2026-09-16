# Especificación medible del mockup — Lección 1.2

Estado: **Fase 1 / Puerta A**. Esta especificación describe la geometría del mockup aprobado antes de introducir color, ilustración final, interactividad o Quarto.

## Referencia

Se toma como referencia exclusivamente la página central del mockup aprobado: **«LECCIÓN 1.2 · ¿Cómo representa la información?»**.

La referencia recortada mide aproximadamente **436 × 1199 px**. Las medidas siguientes se expresan como proporciones del ancho/alto de esa página para que sean trasladables a web.

## 1. Retícula

- Página: una única columna editorial estrecha, sin sidebar, breadcrumbs ni navegación lateral.
- Ancho útil de contenido: aproximadamente **88 %** de la página.
- Margen izquierdo visible: aproximadamente **8 %**.
- Margen derecho visible: aproximadamente **4–5 %**.
- Cabecera superior: una línea con dos referencias pequeñas, izquierda y derecha.
- No existe una cuadrícula de tarjetas general. Los bloques especiales aparecen solo cuando el contenido lo exige.

## 2. Jerarquía vertical observada

Tomando el alto de referencia como 100 %:

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
| Regla 2^n | 65 % | 68 % |
| Sección 3: título + texto | 70 % | 75 % |
| Explorador | 76 % | 85 % |
| Sección 4: título + texto | 87 % | 92 % |
| Fórmula inversa + nota | 93 % | 97 % |
| Pie | 98 % | 100 % |

## 3. Tipografía — especificación funcional, no selección final

El mockup utiliza un lenguaje serif editorial prácticamente continuo. En esta fase no se selecciona todavía la familia definitiva.

Funciones observadas:

1. **Cabecera secundaria**: serif pequeña, regular.
2. **Kicker**: serif o display serif, mayúsculas, peso medio/alto, tracking ligero.
3. **Título principal**: serif de alto contraste, muy pesado, dos líneas, interlineado muy compacto.
4. **Pregunta/deck**: serif regular, sensiblemente menor que el título.
5. **Títulos de sección**: serif negrita.
6. **Cuerpo**: serif regular, compacto.
7. **Etiquetas dentro de gráficos**: pueden ser sans o serif, pero se consideran parte de la figura, no de la tipografía editorial base.

### Regla de control

Durante Puerta A se usa **una única serif neutral** para comprobar proporciones. No se incorporará una segunda familia hasta la Fase 4 del protocolo.

## 4. Escala tipográfica relativa

Tomando el cuerpo como `1`:

- Cabecera superior: `0.72`
- Kicker: `0.95`
- Título principal: `2.7–3.0`
- Deck: `1.15`
- Título de sección: `1.25–1.35`
- Cuerpo: `1`
- Pie: `0.68`

El título debe dominar la página sin convertir la cabecera en un hero web de pantalla completa.

## 5. Patrones de composición visibles

El mockup de 1.2 utiliza solo estos patrones:

1. **Cabecera editorial mínima**.
2. **Título + pregunta**.
3. **Sección textual corta**.
4. **Texto + figura protagonista en una misma banda vertical**.
5. **Tres comparaciones alineadas** (1, 2, 3 bits).
6. **Regla/formalización a ancho completo**.
7. **Interacción en dos columnas**: control/patrones a la izquierda; resultado a la derecha.
8. **Fórmula final + anotación lateral**.
9. **Pie de página mínimo**.

No aparecen tarjetas genéricas repetidas, navegación lateral ni grandes contenedores UI.

## 6. Figuras — función y tratamiento en Puerta A

### Dos estados
- Función: visualizar que dos estados físicos distinguibles bastan como base de representación.
- Mockup: dos estados alineados + anotación editorial a la derecha.
- Puerta A: usar **placeholders geométricos en gris** con la misma ocupación espacial.

### 1 / 2 / 3 bits
- Función: hacer visible el crecimiento `2 → 4 → 8` antes de formalizar `2^n`.
- Mockup: tres columnas de anchura similar y fondo tenue.
- Puerta A: conservar exactamente la disposición en tres columnas, sin color.

### Explorador
- Función: probar combinaciones y enfatizar el total.
- Mockup: panel de control/patrones a la izquierda y total grande a la derecha.
- Puerta A: **estático**. Sin JavaScript.

### Fórmula inversa
- Función: pasar de «n bits → patrones» a «N elementos → bits necesarios».
- Mockup: fórmula centrada en una banda y anotación corta a la derecha.
- Puerta A: mantener composición, sin manuscrita final.

## 7. Espaciado

- Separación título → deck: pequeña.
- Separación deck → regla: media.
- Regla → primera sección: media.
- Secciones: separadas por aire, no por contenedores.
- Visuales: integrados en el flujo, no flotantes ni dentro de cards generales.
- El ritmo es **denso pero respirable**: no hay grandes zonas vacías de hero web.

## 8. Prohibiciones durante Puerta A

- Color.
- Sombras.
- Gradientes.
- `border-radius` decorativo.
- Fuentes externas.
- JavaScript.
- Quarto.
- Sidebar.
- Breadcrumbs.
- Iconos decorativos.
- Ilustraciones finales.
- Post-its reales o caligrafía manuscrita.
- Nuevos patrones no presentes en el mockup.

## 9. Criterio de la Puerta A

La reconstrucción solo avanza si, vista en escala de grises y sin ilustraciones terminadas:

- mantiene la misma jerarquía;
- mantiene una densidad comparable;
- mantiene el mismo orden y peso relativo de bloques;
- la relación texto/visual recuerda inmediatamente a la referencia;
- no parece una landing page ni documentación técnica;
- no necesita color para que se entienda la composición.

Hasta que esta puerta se apruebe, **no se seleccionan fuentes definitivas, no se colorea, no se dibujan figuras finales y no se introduce interactividad**.
