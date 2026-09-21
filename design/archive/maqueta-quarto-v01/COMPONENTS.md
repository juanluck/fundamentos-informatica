> **ARCHIVO HISTÓRICO.** Copia preservada desde la rama `maqueta-quarto-v01`. No es una especificación vigente. La autoría y componentes actuales se rigen por las fuentes vigentes de `design/`.

# Componentes editoriales — v0.1

Este documento define el vocabulario semántico disponible en los capítulos. La lista puede evolucionar, pero no deben crearse componentes nuevos ad hoc dentro de un capítulo.

## Principios

1. El contenido se escribe de forma semántica; la apariencia pertenece a la capa de estilos.
2. Un mismo tipo de contenido usa siempre el mismo componente.
3. La web es el formato prioritario.
4. El PDF debe conservar significado y legibilidad aunque pierda interacción.
5. Las soluciones de ejercicios y tareas permanecen ocultas por defecto en HTML y visibles en PDF.
6. La dificultad usa tres niveles: 1 Básico, 2 Intermedio, 3 Avanzado.

## Componentes

### Concepto clave

```markdown
::: {.concepto-clave}
Contenido.
:::
```

### Importante

```markdown
::: {.importante}
Contenido.
:::
```

### Ejemplo

```markdown
::: {.ejemplo}
Contenido.
:::
```

### Para saber más

```markdown
::: {.para-saber-mas}
Contenido.
:::
```

### Ejercicio

```markdown
::: {.ejercicio titulo="Título" numero="2.4" dificultad="2"}
Enunciado.

::: {.solucion}
Resolución.
:::
:::
```

### Tarea

```markdown
::: {.tarea titulo="Título" numero="3.1" dificultad="3"}
Enunciado.

::: {.solucion}
Resolución, orientación o resultado esperado.
:::
:::
```

### Autoevaluación

```markdown
::: {.autoevaluacion}
Preguntas.
:::
```

### Vídeo

```markdown
::: {.video}
Título, duración, descripción y enlace.
:::
```

### Recurso externo

```markdown
::: {.recurso}
Descripción y enlace.
:::
```

### Objetivos

```markdown
::: {.objetivos}
Lista de objetivos.
:::
```

### Resumen

```markdown
::: {.resumen}
Síntesis.
:::
```

## Elementos nativos

No necesitan componente propio salvo que aparezca una necesidad real:

- encabezados y subsecciones;
- párrafos y listas;
- tablas;
- matemáticas;
- bloques de código;
- figuras y diagramas;
- referencias cruzadas;
- citas y bibliografía.
