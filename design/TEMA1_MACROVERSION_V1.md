# Tema 1 — Macroversión Quarto v1

Estado: **1.1–1.7 implementadas en Quarto sobre Design System v1**.

## Secuencia narrativa

1. **1.1 ¿Qué es un computador?** — informática, entrada/proceso/salida, programa almacenado.
2. **1.2 ¿Cómo representa la información?** — dos estados, bits, combinaciones y número de bits necesarios.
3. **1.3 ¿Qué hay dentro de un computador?** — CPU, CU, ALU, registros, palabra, memoria y mapa funcional.
4. **1.4 ¿Cómo se comunican sus componentes?** — bus de datos, bus de direcciones, direccionamiento y ejercicio de 32 Mbytes/32 bits.
5. **1.5 ¿Cómo ejecuta un programa?** — ciclo CPU-memoria, reloj, CPI, tiempo de ejecución, MIPS y MFLOPS.
6. **1.6 ¿Todos los computadores son iguales?** — clasificación por paralelismo, generalidad de uso y potencia de procesamiento.
7. **1.7 ¿Qué papel juega el software?** — instrucciones, programas, traducción, ejecución y software de ingeniería.

## Trazabilidad respecto al material de origen

La reorganización no elimina material del corpus. Redistribuye los bloques originales de Tema 1 para construir una progresión más gradual.

| Fuente original | Uso en la nueva estructura |
|---|---|
| L1.1 Definiciones básicas | 1.1 y 1.2 |
| Potencias de 2, bits, codificación y logaritmos | 1.2 y ejercicios posteriores |
| Problema “100 Megas / 1 GByte” | permanece en el corpus de ejercicios; no se considera descartado |
| L1.2 Unidades funcionales: CPU, CU, ALU, registros, memoria | 1.3 |
| Bus de datos y bus de direcciones | 1.4 |
| Revelación progresiva CPU ↔ memoria, reloj y prestaciones | 1.5 |
| L1.3 Tipos de computadores | 1.6 |
| L1.4 Software de un computador | 1.7 |
| L1.5 Herramientas software en ingeniería | 1.7 |
| Ejercicios de buses, tiempo de ejecución y prestaciones | integrados cuando ayudan a formalizar el concepto y conservados como corpus de ejercicios |

## Decisiones de adaptación

- Las figuras se redibujan con el lenguaje editorial aprobado en 1.2 en lugar de reutilizar capturas de las diapositivas.
- La secuencia animada CPU-memoria de las diapositivas se transforma en una secuencia explícita de pasos en 1.5, manteniendo su función pedagógica progresiva.
- La clasificación por potencia conserva las categorías de la fuente, pero la página principal no liga esas categorías a las cifras de precio de la tabla original.
- L1.4 y L1.5 originales se reúnen en 1.7 porque ambos responden a la pregunta narrativa sobre el papel del software; siguen diferenciados internamente como software/programas y aplicaciones/herramientas de ingeniería.

## Regla de continuidad

A partir de esta macroversión, las modificaciones del Tema 1 deben realizarse directamente sobre las fuentes `.qmd` y los estilos compartidos. Solo se vuelve a un prototipo aislado si aparece un patrón visual realmente nuevo.
