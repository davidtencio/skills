# Lista de verificación antes de entregar

Ejecuta primero `python3 scripts/revisar_lamina.py <carpeta>`: debe terminar sin errores (textos que se pisan o que se salen de la lámina o de su recuadro). Revisa sus avisos y después cada PNG con Read, y corrige hasta que todo se cumpla.

## Visual
- [ ] Ningún texto se pisa con otro texto, con flechas o con bordes de ilustraciones.
- [ ] Los elementos de dentro de la célula no quedan encima de la membrana; las etiquetas no se salen de la lámina.
- [ ] Los fondos blancos de ilustraciones extraídas no se ven como rectángulos.
- [ ] Letra de al menos 14 px en el cuerpo (el pie puede ser de 12,5 px).
- [ ] Los pasos se leen en orden y las flechas siguen ese orden.
- [ ] Hay una idea principal por lámina y el título la expresa.

## Contenido
- [ ] Cada afirmación tiene fuente; lo no confirmado está en la lista del revisor del material.
- [ ] Las estructuras químicas proceden de PubChem y su fórmula coincide.
- [ ] No se muestra una pose de unión sin estructura cristalográfica que la respalde.
- [ ] Los rótulos de honestidad están presentes (estructura real, esquema, sin escala).
- [ ] El error frecuente y la pregunta de autoevaluación son correctos y útiles para el examen.
- [ ] El glosario explica todas las siglas de las láminas y del material (`scripts/glosario.py` sin pendientes).

## Licencias
- [ ] El pie de cada lámina cita todas las fuentes que usa.
- [ ] Las piezas nuevas están en `assets/ilustraciones/registro.json`.
- [ ] No hay material CC BY-SA sin haberlo avisado.
