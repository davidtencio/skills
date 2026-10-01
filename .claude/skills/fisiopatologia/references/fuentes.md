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
| Guías nacionales en otros idiomas | Käypä hoito, NVL/AWMF, Helsedirektoratet, HAS, Farmacotherapeutisch Kompas (ver `idiomas.md`) | PubMed con filtro de idioma (`ger[la]`, `fin[la]`…) | `fuentes.py pagina`, `pubmed` |
| Afirmaciones sueltas | PubMed (por relevancia) y Europe PMC (por citas) | — | `fuentes.py pubmed`, `europepmc` |
| Órganos, tejidos y células | Biblioteca local (`assets/ilustraciones/`) | Bioicons (Servier), kits de Servier | `recursos.py`, `fuentes.py bioicons`, `servier-*` |
| Flechas, pasos, rótulos, tarjetas | Biblioteca propia | — | `componentes.py`, `piezas.py` |

## Cómo leer una guía

- Busca primero las guías de los últimos 5 años con `python3 scripts/fuentes.py guias "<enfermedad en inglés>"`. Prefiere la que tenga texto completo en PMC (`pmcid` en el resultado).
- Extrae las frases exactas con `python3 scripts/fuentes.py pmc <PMCID> "<regex>" "<regex>"`. Si devuelve `texto_completo: false`, el editor no permite descargarlo: usa el resumen y anótalo en «No verificado».
- Cita cada recomendación con la guía y el año. No mezcles recomendaciones de guías distintas en un mismo algoritmo sin decirlo.

## No disponibles en este entorno

- **diabetesjournals.org** (Normas de Atención de la ADA): devuelve 403 a consultas automáticas. Usa el consenso ADA/EASD de acceso abierto en PMC y las páginas de diabetes.org.
- **NCBI Bookshelf** (StatPearls): pide captcha.
- **UpToDate, DynaMed, BMJ Best Practice:** requieren suscripción; no se usan.

Si otro dominio falla, díselo a la persona usuaria nombrando el dominio y sigue con la fuente siguiente.
