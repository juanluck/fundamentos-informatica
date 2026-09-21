> **ARCHIVO HISTÓRICO.** Copia preservada desde la rama `maqueta-quarto-v01`. No es una especificación vigente. La guía activa de diseño está en `design/DESIGN_SYSTEM_V1.md` y documentos relacionados.

# Guía pedagógica — v0.3

Este documento define los principios pedagógicos que deben guiar la transformación del material docente en el libro **Fundamentos de Informática**. No prescribe una estructura rígida para todos los capítulos; funciona como contrato de diseño del aprendizaje.

## 1. El material fuente es materia prima, no la estructura final

Las diapositivas, vídeos, ejercicios, planificaciones y otros materiales existentes constituyen el **corpus fuente**. Deben leerse con trazabilidad, pero su organización original no tiene por qué trasladarse al libro.

- No convertir diapositivas en HTML de forma mecánica.
- No asumir que una versión sustituye a otra salvo decisión explícita.
- No eliminar contenido por defecto durante la reconstrucción.
- Las notas de planificación aportan contexto, no decisiones editoriales automáticas.
- Los recursos visuales pueden conservarse, redibujarse o sustituirse si así se preserva mejor su función pedagógica.

## 2. Antes de redactar, auditar el lenguaje visual de la fuente

Cuando una lección provenga de diapositivas o de otro material visual, **no basta con extraer su texto**. Antes de reescribirla se debe identificar: qué imágenes contienen información; qué diagramas construyen relaciones; qué secuencias o animaciones revelan un concepto por etapas; qué comparaciones se apoyan en la disposición espacial; y qué elementos son meramente decorativos.

Para cada recurso se decidirá explícitamente entre reutilizarlo, redibujarlo, convertirlo en secuencia web, reemplazarlo por una visualización más clara o no trasladarlo si no cumple función pedagógica.

## 3. Cada capítulo debe construir un modelo mental

Un capítulo no debe percibirse como una lista de definiciones. Debe responder a una pregunta general y desarrollar una narrativa acumulativa. Cada sección debe apoyarse en ideas ya introducidas y recuperar conceptos anteriores cuando una conexión ayude a comprender una idea nueva.

## 4. Formular preguntas antes de ofrecer respuestas

Siempre que sea natural, iniciar una sección con una pregunta que el estudiante pueda comprender antes de conocer el término técnico. Preferir «Tenemos muchas posiciones de memoria. ¿Cómo indicamos cuál queremos leer?» antes que «Un bus de direcciones es…».

## 5. Necesidad antes que terminología

**No introducir un término técnico antes de que el estudiante tenga una razón para necesitarlo.**

```text
problema → intuición → mecanismo → nombre formal → formalización
```

## 6. De la intuición a la formalización

```text
PREGUNTA → INTUICIÓN → VISUALIZACIÓN → CONCEPTO → FORMALIZACIÓN → EJEMPLO → PRÁCTICA → CONEXIÓN
```

No es una plantilla obligatoria, sino una gramática pedagógica. Antes de presentar $2^n$, mostrar combinaciones con 1, 2 y 3 bits; antes de $\log_2$, plantear la pregunta inversa.

## 7. Formalizar solo cuando la fórmula tenga significado

Siempre que sea posible: caso concreto → patrón observable → expresión general → interpretación → ejercicio inmediato.

## 8. El aprendizaje es acumulativo y espiral

Las ideas importantes deben reaparecer. $2^n$ puede introducirse para contar códigos binarios y recuperarse después para contar direcciones de memoria. La conexión debe hacerse explícita.

## 9. Ejercicios junto al concepto

Evitar separar rígidamente «teoría» y «ejercicios». Ritmo recomendado: `concepto → ejemplo → ejercicio → nuevo concepto`.

- `● Básico`: aplica una idea recién aprendida.
- `●● Intermedio`: relaciona varias ideas o exige varios pasos.
- `●●● Avanzado`: integra conceptos y exige seleccionar procedimiento.

## 10. Soluciones progresivas y no invasivas

En HTML, las soluciones permanecen ocultas por defecto. En PDF deben mantenerse accesibles de forma estática.

## 11. La web no es un PDF en HTML

La web debe aprovechar soluciones desplegables, diagramas escalables, controles interactivos pequeños, vídeo integrado, navegación, código copiable y secuencias visuales progresivas. La interactividad no se usa como decoración.

## 12. Componentes semánticos y layouts son cosas distintas

`Concepto clave`, `Importante`, `Ejemplo` o `Ejercicio` describen **la función pedagógica**. Los layouts describen **cómo se compone la página**. El libro necesita ambos niveles.

Layouts mínimos: apertura de capítulo, apertura de lección, texto + figura, figura panorámica, secuencia paso a paso, comparación, visualización interactiva, ejemplo trabajado, ejercicio y cierre.

**No construir toda la página apilando cajas semánticas.**

## 13. El recurso visual debe transportar conocimiento

Una imagen debe mostrar estructura, relación, proceso, comparación, patrón o una representación memorable. Si puede retirarse sin perder comprensión, debe cuestionarse su necesidad.

## 14. Conservar el valor de las animaciones originales

Si una diapositiva explica mediante aparición progresiva, no aplanar automáticamente la secuencia en un diagrama saturado. Convertirla cuando convenga en pasos, controles o varios estados coordinados.

## 15. Ritmo visual

En capítulos introductorios se evitará una sucesión prolongada de párrafos sin anclaje visual. No hay cuota de imágenes: el criterio es cognitivo. Cuando cambia el modelo mental, debe considerarse una representación visual.

## 16. El texto debe poder estudiarse de forma autónoma

Toda idea esencial debe quedar desarrollada sin depender de la exposición oral. Tono claro, directo y respetuoso; sin infantilizar.

## 17. Terminar reconstruyendo el conjunto

Cada capítulo debe volver a la pregunta inicial mediante una historia, proceso, mapa conceptual, resumen, problemas integradores o autoevaluación.

## 18. La publicación visual tiene una puerta de calidad

Que Quarto renderice sin errores **no significa que una página esté terminada**. Antes de extender un patrón a nuevas lecciones debe revisarse la salida publicada en navegador y compararse con la referencia editorial aprobada.

Una página no pasa esta puerta si ocurre alguno de estos casos:

- la interfaz de Quarto domina sobre el contenido;
- hay títulos o numeraciones duplicados;
- la composición se basa principalmente en tarjetas o cajas decorativas;
- las figuras son meras versiones gráficas de texto ya escrito;
- el resultado se aleja claramente de la familia visual aprobada;
- el diseño funciona en el código pero no en la salida HTML real.

## 19. Lista de comprobación

- [ ] ¿Se revisó el material visual fuente, no solo el texto?
- [ ] ¿Existe una pregunta o propósito comprensible?
- [ ] ¿Los términos técnicos aparecen después de su motivación?
- [ ] ¿Las fórmulas se construyen y se interpretan?
- [ ] ¿Los diagramas explican y no solo decoran?
- [ ] ¿La composición alterna texto y representación visual naturalmente?
- [ ] ¿Se preservó la lógica de las secuencias relevantes?
- [ ] ¿Hay práctica cercana a los conceptos importantes?
- [ ] ¿Las soluciones pueden ocultarse en web?
- [ ] ¿El texto puede estudiarse sin explicación oral?
- [ ] ¿La web aporta algo que el PDF no puede aportar?
- [ ] ¿La salida publicada se ha revisado visualmente y respeta la referencia aprobada?
