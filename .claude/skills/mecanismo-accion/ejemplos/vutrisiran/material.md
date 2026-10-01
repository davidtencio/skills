# Vutrisiran: ¿cómo actúa?

> **Prototipo pendiente de revisión farmacológica.** Material educativo para estudiantes de farmacia; no sustituye la ficha técnica vigente.

Serie de ocho láminas (16:9):

1. [De la TTR al amiloide, y dónde actúa cada fármaco](lamina-1.png)
2. [La TTR: del hígado a la sangre, y de ahí al amiloide](lamina-2.png)
3. [Cómo llega vutrisiran al hepatocito](lamina-3.png)
4. [Interferencia por ARN: el ARNm de TTR se corta](lamina-4.png)
5. [Horas en el plasma, meses de efecto](lamina-5.png)
6. [Del mecanismo al paciente](lamina-6.png)
7. [Indicaciones aprobadas: de los nervios al corazón](lamina-7.png)
8. [Del ensayo a la práctica: valor y vida real](lamina-8.png)

## Puntos clave

1. **Tipo de fármaco:** ARN pequeño de interferencia (ARNpi) bicatenario, estabilizado químicamente y unido a un ligando con tres residuos de N-acetilgalactosamina (GalNAc). Código ATC N07XX18. *[CIMA, Amvuttra 5.1]*
2. **Diana:** el ARN mensajero de la transtiretina (TTR), tanto de la variante hereditaria como de la nativa. *[CIMA 5.1; FDA 12.1]*
3. **Entrada en el hígado:** la GalNAc se une al receptor de asialoglucoproteínas (ASGPR) de los hepatocitos, que internaliza el conjugado. *[NCI Thesaurus C152919; UniProt P07306]*
4. **Mecanismo:** por interferencia por ARN, vutrisiran produce la degradación catalítica del ARNm de TTR en el hígado. Baja la TTR sérica y, con ella, el depósito de amiloide. *[CIMA 5.1]*
5. **Magnitud:** la TTR sérica baja un 73 % a la semana 6, un 83 % a los 9 meses y un 88 % a los 18 meses con 25 mg cada 3 meses. *[CIMA 5.1]*
6. **Consecuencia previsible:** baja la vitamina A, porque la TTR transporta la proteína de unión al retinol (RBP4). Por eso se da un suplemento de 2 500 a 3 000 UI al día. *[CIMA 4.2, 4.4, 5.1]*

## Recorrido de las láminas

**1. Contexto.** La TTR es un homotetrámero que circula en sangre y transporta tiroxina. *[UniProt P02766]* Se fabrica sobre todo en el hígado. *[PMID 36345805]* En la amiloidosis por TTR (ATTR), el tetrámero se disocia; los monómeros mal plegados forman fibras amiloides que se depositan en nervios (polineuropatía) y corazón (miocardiopatía). *[UniProt P02766; PMID 36345805]*

| Fármaco | Dónde actúa | Fuente |
|---|---|---|
| Vutrisiran | ARNm de TTR (ARNpi conjugado con GalNAc) | CIMA 5.1; FDA 12.1 |
| Patisiran | ARNm de TTR (ARNpi) | FDA 12.1 |
| Eplontersen | ARNm de TTR (oligonucleótido antisentido conjugado con GalNAc) | FDA 12.1 |
| Tafamidis, acoramidis | Tetrámero de TTR: se unen al sitio de la tiroxina y frenan su disociación, el paso limitante | FDA 12.1 |

**2. Fisiología normal.**

- **En el hepatocito:** el gen TTR se transcribe a ARNm, el ARNm se traduce en subunidades, y cuatro subunidades forman el tetrámero, que se secreta a la sangre. *[UniProt P02766; PMID 36345805]*
- **En la sangre:** el tetrámero tiene un canal central donde caben dos moléculas de tiroxina. *[UniProt P02766; PDB 1ICT]* Además, se une a RBP4 cargada de retinol; así el complejo es más grande y no se filtra en el riñón. *[Reactome R-HSA-2404134]*
- **Amiloide:** la disociación del tetrámero es el paso limitante de la amiloidogénesis. *[FDA, tafamidis 12.1]*

**3. Entrada en el hepatocito.**

1. Inyección subcutánea de 25 mg cada 3 meses. *[CIMA 4.2]*
2. La GalNAc se une al ASGPR, que reconoce galactosa y GalNAc terminales. *[UniProt P07306; NCI C152919]*
3. El complejo se internaliza. El receptor se separa de su ligando en un compartimento de clasificación y vuelve a la superficie. *[UniProt P07306]*
4. El ARNpi llega al citoplasma, donde actúa. *[NCI C152919]*

La lámina muestra la estructura real del dominio de reconocimiento del ASGPR con GalNAc en su sitio de unión (PDB 9G76).

**4. Interferencia por ARN.**

