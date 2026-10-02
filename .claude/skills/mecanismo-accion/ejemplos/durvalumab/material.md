# Durvalumab: ¿cómo actúa?

<!-- portada: 3 -->
<!-- fecha: 2026-10-02 -->

> **Prototipo pendiente de revisión farmacológica.** Material educativo para estudiantes de farmacia; no sustituye la ficha técnica vigente.

Serie de seis láminas (16:9):

1. [Puntos de control: los frenos del linfocito T](lamina-1.png)
2. [Cómo PD-L1 frena al linfocito T que reconoce el tumor](lamina-2.png)
3. [Cómo actúa durvalumab](lamina-3.png)
4. [Del mecanismo al paciente](lamina-4.png)
5. [Indicaciones aprobadas: de la enfermedad avanzada a la cirugía](lamina-5.png)
6. [Del ensayo a la práctica: valor y vida real](lamina-6.png)

## Puntos clave

1. **Tipo de fármaco:** anticuerpo monoclonal completamente humano de tipo IgG1κ dirigido contra PD-L1 (ligando 1 de muerte programada). Grupo ATC L01FF03, inhibidores de PD-1/PD-L1. *[@cima-imfinzi, 5.1]*
2. **Diana:** PD-L1 (gen *CD274*), proteína de membrana que, al unirse al receptor inhibidor PD-1 del linfocito T, limita su respuesta. Los tumores aprovechan esta vía para escapar del sistema inmunitario. *[@uniprot, Q9NZQ7]*
3. **Mecanismo:** durvalumab se une a PD-L1 y bloquea de manera selectiva su interacción con PD-1 y con CD80 (B7.1). Así se libera el freno y aumenta la activación de los linfocitos T. *[@cima-imfinzi, 5.1; @fda-imfinzi, 12.1]*
4. **No es citotóxico:** no induce citotoxicidad celular dependiente de anticuerpos (CCDA); su región Fc se modificó para evitarla. En un modelo animal, su actividad antitumoral dependía por completo de la presencia de linfocitos T. *[@cima-imfinzi, 5.1; @stewart-2015]*
5. **Estructura:** en los cristales, durvalumab ocupa en PD-L1 casi el mismo sitio que PD-1. *[@pdb, 5X8M y 4ZQK; @lee-2017]*

## Recorrido de las láminas

**1. Puntos de control.** El linfocito T reconoce el tumor cuando su receptor (TCR) se une a un péptido tumoral presentado por el MHC. Los puntos de control son frenos de esa respuesta. *[@reactome]*

| Fármaco | Diana | Qué bloquea | Fuente |
|---|---|---|---|
| Durvalumab | PD-L1 | PD-L1 frente a PD-1 y CD80 | *[@cima-imfinzi, 5.1; @fda-imfinzi, 12.1]* |
| Atezolizumab | PD-L1 | PD-L1 frente a PD-1 y B7.1 | *[@fda-12-1, atezolizumab]* |
| Nivolumab, pembrolizumab, cemiplimab | PD-1 | PD-1 frente a PD-L1 y PD-L2 | *[@fda-12-1]* |
| Tremelimumab, ipilimumab | CTLA-4 | CTLA-4 frente a CD80 y CD86 | *[@fda-12-1]* |

**2. Fisiología normal.** La secuencia del freno:

1. El TCR reconoce el antígeno y el linfocito se activa: se fosforilan CD3ζ y ZAP70.
2. El linfocito activado libera IFN-γ. Esta señal inflamatoria induce PD-L1 en las células tumorales y en las células inmunitarias del tumor. *[@cima-imfinzi, 5.1]*
3. PD-L1 se une a PD-1 y a CD80. *[@cima-imfinzi, 5.1]*
4. PD-1 se fosforila y recluta la fosfatasa SHP-2 (PTPN11), que desfosforila CD3ζ, ZAP70 y PKCθ. Así se corta la señal del TCR. *[@uniprot, Q15116; @reactome]*
5. Bajan la actividad citotóxica, la proliferación y la producción de citocinas. El linfocito queda «agotado» y el tumor escapa. *[@cima-imfinzi, 5.1; @uniprot, Q15116]*

