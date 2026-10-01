---
name: fisiopatologia
description: Crea láminas ilustradas y un PDF profesional sobre una enfermedad (fisiopatología, clínica y diagnóstico, y tratamiento farmacológico) para profesionales de salud. Combina ilustraciones profesionales (Servier Medical Art, Bioicons) con datos verificados en MeSH, MONDO, Reactome, UniProt, guías y consensos de acceso abierto (PubMed/PMC), páginas de sociedades científicas, el NIH (NIDDK), la OMS, guías nacionales en otros idiomas (traducidas al español) y las fichas técnicas de los fármacos. Úsala siempre que se pida explicar una enfermedad, su fisiopatología, cómo se produce, sus síntomas o complicaciones, cómo se diagnostica o cómo se trata, o hacer una lámina, infografía, esquema, diapositiva o material didáctico sobre una enfermedad o síndrome (diabetes, hipertensión, insuficiencia cardiaca, asma, artritis reumatoide…), aunque no se mencione la palabra «skill». No es para explicar cómo actúa un medicamento concreto: eso corresponde a la skill mecanismo-accion.
---

# Láminas de fisiopatología de una enfermedad

Produce una serie de **láminas 16:9** (SVG + PNG; tantas como necesite la enfermedad), un **material de apoyo** en Markdown y un **PDF final** con diseño profesional. Explican una enfermedad a profesionales de salud: por qué se produce, cómo se manifiesta, cómo se diagnostica y cómo se trata. El objetivo es que el lector entienda la causa (fisiología normal → qué falla → consecuencias clínicas → por qué cada fármaco corrige un defecto), no que memorice listas.

Hay un ejemplo completo en `ejemplos/diabetes-tipo-2/` (`laminas.py`, `material.md`, `lamina-N.png` y el PDF). Úsalo como modelo de composición, densidad de texto y tono.

## Principios

- **Exactitud antes que estética.** Cada afirmación se apoya en una fuente: guía o consenso, revisión con PMID, base curada o ficha técnica. Si algo no se puede verificar, no entra en las láminas; se anota en «No verificado».
- **Las cifras, literales.** Puntos de corte, porcentajes y umbrales se copian de la fuente y se comprueban con su frase exacta (`fuentes.py pmc` o el texto de la página). Si una revisión dice «en el tercil superior de la intolerancia», la lámina no lo generaliza a toda la intolerancia.
- **El tratamiento sale de una guía con nombre y año.** Si la guía vigente no se puede leer completa, usa la más reciente de acceso abierto, dilo en el subtítulo de la lámina y anótalo en «No verificado».
- **No sugerir precisión que no existe.** Las curvas sin datos llevan «Esquema cualitativo»; los esquemas, «sin escala».
- **Fuentes en cualquier idioma, documento en español.** Además del inglés y el español, se pueden usar fuentes en alemán, finés, noruego, sueco, danés, neerlandés, francés, italiano u otros idiomas. Cada dato se verifica en el idioma original y se traduce al español antes de pasar a las láminas, al material y al PDF. Ver `references/idiomas.md`.
- **Verificación autónoma.** La skill verifica por sí misma cada dato y avanza sin pedir aprobaciones intermedias. Al final solo se muestra la lista breve de lo que no se pudo confirmar. Las láminas llevan la marca «Prototipo pendiente de revisión clínica» hasta que la persona usuaria decida retirarla.

## Preparación del entorno

```bash
pip install playwright pymupdf markdown
# Chromium: se usa /opt/pw-browsers/chromium si existe; si no, `playwright install chromium`.
# Para extraer dibujos de los kits de Servier hace falta LibreOffice Impress (paquete libreoffice-impress).
```

Prueba la red con `python3 scripts/fuentes.py mesh "Diabetes Mellitus, Type 2"`. Si un dominio falla, díselo a la persona usuaria nombrando el dominio (para que lo habilite en la configuración de red) y sigue con la biblioteca local (`assets/ilustraciones/`).