1. El ARNpi se carga en Ago2, el núcleo del complejo RISC. Se conserva la hebra guía y se elimina la pasajera. *[UniProt Q9UKV8; PMID 22233755, 19946268]*
2. La hebra guía se aparea con el ARNm de TTR.
3. Con complementariedad perfecta, Ago2 corta el ARNm. *[UniProt Q9UKV8]*
4. El proceso es catalítico: una misma guía sirve para muchos cortes. *[CIMA 5.1]*

La estructura PDB 9CMP muestra Ago2 humana con una guía y un ARN diana totalmente apareados, en la conformación que corta. Las secuencias son de ejemplo, no las de vutrisiran.

## Farmacocinética e interacciones *[CIMA 4.5, 5.2; FDA 12.2, 12.3]*

- **Absorción:** subcutánea y rápida, con tmáx de unas 3 horas. No se acumula en plasma con la dosis trimestral.
- **Distribución:** sobre todo al hígado; unión a proteínas plasmáticas superior al 80 %.
- **Metabolismo:** endonucleasas y exonucleasas lo cortan en fragmentos. No hay metabolitos circulantes importantes y no lo metaboliza el CYP450.
- **Eliminación:** semivida plasmática de unas 5 horas; entre el 15 % y el 25 % se elimina intacto por la orina.
- **Relación con el efecto:** la reducción de TTR depende de la concentración en el hígado, no en el plasma. Por eso una dosis cada 3 meses mantiene la TTR baja todo el intervalo. *[CIMA 5.2, relación PK/PD]*
- **Interacciones:** no se esperan, porque no usa el CYP450 ni modula transportadores.
- **Ajuste de dosis:** no hace falta en mayores de 65 años ni en insuficiencia renal o hepática leve o moderada. En la grave no se ha estudiado.

## Efectos adversos y precauciones *[CIMA 4.3, 4.4, 4.6, 4.8]*

- **Frecuentes (1–10 %):**
  - Reacción en la zona de inyección: leve, transitoria y sin suspensiones del tratamiento.
  - ALT elevada.
  - Fosfatasa alcalina elevada.
- **ALT en HELIOS-B:** elevaciones leves en el 30 % de los pacientes con vutrisiran frente al 24 % con placebo, todas asintomáticas.
- **Vitamina A:**
  - Corregir el déficit antes de empezar.
  - Dar un suplemento diario de 2 500 a 3 000 UI.
  - Derivar al oftalmólogo si aparecen síntomas oculares, como ceguera nocturna.
- **Embarazo:**
  - Excluirlo antes de iniciar y usar anticoncepción eficaz: tanto el exceso como el déficit de vitamina A pueden causar malformaciones.
  - La vitamina A puede seguir baja más de 12 meses después de la última dosis.
- **Contraindicación:** hipersensibilidad grave, como la anafilaxia.

## Eficacia *[CIMA 5.1]*

- **HELIOS-A (polineuropatía):**
  - Diseño: abierto; 122 pacientes con vutrisiran comparados con el grupo placebo externo del estudio APOLLO, y con patisiran como referencia.
  - A los 18 meses, el mNIS+7 cambió −0,5 puntos con vutrisiran frente a +28,1 con placebo (diferencia de −28,5; p < 0,0001).
  - La reducción de TTR no fue inferior a la de patisiran.
- **HELIOS-B (miocardiopatía):**
  - Diseño: doble ciego, 654 pacientes; el 89 % con ATTR nativa (ATTRwt) y el 40 % ya tomaba tafamidis.
  - Variable primaria, mortalidad y eventos cardiovasculares recurrentes: HR 0,718 en la población global y 0,672 en monoterapia.
  - Mortalidad total hasta el mes 42: −35,5 % (HR 0,645).

## Indicaciones *[CIMA 4.1]*

- Amiloidosis hereditaria por TTR en adultos con polineuropatía en estadio 1 o 2.
- Amiloidosis por TTR nativa o hereditaria en adultos con miocardiopatía.

## Indicaciones aprobadas por la FDA *[Drugs@FDA, NDA 215515; ficha de la FDA del 06/11/2025]*

| Fecha (FDA) | Indicación aprobada | ¿En la ficha de CIMA? |
|---|---|---|
| 13/06/2022 | Polineuropatía de la amiloidosis hereditaria por TTR en adultos | Sí (en la UE, estadio 1 o 2) |
| 20/03/2025 | Miocardiopatía de la amiloidosis por TTR nativa o hereditaria en adultos, para reducir la mortalidad CV, las hospitalizaciones CV y las visitas urgentes por insuficiencia cardiaca | Sí |

La primera autorización en la UE es del 15/09/2022. La FDA y la EMA aprueban por separado; en Costa Rica rige el registro sanitario nacional.

## Del ensayo a la práctica: valor y vida real

No se hallaron en PubMed evaluaciones económicas ni estudios de vida real de Latinoamérica. Se resumen las fuentes disponibles.

**Farmacoeconomía**

