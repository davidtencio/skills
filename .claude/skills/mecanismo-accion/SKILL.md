---
name: mecanismo-accion
description: Crea láminas ilustradas del mecanismo de acción de un medicamento para estudiantes de farmacia y un PDF con las láminas y la ficha del mecanismo, con ilustraciones profesionales, estructuras químicas exactas, la diana real (PDB/AlphaFold) y datos verificados (ficha técnica, ChEMBL, PubMed), con farmacoeconomía y datos de vida real, priorizando Costa Rica y Latinoamérica. Úsala siempre que se pida explicar visualmente cómo actúa un fármaco, hacer una imagen, infografía, lámina, esquema o diapositiva de su mecanismo de acción, farmacodinamia o diana, o material didáctico de farmacología, aunque no se mencione la palabra «skill» ni el formato exacto. También cuando se pida la «ficha del mecanismo de acción» o una «ficha técnica» que explique cómo actúa el fármaco; no confundir con la ficha técnica institucional de compra (especificaciones, empaque, rotulación). Tampoco es para explicar una enfermedad (fisiopatología, clínica, diagnóstico y tratamiento en conjunto): eso corresponde a la skill fisiopatologia.
---

# Láminas de mecanismo de acción

Produce una serie de **láminas 16:9** (SVG + PNG; tantas como necesite el fármaco), un **material de apoyo** en Markdown y un **PDF final** con diseño profesional que explican cómo actúa un medicamento a estudiantes de farmacia. El objetivo es que el estudiante entienda la causa (fisiología → acción del fármaco → consecuencias), no que memorice listas.

Hay ejemplos completos en `ejemplos/darolutamida/`, `ejemplos/atorvastatina/`, `ejemplos/trastuzumab-deruxtecan/`, `ejemplos/durvalumab/` y `ejemplos/vutrisiran/` (`laminas.py`, `material.md`, `lamina-N.png` y el PDF). Úsalo como modelo de composición, densidad de texto y tono.

## Principios

- **Exactitud antes que estética.** Cada afirmación se apoya en una fuente (ficha técnica EMA/FDA, ChEMBL, texto de referencia). Las estructuras químicas salen de PubChem y se verifican por fórmula; nunca se dibujan de memoria. Si algo no se puede verificar, se marca como pendiente en lugar de inventarlo.
- **No sugerir precisión que no existe.** Una pose de unión solo se muestra si hay una estructura cristalográfica del complejo. Si no la hay, el fármaco se dibuja con su símbolo (rombo azul) y la lámina dice «Esquema: posición del fármaco no cristalográfica».
- **Cada fuente hace lo que mejor sabe hacer** y una capa de estilo propia (paleta, tipografía, flechas, pasos numerados) unifica el conjunto. Ver `references/fuentes.md`.
- **Fuentes en cualquier idioma, documento en español.** Además del inglés y el español, se pueden usar fuentes en alemán, finés, noruego, sueco, danés, neerlandés, francés, italiano u otros idiomas. Cada dato se verifica en el idioma original y se traduce al español antes de pasar a las láminas, al material y al PDF. Ver `references/idiomas.md`.
- **Verificación autónoma.** La persona usuaria no tiene tiempo de revisar fichas técnicas: la skill debe verificar por sí misma cada dato en las fuentes (ver paso 2) antes de usarlo, y avanzar sin pedir aprobaciones intermedias. Solo se le muestra, al final, una lista breve de lo que no se pudo confirmar en ninguna fuente. Las láminas llevan la marca «Prototipo pendiente de revisión farmacológica» hasta que ella decida retirarla.

## Preparación del entorno

```bash
pip install rdkit playwright python-pptx pymupdf markdown
# Chromium: se usa /opt/pw-browsers/chromium si existe; si no, `playwright install chromium`.
# Para extraer dibujos de los kits de Servier hace falta LibreOffice Impress (paquete libreoffice-impress).
```

Las fuentes en línea pueden estar bloqueadas por la red del entorno. Prueba antes con `python3 scripts/fuentes.py pubchem aspirin`. Si un dominio falla, díselo a la persona usuaria nombrando el dominio (para que lo habilite en la configuración de red) y sigue con la biblioteca local (`assets/ilustraciones/`).

## Flujo de trabajo

### 1. Confirmar el encargo
Fármaco, público (por defecto: estudiantes de farmacia de pregrado) y uso (proyectar, imprimir). Si el fármaco tiene varios mecanismos, acordar cuál se ilustra.

### 2. Investigar y verificar
Verifica cada dato en este orden y anota la fuente exacta (sección de la ficha, PMID, identificador). Solo lo que no aparezca en ninguna queda como «pendiente de verificar»; no lo presentes como confirmado.

