# Fuentes en otros idiomas

Las guías nacionales de otros países y la literatura en otros idiomas completan a las fuentes en inglés y en español. Sirven para contrastar una recomendación, encontrar una guía de acceso abierto cuando la de referencia está bloqueada, y aportar datos que solo publica un país.

**Todo se traduce al español antes de pasar a las láminas, al material y al PDF.** Ninguna frase en otro idioma llega al documento final, salvo el título original de la fuente en la lista de fuentes.

## Cómo usarlas

1. **Buscar:**
   - **Literatura:** PubMed admite el filtro de idioma `[la]`, con `ger`, `fin`, `nor`, `swe`, `dan`, `dut`, `fre`, `ita`, `por` o `jpn`. Por ejemplo:

     ```
     python3 scripts/fuentes.py pubmed "type 2 diabetes guideline AND ger[la]"
     ```

     En Europe PMC, el filtro es `LANG:` con los mismos códigos (`LANG:nor`).
   - **Páginas de guías:** `python3 scripts/fuentes.py pagina <URL> "<regex>"` descarga la página, quita el HTML y devuelve los fragmentos donde aparece el patrón, con el idioma declarado por la página.
2. **Verificar en el idioma original.** El patrón de búsqueda va en el idioma de la fuente (`Metformiini on`, `Virkningsmekanisme`, `Werking`) y la cifra se comprueba en la frase original, antes de traducir.
3. **Traducir al español:**
   - Traduce con fidelidad, sin resumir de más ni añadir matices.
   - Conserva cifras, unidades y umbrales tal cual; adapta solo el formato decimal (coma decimal: «1,73 m²»).
   - Usa la terminología médica habitual en español («insuficiencia cardiaca», no «fallo cardiaco») y la misma forma en todo el documento y en el glosario.
   - Los nombres de fármacos van en su DCI en español (metformina, no «metformiini»).
4. **Citar:**
   - En el texto: `*[Käypä hoito, Tyypin 2 diabetes (en finés)]*`.
   - En `## Fuentes`: institución, título original, año, URL e idioma; por ejemplo: «Duodecim, Käypä hoito: *Tyypin 2 diabetes* (año de la última actualización), kaypahoito.fi/hoi50056, en finés; traducción propia».
5. **Glosario:** las siglas de la fuente original (NVL, AWMF, HAS…) se incluyen con su desarrollo en el idioma original y la traducción, por ejemplo: `- **NVL:** Nationale VersorgungsLeitlinie, guía nacional de asistencia de Alemania.`
6. **Si dos países recomiendan cosas distintas,** no las mezcles: di qué recomienda cada guía, con su país y su año.

## Fuentes comprobadas desde este entorno

| País e idioma | Fuente | Qué aporta | Acceso |
|---|---|---|---|
| Alemania (alemán) | AWMF, register.awmf.org | Registro de guías de las sociedades científicas alemanas | Responde |
| Alemania (alemán) | Nationale VersorgungsLeitlinien, leitlinien.de | Guías nacionales (diabetes, asma, EPOC, insuficiencia cardiaca…) | Responde |
| Alemania (alemán) | IQWiG, gesundheitsinformation.de | Información basada en la evidencia, revisada por el IQWiG | Responde |
| Finlandia (finés) | Duodecim, Käypä hoito (kaypahoito.fi) | Guías nacionales completas, con niveles de evidencia | Responde; texto completo |
| Finlandia (finés) | Terveyskirjasto (terveyskirjasto.fi) | Textos de Duodecim para pacientes | Responde |
| Noruega (noruego) | Helsedirektoratet (helsedirektoratet.no) | Guías nacionales | Responde (algunas páginas cargan con JavaScript) |
| Suecia (sueco) | Janusinfo (janusinfo.se) | Recomendaciones de la región de Estocolmo | Responde |
| Dinamarca (danés) | pro.medicin.dk | Información profesional de medicamentos y enfermedades | Responde |
| Países Bajos (neerlandés) | Farmacotherapeutisch Kompas | Recomendaciones de tratamiento por enfermedad y fármaco | Responde |
| Francia (francés) | HAS (has-sante.fr) | Guías y evaluaciones de la Haute Autorité de Santé | Responde |
| Italia (italiano) | AIFA (aifa.gov.it) | Notas y planes terapéuticos de la agencia del medicamento | Responde |
| Reino Unido (inglés) | NICE (nice.org.uk) | Guías nacionales | Responde |

