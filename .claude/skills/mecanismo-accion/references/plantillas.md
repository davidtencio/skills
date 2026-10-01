# Plantillas por clase de mecanismo

Todas las series mantienen el mismo arco (contexto → fisiología → fármaco → paciente). Lo que cambia es la escena de las láminas centrales y cuántas hacen falta: L1–L4 indican el papel de cada parte del arco, no un número fijo. Añade láminas cuando una parte no quepa con una idea por lámina (p. ej., L2a y L2b para dos vías fisiológicas, o una lámina de resistencia después de L3).

## Lámina de indicaciones aprobadas (opcional, al final)
Ejemplo: `ejemplos/trastuzumab-deruxtecan/lamina-5.png`. Úsala cuando haya indicaciones nuevas de la FDA en los últimos 3 años o diferencias con la UE.
- Línea de tiempo horizontal con cada aprobación de la FDA: mes y año, indicación en tres líneas y etiqueta «UE: sí» o «UE: aún no» según CIMA 4.1.
- Debajo, dos tarjetas: «Lo último (FDA)» y «Cómo leer esta lámina». La segunda explica que la FDA y la EMA aprueban por separado y que en Costa Rica rige el registro sanitario nacional.

## Lámina de farmacocinética (opcional, entre el mecanismo y el paciente)
Ejemplo: `ejemplos/atorvastatina/lamina-4.png`. Úsala cuando la farmacocinética explique algo del efecto o de la seguridad.
- Escena: recorrido de una dosis con pasos numerados (absorción → órgano de primer paso → célula donde actúa o se metaboliza → eliminación), con los transportadores y enzimas que importan y las cifras de la ficha (biodisponibilidad, unión a proteínas, semivida, vía de eliminación).
- Tarjetas inferiores: interacciones explicadas por esas enzimas y transportadores, farmacogenética (si CPIC da nivel A/B) y un «dato clave» que conecte la farmacocinética con el efecto.
- Potencia y selectividad (ChEMBL/BindingDB) van en la lámina del mecanismo, como datos in vitro.

## Receptor nuclear (andrógenos, glucocorticoides, estrógenos, tiroideas, PPAR)
Ejemplo completo: `ejemplos/darolutamida/`.
- L1: eje hormonal (hipotálamo → hipófisis → glándula → sangre → célula diana) y sitios de acción de cada grupo de fármacos.
- L2: hormona lipofílica atraviesa la membrana → (enzima activadora) → unión al receptor con chaperonas → dímero → poro nuclear → elemento de respuesta en el ADN → coactivadores y ARN pol II → ARNm → proteínas.
- L3: sitio de unión con estructura real (PDB) + puntos de bloqueo en la célula.

## Receptor de membrana acoplado a proteína G (betabloqueadores, opioides, antihistamínicos)
- L1: origen del ligando (neurona, glándula) y órganos donde actúa.
- L2: ligando → receptor de 7 hélices en la membrana → proteína G → segundo mensajero (AMPc, IP3/Ca²⁺) → respuesta celular.
- L3: antagonista/agonista en el sitio ortostérico; consecuencias en la cascada.
- Ilustraciones: `Receptors-channels` de Servier (receptores de 7 hélices, membranas).

## Enzima (estatinas, IECA, IBP, inhibidores de COX, de la xantina oxidasa)
- L1: vía metabólica en el órgano (p. ej., síntesis de colesterol en el hepatocito).
- L2: sustrato → enzima → producto → efecto fisiológico.
- L3: el fármaco en el sitio activo (estructura real si existe complejo en PDB), producto disminuido, mecanismos compensatorios (p. ej., más receptores de LDL).

## Canal iónico (anestésicos locales, bloqueadores de calcio, antiarrítmicos)
- L2: potencial de membrana, apertura del canal, flujo de iones.
- L3: bloqueo del poro o modulación del estado del canal; efecto sobre la excitabilidad.

## Transportador (ISRS, inhibidores de SGLT2, diuréticos)
- L2: transporte normal (dirección, iones acoplados, ubicación en la célula/epitelio).
- L3: transportador bloqueado; acumulación o pérdida de la sustancia y su consecuencia clínica.

## Conjugado anticuerpo-fármaco (ADC: trastuzumab deruxtecán, trastuzumab emtansina, sacituzumab govitecán)
Ejemplo: `ejemplos/trastuzumab-deruxtecan/`.
- L1: la diana en la superficie tumoral y los fármacos que actúan sobre ella (anticuerpos, ADC, inhibidores de tirosina cinasa).
- L2: función normal de la diana (señalización) y del blanco intracelular de la carga útil (p. ej., topoisomerasa I).
- L3: estructura del ADC (anticuerpo + enlazador + carga útil, con el número de moléculas por anticuerpo); unión al antígeno → internalización → lisosoma → liberación de la carga → daño al blanco → apoptosis; efecto espectador si la carga atraviesa membranas.
- L4: efecto, error frecuente (confusión con el anticuerpo solo), farmacocinética del conjugado y de la carga, toxicidades características.

Si el fármaco no encaja en ninguna, combina elementos y explica la elección en la ficha del mecanismo.
