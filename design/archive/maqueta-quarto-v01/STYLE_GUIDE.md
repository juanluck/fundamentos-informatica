> **ARCHIVO HISTÓRICO.** Copia preservada desde la rama `maqueta-quarto-v01`. No es una especificación vigente. La dirección visual vigente está documentada en `design/DESIGN_SYSTEM_V1.md`.

# Guía visual — v0.4

## Dirección aprobada

La referencia visual del proyecto es el mockup editorial aprobado el 16/09/2026: fondo cálido, jerarquía tipográfica fuerte, ilustración con función pedagógica, color terracota como acento y diagramas integrados en la lectura.

La implementación debe parecer **un manual universitario ilustrado adaptado a web**, no documentación Quarto tematizada ni un dashboard educativo.

## Principios operativos

1. **Quarto es el motor, no la interfaz.** En la web editorial se ocultan sidebar, breadcrumbs, TOC y título automático cuando compitan con la composición.
2. **Pocas composiciones maestras.** Portada, apertura de lección, texto + figura, figura protagonista, ejercicio y cierre. No crear una clase CSS nueva para cada idea.
3. **Las ilustraciones importantes se diseñan como ilustraciones.** HTML/CSS se reserva para texto, navegación, ejercicios e interacciones pequeñas.
4. **Los diagramas técnicos deben explicar relaciones.** Evitar cajas decorativas cuyo contenido podría ser simplemente texto.
5. **El color tiene función.** Terracota = énfasis/recorrido principal; azul verdoso = contraste técnico; gris cálido = estructura secundaria.
6. **Aire editorial.** Bordes, fondos y radios se usan con mucha moderación. La separación primaria procede de espacio, tipografía y reglas finas.
7. **Una sola jerarquía.** No duplicar el título de Quarto y el título editorial.
8. **Primero escritorio, después móvil, ambos obligatorios.** El diseño debe reordenarse en móvil sin convertirse en una lista de tarjetas.

## Tipografía web

- Texto y títulos: `Source Serif 4`.
- Navegación, etiquetas y metadatos: `Inter`.
- Código: monoespaciada del sistema.

Se cargan como fuentes web; el PDF tendrá su propia decisión tipográfica.

## Paleta

- Papel: `#FFFAF2`
- Tinta: `#182F3F`
- Cuerpo: `#363A37`
- Terracota: `#B75332`
- Azul verdoso: `#3D7073`
- Línea: `#D8C9B8`

## Criterio de aceptación

Una página no se considera terminada porque Quarto renderice. Debe comprobarse el HTML publicado y responder sí a estas preguntas:

- ¿Se reconoce la familia del mockup aprobado?
- ¿Quarto resulta visualmente secundario?
- ¿La figura principal aporta comprensión real?
- ¿Hay una jerarquía clara sin proliferación de cajas?
- ¿El texto puede estudiarse cómodamente?
- ¿La página sigue funcionando en móvil?
