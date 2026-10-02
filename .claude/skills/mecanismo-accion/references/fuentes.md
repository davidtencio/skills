# Fuentes: qué aporta cada una y en qué orden consultarlas

**Orden de verificación de datos:** ficha técnica (CIMA en español, luego FDA/EMA) → bases curadas (ChEMBL, PubChem, UniProt) → Reactome → NIH (NCBI Gene, NCI Thesaurus, MedlinePlus) → farmacodinamia cuantitativa (ChEMBL actividades, BindingDB) → farmacocinética detallada (openFDA, EPAR de la EMA) → farmacogenética y poblaciones especiales (CPIC, LactMed, LiverTox) → literatura (PubMed y Europe PMC, con PMID) → fuentes en otros idiomas, traducidas al español (ver `idiomas.md`) → «pendiente de verificar». No disponibles en este entorno: Guide to Pharmacology (pide autenticación), DrugBank (bloqueado; licencia restrictiva), PharmGKB (no responde; CPIC cubre sus guías) el texto de NCBI Bookshelf (captcha; LiverTox y LactMed se leen a través de PubMed), CCSS (www.ccss.sa.cr corta las conexiones desde la nube) y BRISA/LILACS (pesquisa.bvsalud.org responde 403 a consultas automáticas), que no dependen de la configuración de red del entorno y solo se pueden consultar con el navegador de la persona usuaria y CDA-AMC y OpenPrescribing (bloquean consultas automáticas).

Cada pieza de una lámina tiene una fuente preferida. Mezclarlas permite aprovechar la fortaleza de cada una; la capa de estilo propia (`componentes.py`) mantiene la coherencia visual.