## Bibliotecas de imágenes en otros idiomas

Completan a Servier cuando falta un dibujo (hongos, micobacterias, paredes bacterianas, coronavirus). Antes de usar una imagen, comprueba su licencia en la ficha de la imagen, no en la portada del sitio.

| Biblioteca e idioma | Qué aporta | Licencia | Cómo usarla |
|---|---|---|---|
| **TogoTV** (DBCLS, Japón; japonés e inglés) | Galería de ciencias de la vida: microorganismos (*M. tuberculosis*, *P. aeruginosa*, *Candida*, *Cryptococcus*, SARS-CoV-2, paredes grampositiva y gramnegativa), órganos, inmunoglobulinas, material de laboratorio | CC BY 4.0. Crédito: «TogoTV (© 2016 DBCLS TogoTV, CC BY 4.0)» | `fuentes.py togopic <término>` y `togopic-descargar <svg> <nombre> <doi>`. Busca en japonés: en inglés solo encuentra por el nombre de la imagen |
| **Wikimedia Commons** (multilingüe) | Diagramas de farmacocinética, ciclos de parásitos, anatomía; se busca en cualquier idioma (`Pharmakokinetik`, `pharmacocinétique`, `farmacocinetica`) | La de cada archivo; `commons` descarta NC y ND, y marca CC BY-SA | `fuentes.py commons <término>` y `commons-descargar "File:…" <nombre>`. Cita la autoría en el material |
| **Planet-Vie** (ENS, Francia; francés) | Esquemas de biología celular y microbiología para docencia | Una por imagen, a menudo con NC o ND | Solo como referencia para dibujar; reutiliza la imagen solo si su ficha dice CC BY, CC BY-SA o CC0 |
| **DocCheck Flexikon** (Alemania; alemán) | Imágenes de usuarios en artículos médicos | Mixta y no siempre visible | No la uses salvo que la ficha de la imagen tenga una licencia libre explícita |

**Términos de búsqueda en TogoTV comprobados:** 感染症 (enfermedad infecciosa), 細菌 (bacteria), ウイルス (virus), 真菌 (hongo), 寄生虫 (parásito), 結核 (tuberculosis), 免疫 (inmunidad), 肺 (pulmón), 薬 (medicamento).

**Estilo:** las imágenes de TogoTV y de Commons no siguen el estilo de Servier. Úsalas cuando no haya un dibujo de Servier, sin mezclar las dos familias en la misma escena (ver `estilo.md`), y prefiere las esquemáticas a las de estilo fotográfico o de acuarela.

**Otras bibliotecas comprobadas, en inglés:** NIH BioArt (bioart.niaid.nih.gov, dominio público, muchos microorganismos; carga con JavaScript, así que la descarga es manual), PHIL de los CDC (phil.cdc.gov, micrografías de dominio público para la lámina de diagnóstico; la página responde, pero la descarga automática no se ha probado), SwissBioPics (CC BY 4.0, también en Bioicons), Health Icons (healthicons.org, CC0) y la biblioteca de iconos de Reactome (CC BY 4.0).

**No disponibles:**

- **NHG-Standaarden** (richtlijnen.nhg.org, Países Bajos): responde 401 y requiere sesión.
- **NICE CKS** (cks.nice.org.uk): responde 403 a consultas automáticas.
- **Norsk legemiddelhåndbok** (legemiddelhandboka.no): no respondió.

Si otra fuente falla, nombra el dominio a la persona usuaria y sigue con la siguiente.