En condiciones normales, esta vía mantiene la tolerancia a lo propio, es decir, evita la autoinmunidad. *[@uniprot, Q9NZQ7 y Q15116]*

**3. Con durvalumab.** La lámina compara dos estructuras reales:

- **PDB 4ZQK:** PD-L1 humano unido a PD-1. *[@zak-2015]*
- **PDB 5X8M:** PD-L1 unido al Fab de durvalumab. *[@lee-2017]*

Medimos los contactos a menos de 4,5 Å en ambas estructuras. PD-1 toca 18 aminoácidos de PD-L1, y durvalumab toca 11 de esos mismos 18: los dos usan la misma cara de PD-L1. Con PD-L1 ocupado:

1. PD-1 queda libre y no recluta SHP-2.
2. CD80 también queda libre.
3. El linfocito sigue activo y destruye la célula tumoral con perforina y granzimas.

*[@cima-imfinzi, 5.1; @fda-imfinzi, 12.1]*

## Farmacocinética e interacciones *[@cima-imfinzi, 4.2, 4.5 y 5.2]*

- **Administración:** perfusión intravenosa de 1 hora; la pauta depende de la indicación (p. ej., 1 500 mg cada 4 semanas o 10 mg/kg cada 2 semanas). La ficha no prevé diferencias clínicamente significativas de eficacia ni de seguridad entre 10 mg/kg cada 2 semanas, 1 120 mg cada 3 semanas y 1 500 mg cada 4 semanas.
- **Linealidad:** farmacocinética no lineal por debajo de 3 mg/kg y lineal a partir de 3 mg/kg.
- **Exposición:** el estado estacionario se alcanza hacia las 16 semanas.
- **Parámetros:** volumen de distribución en estado estacionario de 5,64 L y aclaramiento de 8,16 ml/h el día 365 (disminuye con el tiempo). La semivida terminal es de unos 18 días.
- **Eliminación:** catabolismo proteico por el sistema reticuloendotelial y disposición mediada por la diana. No se esperan interacciones metabólicas, y no se hallaron interacciones farmacocinéticas relevantes con quimioterapia, tremelimumab ni olaparib.
- **Corticoides:** antes de iniciar no se recomiendan corticoides sistémicos (salvo dosis fisiológicas de 10 mg/día de prednisona o menos) ni inmunosupresores, porque pueden interferir con su eficacia. Después de iniciar sí se usan para tratar las reacciones inmunomediadas.
- **Insuficiencia renal o hepática leve o moderada:** sin efecto clínicamente significativo.
- **Inmunogenicidad:** el 2,7 % de los pacientes en monoterapia desarrolló anticuerpos contra el fármaco, sin efecto clínicamente relevante. *[@cima-imfinzi, 4.8]*

## Efectos adversos *[@cima-imfinzi, 4.4, 4.6 y 4.8]*

- **Inmunomediados**, en cualquier órgano, porque se libera un freno que también protege los tejidos sanos:
  - Neumonitis, hepatitis y colitis.
  - Endocrinopatías: hipotiroidismo, hipertiroidismo, tiroiditis, insuficiencia suprarrenal, diabetes tipo 1 e hipofisitis.
  - Nefritis, erupción y miocarditis, que puede ser mortal.
  - **Manejo:** suspender el tratamiento y dar corticoides según el grado.
- **Más frecuentes en monoterapia** (4 642 pacientes): tos (18,1 %), diarrea (15,1 %), erupción (15,0 %), pirexia (12,5 %), artralgia (12,4 %) e hipotiroidismo (11,6 %). El tratamiento se suspendió por reacciones adversas en el 3,9 % de los pacientes.
- **Embarazo:** puede causar daño fetal; la vía PD-1/PD-L1 mantiene la tolerancia materna al feto. Se deben usar anticonceptivos eficaces durante el tratamiento y al menos 3 meses después de la última dosis.

