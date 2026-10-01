# Atorvastatina: ¿cómo actúa?

> **Prototipo pendiente de revisión farmacológica.** Material educativo para estudiantes de farmacia; no sustituye la ficha técnica vigente.

Serie de seis láminas (16:9):

1. [¿De dónde viene el colesterol LDL y dónde actúa cada fármaco?](lamina-1.png)
2. [Cómo regula el hepatocito su colesterol](lamina-2.png)
3. [Cómo actúa atorvastatina](lamina-3.png)
4. [Farmacocinética: el hígado es diana y filtro](lamina-4.png)
5. [Del mecanismo al paciente](lamina-5.png)
6. [Del ensayo a la práctica: valor y vida real](lamina-6.png)

## Puntos clave

1. **Diana:** la HMG-CoA reductasa, enzima del retículo endoplásmico que cataliza el paso limitante de la síntesis de colesterol (HMG-CoA → mevalonato). *[UniProt P04035; CIMA 5.1]*
2. **Mecanismo:** atorvastatina es un inhibidor **selectivo y competitivo** de la enzima. Ocupa parte del sitio de unión del HMG-CoA y bloquea el acceso del sustrato. *[CIMA 5.1; PMID 11349148]*
3. **Por qué baja la LDL en sangre:** al disminuir el colesterol dentro del hepatocito, se activa SREBP-2. La célula aumenta la expresión del receptor de LDL y capta más LDL de la sangre. *[CIMA 5.1; Reactome R-HSA-1655829; PMID 20566875]*
4. **Compensación:** SREBP-2 también activa el gen de la propia HMG-CoA reductasa; la célula intenta fabricar más enzima. *[Reactome R-HSA-1655829]*
5. **Magnitud:** reduce el colesterol LDL entre 41 % y 61 % según la dosis. *[CIMA 5.1]*
6. **Potencia y selectividad:** inhibe la enzima a concentraciones nanomolares, con IC50 de 6–13 nM y Ki de 6,2 nM. Para inhibir OATP1B1 (IC50 0,6–1,6 µM) o CYP3A4 (IC50 5,1 µM) hacen falta concentraciones unas 100 a 600 veces mayores. *[ChEMBL CHEMBL1487; BindingDB, PMID 15686906, 23570542, 31188592]*
7. **El hígado es diana y filtro:** entra al hepatocito por el transportador OATP1B1 y allí actúa. La dosis se correlaciona mejor con la reducción de LDL que la concentración en sangre. *[FDA 12.2, 12.3; CIMA 5.2]*

## Recorrido de las láminas

**1. Contexto.** El colesterol procede de la dieta (absorción intestinal) y de la síntesis hepática. El hígado libera lipoproteínas y retira la LDL de la sangre mediante sus receptores. Sitios de acción:

| Fármaco | Mecanismo | Fuente |
|---|---|---|
| Ezetimiba | Inhibe NPC1L1 en el intestino delgado: ↓ absorción de colesterol | FDA 12.1 |
| Estatinas | Inhiben la HMG-CoA reductasa en el hígado | CIMA 5.1 |
| Colesevelam | Secuestra ácidos biliares; el hígado usa más colesterol para fabricarlos | FDA 12.1 |
| Evolocumab / inclisirán | Evitan la degradación del receptor de LDL mediada por PCSK9 | FDA 12.1 |

**2. Fisiología normal.** Acetil-CoA → HMG-CoA → (HMG-CoA reductasa) → mevalonato → varios pasos → colesterol. Con colesterol suficiente, el complejo SREBP-2/SCAP queda retenido en el retículo endoplásmico, la transcripción de los genes LDLR y HMGCR es basal y la célula mantiene pocos receptores de LDL. *[Reactome R-HSA-1655829]*

**3. Con atorvastatina.**

1. Inhibe la enzima y baja el colesterol intracelular.
2. SREBP-2 viaja del retículo al Golgi, se activa y entra al núcleo.
3. Aumenta la transcripción del gen LDLR (y de HMGCR).
4. Hay más receptores de LDL en la membrana, que captan más LDL de la sangre.

