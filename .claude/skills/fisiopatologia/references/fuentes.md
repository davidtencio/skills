# Fuentes: qué aporta cada una y en qué orden consultarlas

**Orden de verificación de datos:**

1. Definición de la enfermedad (MeSH, MONDO).
2. Fisiopatología (revisiones con texto completo en PMC, Reactome, UniProt).
3. Clínica y diagnóstico (guías y páginas de sociedades científicas, NIDDK y otros institutos del NIH, OMS, OPS, MedlinePlus).
4. Tratamiento:
   - Guías o consensos de acceso abierto, buscados con `fuentes.py guias`.
   - Fichas técnicas de los fármacos para el mecanismo: FDA sección 12.1 (`fuentes.py openfda`) y CIMA 5.1 (`fuentes.py cima`).
5. Literatura (PubMed, Europe PMC, con PMID).
6. Fuentes en otros idiomas (guías nacionales, literatura con filtro de idioma), traducidas al español: ver `idiomas.md`.
7. Si nada de lo anterior lo confirma, el dato queda como «pendiente de verificar».

| Papel | Fuente preferida | Alternativas | Herramienta |
|---|---|---|---|
| Definición y sinónimos | MeSH (NLM, NIH), con la nota de alcance | MONDO (EBI OLS), NCI Thesaurus | `fuentes.py mesh`, `mondo`, `nci` |
| Fisiopatología | Revisión de referencia con texto completo en PMC | Resúmenes de PubMed; Europe PMC | `fuentes.py pubmed`, `pmc <PMCID> <regex…>` |
| Vías moleculares | Reactome | UniProt (función con PMID), NCBI Gene | `fuentes.py reactome`, `uniprot`, `gen` |
| Criterios diagnósticos | Página de la sociedad científica (p. ej., diabetes.org) o del instituto del NIH (p. ej., NIDDK) | Guía de práctica clínica en PMC | `fuentes.py pagina`, `pmc` |
| Síntomas y complicaciones | OMS (notas descriptivas), NIDDK | MedlinePlus (español), OPS | `fuentes.py pagina`, `medlineplus` |
| Algoritmo de tratamiento | Guía o consenso de acceso abierto (texto completo en PMC) | Resumen de la guía en PubMed | `fuentes.py guias`, `pmc` |
| Mecanismo de cada fármaco | Ficha de la FDA, sección 12.1 | CIMA 5.1 | `fuentes.py openfda`, `cima` |
| Guías nacionales en otros idiomas | Käypä hoito, NVL/AWMF, Helsedirektoratet, HAS, Farmacotherapeutisch Kompas (ver `idiomas.md`) | PubMed con filtro de idioma (`ger[la]`, `fin[la]`…) | `fuentes.py pagina`, `pdf`, `pubmed` |
| Afirmaciones sueltas | PubMed (por relevancia) y Europe PMC (por citas) | — | `fuentes.py pubmed`, `europepmc` |
| Órganos, tejidos y células | Biblioteca local (`assets/ilustraciones/`) | Bioicons (Servier), kits de Servier; TogoTV y Wikimedia Commons (ver «Bibliotecas de imágenes en otros idiomas» en `idiomas.md`) | `recursos.py`, `fuentes.py bioicons`, `servier-*`, `togopic`, `commons` |
| Flechas, pasos, rótulos, tarjetas | Biblioteca propia | — | `componentes.py`, `piezas.py` |

## Infecciones

Las fuentes de arriba sirven igual; además, en una enfermedad infecciosa:

| Papel | Fuente preferida | Alternativas | Herramienta |
|---|---|---|---|
| Agente, transmisión, clínica y prevención | Notas descriptivas de la OMS | NIAID (niaid.nih.gov), OPS (paho.org), MedlinePlus | `fuentes.py pagina`, `medlineplus` |
| Tratamiento | Guías de la IDSA (idsociety.org) y de la ESCMID con texto completo en PMC; guías de la OMS y la OPS | Guías nacionales en otros idiomas (ver `idiomas.md`) | `fuentes.py guias`, `pmc`, `pagina` |
| VIH | Guías del NIH/HHS (clinicalinfo.hiv.gov) | Guías de la OMS; EACS (eacsociety.org) | `fuentes.py pagina` |
| Tuberculosis, malaria, enfermedades desatendidas | Guías y manuales de la OMS | OPS, guías nacionales | `fuentes.py pagina` |
| Farmacocinética de un antimicrobiano | Ficha de la FDA, sección 12.3 (campo `pharmacokinetics`) | CIMA 5.2 | `fuentes.py openfda`, `cima` |
| Índices y objetivos FC/FD por familia | Documento de posición sobre monitorización de antimicrobianos en pacientes críticos (*Intensive Care Med* 2020, PMID 32383061, texto completo en PMC7223855) | Documentos de justificación de EUCAST (eucast.org/publications-and-documents/rd), que explican los puntos de corte FC/FD de cada fármaco | `fuentes.py pmc`, `pagina` |
| Monitorización de vancomicina | Consenso revisado de 2020 (*Clin Infect Dis*, PMID 32658968; sin texto completo en PMC: usa el resumen y anótalo) | Resumen ejecutivo en *Pharmacotherapy* (PMID 32227354) | `fuentes.py pubmed` |
| Mecanismo y resistencia de un antimicrobiano | Ficha de la FDA, sección 12.4 *Microbiology* (campo `microbiology` en openFDA) | CIMA 5.1; DailyMed «12.4 Microbiology» | `fuentes.py openfda`, `cima`, `dailymed` |
| Puntos de corte de sensibilidad | EUCAST (eucast.org, tablas de puntos de corte) | CLSI (resúmenes públicos) | `fuentes.py pagina` |
| Uso racional de antimicrobianos | Clasificación AWaRe y manual de antibióticos de la OMS | — | `fuentes.py pagina` |
| Resistencia local | Costa Rica: Laboratorio de Antimicrobianos del INCIENSA (vigilancia EVILABRA; ver abajo) | OPS (red ReLAVRA+), GLASS de la OMS, informes de cada hospital | `fuentes.py pagina` |
| Vacunas | Ficha técnica de la vacuna (CIMA, FDA) | Documentos de posición de la OMS; guías nacionales | `fuentes.py cima`, `pagina` |