## Indicaciones *[@cima-imfinzi, 4.1]*

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

## Indicaciones aprobadas por la FDA: evolución y novedades *[@drugs-fda; @fda-imfinzi, sección 1; @ema-imfinzi]*

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

- **Chile (2024):** análisis de impacto presupuestario de durvalumab de consolidación en CPNM estadio III. En el sistema público, el costo pasaría de USD 1,27 millones el primer año a 8,5 millones el quinto, con ahorros parciales en seguimiento, efectos adversos y final de vida. Los autores piden un análisis completo de costo-efectividad. *[@chile-2024]*
- **Brasil, Estados Unidos, Singapur y España (2024):** modelo de Markov con datos del ensayo PACIFIC *[@pacific-2017]*, en USD. La razón de costo-efectividad incremental fue de USD 141 146 por AVAC en Brasil, frente a un umbral de USD 22 251, y de USD 228 788 en Estados Unidos. A los precios usados, no fue costo-efectivo en ninguno de los cuatro países. *[@markov-2024]*
- **Reino Unido, NICE TA798 (2022):** recomendado en CPNM estadio III con PD-L1 ≥ 1 % tras quimiorradioterapia concurrente, con un acuerdo comercial (descuento confidencial). El precio de lista es de £2 466 por vial de 500 mg. *[@nice-ta798]*
- **Reino Unido, NICE TA944 (2024):** en vías biliares, con gemcitabina y cisplatino, el comité estimó entre £20 000 y £30 000 por AVAC, con ponderación por gravedad. Recomendado con acuerdo comercial. *[@nice-ta944]*

**Vida real**

- **Brasil, LACOG 0120 (2025):** 31 pacientes con CPNM estadio III de 7 centros, tratados en un programa de acceso expandido. La supervivencia libre de progresión mediana fue de 9,9 meses y la supervivencia global mediana de 34,9 meses. Hubo neumonitis en el 12,9 % y no aparecieron problemas de seguridad nuevos. *[@lacog-2025]*
- **PACIFIC-R, internacional (2026):** cohorte observacional retrospectiva de 1 153 pacientes. La supervivencia libre de progresión en vida real tuvo una mediana de 24,3 meses y la supervivencia global de 59,0 meses; a 5 años, el 49,2 % seguía vivo. *[@pacific-r-2026]*

## Error frecuente

«Durvalumab es una quimioterapia que ataca al tumor». **Falso.** No es citotóxico ni induce CCDA: bloquea PD-L1 y deja que los linfocitos T del propio paciente actúen. Por eso sus efectos adversos característicos son inflamatorios e inmunomediados (neumonitis, colitis, tiroiditis), no la toxicidad típica de un citotóxico. *[@cima-imfinzi, 4.4 y 5.1; @stewart-2015]*

## Pregunta de autoevaluación

¿Por qué la ficha técnica desaconseja los corticoides sistémicos antes de iniciar durvalumab, pero los recomienda para tratar sus efectos adversos inmunomediados?

<details>
<summary>Respuesta</summary>

Durvalumab funciona porque reactiva linfocitos T. Si antes de empezar se suprime el sistema inmunitario con corticoides o inmunosupresores, se puede interferir con su actividad y su eficacia. Una vez iniciado, el riesgo es el opuesto: una respuesta inmunitaria excesiva contra tejidos sanos. Los corticoides sirven entonces para frenar esa inflamación según el grado de la reacción. *[@cima-imfinzi, 4.4 y 4.5]*
</details>

## Simplificaciones de las láminas