| Papel | Fuente preferida | Alternativas | Licencia | Herramienta |
|---|---|---|---|---|
| Diana y mecanismo | Ficha técnica en español: CIMA/AEMPS (5.1) | FDA (DailyMed 12.1; en antimicrobianos, 12.4), EMA, ChEMBL | Uso con cita / CC BY-SA 3.0 | `fuentes.py cima`, `dailymed`, `chembl` |
| Indicaciones, PK, interacciones, efectos adversos | CIMA (4.1, 4.2, 4.5, 4.8, 5.2) | DailyMed, EMA | Uso con cita | `fuentes.py cima`, `dailymed` |
| Función de la diana y proteínas de la vía | UniProt (con PMID) | NCBI Gene (NIH), QuickGO | CC BY 4.0 / dominio público | `fuentes.py uniprot`, `gen` |
| Definición revisada del fármaco (mecanismo, diana, clase) | NCI Thesaurus (NIH) | ChEMBL | Dominio público (cita) | `fuentes.py nci` |
| Estado en la UE, fechas y versión del EPAR | Datos públicos de la EMA (estado, autorización, revisión, última actualización, página del EPAR) | CIMA (`autorizacion_europea`) | Uso con cita | `fuentes.py ema` |
| Ensayos pivotales | PubMed: ensayos aleatorizados con el fármaco en el título, fase III y registro primero | Sección 14 de la FDA y 5.1 de la ficha europea (nombran los ensayos de la autorización); ClinicalTrials.gov | Cita con PMID y NCT | `fuentes.py ensayos`, `ensayo <NCT>` |
| Alertas de seguridad | Notas de seguridad de la AEMPS (en `cima`, campo `notas_seguridad`) | Ficha técnica 4.4; FAERS solo orienta | Uso con cita | `fuentes.py cima` |
| Indicaciones aprobadas en EE. UU. y su historial | Drugs@FDA (suplementos de eficacia y cartas de aprobación) + openFDA (sección 1 vigente y «Recent Major Changes») | CIMA 4.1 para comparar con la UE | Dominio público | `fuentes.py fda-indicaciones` |
| Potencia y selectividad (IC50, Ki) | ChEMBL, actividades | BindingDB (segunda fuente) | CC BY-SA 3.0 / CC BY 3.0 (cita) | `fuentes.py actividad`, `fuentes.bindingdb` |
| Farmacocinética detallada, exposición-respuesta | EPAR de la EMA (autorización centralizada) | openFDA (ficha FDA por secciones) | Uso con cita / dominio público | `fuentes.py epar`, `openfda` |
| Farmacogenética | CPIC (nivel A/B: hay recomendación) | Sección de farmacogenómica de la FDA | CC0 | `fuentes.py cpic` |
| Lactancia | LactMed (NICHD, NIH) | Ficha técnica 4.6 | Dominio público | `fuentes.py lactmed` |
| Hepatotoxicidad | LiverTox (NIDDK, NIH; si el fármaco no tiene monografía propia, la de su clase) | Ficha técnica 4.4 y 4.8 | Dominio público | `fuentes.py livertox` |
| Farmacoeconomía (prioridad Latinoamérica) | PubMed con filtros MeSH de evaluación económica y de Latinoamérica | NICE, OMS (eEML), OPS (Fondo Estratégico), NADAC; CONITEC, IETS, CONETEC, CENETEC, IETSI, HAS, G-BA, ICER, PBAC (`valor.py agencias`) | Cita con país, año y moneda | `valor.py economia`, `nice`, `eml`, `ops`, `nadac` |
| Estudios de vida real | PubMed (estudios observacionales, prioridad Latinoamérica) | ClinicalTrials.gov (observacionales), catálogo de vida real de la EMA | Cita con diseño y tamaño | `valor.py vida-real`, `observacionales`, `ema-rwd` |
| Orientación sobre efectos adversos notificados | FAERS (openFDA) | — | Dominio público; no da frecuencias | `fuentes.py openfda-eventos` |
| Fichas y formularios de otros países | Felleskatalogen, pro.medicin.dk, Farmacotherapeutisch Kompas, FASS, base pública francesa (ver `idiomas.md`) | PubMed con filtro de idioma (`ger[la]`, `nor[la]`…) | Cita con idioma; traducción propia | `fuentes.py pagina`, `pubmed` |
| Lenguaje para pacientes en español | MedlinePlus (NLM, NIH) | — | Dominio público (cita) | `fuentes.py medlineplus` |
| Secuencia de pasos de la vía | Reactome | Texto de referencia | CC BY 4.0 | `fuentes.py reactome` |
| Afirmaciones que no estén en las anteriores | PubMed (NCBI, por relevancia, admite filtrar revisiones) y Europe PMC (por citas) | Bookshelf (StatPearls) | Cita con PMID | `fuentes.py pubmed`, `europepmc` |
| Estructura química | PubChem (`fuentes.py pubchem`) | ChEMBL, Wikidata (CC0) | Dominio público | `estructuras.py` (RDKit) |
| Forma real de la diana | RCSB PDB con el ligando natural o el fármaco | AlphaFold DB (`alphafold_descargar`) | CC0 / CC BY 4.0 | `superficie.py` |
| Célula, organelos, proteínas genéricas | Biblioteca local (`assets/ilustraciones/`) | Bioicons (Servier) | CC BY 3.0 | `recursos.py` |
| Órganos y tejidos | Kits de Servier (`servier-kits`, `servier-diapositivas`, `servier-extraer`) | NIH BioArt, Bioicons | CC BY 4.0 / dominio público | `fuentes.py` |
| Flechas, pasos, rótulos, bloqueos, ADN | Biblioteca propia | — | Propia | `componentes.py` |

## Antimicrobianos: sección 12.4

En las fichas de la FDA de antibióticos, antivirales, antifúngicos y antiparasitarios, la sección 12.1 suele decir solo que el fármaco es un antimicrobiano «[ver Microbiología (12.4)]». El mecanismo, el espectro de actividad y los mecanismos de resistencia están en la 12.4.

- `fuentes.py dailymed` devuelve la sección «12.4 Microbiology», y `fuentes.py openfda` la devuelve en el campo `microbiology`.
- **Fichas antiguas**, sin el formato actual: no tienen el campo `microbiology`, y su apartado «Microbiology» va dentro de `clinical_pharmacology`. Si `openfda` lo corta, búscalo con `dailymed` o usa CIMA 5.1.
- **Combinaciones a dosis fija:** `openfda`, `dailymed` y `cima` prefieren la ficha del principio activo solo (aunque lleve sal: «METFORMIN HYDROCHLORIDE») y, en CIMA, el original comercializado antes que los genéricos. Si el fármaco solo existe en combinación, devuelven la de la combinación: comprueba en `producto` (openFDA) o en `fuente` que la frase citada habla del fármaco de la lámina.
- **Resistencia:** la 12.4 enumera los mecanismos de resistencia (p. ej., en meropenem: menos porinas, PBP con menor afinidad, bombas de expulsión y carbapenemasas). Sirven para explicar en la lámina por qué el fármaco deja de funcionar, citando la ficha.

