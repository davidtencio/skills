# Trastuzumab deruxtecán: ¿cómo actúa?

> **Prototipo pendiente de revisión farmacológica.** Material educativo para estudiantes de farmacia; no sustituye la ficha técnica vigente.

Serie de cinco láminas (16:9):

1. [HER2: la diana y los fármacos que actúan sobre ella](lamina-1.png)
2. [Señalización de HER2 y función de la topoisomerasa I](lamina-2.png)
3. [Cómo actúa trastuzumab deruxtecán](lamina-3.png)
4. [Del mecanismo al paciente](lamina-4.png)
5. [Indicaciones aprobadas: de la enfermedad avanzada a la temprana](lamina-5.png)

## Puntos clave

1. **Tipo de fármaco:** es un conjugado anticuerpo-fármaco (ADC). Tiene tres partes:
   - Un anticuerpo IgG1 anti-HER2 con la misma secuencia de aminoácidos que trastuzumab.
   - Un enlazador tetrapeptídico escindible.
   - DXd, un derivado de exatecán que inhibe la topoisomerasa I.

   Lleva unas 8 moléculas de DXd por anticuerpo. *[CIMA, Enhertu 5.1]*
2. **Mecanismo:**
   1. Se une a HER2 en la célula tumoral.
   2. Se internaliza.
   3. En el lisosoma, enzimas que están aumentadas en las células tumorales cortan el enlazador.
   4. DXd queda libre, daña el ADN y la célula muere por apoptosis.

   *[CIMA 5.1; ChEMBL: dos mecanismos, unión a HER2 e inhibición de TOP1]*
3. **Potencia:** DXd es unas 10 veces más potente que SN-38, el metabolito activo de irinotecán. *[CIMA 5.1]*
4. **Otras acciones:** citotoxicidad celular dependiente de anticuerpos (ADCC) e inhibición de la vía PI3K. *[CIMA 5.1]*
5. **Efecto espectador:** DXd atraviesa membranas y puede matar células vecinas, aunque no expresen HER2. Esto se demostró en modelos preclínicos. *[CIMA 5.1; PMID 27166974]*

## Recorrido de las láminas

**1. HER2 y sus fármacos.** HER2 (gen *ERBB2*) es un receptor tirosina cinasa de membrana *[UniProt P04626]*. Su amplificación génica lleva a sobreexpresión y señalización oncogénica *[Reactome R-HSA-1227986]*.

| Fármaco | Dónde actúa | Fuente |
|---|---|---|
| Trastuzumab | Subdominio IV extracelular de HER2 | FDA (Kadcyla 12.1) |
| Pertuzumab | Subdominio II; impide la dimerización | FDA 12.1 |
| Trastuzumab emtansina (T-DM1) | ADC con DM1, que inhibe los microtúbulos | FDA 12.1 |
| Trastuzumab deruxtecán | ADC con DXd (topoisomerasa I) | CIMA 5.1 |
| Lapatinib, tucatinib | Inhiben la cinasa intracelular | FDA 12.1 |

**2. Fisiología normal.**

- **HER2:** no tiene ligando conocido. Actúa formando heterodímeros con otros receptores HER que sí lo tienen, como HER3 activado por neurregulina. El dímero se fosforila y activa las vías MAPK y PI3K/AKT. *[Reactome R-HSA-1227986; UniProt P04626]*
- **Topoisomerasa I:** relaja el ADN superenrollado durante la replicación y la transcripción en tres pasos:
  1. Corta una hebra.
  2. Queda unida a ella de forma transitoria y deja girar la hebra.
  3. Vuelve a unirla.

  *[UniProt P11387]*

**3. Con trastuzumab deruxtecán.** La lámina sigue los cinco pasos del mecanismo:

1. Unión a HER2.
2. Internalización.
3. Corte del enlazador en el lisosoma.
4. Daño del ADN.
5. Efecto espectador.

*[CIMA 5.1; PMID 27166974]*

Estructuras reales:
- **PDB 1N8Z:** HER2 con el Fab de trastuzumab.
- **PDB 1K4T:** topoisomerasa I con ADN y topotecán.

Topotecán es un derivado de la camptotecina, la misma familia que DXd. No hay estructura publicada de la topoisomerasa I con DXd (búsqueda en RCSB PDB), así que la lámina usa topotecán y lo señala.

## Farmacocinética e interacciones *[CIMA 4.5, 5.2]*

- Perfusión intravenosa.
- Semivida de eliminación de unos 7 días, tanto del conjugado como del DXd liberado.
- **Metabolismo:**
  - El anticuerpo se degrada en péptidos, como una IgG endógena.
  - DXd se metaboliza sobre todo por CYP3A4.
- Unión de DXd a proteínas plasmáticas de ~97 %.
- **Interacciones:** ritonavir (inhibidor de OATP1B y CYP3A) e itraconazol (inhibidor potente de CYP3A) aumentan la exposición entre un 10 % y un 20 %. No requieren ajuste de dosis.

## Efectos adversos *[CIMA 4.4, 4.6, 4.8]*

- **Advertencia principal:** enfermedad pulmonar intersticial o neumonitis, con casos mortales. Se debe consultar ante tos, disnea, fiebre o síntomas respiratorios nuevos.
- **Más frecuentes:** náuseas (70 %), fatiga (57 %), vómitos, neutropenia, anemia y alopecia.
- **Embarazo:** comprobar el estado de embarazo antes de iniciar y usar anticoncepción eficaz. No hay datos en embarazadas; la ficha advierte que trastuzumab puede causar daño fetal.