- No hay escala entre las células, las proteínas y el anticuerpo.
- PD-1, PD-L1, CD80, TCR y MHC se dibujan como dominios de inmunoglobulina genéricos.
- CD80 se dibuja en la membrana del linfocito para mostrar que PD-L1 tiene dos parejas. La ficha técnica no precisa en qué célula ocurre esa unión.
- La señal intracelular se reduce a CD3ζ, ZAP70 y SHP-2.
- Las superficies proteicas son de estructuras reales, pero se muestran sin glicanos y orientadas para ver la interfaz.
- El anticuerpo se dibuja unido por un brazo y sin escala.

## Glosario

- **AEMPS:** Agencia Española de Medicamentos y Productos Sanitarios.
- **ATC:** Clasificación Anatómica, Terapéutica y Química de la OMS.
- **AVAC:** Año de vida ajustado por calidad (en inglés, QALY).
- **BCG:** Bacilo de Calmette-Guérin, usado como inmunoterapia intravesical.
- **BLA:** Solicitud de licencia de un producto biológico ante la FDA (Biologics License Application).
- **CCDA:** Citotoxicidad celular dependiente de anticuerpos (en inglés, ADCC).
- **CD274:** Gen que codifica PD-L1.
- **CD3ζ:** Cadena zeta del complejo CD3, que transmite la señal del TCR.
- **CD80:** Proteína coestimuladora (B7.1); se une a CD28, CTLA-4 y PD-L1.
- **CD86:** Proteína coestimuladora (B7.2); se une a CD28 y CTLA-4.
- **CIMA:** Centro de Información de Medicamentos de la AEMPS, donde se consultan las fichas técnicas españolas.
- **CPNM:** Cáncer de pulmón no microcítico.
- **CTLA-4:** Antígeno 4 del linfocito T citotóxico, receptor inhibidor del linfocito T.
- **CYP:** Citocromo P450, familia de enzimas que metabolizan fármacos.
- **dMMR:** Deficiencia del sistema de reparación de errores de emparejamiento del ADN.
- **EMA:** Agencia Europea de Medicamentos.
- **FDA:** Administración de Alimentos y Medicamentos de EE. UU.
- **FLOT:** Quimioterapia con fluorouracilo, leucovorina, oxaliplatino y docetaxel.
- **IFN-γ:** Interferón gamma, citocina inflamatoria del linfocito activado.
- **IgG1κ:** Inmunoglobulina G1 con cadena ligera kappa.
- **LACOG:** Grupo Cooperativo Latinoamericano de Oncología (Latin American Cooperative Oncology Group).
- **MHC:** Complejo mayor de histocompatibilidad, que presenta péptidos al linfocito T.
- **NCI:** Instituto Nacional del Cáncer de EE. UU.
- **NICE:** Instituto Nacional para la Excelencia en Salud y Atención del Reino Unido.
- **PACIFIC:** Ensayo de fase 3 de durvalumab tras quimiorradioterapia en CPNM estadio III.
- **PACIFIC-R:** Estudio observacional internacional de durvalumab en la práctica clínica (vida real).
- **PD-1:** Proteína 1 de muerte celular programada, receptor inhibidor del linfocito T.
- **PDB:** Protein Data Bank, banco de estructuras tridimensionales de proteínas.
- **PD-L1:** Ligando 1 de muerte programada, que se une a PD-1 y a CD80.
- **PD-L2:** Ligando 2 de muerte programada, que se une a PD-1.
- **PKCθ:** Proteína cinasa C theta, de la señal del TCR.
- **PMID:** Identificador de un artículo en PubMed.
- **pMMR:** Sistema de reparación de errores de emparejamiento del ADN competente.
- **PTPN11:** Gen que codifica la fosfatasa SHP-2.
- **QT:** Quimioterapia.
- **SHP-2:** Tirosina fosfatasa que recluta PD-1 (gen PTPN11).
- **TCR:** Receptor del linfocito T.
- **UE:** Unión Europea.
- **USD:** Dólares estadounidenses.
- **ZAP70:** Cinasa asociada a la cadena zeta, de la señal del TCR.

## Fuentes

<!-- bibliografia: inicio -->