Las estructuras reales del sitio activo provienen de PDB 1DQ9 (enzima humana con HMG-CoA) y PDB 1HWK (enzima humana con atorvastatina), superpuestas para verlas desde el mismo ángulo. La potencia (IC50 de 6–13 nM) coincide en ChEMBL y BindingDB.

**4. Farmacocinética.** El recorrido de una dosis:

1. Se absorbe en el intestino (Cmax en 1–2 h) y llega al hígado por la vena porta. *[CIMA 5.2]*
2. Entra al hepatocito por OATP1B1 y OATP1B3. Sus metabolitos también son sustratos de OATP1B1. *[CIMA 5.2; FDA 12.3]* OATP1B1 está codificado por el gen *SLCO1B1*, específico del hígado, cuyos polimorfismos reducen su función. *[NCBI Gene 10599]*
3. Dentro del hepatocito inhibe la HMG-CoA reductasa, y CYP3A4 lo transforma en metabolitos orto- y parahidroxilados. Estos son igual de activos y aportan ~70 % de la actividad circulante. *[FDA 12.3]*
4. Se elimina sobre todo por la bilis. Los transportadores de salida BCRP y P-gp limitan la absorción y el aclaramiento biliar. *[CIMA 5.2]*
5. A la sangre llega poco: biodisponibilidad ~12–14 % y actividad inhibitoria sistémica ~30 %. *[CIMA 5.2; FDA 12.3]*

Mensaje de la lámina: el primer paso hepático no es una pérdida, porque lleva el fármaco a donde actúa. *[FDA 12.2: «el hígado es el lugar principal de acción»]*

## Farmacocinética e interacciones *[CIMA 4.2, 4.5, 5.2; FDA 12.2, 12.3]*

- Absorción rápida (Cmax en 1–2 h). Biodisponibilidad absoluta ~12 % (CIMA) o ~14 % (FDA) por aclaramiento presistémico y primer paso hepático.
- Se puede tomar a cualquier hora del día, con o sin alimentos (FDA 2.1).
- Unión a proteínas ≥ 98 %. Metabolismo por CYP3A4 a derivados orto- y parahidroxilados activos, responsables de ~70 % de la actividad inhibitoria circulante.
- Semivida de ~14 h; la actividad inhibitoria dura de 20 a 30 h por los metabolitos.
- Eliminación principalmente biliar, sin recirculación enterohepática; menos del 2 % se recupera en la orina.
- Es sustrato de OATP1B1/1B3, P-gp y BCRP.
- **Inhibidores de CYP3A4** (claritromicina, itraconazol, ketoconazol, inhibidores de la proteasa del VIH) e **inhibidores de OATP1B1** (ciclosporina) aumentan su concentración y el riesgo de miopatía. No se recomienda el jugo de toronja (FDA 5.1). La ciclosporina y glecaprevir/pibrentasvir no se recomiendan o están contraindicados.

## Farmacogenética *[CPIC, PMID 35152405]*

CPIC clasifica el par *SLCO1B1*–atorvastatina en el nivel A, el que tiene recomendación de prescripción. Con un OATP1B1 menos funcional entra menos fármaco al hígado, aumenta la exposición en sangre y puede subir el riesgo de miopatía.

| Fenotipo de SLCO1B1 | Recomendación de CPIC |
|---|---|
| Función normal o aumentada | Dosis inicial habitual |
| Función disminuida o posiblemente disminuida | Iniciar con ≤ 40 mg; vigilar la miopatía, sobre todo con 40 mg |
| Función pobre | Iniciar con ≤ 20 mg; si hace falta más, valorar rosuvastatina o una combinación |

Otros genes (CYP3A4, CYP3A5, HMGCR y otros) tienen niveles C o D en CPIC: no hay recomendación de prescripción.

## Farmacoeconomía (prioridad: Costa Rica y Latinoamérica)

Cada cifra depende del país, el año, la moneda, el comparador y el umbral de disposición a pagar. No es trasladable sin ajustes.