## Indicaciones *[CIMA 4.1]*

Monoterapia en adultos con:
- Cáncer de mama HER2-positivo irresecable o metastásico tras tratamiento previo anti-HER2.
- Cáncer de mama HER2-bajo o HER2-muy bajo, según los criterios de la ficha.
- Cáncer de pulmón no microcítico avanzado con mutación activadora de HER2.
- Adenocarcinoma gástrico o de la unión gastroesofágica HER2-positivo avanzado.
- Tumores sólidos HER2-positivos (IHC 3+) sin otras opciones.

## Indicaciones aprobadas por la FDA: evolución y novedades *[Drugs@FDA, BLA 761139, cartas de aprobación; ficha de la FDA del 15/05/2026]*

| Fecha (FDA) | Indicación aprobada | ¿En la ficha de CIMA? |
|---|---|---|
| 20/12/2019 | Cáncer de mama HER2+ metastásico tras ≥ 2 pautas anti-HER2 (aprobación acelerada) | Sí (hoy, tras ≥ 1 pauta) |
| 15/01/2021 | Adenocarcinoma gástrico o de la unión gastroesofágica HER2+ tras trastuzumab | Sí |
| 04/05/2022 | Cáncer de mama HER2+ metastásico tras 1 pauta anti-HER2 (aprobación regular) | Sí |
| 05/08/2022 | Cáncer de mama HER2-bajo tras quimioterapia | Sí |
| 11/08/2022 | Cáncer de pulmón no microcítico con mutación activadora de HER2 | Sí |
| 05/04/2024 | Tumores sólidos HER2+ (IHC 3+) sin otras opciones (aprobación acelerada) | Sí |
| 27/01/2025 | Cáncer de mama RH+, HER2-bajo o HER2-ultrabajo tras terapia endocrina | Sí |
| 15/12/2025 | Con pertuzumab, en primera línea del cáncer de mama HER2+ metastásico | **No** |
| 15/05/2026 | Cáncer de mama HER2+ temprano, estadio II–III: neoadyuvante (seguido de taxano, trastuzumab y pertuzumab) y adyuvante con enfermedad invasiva residual | **No** |

Mensaje para el estudiante: en siete años, las indicaciones pasaron de la enfermedad metastásica ya tratada a la primera línea y a la enfermedad temprana. La FDA y la EMA aprueban por separado; en Costa Rica rige el registro sanitario nacional.

## Error frecuente

«Es lo mismo que trastuzumab». **Falso.** Comparte el anticuerpo, pero lleva unas 8 moléculas de un citotóxico. No son intercambiables: la ficha técnica pide comprobar la etiqueta del vial para no confundirlo con trastuzumab ni con trastuzumab emtansina. *[CIMA 4.2]*

## Pregunta de autoevaluación

¿Por qué trastuzumab deruxtecán puede ser útil en tumores con poca expresión de HER2 (HER2-bajo), donde trastuzumab solo es poco eficaz?

<details>
<summary>Respuesta</summary>

Su efecto no depende solo de bloquear la señal de HER2. Basta con que entren algunas moléculas del conjugado para liberar DXd dentro de la célula. Además, DXd atraviesa membranas y puede actuar sobre células vecinas (efecto espectador), aunque expresen poco o nada de HER2. *[CIMA 5.1; PMID 27166974]*
</details>

## Simplificaciones de las láminas

- No hay escala entre el anticuerpo, el receptor, el núcleo y las células.
- HER2 se dibuja con cuatro dominios extracelulares, un segmento transmembrana y una cinasa. No se muestran sus cambios de conformación.
- El conjugado se dibuja con pocos rombos; el valor real es de unas 8 moléculas de DXd por anticuerpo.
- Las estructuras químicas (RDKit) se dibujan sin estereoquímica.
- Las superficies proteicas son de estructuras reales, pero recortadas o simplificadas.
- La topoisomerasa I del núcleo es una ilustración genérica de proteína.

## Fuentes

- AEMPS, CIMA: ficha técnica de Enhertu 100 mg, secciones 4.1, 4.2, 4.4, 4.5, 4.6, 4.8, 5.1 y 5.2.
- FDA, DailyMed: fichas técnicas de pertuzumab (Perjeta), trastuzumab emtansina (Kadcyla), lapatinib (Tykerb) y tucatinib (Tukysa), sección 12.1.
- ChEMBL: mecanismos de trastuzumab deruxtecán.
- UniProt P04626 (ERBB2/HER2) y P11387 (TOP1).
- Reactome R-HSA-1227986, «Signaling by ERBB2».
- Ogitani Y et al. Bystander killing effect of DS-8201a. *Cancer Sci* 2016. PMID 27166974.
- RCSB PDB 1N8Z y 1K4T (CC0).
- PubChem CID 117888634 (DXd) y 60700 (topotecán).
- FDA, Drugs@FDA: historial de la BLA 761139 (Enhertu) y cartas de aprobación de los suplementos S-011, S-017/S-020, S-021, S-022, S-028, S-032, S-038 y S-041/S-043. Ficha de la FDA vigente (15/05/2026, openFDA).
- Ilustraciones: Servier Medical Art (CC BY 3.0 y 4.0).

## No verificado

Nada. Todos los datos de las láminas y de este material se comprobaron en las fuentes citadas. Lo que no se pudo confirmar quedó fuera: no hay estructura cristalográfica de la topoisomerasa I con DXd, así que se muestra topotecán y se indica en la lámina.

Queda, como en todo prototipo, la revisión farmacológica del nivel y los mensajes para estudiantes de pregrado.
