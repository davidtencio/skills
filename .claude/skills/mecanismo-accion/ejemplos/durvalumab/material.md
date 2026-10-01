# Durvalumab: ¿cómo actúa?

> **Prototipo pendiente de revisión farmacológica.** Material educativo para estudiantes de farmacia; no sustituye la ficha técnica vigente.

Serie de seis láminas (16:9):

1. [Puntos de control: los frenos del linfocito T](lamina-1.png)
2. [Cómo PD-L1 frena al linfocito T que reconoce el tumor](lamina-2.png)
3. [Cómo actúa durvalumab](lamina-3.png)
4. [Del mecanismo al paciente](lamina-4.png)
5. [Indicaciones aprobadas: de la enfermedad avanzada a la cirugía](lamina-5.png)
6. [Del ensayo a la práctica: valor y vida real](lamina-6.png)

## Puntos clave

1. **Tipo de fármaco:** anticuerpo monoclonal completamente humano de tipo IgG1κ dirigido contra PD-L1 (ligando 1 de muerte programada). Grupo ATC L01FF03, inhibidores de PD-1/PD-L1. *[CIMA, Imfinzi 5.1]*
2. **Diana:** PD-L1 (gen *CD274*), proteína de membrana que, al unirse al receptor inhibidor PD-1 del linfocito T, limita su respuesta. Los tumores aprovechan esta vía para escapar del sistema inmunitario. *[UniProt Q9NZQ7]*
3. **Mecanismo:** durvalumab se une a PD-L1 y bloquea de manera selectiva su interacción con PD-1 y con CD80 (B7.1). Así se libera el freno y aumenta la activación de los linfocitos T. *[CIMA 5.1; FDA 12.1]*
4. **No es citotóxico:** no induce citotoxicidad celular dependiente de anticuerpos (CCDA); su región Fc se modificó para evitarla. En un modelo animal, su actividad antitumoral dependía por completo de la presencia de linfocitos T. *[CIMA 5.1; PMID 25943534]*
5. **Estructura:** en los cristales, durvalumab ocupa en PD-L1 casi el mismo sitio que PD-1. *[PDB 5X8M y 4ZQK; PMID 28717238]*

## Recorrido de las láminas

**1. Puntos de control.** El linfocito T reconoce el tumor cuando su receptor (TCR) se une a un péptido tumoral presentado por el MHC. Los puntos de control son frenos de esa respuesta. *[Reactome R-HSA-389948]*

| Fármaco | Diana | Qué bloquea | Fuente |
|---|---|---|---|
| Durvalumab | PD-L1 | PD-L1 frente a PD-1 y CD80 | CIMA 5.1; FDA 12.1 |
| Atezolizumab | PD-L1 | PD-L1 frente a PD-1 y B7.1 | FDA 12.1 |
| Nivolumab, pembrolizumab, cemiplimab | PD-1 | PD-1 frente a PD-L1 y PD-L2 | FDA 12.1 |
| Tremelimumab, ipilimumab | CTLA-4 | CTLA-4 frente a CD80 y CD86 | FDA 12.1 |

**2. Fisiología normal.** La secuencia del freno:

1. El TCR reconoce el antígeno y el linfocito se activa: se fosforilan CD3ζ y ZAP70.
2. El linfocito activado libera IFN-γ. Esta señal inflamatoria induce PD-L1 en las células tumorales y en las células inmunitarias del tumor. *[CIMA 5.1]*
3. PD-L1 se une a PD-1 y a CD80. *[CIMA 5.1]*
4. PD-1 se fosforila y recluta la fosfatasa SHP-2 (PTPN11), que desfosforila CD3ζ, ZAP70 y PKCθ. Así se corta la señal del TCR. *[UniProt Q15116; Reactome R-HSA-389948]*
5. Bajan la actividad citotóxica, la proliferación y la producción de citocinas. El linfocito queda «agotado» y el tumor escapa. *[CIMA 5.1; UniProt Q15116]*

En condiciones normales, esta vía mantiene la tolerancia a lo propio, es decir, evita la autoinmunidad. *[UniProt Q9NZQ7, Q15116]*

**3. Con durvalumab.** La lámina compara dos estructuras reales:

- **PDB 4ZQK:** PD-L1 humano unido a PD-1. *[PMID 26602187]*
- **PDB 5X8M:** PD-L1 unido al Fab de durvalumab. *[PMID 28717238]*