1. **Ficha técnica**, primero en español: `python3 scripts/fuentes.py cima <nombre>` (AEMPS; secciones 4.1, 4.2, 4.5, 4.8, 5.1, 5.2, 5.3). Contrasta con `fuentes.py dailymed <nombre en inglés>` (FDA) o con la EMA. Si las fichas difieren en una cifra, muestra el rango y cita ambas.
2. **Fármaco y diana en bases curadas:** `fuentes.py chembl <nombre en inglés>` (mecanismo y diana), `fuentes.py pubchem <nombre>` (SMILES, fórmula, CID del fármaco y de los ligandos o sustratos naturales), `fuentes.py uniprot <GEN>` (función de la diana, con PMID).
3. **Vía biológica:** `fuentes.py reactome "<términos>"` para confirmar la secuencia de pasos de la lámina 2 y los mecanismos compensatorios.
4. **NIH:** `fuentes.py gen <GEN>` (resumen curado de NCBI Gene), `fuentes.py nci <nombre en inglés>` (definición del NCI Thesaurus: mecanismo y diana, sobre todo en oncología) y `fuentes.py medlineplus <nombre>` (información en español para pacientes; útil para el lenguaje de la lámina final).
5. **Farmacodinamia cuantitativa:** `fuentes.py actividad <nombre en inglés> [texto de la diana]` (ChEMBL: IC50, Ki, Kd y EC50 por diana, con mediana y rango) y `fuentes.bindingdb(<UniProt>, <SMILES de PubChem>)` como segunda fuente. Úsalas para dar la potencia sobre la diana y la selectividad frente a otras proteínas medidas, siempre como datos in vitro.
6. **Indicaciones aprobadas por la FDA (siempre):** `fuentes.py fda-indicaciones <nombre en inglés>` devuelve la sección 1 vigente de la ficha de la FDA con su fecha y «Recent Major Changes». Devuelve también el historial de aprobaciones de eficacia de Drugs@FDA, con la fecha y la frase de la carta de aprobación que dice qué se aprobó.
   - Distingue las **indicaciones nuevas** («new indication», «indicated for») de las simples revisiones de ficha.
   - Compara cada indicación con la sección 4.1 de CIMA y marca las que aún no constan en la UE.
   - Si hay indicaciones nuevas en los últimos 3 años o diferencias con la UE, añade la lámina «Indicaciones aprobadas» (línea de tiempo; ejemplo: lámina 5 de trastuzumab deruxtecán). Si no, basta una sección breve en el material.
7. **Farmacocinética detallada:** `fuentes.py openfda <nombre en inglés>` (ficha de la FDA por secciones: 12.2, 12.3, 7, 8, farmacogenómica) y `fuentes.py epar <marca> "<regex>"` (informe de evaluación de la EMA, con página; solo existe para medicamentos de autorización centralizada: biológicos, oncológicos y la mayoría de los nuevos). `fuentes.py openfda-eventos` da las notificaciones de FAERS, que solo orientan y nunca dan frecuencias.
8. **Farmacogenética y poblaciones especiales:** `fuentes.py cpic <nombre en inglés>` (pares gen-fármaco con nivel CPIC y recomendaciones por fenotipo), `fuentes.py lactmed <nombre>` (lactancia) y `fuentes.py livertox <nombre>` (hepatotoxicidad), ambas del NIH y con PMID.
9. **Literatura:** `fuentes.py pubmed "<consulta>" "<regex de la frase>"` (PubMed, por relevancia; incluye revisiones recientes) y `fuentes.py europepmc ...` (ordenado por citas) devuelven frases de resúmenes que respaldan una afirmación concreta; cita el PMID en el material.
10. **Farmacoeconomía y vida real** (para la lámina opcional «Del ensayo a la práctica»), con `scripts/valor.py`, **priorizando Costa Rica y Latinoamérica** y completando con fuentes globales:
   - Evaluaciones económicas y estudios observacionales: `valor.py economia <nombre en inglés> latam` y `valor.py vida-real <nombre en inglés> latam`. Usan PubMed con filtros de Latinoamérica y, si no hay resultados, pasan a la búsqueda global. Lee el resumen completo (`fuentes.pubmed("<PMID>[uid]", completo=True)`) antes de citar una cifra.
   - Medicamento esencial: `valor.py eml`. Fondo Estratégico de la OPS: `valor.py ops`.
   - Agencias: NICE (`valor.py nice`); `valor.py agencias` da las rutas de CONITEC, IETS, CONETEC, CENETEC, IETSI, BRISA/RedETSA, HAS, G-BA, ICER, PBAC y CDA-AMC.
   - Precio de referencia de genéricos: `valor.py nadac`.
   - Registros observacionales: `valor.py observacionales <nombre> latam` (ClinicalTrials.gov) y `valor.py ema-rwd` (catálogo de vida real de la EMA).
   - Cada dato económico lleva país, año, moneda y fuente. Los estudios observacionales se presentan como asociaciones, con su diseño y tamaño.