- **Medicamento esencial:** la Lista Modelo de la OMS incluye atorvastatina como equivalente terapéutico de simvastatina y en polipíldoras para prevención cardiovascular (con AAS y ramipril, o con perindopril y amlodipino). *[OMS, eEML]*
- **Compra conjunta en las Américas:** el Fondo Estratégico de la OPS incluye atorvastatina de 40 y 80 mg; en la lista de 2026 aún no tiene precio publicado. *[OPS, precios de referencia del Fondo Estratégico, 2026]*
- **Brasil (SUS), 2015:** modelo de Markov con datos de 136 000 pacientes y un umbral igual al PIB per cápita (~Int$ 11 770).
  - Intensidad intermedia (p. ej., atorvastatina 10 mg): menos de Int$ 10 000 por AVAC en todos los escenarios.
  - Alta intensidad frente a intermedia: más de Int$ 27 000 por AVAC.

  *[PMID 25409878]*
- **Brasil y Colombia, 2014:** con precios reales de cada país, rosuvastatina frente a atorvastatina costaría más de 700 000 $ por AVAC en prevención primaria y más de 200 000 $ en secundaria en Colombia, con resultados parecidos. En Brasil, los precios eran similares y las razones resultaron menores. *[PMID 29702787]*
- **Reino Unido (NICE NG238, 2023):** las estatinas de alta intensidad son clínicamente eficaces y coste-efectivas frente a no tratar o a intensidades menores. NICE recomienda atorvastatina 20 mg en prevención primaria con QRISK3 ≥ 10 %. *[NICE NG238]*
- **Precio de referencia de un genérico (EE. UU., septiembre de 2026):** entre 0,023 US$ (10 mg) y 0,069 US$ (80 mg) por comprimido. *[NADAC, Medicaid]*

## Estudios de vida real

Los estudios observacionales muestran asociaciones, no causas; complementan los ensayos clínicos.

- **Costa Rica (CRELES):** en una muestra nacional de 542 personas de 60 años o más con diabetes, el 78 % tenía LDL ≥ 100 mg/dl. Los datos se publicaron en 2008. La eficacia demostrada en ensayos no garantiza el control en la población. *[PMID 18447930]*
- **Brasil, hospital público terciario:**
  - 9 594 pacientes con estatina en un año. El 18 % no tenía LDL reciente, el 17,1 % tenía LDL de 130–190 mg/dl y el 2,4 % ≥ 190 mg/dl.
  - Solo se usaban simvastatina (77,6 %) y atorvastatina.

  *[PMID 33886720]*
- **Brasil (ELSA-Brasil MSK):** en 2 156 personas no hubo asociación global entre el uso de estatinas y el dolor o la debilidad muscular. En un análisis secundario, atorvastatina se asoció con debilidad en una de las dos pruebas. *[PMID 37261675]*
- **Registros en marcha o terminados:** ClinicalTrials.gov lista un estudio observacional de vida real sobre el uso de estatinas en la atención primaria de Brasil (NCT05285085). El catálogo de la EMA tiene 5 estudios posautorización con atorvastatina, de Japón.

## Efectos adversos y contraindicaciones *[CIMA 4.3, 4.8]*

- **Frecuentes:** nasofaringitis, reacciones alérgicas, hiperglucemia, cefalea, molestias digestivas, mialgia, artralgia, dolor en extremidades.
- **Raras:** miopatía, miositis, rabdomiólisis. Consultar ante dolor o debilidad muscular inexplicable.
- **Hepáticos:** aumento de transaminasas; hepatitis poco frecuente. Según LiverTox, las elevaciones suelen ser leves, asintomáticas y autolimitadas, y la lesión hepática clínicamente evidente es rara. *[LiverTox, PMID 31643561]*
- **Lactancia:** LactMed recuerda que el consenso es no amamantar durante el tratamiento y preferir otra opción, sobre todo con recién nacidos o prematuros. *[LactMed, PMID 30000420]*
- **Contraindicada en:** enfermedad hepática activa, embarazo, lactancia, mujeres en edad fértil sin anticoncepción adecuada, y con glecaprevir/pibrentasvir.

## Indicaciones aprobadas por la FDA *[Drugs@FDA, NDA 020702 (Lipitor); ficha de la FDA del 15/04/2024]*