Medimos los contactos a menos de 4,5 Å en ambas estructuras. PD-1 toca 18 aminoácidos de PD-L1, y durvalumab toca 11 de esos mismos 18: los dos usan la misma cara de PD-L1. Con PD-L1 ocupado:

1. PD-1 queda libre y no recluta SHP-2.
2. CD80 también queda libre.
3. El linfocito sigue activo y destruye la célula tumoral con perforina y granzimas.

*[CIMA 5.1; FDA 12.1]*

## Farmacocinética e interacciones *[CIMA 4.2, 4.5, 5.2]*

- **Administración:** perfusión intravenosa de 1 hora; la pauta depende de la indicación (p. ej., 1 500 mg cada 4 semanas o 10 mg/kg cada 2 semanas). La ficha no prevé diferencias clínicamente significativas de eficacia ni de seguridad entre 10 mg/kg cada 2 semanas, 1 120 mg cada 3 semanas y 1 500 mg cada 4 semanas.
- **Linealidad:** farmacocinética no lineal por debajo de 3 mg/kg y lineal a partir de 3 mg/kg.
- **Exposición:** el estado estacionario se alcanza hacia las 16 semanas.
- **Parámetros:** volumen de distribución en estado estacionario de 5,64 L y aclaramiento de 8,16 ml/h el día 365 (disminuye con el tiempo). La semivida terminal es de unos 18 días.
- **Eliminación:** catabolismo proteico por el sistema reticuloendotelial y disposición mediada por la diana. No se esperan interacciones metabólicas, y no se hallaron interacciones farmacocinéticas relevantes con quimioterapia, tremelimumab ni olaparib.
- **Corticoides:** antes de iniciar no se recomiendan corticoides sistémicos (salvo dosis fisiológicas de 10 mg/día de prednisona o menos) ni inmunosupresores, porque pueden interferir con su eficacia. Después de iniciar sí se usan para tratar las reacciones inmunomediadas.
- **Insuficiencia renal o hepática leve o moderada:** sin efecto clínicamente significativo.
- **Inmunogenicidad:** el 2,7 % de los pacientes en monoterapia desarrolló anticuerpos contra el fármaco, sin efecto clínicamente relevante. *[CIMA 4.8]*

## Efectos adversos *[CIMA 4.4, 4.6, 4.8]*

- **Inmunomediados**, en cualquier órgano, porque se libera un freno que también protege los tejidos sanos:
  - Neumonitis, hepatitis y colitis.
  - Endocrinopatías: hipotiroidismo, hipertiroidismo, tiroiditis, insuficiencia suprarrenal, diabetes tipo 1 e hipofisitis.
  - Nefritis, erupción y miocarditis, que puede ser mortal.
  - **Manejo:** suspender el tratamiento y dar corticoides según el grado.
- **Más frecuentes en monoterapia** (4 642 pacientes): tos (18,1 %), diarrea (15,1 %), erupción (15,0 %), pirexia (12,5 %), artralgia (12,4 %) e hipotiroidismo (11,6 %). El tratamiento se suspendió por reacciones adversas en el 3,9 % de los pacientes.
- **Embarazo:** puede causar daño fetal; la vía PD-1/PD-L1 mantiene la tolerancia materna al feto. Se deben usar anticonceptivos eficaces durante el tratamiento y al menos 3 meses después de la última dosis.

## Indicaciones *[CIMA 4.1]*

En adultos:

- **Cáncer de pulmón no microcítico (CPNM):**
  - Resecable de alto riesgo, antes y después de la cirugía.
  - Estadio III irresecable sin progresión tras quimiorradioterapia, si PD-L1 ≥ 1 %.
  - Metastásico, con tremelimumab y quimioterapia.
- **Cáncer de pulmón microcítico:**
  - Estadio limitado, tras quimiorradioterapia.
  - Estadio extendido, en primera línea con etopósido y platino.
- **Cáncer de vías biliares**, con gemcitabina y cisplatino.
- **Carcinoma hepatocelular**, en monoterapia o con tremelimumab.
- **Cáncer de endometrio**, con carboplatino y paclitaxel; después, mantenimiento solo (dMMR) o con olaparib (pMMR).
- **Cáncer de vejiga músculo-invasivo**, antes y después de la cistectomía.
- **Adenocarcinoma gástrico o de la unión gastroesofágica**, antes y después de la cirugía, con FLOT.