## Flujo de trabajo

### 1. Confirmar el encargo
Enfermedad, público (por defecto: profesionales de salud) y uso (proyectar, imprimir). Por defecto se cubren fisiopatología, clínica y diagnóstico, y tratamiento farmacológico. La epidemiología solo se incluye si se pide.

### 2. Investigar y verificar
Sigue el orden de `references/fuentes.md` y anota la fuente exacta de cada dato (PMID, PMCID, identificador, URL de la guía).

1. **Definición:** `fuentes.py mesh "<término MeSH>"` y `fuentes.py mondo "<nombre en inglés>"`.
2. **Fisiopatología:**
   - Busca una revisión de referencia con `fuentes.py pubmed "<consulta>" "<regex>"`.
   - Si tiene texto completo en PMC, extrae las frases que respaldan cada afirmación con `fuentes.py pmc <PMCID> "<regex>" …`.
   - Confirma las vías moleculares con `fuentes.py reactome` y las proteínas con `fuentes.py uniprot <GEN>`.
3. **Clínica y diagnóstico:** páginas de la sociedad científica y del instituto del NIH correspondiente (p. ej., diabetes.org y NIDDK), notas descriptivas de la OMS y `fuentes.py medlineplus`. Léelas con `fuentes.py pagina <URL> "<regex>"`, que quita el HTML y devuelve la frase exacta.
4. **Tratamiento:**
   - `fuentes.py guias "<enfermedad en inglés>"` lista guías y consensos de los últimos 5 años con su PMCID; lee la de texto completo con `fuentes.py pmc`.
   - El mecanismo de cada grupo de fármacos sale de la sección 12.1 de la ficha de la FDA (`fuentes.py openfda <fármaco>`) o de la 5.1 de CIMA (`fuentes.py cima <fármaco>`).
5. **Fuentes en otros idiomas:** guías nacionales de otros países (Käypä hoito en Finlandia, Nationale VersorgungsLeitlinien y AWMF en Alemania, Helsedirektoratet en Noruega, HAS en Francia, Farmacotherapeutisch Kompas en los Países Bajos…) y literatura con el filtro de idioma de PubMed (`ger[la]`, `fin[la]`, `nor[la]`…).
   - Úsalas para contrastar una recomendación, sustituir una guía bloqueada o añadir datos que solo publica un país.
   - Lee las páginas con `fuentes.py pagina <URL> "<regex en el idioma original>"`.
   - Traduce al español antes de usar el dato y cita el idioma de la fuente. Ver `references/idiomas.md`.
6. Si una fuente no responde, nombra el dominio a la persona usuaria y sigue con la siguiente; nunca rellenes el hueco con suposiciones.

### 3. Elegir la plantilla y el número de láminas
Según el tipo de enfermedad, ver `references/plantillas.md` (metabólica, cardiovascular, inflamatoria o autoinmune, infecciosa, oncológica, neurológica). El arco es siempre el mismo y cada lámina explica una sola idea (ver «Densidad» en `references/estilo.md`):

1. **Contexto:** qué falla y dónde.
2. **Fisiología normal:** cómo funciona el sistema sano.
3. **Fisiopatología:** qué se altera y en qué orden.
4. **Clínica:** síntomas explicados por el mecanismo, y complicaciones.
5. **Diagnóstico:** criterios en tabla y cómo se confirma.
6. **Tratamiento:** mapa de dónde actúa cada grupo de fármacos y estrategia según la guía.

Numera «LÁMINA N DE TOTAL» con el total real.

### 4. Reunir las piezas visuales
Biblioteca local (`assets/ilustraciones/`: órganos, tejidos, células) → Bioicons (`fuentes.py bioicons`) → kits de Servier (`fuentes.py servier-kits`, `servier-diapositivas`, `servier-extraer`) → dibujo propio. Cuando haya varias opciones, genera una hoja de comparación (`python3 scripts/hoja_comparacion.py hoja.png a.svg b.svg ...`), revísala con Read y elige. Registra cada pieza nueva en `assets/ilustraciones/registro.json`.