11. **Estructura de la diana:** `fuentes.py pdb-buscar "<diana> <fármaco>"` y `pdb-ligandos <ID>`; busca un complejo con el fármaco y otro con el sustrato o ligando natural.
12. **Fuentes en otros idiomas:** fichas y formularios de otros países (Felleskatalogen en Noruega, pro.medicin.dk en Dinamarca, Farmacotherapeutisch Kompas en los Países Bajos, FASS en Suecia, la base pública de medicamentos y la HAS en Francia…) y literatura con el filtro de idioma de PubMed (`ger[la]`, `nor[la]`, `fre[la]`…).
   - Úsalas para contrastar la ficha técnica y añadir lo que solo publica un país.
   - Lee las páginas con `fuentes.py pagina <URL> "<regex en el idioma original>"`.
   - Traduce al español antes de usar el dato y cita el idioma de la fuente. Ver `references/idiomas.md`.
13. Si una fuente no responde, nombra el dominio a la persona usuaria y sigue con la siguiente; nunca rellenes el hueco con suposiciones.

### 3. Ficha del mecanismo (documento interno, sin esperar aprobación)
Redacta la ficha con la plantilla de `references/ficha-mecanismo.md`, con la fuente de cada dato, y continúa directamente. No pidas a la persona usuaria que revise la ficha técnica ni que apruebe la ficha. Si un dato no se puede verificar tras recorrer todas las fuentes, **no lo incluyas en las láminas**; anótalo en la lista final del material. Solo pregunta antes de dibujar si hay una decisión que no se puede resolver con fuentes (p. ej., cuál de varios mecanismos ilustrar cuando el encargo es ambiguo).

### 4. Elegir la plantilla y el número de láminas
Según la clase de mecanismo, ver `references/plantillas.md` (receptor nuclear, receptor de membrana, enzima, canal iónico, transportador, conjugado anticuerpo-fármaco, anticuerpo contra un punto de control inmunitario, ARN de interferencia). La serie sigue siempre el mismo arco, pero **el número de láminas no es fijo**: usa las que el fármaco necesite para que cada lámina explique una sola idea (ver «Densidad» en `references/estilo.md`).
1. **Contexto:** de dónde viene la señal y dónde actúa cada fármaco de la vía.
2. **Fisiología normal:** la vía paso a paso en una célula ilustrada.
3. **Mecanismo del fármaco:** el sitio de unión (estructura real si existe) y los puntos de bloqueo en la célula.
4. **Del mecanismo al paciente:** efecto terapéutico, error frecuente, farmacocinética e interacciones, efectos adversos.

Dos añadidos frecuentes:
- **Lámina de farmacocinética** (entre el mecanismo y el paciente) cuando la farmacocinética enseña algo propio: un profármaco, un metabolito activo, un transportador que lleva el fármaco a su lugar de acción, una eliminación que condiciona la dosis. Ejemplo: lámina 4 de atorvastatina.
- **Lámina «Del ensayo a la práctica: valor y vida real»** (al final) cuando haya evaluaciones económicas o estudios de vida real con datos citables. Usa dos columnas de fichas, con farmacoeconomía a la izquierda y vida real a la derecha. Cada ficha lleva país, cifra y fuente con año, y la lámina incluye un recuadro «Cómo leer estos datos». Ejemplo: lámina 6 de atorvastatina.
- **Recuadro de farmacogenética** cuando CPIC tenga un par gen-fármaco de nivel A o B: el gen, qué cambia en el fenotipo de función disminuida y la recomendación. Con niveles C o D no se incluye en las láminas (solo una línea en el material).

Otros casos en los que hacen falta más láminas, por ejemplo: dos mecanismos distintos (una lámina para cada uno), dos vías fisiológicas (p. ej., HER2 y topoisomerasa I), un sitio de unión que merece su propia lámina, un efecto compensatorio o de resistencia relevante, farmacocinética con un concepto propio (profármaco, circulación enterohepática) o efectos adversos que se explican por el mecanismo. Con un mecanismo sencillo pueden bastar tres. Numera «LÁMINA N DE TOTAL» con el total real.