1. Agencia Española de Medicamentos y Productos Sanitarios (AEMPS). Ficha técnica de IMFINZI 50 MG/ML CONCENTRADO PARA SOLUCION PARA PERFUSION. CIMA, n.º de registro 1181322001. Disponible en: [cima.aemps.es/cima/dochtml/ft/1181322001/FT_1181322001.html](https://cima.aemps.es/cima/dochtml/ft/1181322001/FT_1181322001.html). Consultado el 2 de octubre de 2026. Autorización europea: la fecha de la revisión está en el EPAR.
2. UniProt Knowledgebase. Entradas Q9NZQ7 (CD274, PD-L1), Q15116 (PDCD1, PD-1) y P33681 (CD80). Disponible en: [uniprot.org/](https://www.uniprot.org/). Consultado el 2 de octubre de 2026.
3. U.S. Food and Drug Administration. Prescribing information: IMFINZI (durvalumab) injection, for intravenous use. Set id 8baba4ea-2855-42fa-9bd9-5a7548d4cec3; consultada en openFDA. Disponible en: [dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=8baba4ea…](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=8baba4ea-2855-42fa-9bd9-5a7548d4cec3). Versión del 31 de agosto de 2026. Consultado el 2 de octubre de 2026. DailyMed publicó después la versión 34 (7 de septiembre de 2026), que no se revisó.
4. Stewart R, Morrow M, Hammond SA, Mulgrew K, Marcus D, Poon E, et al. Identification and Characterization of MEDI4736, an Antagonistic Anti-PD-L1 Monoclonal Antibody. Cancer Immunol Res. 2015;3(9):1052-62. doi:[10.1158/2326-6066.CIR-14-0191](https://doi.org/10.1158/2326-6066.CIR-14-0191). PMID [25943534](https://pubmed.ncbi.nlm.nih.gov/25943534/).
5. RCSB Protein Data Bank. Estructuras 4ZQK (PD-1 con PD-L1) y 5X8M (PD-L1 con el Fab de durvalumab). Disponible en: [rcsb.org/structure/5X8M](https://www.rcsb.org/structure/5X8M). Consultado el 2 de octubre de 2026.
6. Lee HT, Lee JY, Lim H, Lee SH, Moon YJ, Pyo HJ, et al. Molecular mechanism of PD-1/PD-L1 blockade via anti-PD-L1 antibodies atezolizumab and durvalumab. Sci Rep. 2017;7(1):5532. doi:[10.1038/s41598-017-06002-8](https://doi.org/10.1038/s41598-017-06002-8). PMID [28717238](https://pubmed.ncbi.nlm.nih.gov/28717238/). [PMC5514103](https://pmc.ncbi.nlm.nih.gov/articles/PMC5514103/).
7. Reactome Pathway Knowledgebase. Co-inhibition by PD-1 (R-HSA-389948). Disponible en: [reactome.org/content/detail/R-HSA-389948](https://reactome.org/content/detail/R-HSA-389948). Consultado el 2 de octubre de 2026.
8. U.S. Food and Drug Administration. Fichas técnicas de los inhibidores de puntos de control (prescribing information), sección 12.1 Mechanism of Action; consultadas en openFDA. Disponible en: [open.fda.gov/apis/drug/label/](https://open.fda.gov/apis/drug/label/). Consultado el 2 de octubre de 2026. Fichas (producto, set id y fecha de la versión): atezolizumab (Tecentriq, 6fa682c9-a312-4932-9831-f286908660ee, 2026-05-20); nivolumab (Opdivo, f570b9c4-6846-4de2-abfa-4d0a4ae4e394, 2026-08-12); pembrolizumab (Keytruda, 9333c79b-d487-4538-a9f0-71b91a02b287); cemiplimab (Libtayo, 4347ae1f-d397-4f18-8b70-03897e1c054a, 2026-08-31); tremelimumab (Imjudo, 6690679c-be2f-4588-a2e4-89fff74dd6be, 2026-08-31); ipilimumab (Yervoy, 2265ef30-253e-11df-8a39-0800200c9a66, 2026-08-20).
9. Zak KM, Kitel R, Przetocka S, Golik P, Guzik K, Musielak B, et al. Structure of the Complex of Human Programmed Death 1, PD-1, and Its Ligand PD-L1. Structure. 2015;23(12):2341-2348. doi:[10.1016/j.str.2015.09.010](https://doi.org/10.1016/j.str.2015.09.010). PMID [26602187](https://pubmed.ncbi.nlm.nih.gov/26602187/). [PMC4752817](https://pmc.ncbi.nlm.nih.gov/articles/PMC4752817/).
10. U.S. Food and Drug Administration. Drugs@FDA: IMFINZI, BLA 761069. Historial de aprobaciones y cartas de aprobación de los suplementos S-002, S-018, S-029, S-033, S-035, S-036, S-043, S-045, S-049, S-050, S-052 y S-053. Disponible en: [accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overv…](https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overview.process&ApplNo=761069). Consultado el 2 de octubre de 2026.
11. European Medicines Agency. Imfinzi (durvalumab): EPAR, información del producto. EMEA/H/C/004771; autorizado el 21 de septiembre de 2018. Disponible en: [ema.europa.eu/en/medicines/human/EPAR/imfinzi](https://www.ema.europa.eu/en/medicines/human/EPAR/imfinzi). Versión 28, del 18 de mayo de 2026. Consultado el 2 de octubre de 2026.
12. Armijo N, Salas C, Espinoza N, Espinoza M, Balmaceda C. Budget impact analysis of durvalumab consolidation therapy vs no consolidation therapy after chemoradiotherapy in stage III non-small cell lung cancer in the context of the Chilean health care system. PLoS One. 2024;19(7):e0307473. doi:[10.1371/journal.pone.0307473](https://doi.org/10.1371/journal.pone.0307473). PMID [39058755](https://pubmed.ncbi.nlm.nih.gov/39058755/). [PMC11280244](https://pmc.ncbi.nlm.nih.gov/articles/PMC11280244/).
13. Antonia SJ, Villegas A, Daniel D, Vicente D, Murakami S, Hui R, et al. Durvalumab after Chemoradiotherapy in Stage III Non-Small-Cell Lung Cancer. N Engl J Med. 2017;377(20):1919-1929. doi:[10.1056/NEJMoa1709937](https://doi.org/10.1056/NEJMoa1709937). PMID [28885881](https://pubmed.ncbi.nlm.nih.gov/28885881/).
14. Kareff SA, Han S, Haaland B, Jani CJ, Kohli R, Aguiar PN Jr, et al. International Cost-Effectiveness Analysis of Durvalumab in Stage III Non-Small Cell Lung Cancer. JAMA Netw Open. 2024;7(5):e2413938. doi:[10.1001/jamanetworkopen.2024.13938](https://doi.org/10.1001/jamanetworkopen.2024.13938). PMID [38814640](https://pubmed.ncbi.nlm.nih.gov/38814640/). [PMC11140532](https://pmc.ncbi.nlm.nih.gov/articles/PMC11140532/).
15. National Institute for Health and Care Excellence (NICE). Durvalumab for maintenance treatment of unresectable non-small-cell lung cancer after platinum-based chemoradiation. Technology appraisal guidance TA798; 2022. Disponible en: [nice.org.uk/guidance/ta798](https://www.nice.org.uk/guidance/ta798). Consultado el 2 de octubre de 2026.
16. National Institute for Health and Care Excellence (NICE). Durvalumab with gemcitabine and cisplatin for treating unresectable or advanced biliary tract cancer. Technology appraisal guidance TA944; 2024. Disponible en: [nice.org.uk/guidance/ta944](https://www.nice.org.uk/guidance/ta944). Consultado el 2 de octubre de 2026.
17. Zukin M, Gondim V, Shimada AK, Lima EMEA, Mathias C, Barra WF, et al. Durvalumab as consolidation therapy in patients who received chemoradiotherapy for unresectable stage III NSCLC: Real-world data from an expanded access program in Brazil (LACOG 0120). J Bras Pneumol. 2025;50(6):e20240228. doi:[10.36416/1806-3756/e20240228](https://doi.org/10.36416/1806-3756/e20240228). PMID [39813498](https://pubmed.ncbi.nlm.nih.gov/39813498/). [PMC12063600](https://pmc.ncbi.nlm.nih.gov/articles/PMC12063600/).
18. Girard N, Bar J, Baas P, Chouaid C, Christoph DC, Field JK, et al. Real-world 5-year outcomes with durvalumab after chemoradiotherapy in unresectable stage III NSCLC. ESMO Open. 2026;11(2):106070. doi:[10.1016/j.esmoop.2026.106070](https://doi.org/10.1016/j.esmoop.2026.106070). PMID [41643268](https://pubmed.ncbi.nlm.nih.gov/41643268/). [PMC12919254](https://pmc.ncbi.nlm.nih.gov/articles/PMC12919254/).
19. National Cancer Institute. NCI Thesaurus: Durvalumab (C103194). Disponible en: [ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary…](https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&code=C103194). Consultado el 2 de octubre de 2026.

<!-- bibliografia: fin -->

**Ilustraciones:** Servier Medical Art (CC BY 3.0 y 4.0), incluido el linfocito T vía Bioicons. Estructuras de RCSB PDB (CC0).

## Cómo se buscó

<!-- busqueda: inicio -->

Búsqueda realizada el 2 de octubre de 2026 con las herramientas de la skill (`fuentes.py`), 30 consultas en total.

- **Fuentes consultadas:** openFDA (7); páginas web (5); PubMed (5); UniProt (3); ema_medicamento (2); nci_tesauro (2); CIMA (AEMPS) (1); Drugs@FDA (1); Reactome (1); ensayos (1); ensayo (1); livertox (1).
- **Búsquedas de literatura:**
  - PubMed: `39813498[uid]` (1 resultado)
  - PubMed: `41643268[uid]` (1 resultado)
  - PubMed: `25943534[uid] OR 28717238[uid] OR 26602187[uid]` (3 resultados)
  - PubMed: `("durvalumab"[tiab] AND ("Cost-Benefit Analysis"[MeSH] OR "Quality-Adjusted Life Years"[MeSH] OR "Costs and Cost Analysis"[MeSH] OR cost-effectiveness[tiab] OR "budget impact"[tiab] OR cost-utility[tiab])) AND ("Latin America"[MeSH] OR "Central America"[MeSH] OR "South America"[MeSH] OR "Mexico"[MeSH] OR "Caribbean Region"[MeSH] OR "Costa Rica"[tiab] OR "Latin America"[tiab])` (2 resultados)
  - PubMed: `("durvalumab"[tiab] AND ("Observational Study"[pt] OR "real-world"[tiab] OR "real world"[tiab] OR registry[tiab] OR cohort[tiab] OR "routine clinical practice"[tiab])) AND ("Latin America"[MeSH] OR "Central America"[MeSH] OR "South America"[MeSH] OR "Mexico"[MeSH] OR "Caribbean Region"[MeSH] OR "Costa Rica"[tiab] OR "Latin America"[tiab])` (2 resultados)
- **Criterios:** guías y consensos de los últimos 5 años, con prioridad para el texto completo; cada cifra se comprobó en la frase original de la fuente (registro de evidencias).

<!-- busqueda: fin -->

## No verificado

- **ChEMBL:** el servidor (www.ebi.ac.uk) devolvió error 500 durante la consulta. El mecanismo y la diana se confirmaron con la ficha técnica, la FDA, el NCI Thesaurus y UniProt. *[@nci]* No se incluyen datos de afinidad (Kd).

Queda, como en todo prototipo, la revisión farmacológica del nivel y los mensajes para estudiantes de pregrado.
