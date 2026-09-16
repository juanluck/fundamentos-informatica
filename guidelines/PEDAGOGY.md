# Guía pedagógica — v0.1

Este documento define los principios pedagógicos que deben guiar la transformación del material docente en el libro **Fundamentos de Informática**. No prescribe una estructura rígida para todos los capítulos; funciona como contrato de diseño del aprendizaje.

## 1. El material fuente es materia prima, no la estructura final

Las diapositivas, vídeos, ejercicios, planificaciones y otros materiales existentes constituyen el **corpus fuente**. Deben leerse y conservarse con trazabilidad, pero su organización original no tiene por qué trasladarse al libro.

- No convertir diapositivas en HTML de forma mecánica.
- No asumir que una versión sustituye a otra salvo que se haya decidido explícitamente.
- No eliminar contenido por defecto durante la fase de reconstrucción.
- Las notas de planificación sirven como contexto, no como decisiones editoriales automáticas.
- Diagramas o recursos visuales pueden regenerarse cuando ello mejore claridad, legibilidad o coherencia visual.

## 2. Cada capítulo debe construir un modelo mental

Un capítulo no debe percibirse como una lista de definiciones. Debe responder a una pregunta general y desarrollar una narrativa acumulativa.

Ejemplo del Tema 1:

> ¿Qué es realmente un computador y cómo consigue ejecutar un programa?

Cada nueva sección debe apoyarse en ideas ya introducidas y, cuando sea útil, recuperar conceptos anteriores en un contexto nuevo.

## 3. Formular preguntas antes de ofrecer respuestas

Siempre que sea natural, iniciar una sección con una pregunta que el estudiante pueda comprender antes de conocer el término técnico.

Preferir:

> Tenemos muchas posiciones de memoria. ¿Cómo indicamos cuál queremos leer?

antes que:

> Un bus de direcciones es...

Los títulos en forma de pregunta son apropiados cuando expresan con claridad el problema de aprendizaje, pero no son obligatorios si resultan artificiales.

## 4. Necesidad antes que terminología

**No introducir un término técnico antes de que el estudiante tenga una razón para necesitarlo.**

Secuencia preferente:

```text
problema → intuición → mecanismo → nombre formal → formalización
```

El vocabulario técnico debe consolidar una idea ya comprensible, no sustituir a la explicación.

## 5. De la intuición a la formalización

Cuando un concepto tenga componente matemático o formal, avanzar de forma gradual:

```text
PREGUNTA
   ↓
INTUICIÓN
   ↓
VISUALIZACIÓN
   ↓
CONCEPTO
   ↓
FORMALIZACIÓN
   ↓
EJEMPLO
   ↓
PRÁCTICA
   ↓
CONEXIÓN CON LO ANTERIOR
```

No es una plantilla obligatoria de ocho pasos, sino una gramática pedagógica.

Ejemplo: antes de presentar $2^n$, mostrar explícitamente las combinaciones disponibles con 1, 2 y 3 bits. Antes de introducir $\log_2$, plantear la pregunta inversa: cuántos bits hacen falta para representar un número dado de símbolos.

## 6. Formalizar solo cuando la fórmula tenga significado

Las fórmulas deben aparecer después de que el estudiante entienda qué magnitudes relacionan y qué pregunta responden.

Siempre que sea posible:

1. caso concreto;
2. patrón observable;
3. expresión general;
4. interpretación;
5. ejercicio inmediato.

## 7. El aprendizaje es acumulativo y espiral

Las ideas importantes deben reaparecer.

Por ejemplo, $2^n$ puede introducirse primero para contar códigos binarios y recuperarse después para contar direcciones de memoria. Esta reutilización hace explícito que una misma herramienta conceptual explica fenómenos distintos.

Cuando se recupere una idea anterior, señalar la conexión en el texto.

## 8. Ejercicios junto al concepto, no únicamente al final

Evitar una separación rígida entre «teoría» y «ejercicios».

Ritmo recomendado:

```text
concepto → ejemplo → ejercicio → nuevo concepto
```

Los problemas finales se reservan principalmente para integrar varias ideas.

### Niveles de dificultad

- `● Básico`: aplica directamente una única idea recién aprendida.
- `●● Intermedio`: exige relacionar dos o más ideas o realizar varios pasos.
- `●●● Avanzado`: integra conceptos, exige seleccionar un procedimiento o incluye mayor carga de razonamiento.

