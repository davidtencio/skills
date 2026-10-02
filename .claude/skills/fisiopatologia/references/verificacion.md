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
- [ ] Las cifras (puntos de corte, porcentajes, umbrales de TFGe…) coinciden literalmente con la fuente citada.
- [ ] `scripts/verificar_evidencias.py <carpeta> --en-linea` termina sin errores: cada cifra de las láminas está en `evidencias.json` con la frase de su fuente.
- [ ] Las recomendaciones de tratamiento dicen de qué guía o consenso salen y de qué año; si la guía vigente no se pudo leer, consta en «No verificado».
- [ ] Las gráficas sin datos llevan el rótulo «Esquema cualitativo».
- [ ] Los rótulos de honestidad están presentes (esquema, sin escala).
- [ ] El error frecuente es correcto y útil en la práctica clínica.
- [ ] En una infección: el tratamiento empírico dice de qué guía y país sale, y si depende de la resistencia local; los puntos de corte llevan su versión (EUCAST o CLSI); el mecanismo de los antimicrobianos sale de la sección 12.4 de la FDA o de la 5.1 de CIMA.
- [ ] En una infección tratada con antibacterianos o antifúngicos: hay lámina de FC/FD; el índice de cada familia y sus objetivos salen de una fuente citada; la curva lleva «Esquema cualitativo».
- [ ] En una infección: la tabla de diagnóstico dice qué detecta cada prueba y cuándo se positiviza.
- [ ] El glosario explica todas las siglas de las láminas y del material (`scripts/glosario.py` sin pendientes).

## Licencias
- [ ] El pie de cada lámina cita todas las fuentes que usa, con el crédito de cada biblioteca de ilustraciones (`recursos.atribucion`).
- [ ] Las piezas nuevas están en `assets/ilustraciones/registro.json`.
- [ ] No hay material CC BY-SA sin haberlo avisado.