### 5. Componer
Crea `ejemplos/<enfermedad>/laminas.py` a partir del de diabetes tipo 2. Bibliotecas disponibles:
- `scripts/piezas.py`:
   - `Lamina(enfermedad, fuentes)` dibuja el marco común: cabecera, título, pie y aviso.
   - `tarjeta`, `ficha`, `caja`, `leyenda_paso`, `membrana` y `organo_ilustrado`.
- `scripts/componentes.py`: capa de estilo con textos, flechas, pasos, bloqueos, vesículas, mitocondria, `etiqueta_farmaco` y la paleta `COLOR`.
- `scripts/recursos.py`: `ilustracion(nombre, x, y, w, h)` inserta un SVG de `assets/ilustraciones/`.
- `scripts/fuentes.py`: consultas a las fuentes y descargas de ilustraciones.

Reglas de estilo en `references/estilo.md`. El pie común lleva las fuentes generales en una línea; si una lámina necesita citar más, hazlo dentro de la lámina (recuadro) o en el material, nunca alargando el pie.

### 6. Renderizar y verificar
`python3 scripts/renderizar.py ejemplos/<enfermedad>/lamina-N.svg ejemplos/<enfermedad>/lamina-N.png` y **mira cada PNG con Read**. Corrige hasta que pase la lista de `references/verificacion.md`: textos que se pisan, pies que se desbordan, recuadros con espacio vacío, tamaño mínimo de letra y rótulos de esquema. Es normal necesitar 2–4 rondas por lámina.

### 7. Material de apoyo
Escribe `material.md` con la estructura del de diabetes tipo 2:

- Título `# <Enfermedad>: fisiopatología, diagnóstico y tratamiento`.
- Lista numerada de láminas con enlace (`1. [Título](lamina-1.png)`).
- Puntos clave y recorrido de cada lámina, con tablas para los criterios diagnósticos y el mapa de fármacos.
- Error frecuente y simplificaciones de las láminas.
- **Glosario** y fuentes.
- Al final, **«No verificado»**: solo los datos que no se pudieron confirmar y las guías que no se pudieron leer.

Cita cada afirmación con `*[Fuente]*`.

**Glosario (obligatorio):** sección `## Glosario`, en el material justo antes de `## Fuentes` (en el PDF, `pdf.py` la coloca tras el índice). Incluye cada sigla o abreviatura de las láminas y del material, en orden alfabético, con el formato `- **SIGLA:** Desarrollo en español y, si hace falta, qué es en una frase.` Comprueba que no falte ninguna con `python3 scripts/glosario.py ejemplos/<enfermedad>`.

### 8. PDF final y entrega
`python3 scripts/pdf.py ejemplos/<enfermedad>` crea `ejemplos/<enfermedad>/<enfermedad>.pdf` (A4) con:
- Portada con una lámina de fisiopatología, las fuentes de verificación y los datos del documento.
- Índice con números de página y marcadores.
- Glosario en dos columnas, justo después del índice.
- Una lámina por página, en horizontal.
- La ficha de la enfermedad con diseño editorial.

Usa `--portada N` para elegir otra lámina de portada. Revisa las páginas convertidas a PNG con Read antes de entregar. Entrega solo el PDF (con SendUserFile si está disponible) y, en el mensaje final, resume en pocas líneas qué se verificó, qué se corrigió y qué no se pudo confirmar.

## Licencias
- Usa preferentemente CC0, dominio público y CC BY. Evita CC BY-SA salvo que no haya alternativa, y avísalo.
- Cada lámina lleva en el pie la atribución de las ilustraciones: «Ilustraciones: Servier Medical Art (CC BY 3.0 y 4.0)». `assets/ilustraciones/ATRIBUCION.md` y `registro.json` documentan cada archivo.