## Indicaciones aprobadas por la FDA: evolución y novedades *[Drugs@FDA, BLA 761069, cartas de aprobación; ficha de la FDA del 31/08/2026]*

| Fecha (FDA) | Indicación aprobada | ¿En la ficha de CIMA? |
|---|---|---|
| 01/05/2017 | Carcinoma urotelial avanzado tras platino (aprobación acelerada) | No; retirada por la FDA el 19/02/2021 |
| 16/02/2018 | CPNM estadio III irresecable sin progresión tras quimiorradioterapia | Sí (en la UE, solo con PD-L1 ≥ 1 %) |
| 27/03/2020 | Microcítico extendido, primera línea con etopósido y platino | Sí |
| 02/09/2022 | Vías biliares, con gemcitabina y cisplatino | Sí |
| 21/10/2022 | Hepatocarcinoma irresecable, con tremelimumab | Sí |
| 10/11/2022 | CPNM metastásico, con tremelimumab y quimioterapia | Sí |
| 14/06/2024 | Endometrio dMMR avanzado o recurrente, con carboplatino y paclitaxel | Sí |
| 15/08/2024 | CPNM resecable: neoadyuvante con quimioterapia y adyuvante | Sí |
| 04/12/2024 | Microcítico limitado tras quimiorradioterapia | Sí |
| 28/03/2025 | Vejiga músculo-invasivo: neoadyuvante con quimioterapia y adyuvante | Sí |
| 25/11/2025 | Gástrico o de la unión gastroesofágica resecable, con FLOT | Sí |
| 28/05/2026 | Vejiga no músculo-invasivo de alto riesgo sin BCG previo, con BCG | **No** |

**Diferencias en sentido inverso:** la UE aprueba dos usos que la ficha de la FDA no incluye: el hepatocarcinoma en monoterapia y el cáncer de endometrio pMMR con olaparib.

**Mensaje para el estudiante:** en nueve años, las indicaciones pasaron de la enfermedad avanzada ya tratada a la primera línea y al tratamiento alrededor de la cirugía. La FDA y la EMA aprueban por separado; en Costa Rica rige el registro sanitario nacional.

## Del ensayo a la práctica: valor y vida real

Prioridad para Latinoamérica. Los estudios observacionales muestran asociaciones, no causas.

**Farmacoeconomía**

- **Chile (2024):** análisis de impacto presupuestario de durvalumab de consolidación en CPNM estadio III. En el sistema público, el costo pasaría de USD 1,27 millones el primer año a 8,5 millones el quinto, con ahorros parciales en seguimiento, efectos adversos y final de vida. Los autores piden un análisis completo de costo-efectividad. *[PMID 39058755]*
- **Brasil, Estados Unidos, Singapur y España (2024):** modelo de Markov con datos de PACIFIC, en USD. La razón de costo-efectividad incremental fue de USD 141 146 por AVAC en Brasil, frente a un umbral de USD 22 251, y de USD 228 788 en Estados Unidos. A los precios usados, no fue costo-efectivo en ninguno de los cuatro países. *[PMID 38814640]*
- **Reino Unido, NICE TA798 (2022):** recomendado en CPNM estadio III con PD-L1 ≥ 1 % tras quimiorradioterapia concurrente, con un acuerdo comercial (descuento confidencial). El precio de lista es de £2 466 por vial de 500 mg.
- **Reino Unido, NICE TA944 (2024):** en vías biliares, con gemcitabina y cisplatino, el comité estimó entre £20 000 y £30 000 por AVAC, con ponderación por gravedad. Recomendado con acuerdo comercial.

**Vida real**

- **Brasil, LACOG 0120 (2025):** 31 pacientes con CPNM estadio III de 7 centros, tratados en un programa de acceso expandido. La supervivencia libre de progresión mediana fue de 9,9 meses y la supervivencia global mediana de 34,9 meses. Hubo neumonitis en el 12,9 % y no aparecieron problemas de seguridad nuevos. *[PMID 39813498]*
- **PACIFIC-R, internacional (2026):** cohorte observacional retrospectiva de 1 153 pacientes. La supervivencia libre de progresión en vida real tuvo una mediana de 24,3 meses y la supervivencia global de 59,0 meses; a 5 años, el 49,2 % seguía vivo. *[PMID 41643268]*