- **Reino Unido, NICE TA868 (2023), polineuropatía:** recomendado en estadio 1 o 2, dentro de su autorización y con acuerdo comercial. El precio de lista es de £95 862,36 por jeringa, unas £383 449 al año.
- **Reino Unido, NICE TA1115 (2025), miocardiopatía:** puede usarse con acuerdo comercial. Se debe elegir la opción más barata entre vutrisiran y tafamidis.
- **Canadá, CDA-AMC (2026), miocardiopatía:** recomienda el reembolso con condiciones. Entre ellas, que el costo no supere al de tafamidis y que no se combine con otro tratamiento modificador de la enfermedad. *[PMID 42118893]*

**Vida real**

- **Estados Unidos (2026):** análisis retrospectivo de reclamaciones de seguros en 111 pacientes que iniciaron vutrisiran cuando solo estaba aprobado para la polineuropatía; el 70 % tenía insuficiencia cardiaca.
  - Con un seguimiento medio de 1,5 años, el 37 % fue hospitalizado.
  - En los primeros 12 meses, el 12 % murió y otro 12 % suspendió el tratamiento.

  *[PMID 42455256]*
- **Metaanálisis (2025):** 10 estudios con 5 203 pacientes con miocardiopatía. El conjunto de tratamientos dirigidos contra la ATTR se asoció a un 39 % menos de mortalidad (RR 0,61) y un 31 % menos de hospitalizaciones CV. No es un análisis específico de vutrisiran. *[PMID 41311351]*

## Error frecuente

«Vutrisiran edita el gen TTR». **Falso.** No modifica el ADN: destruye el ARNm de TTR mediante interferencia por ARN, por eso hay que repetir la dosis cada 3 meses. Tampoco es un estabilizador como tafamidis: tafamidis protege la TTR que ya circula y vutrisiran reduce la que se fabrica. *[CIMA 4.2, 5.1; FDA, tafamidis 12.1]*

## Pregunta de autoevaluación

¿Por qué un paciente tratado con vutrisiran necesita un suplemento de vitamina A, y por qué no conviene subir esa dosis por encima de 3 000 UI al día?

<details>
<summary>Respuesta</summary>

La TTR transporta en sangre la proteína de unión al retinol (RBP4). Al bajar la TTR, baja el retinol sérico entre un 62 % y un 70 %, y el suplemento reduce el riesgo de síntomas oculares por déficit. Subir la dosis no corrige el retinol plasmático, porque el problema es la falta de transportador. Además, el exceso de vitamina A puede ser perjudicial, sobre todo en el embarazo. *[CIMA 4.4, 5.1; Reactome R-HSA-2404134]*
</details>

## Simplificaciones de las láminas

- No hay escala entre los órganos, las células, las moléculas y las proteínas.
- El tetrámero de TTR se dibuja como cuatro cuadrados; su forma real se muestra con la estructura PDB 1ICT.
- La hebra con la GalNAc se dibuja según la convención habitual de los conjugados con GalNAc. La ficha técnica no indica en qué hebra va el ligando.
- No se dibujan las modificaciones químicas del ARNpi.
- La salida del endosoma se resume en una flecha.
- Ago2 se representa con una ilustración genérica de proteína; su forma real se muestra con la estructura PDB 9CMP.
- Las curvas de la lámina 5 son un esquema cualitativo: las cifras están en las tarjetas y en este material.

## Fuentes

- **AEMPS, CIMA:** ficha técnica de Amvuttra 25 mg (n.º de registro 1221681001), secciones 4.1–4.8, 5.1–5.3 y 9.
- **FDA:**
  - Ficha de Amvuttra del 06/11/2025 (openFDA), secciones 1, 12.1, 12.2 y 12.3.
  - Sección 12.1 de las fichas de tafamidis, acoramidis, patisiran y eplontersen.
  - Drugs@FDA: NDA 215515, aprobación original y suplemento S-006.
- **UniProt:** P02766 (TTR), Q9UKV8 (AGO2) y P07306 (ASGR1).
- **Reactome:** R-HSA-2404134, «RBP4:atROL binds TTR».
- **NCI Thesaurus:** C152919 (vutrisiran).
- **Artículos:**
  - Liver-directed drugs for transthyretin-mediated amyloidosis. 2022. PMID 36345805.
  - The N domain of Argonaute drives duplex unwinding during RISC assembly. 2012. PMID 22233755.
  - Distinct passenger strand and mRNA cleavage activities of human Argonaute proteins. 2009. PMID 19946268.
- **RCSB PDB:** 1ICT, 9G76 y 9CMP (CC0).
- **Farmacoeconomía y vida real:** NICE TA868 (2023) y TA1115 (2025); PMID 42118893, 42455256 y 41311351.
- **Ilustraciones:** Servier Medical Art (CC BY 3.0 y 4.0): hígado, nervio, corazón, célula, núcleo, proteína y jeringa.

## No verificado

- **ChEMBL:** el servidor (www.ebi.ac.uk) devolvió error 500. El mecanismo y la diana se confirmaron con la ficha técnica, la FDA, el NCI Thesaurus y UniProt.
- **Fechas de la UE:** no se confirmó la fecha en que la UE aprobó la indicación de miocardiopatía; solo consta en la ficha vigente.

Queda, como en todo prototipo, la revisión farmacológica del nivel y los mensajes para estudiantes de pregrado.