La dificultad mide demanda cognitiva, no importancia.

## 9. Soluciones progresivas y no invasivas

En HTML, la solución de ejercicios y tareas permanece oculta por defecto. El estudiante debe poder intentar la actividad antes de verla.

En PDF, las soluciones deben mantenerse accesibles de forma estática. Su ubicación concreta podrá variar según el tipo de publicación, pero nunca debe perderse la correspondencia inequívoca con el enunciado.

## 10. Web primero, no «PDF en HTML»

La web es el formato prioritario. Debe aprovechar aquello que aporte valor pedagógico:

- soluciones desplegables;
- diagramas claros y escalables;
- pequeños simuladores o controles interactivos cuando ayuden a formar intuición;
- vídeo integrado;
- navegación y referencias cruzadas;
- código copiable;
- visualizaciones progresivas.

La interactividad no debe utilizarse como decoración. Si no mejora comprensión o práctica, es preferible una representación estática simple.

## 11. Visualizar relaciones y procesos

Preferir diagramas regenerados, coherentes con la identidad del libro, frente a capturas de diapositivas cuando sea posible.

Un buen diagrama debe responder a una pregunta concreta: qué componentes existen, cómo se relacionan o qué cambia durante un proceso.

Los diagramas complejos deben construirse de lo simple a lo completo.

## 12. El texto debe poder estudiarse de forma autónoma

Las diapositivas pueden depender de la explicación oral; el libro no.

Toda idea esencial debe quedar suficientemente desarrollada para que un estudiante pueda comprenderla sin haber asistido a la exposición correspondiente.

El tono será claro, directo y respetuoso. No infantilizar. Evitar tanto la densidad enciclopédica como las simplificaciones que introduzcan conceptos incorrectos.

## 13. Diferenciar introducción de profundidad

En un curso de fundamentos es legítimo presentar un modelo simplificado si:

- ayuda a construir una intuición correcta;
- se indica su alcance cuando sea necesario;
- no contradice la explicación más detallada que aparecerá después.

Los capítulos iniciales pueden anticipar conceptos que se desarrollarán posteriormente, pero no deben duplicar innecesariamente capítulos futuros.

## 14. Terminar reconstruyendo el conjunto

Cada capítulo debe incluir, cuando sea apropiado, un cierre integrador que vuelva a la pregunta inicial.

El cierre puede incluir:

- una historia o proceso completo;
- mapa conceptual;
- resumen de ideas esenciales;
- problemas integradores;
- autoevaluación.

El objetivo es que el estudiante vea cómo las piezas forman un sistema.

## 15. Uso de componentes editoriales

Los componentes visuales definidos en `COMPONENTS.md` tienen función semántica:

- **Concepto clave**: idea fundamental que merece reconocimiento inmediato.
- **Importante**: observación que no debe pasar desapercibida.
- **Ejemplo**: aterriza una explicación en un caso concreto.
- **Para saber más**: extensión no necesaria para seguir el hilo principal.
- **Ejercicio / Tarea**: práctica activa con nivel de dificultad.
- **Autoevaluación**: comprobación al final de una unidad o bloque.
- **Resumen**: síntesis, no repetición literal del texto.

No crear nuevos tipos de caja para resolver necesidades puntuales sin discutir antes si representan una categoría pedagógica estable.

## 16. Lista de comprobación para un capítulo

Antes de considerar estable un capítulo, comprobar:

- [ ] ¿Existe una pregunta o propósito general comprensible?
- [ ] ¿Cada sección necesita razonablemente lo aprendido antes?
- [ ] ¿Los términos técnicos aparecen después de su motivación?
- [ ] ¿Las fórmulas se construyen y se interpretan?
- [ ] ¿Los diagramas explican algo y no solo decoran?
- [ ] ¿Hay práctica cercana a los conceptos importantes?
- [ ] ¿Los niveles de dificultad son coherentes?
- [ ] ¿Las soluciones pueden ocultarse en web?
- [ ] ¿Se recuperan conexiones con ideas anteriores?
- [ ] ¿El texto puede estudiarse sin explicación oral?
- [ ] ¿El cierre reconstruye el modelo mental del capítulo?
- [ ] ¿La versión web aporta algo más que una sucesión de páginas estáticas?