### 5. Reunir y elegir las piezas visuales
Sigue el orden de `references/fuentes.md`: biblioteca local → kits de Servier → Bioicons → NIH BioArt → dibujo propio. Cuando haya varias opciones, genera una hoja de comparación (`python3 scripts/hoja_comparacion.py hoja.png a.svg b.svg ...`), revísala con Read y elige por exactitud, coherencia de estilo y licencia. Registra cada pieza nueva con `fuentes.registrar(...)` (lo hace solo `servier_extraer`).

### 6. Componer
Crea `ejemplos/<farmaco>/laminas.py` a partir del de darolutamida. Bibliotecas disponibles:
- `scripts/recursos.py` → `ilustracion(nombre, x, y, w, h, ...)` para insertar SVG de `assets/ilustraciones/`.
- `scripts/estructuras.py` → `molecula(smiles, formula)` y `estructura(mol, x, y, w, h)` (RDKit).
- `scripts/superficie.py` → `superficie_corte(pdb, cadena, ligando)` y `como_imagen(...)`: superficie real de la diana cortada para ver el bolsillo.
- `scripts/fuentes.py` → descargas (PubChem, ChEMBL, PDB, AlphaFold, Bioicons, kits de Servier).
- `scripts/componentes.py` → capa de estilo: textos, flechas, pasos, bloqueos, ADN, etiquetas de fármaco, paleta `COLOR`.
Reglas de estilo en `references/estilo.md`.

### 7. Renderizar y verificar
`python3 scripts/renderizar.py lamina-N.svg` y **mira cada PNG con Read**. Corrige hasta que pase la lista de `references/verificacion.md` (textos que se pisan, elementos sobre la membrana, tamaño mínimo de letra, atribuciones, rótulos de esquema). Es normal necesitar 2–4 rondas por lámina.

### 8. Material de apoyo
Escribe `material.md` con la estructura del de trastuzumab deruxtecán: título `# <Fármaco>: ¿cómo actúa?`, lista numerada de láminas con enlace (`1. [Título](lamina-1.png)`), puntos clave, recorrido de cada lámina, farmacocinética, clase farmacológica, error frecuente, pregunta de autoevaluación con respuesta, simplificaciones, **glosario** y fuentes, con la cita de cada afirmación. Termina con **«No verificado»**: solo los datos que no se pudieron confirmar (idealmente, ninguno). Usa listas con línea en blanco antes y sangría de 3–4 espacios para las sublistas, y cita con `*[Fuente]*`.

**Glosario (obligatorio):** sección `## Glosario` (en el material, justo antes de `## Fuentes`; en el PDF, `pdf.py` la coloca tras el índice), con cada sigla o abreviatura que aparezca en las láminas o en el material, en orden alfabético y con el formato `- **SIGLA:** Desarrollo en español y, si hace falta, qué es en una frase.` Incluye también las de las fuentes (CIMA, FDA, PDB, PMID…), las de los ensayos clínicos y los símbolos de genes y proteínas. Comprueba que no falte ninguna con `python3 scripts/glosario.py ejemplos/<farmaco>`, que lista las siglas sin definición y termina con error si falta alguna.

### 9. PDF final y entrega
`python3 scripts/pdf.py ejemplos/<farmaco>` crea `ejemplos/<farmaco>/<farmaco>.pdf` (A4) con:
- Portada con la lámina del mecanismo, las fuentes de verificación y los datos del documento.
- Índice con números de página y marcadores.
- Una lámina por página, en horizontal.
- La ficha del mecanismo con diseño editorial: puntos clave en tarjetas, tablas, citas como etiquetas y recuadros para el error frecuente, la autoevaluación y lo no verificado.
- El glosario de siglas, en dos columnas, justo después del índice y antes de las láminas, para conocer las abreviaturas antes de empezar a leer.

Antes de generarlo, `python3 scripts/glosario.py ejemplos/<farmaco>` debe terminar sin siglas pendientes.

Usa `--portada N` para elegir otra lámina de portada. Revisa las páginas convertidas a PNG (pymupdf) con Read antes de entregar. Entrega el PDF (con SendUserFile si está disponible), los PNG y el material, y en el mensaje final resume en pocas líneas qué se verificó, qué se corrigió y qué no se pudo confirmar.

## Licencias
- Usa preferentemente CC0, dominio público y CC BY. Evita CC BY-SA salvo que no haya alternativa (obliga a compartir la lámina con la misma licencia) y avísalo.
- Cada lámina lleva en el pie las atribuciones de lo que usa (Servier, PDB, PubChem/RDKit). `assets/ilustraciones/ATRIBUCION.md` y `registro.json` documentan cada archivo.
