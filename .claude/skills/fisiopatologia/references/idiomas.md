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

**No disponibles:**

- **NHG-Standaarden** (richtlijnen.nhg.org, Países Bajos): responde 401 y requiere sesión.
- **NICE CKS** (cks.nice.org.uk): responde 403 a consultas automáticas.
- **Norsk legemiddelhåndbok** (legemiddelhandboka.no): no respondió.

Si otra fuente falla, nombra el dominio a la persona usuaria y sigue con la siguiente.