- **Mecanismo de los antimicrobianos:** en su ficha de la FDA, la sección 12.1 suele decir solo «es un antibacteriano [ver Microbiología (12.4)]». El mecanismo, la resistencia y la actividad están en la 12.4. Las fichas antiguas, sin el formato actual, no tienen el campo `microbiology`: la sección «Microbiology» va dentro de `clinical_pharmacology`. Si `openfda` la corta, búscala con `dailymed` o usa CIMA 5.1.
- **Combinaciones a dosis fija:** `openfda` prefiere la ficha del principio activo solo y, entre varias, la que tiene las secciones pedidas. Si el fármaco solo existe en combinación (p. ej., piperacilina/tazobactam), devuelve una ficha de la combinación: comprueba que la frase citada habla del fármaco que te interesa.
- **Resistencia y elección del tratamiento empírico:** dependen del país. Si la guía usada es extranjera, dilo y busca datos de resistencia de Costa Rica o de Latinoamérica; si no los encuentras, anótalo en «No verificado».
- **Resistencia en Costa Rica:** el Centro Nacional de Referencia de Bacteriología del INCIENSA coordina la vigilancia de laboratorio EVILABRA (perfiles de resistencia por microorganismo, tipo de muestra y tipo de infección, con datos de los laboratorios participantes) y es el punto focal de ReLAVRA+ y centro colaborador de la OMS en resistencia. La descripción está en https://www.inciensa.sa.cr/laboratorio-de-antimicrobianos/ (léela con `fuentes.py pagina`). Los datos se publican en un informe interactivo acumulado (enlazado desde https://www.inciensa.sa.cr/informes-interactivos/; el primero cubre 2018–2022, según la OPS) que se genera con JavaScript: `pagina` no lee sus cifras. Para citar un porcentaje de resistencia, pide a la persona usuaria la cifra del informe (o una captura) con su fecha y anota «INCIENSA, EVILABRA, informe interactivo, consultado el …»; si no está disponible, anótalo en «No verificado». La página de datos de resistencia de la OPS (www3.paho.org/data) respondió con error 502 en octubre de 2026.
- **Objetivos FC/FD:** cópialos con el índice, la familia y la fuente («%fT > CMI», «ABC₀₋₂₄/CMI ≥ …»). Los objetivos cambian según la gravedad y el microorganismo: no los generalices de un fármaco a toda la familia sin que la fuente lo diga.
- **Puntos de corte:** cópialos literalmente con su versión (p. ej., «EUCAST, tabla v. 15.0») y no los conviertas entre EUCAST y CLSI.
- Responden desde este entorno: who.int, paho.org, niaid.nih.gov, idsociety.org, escmid.org, clinicalinfo.hiv.gov, eacsociety.org, eucast.org e inciensa.sa.cr. Algunas son índices de guías: sigue el enlace a la guía o búscala en PMC.

## Cómo leer una guía

- Busca primero las guías de los últimos 5 años con `python3 scripts/fuentes.py guias "<enfermedad en inglés>"`. Si salen muchas guías de otros temas, usa `guias-titulo`, que exige las palabras en el título. Prefiere la que tenga texto completo en PMC (`pmcid` en el resultado).
- Extrae las frases exactas con `python3 scripts/fuentes.py pmc <PMCID> "<regex>" "<regex>"`. Lo pide a NCBI y, si no lo da, a Europe PMC (el campo `fuente` dice cuál). Si devuelve `texto_completo: false`, ninguno lo tiene: usa el resumen y anótalo en «No verificado».
- Si la guía es un PDF (sociedades, ministerios, AWMF, OMS), extrae las frases con `python3 scripts/fuentes.py pdf <URL> "<regex>"`: cada fragmento lleva su página, que se cita en el material («guía S3, p. 11»). Si el resultado trae `aviso`, el PDF es un escaneo sin texto.
- Cita cada recomendación con la guía y el año. No mezcles recomendaciones de guías distintas en un mismo algoritmo sin decirlo.

## No disponibles en este entorno

- **diabetesjournals.org** (Normas de Atención de la ADA): devuelve 403 a consultas automáticas. Usa el consenso ADA/EASD de acceso abierto en PMC y las páginas de diabetes.org.
- **NCBI Bookshelf** (StatPearls): pide captcha.
- **cdc.gov:** devuelve 403 a consultas automáticas. Usa la OMS, el NIAID o MedlinePlus.
- **UpToDate, DynaMed, BMJ Best Practice:** requieren suscripción; no se usan.

Si otro dominio falla, díselo a la persona usuaria nombrando el dominio y sigue con la fuente siguiente.