## Versiones, fechas y vigencia de lo que se cita

- **Fichas técnicas:** cambian varias veces al año. Cítalas con su versión:
  - CIMA da `fecha_ficha` (las de autorización europea no la tienen: usa la revisión del EPAR con `fuentes.py ema`).
  - DailyMed da `version` y `fecha`; openFDA da `set_id` y `fecha`.
  - `bibliografia.py nueva <carpeta> <clave> --cima|--dailymed|--ema <nombre>` crea la referencia con esos datos.
- **Ensayos:** cita la publicación del resultado principal (PMID) y su registro (NCT): `--pmid` y `--nct`. Comprueba en la ficha (FDA 14, ficha europea 5.1) que es el ensayo de la autorización. Un análisis post hoc o de subgrupos no sustituye al ensayo principal.
- **Revisiones y guías:** antes de usarlas, comprueba con `fuentes.py vigencia <PMID>` si hay una versión posterior, una fe de erratas o una retractación. Lee el texto completo con `fuentes.py texto <PMID|PMCID|DOI> "<regex>"` (PMC y, si no, copias en acceso abierto de Unpaywall).
- **Monografías del NIH:** LiverTox y LactMed traen la fecha de su última revisión (`revisado`).

## Costa Rica

- **Lista Oficial de Medicamentos (LOM) de la CCSS:** no se puede consultar desde este entorno (www.ccss.sa.cr corta la conexión). Si el material la necesita (p. ej., si el fármaco está en la LOM y en qué nivel), pide a la persona usuaria el dato o una captura con su fecha y anótalo; si no, va a «No verificado».
- **Registro sanitario del Ministerio de Salud** (registrelo.go.cr): la página se genera con JavaScript y `pagina` no la lee.
- **BINASSS** (`fuentes.py binasss "<término>"`): protocolos, normas y guías de la CCSS y copias de guías internacionales, en PDF.

## Orden de búsqueda de ilustraciones
1. **Biblioteca local** `assets/ilustraciones/` (consulta `registro.json`). Reutilizar lo ya elegido mantiene la coherencia entre fármacos.
2. **Kits de Servier** (más de 3.000 dibujos vectoriales en ~50 kits por categoría: Endocrinology, Reproduction, Urinary-system, Nervous-system, Heart-physiology, Digestive-system, Intracellular-components, Receptors-channels, Drugs…). Flujo: `servier-kits` → `servier-diapositivas <kit>` (lista grupos de dibujo con títulos) → `servier-extraer <kit> <diapositiva> "<grupo>" <nombre>` (usa `recorte=(x0,y0,x1,y1)` en puntos para una parte). Revisa el resultado con una hoja de comparación.
3. **Bioicons** (`fuentes.py bioicons <término>`): incluye Servier antiguo y otros autores; la licencia está en la carpeta (`cc-0`, `cc-by-3.0`, `cc-by-4.0`, `cc-by-sa-*`).
4. **NIH BioArt** (bioart.niaid.nih.gov): buena alternativa de dominio público.
5. **Dibujo propio** con `componentes.py`, indicándolo en las simplificaciones del material.

## Estructuras químicas
- Obtén SMILES y fórmula con `fuentes.py pubchem`; crea la molécula con `molecula(smiles, formula)` para verificar.
- Si PubChem y otra fuente discrepan en la fórmula o la conectividad, detente y avisa; no elijas por tu cuenta.
- Por defecto se dibuja sin estereoquímica (más legible); actívala (`estereo=True`) si el tema la requiere (p. ej., enantiómeros con actividad distinta).

## Estructura de la diana
- Busca primero un complejo con el fármaco (`pdb-buscar "<diana> <fármaco>"`, luego `pdb-ligandos`). Comprueba el código del ligando: los títulos pueden engañar.
- Si solo existe el complejo con el ligando natural, muéstralo como «Estructura real: PDB XXXX» y dibuja el fármaco como esquema con su rótulo.
- Sin estructura experimental, usa AlphaFold y rotúlalo como «estructura predicha».

## Cuando una fuente no responde
`fuentes.py` lanza un error con el dominio. Informa a la persona usuaria («el entorno bloquea X; puede habilitarlo en la configuración de red») y continúa con la siguiente fuente del orden. Nunca rellenes datos faltantes con suposiciones.