## Error frecuente

«Durvalumab es una quimioterapia que ataca al tumor». **Falso.** No es citotóxico ni induce CCDA: bloquea PD-L1 y deja que los linfocitos T del propio paciente actúen. Por eso sus efectos adversos característicos son inflamatorios e inmunomediados (neumonitis, colitis, tiroiditis), no la toxicidad típica de un citotóxico. *[CIMA 4.4, 5.1; PMID 25943534]*

## Pregunta de autoevaluación

¿Por qué la ficha técnica desaconseja los corticoides sistémicos antes de iniciar durvalumab, pero los recomienda para tratar sus efectos adversos inmunomediados?

<details>
<summary>Respuesta</summary>

Durvalumab funciona porque reactiva linfocitos T. Si antes de empezar se suprime el sistema inmunitario con corticoides o inmunosupresores, se puede interferir con su actividad y su eficacia. Una vez iniciado, el riesgo es el opuesto: una respuesta inmunitaria excesiva contra tejidos sanos. Los corticoides sirven entonces para frenar esa inflamación según el grado de la reacción. *[CIMA 4.4, 4.5]*
</details>

## Simplificaciones de las láminas

- No hay escala entre las células, las proteínas y el anticuerpo.
- PD-1, PD-L1, CD80, TCR y MHC se dibujan como dominios de inmunoglobulina genéricos.
- CD80 se dibuja en la membrana del linfocito para mostrar que PD-L1 tiene dos parejas. La ficha técnica no precisa en qué célula ocurre esa unión.
- La señal intracelular se reduce a CD3ζ, ZAP70 y SHP-2.
- Las superficies proteicas son de estructuras reales, pero se muestran sin glicanos y orientadas para ver la interfaz.
- El anticuerpo se dibuja unido por un brazo y sin escala.

## Fuentes

- **AEMPS, CIMA:** ficha técnica de Imfinzi 50 mg/ml concentrado para solución para perfusión (n.º de registro 1181322001), secciones 4.1, 4.2, 4.4, 4.5, 4.6, 4.8, 5.1, 5.2 y 5.3.
- **FDA:**
  - Ficha de Imfinzi del 31/08/2026 (openFDA), secciones 1 y 12.1.
  - Sección 12.1 de las fichas de atezolizumab, nivolumab, pembrolizumab, cemiplimab, tremelimumab e ipilimumab.
  - Drugs@FDA: historial de la BLA 761069 y cartas de aprobación de los suplementos S-002, S-018, S-029, S-033, S-035, S-036, S-043, S-045, S-049, S-050, S-052 y S-053.
- **UniProt:** Q9NZQ7 (CD274/PD-L1), Q15116 (PDCD1/PD-1) y P33681 (CD80).
- **Reactome:** R-HSA-389948, «Co-inhibition by PD-1».
- **NCI Thesaurus:** C103194 (durvalumab).
- **Artículos:**
  - Stewart R et al. Identification and characterization of MEDI4736. *Cancer Immunol Res* 2015. PMID 25943534.
  - Lee HT et al. Molecular mechanism of PD-1/PD-L1 blockade via anti-PD-L1 antibodies atezolizumab and durvalumab. *Sci Rep* 2017. PMID 28717238.
  - Zak KM et al. Structure of the complex of human PD-1 and its ligand PD-L1. *Structure* 2015. PMID 26602187.
- **RCSB PDB:** 4ZQK y 5X8M (CC0).
- **Farmacoeconomía y vida real:** PMID 39058755, 38814640, 39813498 y 41643268; NICE TA798 (2022) y TA944 (2024).
- **Ilustraciones:** Servier Medical Art (CC BY 3.0 y 4.0), incluido el linfocito T vía Bioicons.

## No verificado

- **ChEMBL:** el servidor (www.ebi.ac.uk) devolvió error 500 durante la consulta. El mecanismo y la diana se confirmaron con la ficha técnica, la FDA, el NCI Thesaurus y UniProt. No se incluyen datos de afinidad (Kd).
- **Costa Rica:** los precios adjudicados por la CCSS no se consultaron, porque requieren SICOP desde el navegador de la persona usuaria; se pueden añadir con la skill `estudio-mercado-sicop`.

Queda, como en todo prototipo, la revisión farmacológica del nivel y los mensajes para estudiantes de pregrado.
