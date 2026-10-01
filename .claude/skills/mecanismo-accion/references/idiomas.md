# Fuentes en otros idiomas

Las fichas técnicas nacionales, los formularios terapéuticos y la literatura en otros idiomas completan a CIMA, la FDA y las fuentes en inglés. Sirven para contrastar un dato de la ficha técnica, encontrar información que solo publica un país (recomendaciones de uso, comparaciones entre fármacos) y enriquecer la lámina del paciente.

**Todo se traduce al español antes de pasar a las láminas, al material y al PDF.** Ninguna frase en otro idioma llega al documento final, salvo el título original de la fuente en la lista de fuentes.

**La ficha técnica de referencia sigue siendo CIMA (y la FDA para contrastar).** Las fichas nacionales de otros países de la UE derivan de la misma ficha europea; úsalas para confirmar, no para sustituirla. Si una cifra difiere, muestra el rango y cita ambas.

## Cómo usarlas

1. **Buscar:**
   - **Literatura:** PubMed admite el filtro de idioma `[la]`, con `ger`, `fin`, `nor`, `swe`, `dan`, `dut`, `fre`, `ita`, `por` o `jpn`. Por ejemplo:

     ```
     python3 scripts/fuentes.py pubmed "metformin mechanism AND ger[la]"
     ```

     En Europe PMC, el filtro es `LANG:` con los mismos códigos (`LANG:nor`).
   - **Fichas y formularios:** `python3 scripts/fuentes.py pagina <URL> "<regex>"` descarga la página, quita el HTML y devuelve los fragmentos donde aparece el patrón, con el idioma declarado por la página.
2. **Verificar en el idioma original.** El patrón va en el idioma de la fuente (`Virkningsmekanisme`, `Werking`, `Wirkmechanismus`, `Mécanisme d'action`) y la cifra se comprueba en la frase original, antes de traducir.
3. **Traducir al español:**
   - Traduce con fidelidad, sin resumir de más ni añadir matices.
   - Conserva cifras, unidades y umbrales tal cual; adapta solo el formato decimal (coma decimal).
   - Usa la terminología farmacológica habitual en español y la DCI en español del fármaco (metformina, no «metformiini»), con la misma forma en todo el documento y en el glosario.
4. **Citar:**
   - En el texto: `*[Felleskatalogen, Glucophage (en noruego)]*`.
   - En `## Fuentes`: institución, título original, año si consta, URL e idioma; por ejemplo: «Felleskatalogen: *Glucophage «Merck»*, felleskatalogen.no, en noruego; traducción propia».
5. **Glosario:** las siglas de la fuente original se incluyen con su desarrollo en el idioma original y la traducción.

## Fuentes comprobadas desde este entorno

| País e idioma | Fuente | Qué aporta | Acceso |
|---|---|---|---|
| Noruega (noruego) | Felleskatalogen (felleskatalogen.no) | Textos de producto con mecanismo de acción («Virkningsmekanisme»), farmacocinética y efectos adversos | Responde; busca con `/medisin/sok?sokord=<fármaco>` |
| Dinamarca (danés) | pro.medicin.dk | Información profesional de medicamentos | Responde |
| Países Bajos (neerlandés) | Farmacotherapeutisch Kompas | Monografías de fármacos y recomendaciones de uso | Responde |
| Suecia (sueco) | FASS (fass.se) y Janusinfo (janusinfo.se) | Fichas de producto; recomendaciones regionales de Estocolmo | Responden; la búsqueda de FASS se genera con JavaScript |
| Finlandia (finés) | Duodecim, Käypä hoito (kaypahoito.fi) | Guías nacionales con el lugar de cada fármaco en el tratamiento | Responde; texto completo |
| Alemania (alemán) | AWMF (register.awmf.org) y Nationale VersorgungsLeitlinien (leitlinien.de) | Guías con el lugar de cada fármaco | Responden |
| Francia (francés) | Base de données publique des médicaments (base-donnees-publique.medicaments.gouv.fr) y HAS (has-sante.fr) | Fichas (RCP) y evaluaciones del beneficio clínico (SMR, ASMR) | Responden; la búsqueda de la base pública se genera con JavaScript |
| Italia (italiano) | AIFA (aifa.gov.it) | Notas de prescripción y planes terapéuticos | Responde |

**No disponibles:** Norsk legemiddelhåndbok (legemiddelhandboka.no) no respondió. Si otra fuente falla, nombra el dominio a la persona usuaria y sigue con la siguiente.