No hay indicaciones nuevas recientes. La última ampliación de indicación de la FDA fue en octubre de 2002: hipercolesterolemia familiar heterocigota en adolescentes de 10 a 17 años, con 10–20 mg al día (suplemento S-033). Los suplementos posteriores revisaron la ficha sin añadir indicaciones.

## Clase farmacológica

Inhibidores de la HMG-CoA reductasa (estatinas), código ATC C10AA05. Otras estatinas: simvastatina, rosuvastatina, pravastatina, pitavastatina, fluvastatina, lovastatina.

## Error frecuente

«La estatina saca el colesterol de la sangre». **Falso:** inhibe la síntesis de colesterol en el hígado. La LDL baja porque el hepatocito, con menos colesterol, fabrica más receptores de LDL y la capta de la sangre.

## Pregunta de autoevaluación

¿Por qué una estatina reduce menos la LDL en un paciente sin receptores de LDL funcionales (hipercolesterolemia familiar homocigótica con mutaciones nulas del receptor)?

<details>
<summary>Respuesta</summary>

Porque buena parte del efecto depende de que el hepatocito aumente sus receptores de LDL en respuesta al déficit de colesterol intracelular. Si el receptor no es funcional, ese aumento no se traduce en mayor captación de LDL. Por eso estos pacientes necesitan tratamientos combinados u otras alternativas (CIMA 4.1 menciona la combinación con aféresis de LDL).
</details>

## Simplificaciones de las láminas

- Sin escala; la vía de síntesis se resume (los pasos entre mevalonato y colesterol no se dibujan).
- El receptor de LDL y SREBP-2/SCAP se representan con ilustraciones genéricas de proteínas.
- Las estructuras químicas se dibujan sin estereoquímica.
- Las superficies de la enzima muestran solo la región del sitio activo (radio de 16 Å), cortada para ver el ligando.
- En la lámina 4, OATP1B1, BCRP/P-gp y CYP3A4 son ilustraciones genéricas de proteínas. Los valores de IC50 vienen de ensayos in vitro y no equivalen a concentraciones en el paciente.

## Glosario

- **AAS:** Ácido acetilsalicílico.
- **Acetil-CoA:** Acetil-coenzima A, molécula de partida de la síntesis de colesterol.
- **ATC:** Clasificación Anatómica, Terapéutica y Química de la OMS.
- **AVAC:** Año de vida ajustado por calidad (en inglés, QALY).
- **BCRP:** Proteína de resistencia del cáncer de mama, transportador de salida de fármacos.
- **BRISA:** Base Regional de Informes de Evaluación de Tecnologías en Salud de las Américas (OPS).
- **CIMA:** Centro de Información de Medicamentos de la AEMPS, donde se consultan las fichas técnicas españolas.
- **CPIC:** Clinical Pharmacogenetics Implementation Consortium, consorcio que publica guías de farmacogenética.
- **CRELES:** Estudio de Longevidad y Envejecimiento Saludable de Costa Rica.
- **CYP3A4:** Isoenzima 3A4 del citocromo P450.
- **CYP3A5:** Isoenzima 3A5 del citocromo P450.
- **eEML:** Lista Modelo de Medicamentos Esenciales de la OMS en formato electrónico.
- **ELSA-Brasil:** Estudio Longitudinal de Salud del Adulto, cohorte de Brasil.
- **EMA:** Agencia Europea de Medicamentos.
- **EPAR:** Informe público europeo de evaluación de la EMA.
- **FDA:** Administración de Alimentos y Medicamentos de EE. UU.
- **HMG-CoA:** 3-hidroxi-3-metilglutaril-coenzima A, sustrato de la enzima que bloquean las estatinas.
- **HMGCR:** HMG-CoA reductasa (enzima y gen), diana de las estatinas.
- **IC50:** Concentración que inhibe el 50 % de la actividad medida (in vitro).
- **LDL:** Lipoproteína de baja densidad.
- **LDLR:** Receptor de LDL.
- **MSK:** Musculoesquelético (subestudio del ELSA-Brasil).
- **NADAC:** Costo medio nacional de adquisición de medicamentos en EE. UU. (Medicaid).
- **NCBI:** Centro Nacional de Información Biotecnológica de EE. UU.
- **NDA:** Solicitud de autorización de un fármaco nuevo ante la FDA (New Drug Application).
- **NICE:** Instituto Nacional para la Excelencia en Salud y Atención del Reino Unido.
- **NPC1L1:** Proteína Niemann-Pick C1-like 1, que absorbe colesterol en el intestino.
- **OATP1B1:** Polipéptido transportador de aniones orgánicos 1B1, captación hepática (gen SLCO1B1).
- **OATP1B3:** Polipéptido transportador de aniones orgánicos 1B3, captación hepática.
- **OH:** Grupo hidroxilo (orto-OH y para-OH: metabolitos hidroxilados).
- **OMS:** Organización Mundial de la Salud.
- **OPS:** Organización Panamericana de la Salud.
- **PCSK9:** Proproteína convertasa subtilisina/kexina tipo 9, que degrada el receptor de LDL.
- **PDB:** Protein Data Bank, banco de estructuras tridimensionales de proteínas.
- **P-gp:** Glucoproteína P, transportador de salida de fármacos.
- **PIB:** Producto interno bruto.
- **PMID:** Identificador de un artículo en PubMed.
- **QRISK3:** Calculadora británica del riesgo cardiovascular a 10 años.
- **RE:** Retículo endoplásmico.
- **RedETSA:** Red de Evaluación de Tecnologías en Salud de las Américas.
- **SCAP:** Proteína activadora del corte de SREBP.
- **SLCO1B1:** Gen que codifica el transportador OATP1B1.
- **SREBP-2:** Proteína 2 de unión al elemento regulador de esteroles, factor de transcripción.
- **SUS:** Sistema Único de Salud de Brasil.
- **VIH:** Virus de la inmunodeficiencia humana.

## Fuentes

- AEMPS, CIMA: ficha técnica de atorvastatina (secciones 4.1–4.8, 5.1, 5.2).
- FDA, DailyMed y openFDA: fichas técnicas de atorvastatina (12.2, 12.3), ezetimiba, colesevelam, evolocumab e inclisirán (sección 12).
- UniProt P04035 (HMGCR) y Q12772 (SREBF2).
- Reactome R-HSA-1655829, «Regulation of cholesterol biosynthesis by SREBP (SREBF)».
- NCBI Gene 10599 (*SLCO1B1*).
- ChEMBL CHEMBL1487, actividades frente a HMGCR, OATP1B1 y CYP3A4. BindingDB, afinidades frente a P04035 (PMID 15686906, 23570542, 31188592).
- CPIC: guía de *SLCO1B1*, *ABCG2*, *CYP2C9* y estatinas (PMID 35152405).
- LiverTox: atorvastatina (PMID 31643561). LactMed: atorvastatina (PMID 30000420).
- OMS, Lista Modelo de Medicamentos Esenciales (eEML). OPS, precios de referencia del Fondo Estratégico (2026). NICE NG238 (2023). NADAC, Medicaid (septiembre de 2026).
- Farmacoeconomía: PMID 25409878 (Brasil) y 29702787 (Brasil y Colombia). Vida real: PMID 18447930 (Costa Rica), 33886720 y 37261675 (Brasil). ClinicalTrials.gov NCT05285085. Catálogo de estudios de vida real de la EMA.
- Istvan ES, Deisenhofer J. Structural mechanism for statin inhibition of HMG-CoA reductase. *Science* 2001. PMID 11349148.
- Marquart TJ et al. miR-33 links SREBP-2 induction to repression of sterol transporters. *PNAS* 2010. PMID 20566875.
- RCSB PDB 1DQ9 y 1HWK (CC0). PubChem CID 60823, 445127, 449 y 5997.
- Ilustraciones: Servier Medical Art (CC BY 3.0 y 4.0).

## No verificado

Nada. Todos los datos se comprobaron en las fuentes citadas. No se incluyeron informes de BRISA/RedETSA (el sitio rechaza las consultas automáticas). Atorvastatina no tiene informe de evaluación de la EMA (EPAR) porque se autorizó por procedimientos nacionales. Los datos de farmacocinética se tomaron de las fichas técnicas de CIMA y de la FDA.

Queda, como en todo prototipo, la revisión farmacológica del nivel y los mensajes para estudiantes de pregrado.
