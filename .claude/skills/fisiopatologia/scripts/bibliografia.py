"""Bibliografía estructurada del material: cada fuente una vez, con sus identificadores, citada por su clave.

Uso:
    python3 scripts/bibliografia.py nueva ejemplos/<tema> <clave> --pmid 27418577 [--tipo guia] [--sello IDSA]
    python3 scripts/bibliografia.py nueva ejemplos/<tema> <clave> --doi 10.1093/cid/ciw353
    python3 scripts/bibliografia.py nueva ejemplos/<tema> <clave> --url <URL> --cita "Organismo. Título. Año."
    python3 scripts/bibliografia.py nueva ejemplos/<tema> <clave> --cima empagliflozina    # ficha técnica (AEMPS)
    python3 scripts/bibliografia.py nueva ejemplos/<tema> <clave> --dailymed empagliflozin # ficha de la FDA
    python3 scripts/bibliografia.py nueva ejemplos/<tema> <clave> --ema jardiance          # EPAR de la EMA
    python3 scripts/bibliografia.py nueva ejemplos/<tema> <clave> --nct NCT01131676        # registro del ensayo
    python3 scripts/bibliografia.py nueva ejemplos/<tema> <clave> --nice NG28              # guía del NICE
    python3 scripts/bibliografia.py comprobar ejemplos/<tema> [--en-linea]
    python3 scripts/bibliografia.py lista ejemplos/<tema> [--escribir]
    python3 scripts/bibliografia.py busqueda ejemplos/<tema> [--escribir]

`bibliografia.json` guarda cada referencia una vez:

    {"referencias": [{"clave": "idsa-2016", "tipo": "guia",
                      "cita": "Kalil AC, Metersky ML, ... et al. Management of Adults With ... Clin Infect Dis. 2016;63(5):e61-e111.",
                      "pmid": "27418577", "pmcid": "PMC4981759", "doi": "10.1093/cid/ciw353", "url": null,
                      "idioma": "en", "version": null, "consultado": "2026-10-02", "sello": "IDSA/ATS",
                      "nota": "Texto completo leído en el repositorio de la Universitat de Barcelona."}]}

Tipos: guia, articulo, revision, ficha (ficha técnica), web, base (MeSH, UniProt…), libro, documento.
`sello` es el nombre que aparece en la portada del PDF («Datos verificados en»).

En el material se cita con la clave y, si hace falta, dónde: *[@idsa-2016, p. e63]*, *[@s3-2024; @ers-2017]*.
Las claves van en minúsculas, con cifras y guiones. El PDF numera las referencias por orden de aparición,
enlaza cada cita con su referencia y cada referencia con PubMed, PMC, el DOI o la página.
La lista de `## Fuentes` se genera con `lista --escribir`, entre <!-- bibliografia: inicio --> y
<!-- bibliografia: fin -->; el texto fuera de las marcas (p. ej., el crédito de las ilustraciones) se conserva.
`busqueda --escribir` resume busquedas.jsonl (fuentes.py --registro) en la sección `## Cómo se buscó`.

`comprobar` falla si una cita usa una clave que no existe, si una referencia no se cita, si una evidencia de
evidencias.json apunta a una clave inexistente o si la lista de Fuentes no coincide con bibliografia.json.
Con --en-linea consulta PubMed: una referencia retractada es un error; la fe de erratas y las versiones
posteriores de una guía son avisos que hay que revisar.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

CITA = re.compile(r"\[(@[^\]]+)\]")
CLAVE = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
MARCAS = ("<!-- bibliografia: inicio -->", "<!-- bibliografia: fin -->")
MARCAS_BUSQUEDA = ("<!-- busqueda: inicio -->", "<!-- busqueda: fin -->")
TIPOS = {"guia", "articulo", "revision", "ficha", "web", "base", "libro", "documento"}
IDIOMAS = {"de": "alemán", "fi": "finés", "no": "noruego", "nb": "noruego", "sv": "sueco", "da": "danés",
           "nl": "neerlandés", "fr": "francés", "it": "italiano", "pt": "portugués", "ja": "japonés"}
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
         "noviembre", "diciembre"]


def cargar(carpeta):
    ruta = Path(carpeta) / "bibliografia.json"
    return json.loads(ruta.read_text(encoding="utf-8"))["referencias"] if ruta.exists() else []


def guardar(carpeta, referencias):
    (Path(carpeta) / "bibliografia.json").write_text(
        json.dumps({"referencias": referencias}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def citas(texto):
    """Citas del texto en orden, como (clave, localizador). «@s3-2024, rec. 21; traducción propia» da
    («s3-2024», «rec. 21; traducción propia»): lo que sigue sin «@» es parte del localizador anterior."""
    salida = []
    for m in CITA.finditer(texto):
        for parte in m.group(1).split(";"):
            parte = parte.strip()
            c = re.match(r"@([\w.-]+)\s*(?:,\s*(.+))?$", parte)
            if c:
                salida.append([c.group(1), c.group(2) or ""])
            elif salida and parte:
                salida[-1][1] = f"{salida[-1][1]}; {parte}".lstrip("; ")
    return [tuple(x) for x in salida]


def _sin_listas(material):
    """El material sin las partes generadas (lista de fuentes y resumen de la búsqueda)."""
    for inicio, fin in (MARCAS, MARCAS_BUSQUEDA):
        material = re.sub(re.escape(inicio) + r".*?" + re.escape(fin), "", material, flags=re.S)
    return material


def numeracion(carpeta):
    """Número de cada referencia, por orden de primera cita en el material (estilo Vancouver)."""
    material = _sin_listas((Path(carpeta) / "material.md").read_text(encoding="utf-8"))
    numeros = {}
    for clave, _ in citas(material):
        numeros.setdefault(clave, len(numeros) + 1)
    return numeros


def fecha_es(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def _enlaces(ref):
    partes = []
    if ref.get("doi"):
        partes.append(f"doi:[{ref['doi']}](https://doi.org/{ref['doi']})")
    if ref.get("pmid"):
        partes.append(f"PMID [{ref['pmid']}](https://pubmed.ncbi.nlm.nih.gov/{ref['pmid']}/)")
    if ref.get("pmcid"):
        partes.append(f"[{ref['pmcid']}](https://pmc.ncbi.nlm.nih.gov/articles/{ref['pmcid']}/)")
    if ref.get("url") and not (ref.get("doi") or ref.get("pmid")):
        visible = re.sub(r"^https?://(www\.)?", "", ref["url"])
        visible = visible if len(visible) <= 60 else visible[:57] + "…"
        partes.append(f"Disponible en: [{visible}]({ref['url']})")
    return ". ".join(partes)


def formatear(ref):
    """La referencia en Vancouver, con sus identificadores enlazados, la versión, el idioma y la fecha de consulta."""
    texto = re.sub(r"<[^>]+>", "", re.sub(r"</?(?:i|em)>", "*", ref["cita"])).rstrip()
    texto += "" if texto.endswith(".") else "."
    extras = [_enlaces(ref)]
    if ref.get("version"):
        extras.append(f"Versión {ref['version']}")
    if ref.get("idioma") in IDIOMAS:
        extras.append(f"En {IDIOMAS[ref['idioma']]}; traducción propia")
    if ref.get("consultado") and (ref.get("url") or ref.get("tipo") in ("ficha", "web", "base", "documento")):
        extras.append(f"Consultado el {fecha_es(ref['consultado'])}")
    if ref.get("nota"):
        extras.append(ref["nota"].rstrip("."))
    return " ".join([texto] + [e + "." for e in extras if e])


def lista(carpeta):
    """Lista numerada de Fuentes en Markdown, en el orden de la numeración."""
    referencias = {r["clave"]: r for r in cargar(carpeta)}
    numeros = numeracion(carpeta)
    orden = sorted((n, c) for c, n in numeros.items() if c in referencias)
    return "\n".join(f"{n}. {formatear(referencias[c])}" for n, c in orden)


def _escribir_entre_marcas(carpeta, seccion, marcas, contenido):
    ruta = Path(carpeta) / "material.md"
    material = ruta.read_text(encoding="utf-8")
    bloque = f"{marcas[0]}\n\n{contenido}\n\n{marcas[1]}"
    if marcas[0] in material:
        material = re.sub(re.escape(marcas[0]) + r".*?" + re.escape(marcas[1]), lambda _: bloque, material,
                          flags=re.S)
    elif re.search(rf"^## {seccion}\s*$", material, re.M):
        material = re.sub(rf"^(## {seccion}\s*\n)\n?", lambda m: f"{m.group(1)}\n{bloque}\n\n", material, count=1,
                          flags=re.M)
    else:
        raise ValueError(f"material.md no tiene la sección «## {seccion}»")
    ruta.write_text(material, encoding="utf-8")


def escribir_lista(carpeta):
    _escribir_entre_marcas(carpeta, "Fuentes", MARCAS, lista(carpeta))


# --- Nuevas referencias -----------------------------------------------------------------------------------------

def _autor(a):
    if a.get("literal"):
        return a["literal"].rstrip("*").strip()
    iniciales = "".join(p[0] for p in re.split(r"[\s.\-]+", a.get("given", "")) if p)
    familia = a.get("family", "").rstrip("*").strip()  # «…Committee for Diabetes*»: llamada a la nota de autoría
    return " ".join(x for x in (familia, iniciales, a.get("suffix", "")) if x)


def vancouver(csl):
    """Cita en estilo Vancouver (ICMJE) desde metadatos CSL: hasta 6 autores y «et al.»."""
    autores = [_autor(a) for a in csl.get("author", [])]
    texto_autores = ", ".join(autores[:6]) + (", et al" if len(autores) > 6 else "")
    revista = csl.get("container-title-short") or csl.get("journalAbbreviation") or csl.get("container-title", "")
    anio = ((csl.get("issued") or {}).get("date-parts") or [[None]])[0][0]
    detalle = str(anio or "") + (f";{csl['volume']}" if csl.get("volume") else "") + \
        (f"({re.sub(r'(?i)supplement[_ ]?', 'Suppl ', csl['issue'])})" if csl.get("issue") else "") + (f":{csl['page']}" if csl.get("page") else "")
    titulo = re.sub(r"</?(?:i|em)>", "*", csl.get("title") or "")  # cursivas de PubMed (nombres de especie)
    titulo = re.sub(r"<[^>]+>", "", titulo).rstrip(".")
    partes = [texto_autores, titulo, revista, detalle]
    return ". ".join(p for p in partes if p) + "."


def _csl_de_crossref(m):
    return {"author": m.get("author", []), "title": (m.get("title") or [""])[0],
            "container-title-short": (m.get("short-container-title") or [None])[0],
            "container-title": (m.get("container-title") or [""])[0], "issued": m.get("issued"),
            "volume": m.get("volume"), "issue": m.get("issue"), "page": m.get("page")}


def _fecha(texto):
    """Fecha de una fuente («Feb 02, 2026», «24/03/2026», «2026-03-24») en español."""
    from datetime import datetime
    for formato in ("%b %d, %Y", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            return fecha_es(datetime.strptime(texto.strip(), formato).date().isoformat())
        except (ValueError, AttributeError):
            continue
    return texto


def _ficha(cima=None, dailymed=None, ema=None, nct=None, nice=None):
    """Referencia de una ficha técnica o de un registro de ensayo, con su versión y su fecha."""
    import fuentes
    if cima:
        f = fuentes.cima(cima, secciones=())
        if not f:
            raise ValueError(f"CIMA no tiene ficha técnica de «{cima}»")
        nombre = f["fuente"].split("ficha técnica de ")[1].split(" (n.º")[0]
        return {"tipo": "ficha", "url": f["url"], "idioma": "es", "sello": "CIMA (AEMPS)",
                "cita": f"Agencia Española de Medicamentos y Productos Sanitarios (AEMPS). Ficha técnica de {nombre}. "
                        f"CIMA, n.º de registro {f['nregistro']}",
                "version": f"del {fecha_es(f['fecha_ficha'])}" if f.get("fecha_ficha") else None,
                "nota": None if f.get("fecha_ficha") or not f.get("autorizacion_europea") else
                "Autorización europea: la fecha de la revisión está en el EPAR"}
    if dailymed:
        f = fuentes.dailymed(dailymed, secciones=())
        if not f:
            raise ValueError(f"DailyMed no tiene ficha de «{dailymed}»")
        titulo = f["fuente"].removeprefix("DailyMed, ").split(" (setid")[0]
        return {"tipo": "ficha", "url": f["url"], "sello": "Fichas de la FDA",
                "cita": f"U.S. Food and Drug Administration. Prescribing information: {titulo}. DailyMed, set id "
                        f"{f['setid']}", "version": f"{f['version']}, del {_fecha(f['fecha'])}"}
    if ema:
        m = (fuentes.ema_medicamento(ema) or [None])[0]
        if not m:
            raise ValueError(f"La EMA no tiene un medicamento de autorización centralizada llamado «{ema}»")
        return {"tipo": "ficha", "url": m["url"], "sello": "EMA",
                "cita": f"European Medicines Agency. {m['nombre']} ({m['principio_activo']}): EPAR, información del "
                        f"producto. {m['procedimiento']}; autorizado el {_fecha(m['autorizacion'])}",
                "version": f"{m['revision']}, del {_fecha(m['actualizado'])}"}
    if nice:
        g = fuentes.nice_guia(nice, capitulos="^$")  # solo la portada: título y fechas
        anio = (g.get("publicada") or "")[:4]
        return {"tipo": "guia", "url": g["url"], "idioma": "en", "sello": "NICE (Reino Unido)",
                "cita": f"National Institute for Health and Care Excellence (NICE). {g['titulo']}. Guía "
                        f"{g['codigo']}. Londres: NICE; {anio}",
                "version": f"del {fecha_es(g['actualizada'])}" if g.get("actualizada") else None}
    e = fuentes.ensayo(nct)
    return {"tipo": "documento", "url": e["url"], "sello": "ClinicalTrials.gov",
            "cita": f"{e['patrocinador']}. {e['titulo']} ({e['acronimo'] + ', ' if e.get('acronimo') else ''}"
                    f"{nct}). ClinicalTrials.gov"}


def nueva(carpeta, clave, pmid=None, doi=None, url=None, tipo=None, cita=None, sello=None, idioma=None,
          version=None, nota=None, cima=None, dailymed=None, ema=None, nct=None, nice=None):
    """Añade (o actualiza) una referencia. Con PMID toma los metadatos de PubMed (exportador de citas del NCBI);
    con DOI, de Crossref; con cima, dailymed, ema o nct, de la ficha técnica o del registro del ensayo (con su
    versión y su fecha); con nice, de la guía del NICE (con su última actualización); con URL hace falta la cita escrita a mano (organismo, título, año)."""
    import fuentes
    if not CLAVE.match(clave):
        raise ValueError("La clave va en minúsculas, con cifras y guiones (p. ej., idsa-2016)")
    ref = {"clave": clave, "tipo": tipo, "cita": cita, "pmid": pmid, "pmcid": None, "doi": doi, "url": url,
           "idioma": idioma, "version": version, "consultado": date.today().isoformat(), "sello": sello, "nota": nota}
    if pmid:
        csl = json.loads(fuentes._get(f"https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/?format=csl&id={pmid}"))
        articulo = fuentes.pubmed(f"{pmid}[uid]", maximo=1)[0]
        ref.update({"cita": cita or vancouver(csl), "pmcid": articulo.get("pmcid"), "doi": doi or articulo.get("doi"),
                    "tipo": tipo or ("guia" if {"Practice Guideline", "Guideline"} & set(articulo["tipos"]) else
                                     "revision" if "Review" in articulo["tipos"] else "articulo")})
        if articulo["avisos"]:
            print(f"Aviso de la NLM para {clave}: {'; '.join(articulo['avisos'])}", file=sys.stderr)
    elif doi:
        m = json.loads(fuentes._get(f"https://api.crossref.org/works/{doi}",
                                    cabeceras={"User-Agent": "skills-docencia/1.0"}))["message"]
        ref.update({"cita": cita or vancouver(_csl_de_crossref(m)), "tipo": tipo or "articulo"})
    elif cima or dailymed or ema or nct or nice:
        datos = _ficha(cima, dailymed, ema, nct, nice)
        ref.update({k: v for k, v in datos.items() if v and not ref.get(k)})
    elif not (url and cita):
        raise ValueError("Indica --pmid, --doi, --cima, --dailymed, --ema, --nct, --nice o --url con --cita")
    ref["tipo"] = ref["tipo"] or "web"
    referencias = [r for r in cargar(carpeta) if r["clave"] != clave] + [{k: v for k, v in ref.items() if v}]
    guardar(carpeta, referencias)
    return ref


# --- Comprobaciones ---------------------------------------------------------------------------------------------

def comprobar(carpeta, en_linea=False):
    """Devuelve (errores, avisos)."""
    carpeta = Path(carpeta)
    referencias = cargar(carpeta)
    errores, avisos = [], []
    if not referencias:
        return errores, avisos
    claves = [r.get("clave", "") for r in referencias]
    for r in referencias:
        nombre = r.get("clave", "(sin clave)")
        if not CLAVE.match(r.get("clave", "")):
            errores.append(f"{nombre}: clave no válida (minúsculas, cifras y guiones)")
        if not r.get("cita"):
            errores.append(f"{nombre}: falta «cita»")
        if r.get("tipo") not in TIPOS:
            errores.append(f"{nombre}: tipo «{r.get('tipo')}» no válido ({', '.join(sorted(TIPOS))})")
        if not (r.get("pmid") or r.get("doi") or r.get("url") or r.get("tipo") == "base"):
            errores.append(f"{nombre}: falta un identificador (pmid, doi o url)")
    errores += [f"{c}: clave repetida" for c in sorted({c for c in claves if claves.count(c) > 1})]
    material = (carpeta / "material.md").read_text(encoding="utf-8")
    citadas = {c for c, _ in citas(_sin_listas(material))}
    errores += [f"cita a una clave inexistente: @{c}" for c in sorted(citadas - set(claves))]
    errores += [f"{c}: no se cita en el material" for c in claves if c not in citadas]
    evidencias = carpeta / "evidencias.json"
    if evidencias.exists():
        for k, e in enumerate(json.loads(evidencias.read_text(encoding="utf-8")).get("evidencias", []), 1):
            if e.get("ref") and e["ref"] not in claves:
                errores.append(f"evidencia {k}: «ref» apunta a una clave inexistente ({e['ref']})")
    actual = re.search(re.escape(MARCAS[0]) + r"\s*(.*?)\s*" + re.escape(MARCAS[1]), material, re.S)
    if not actual:
        errores.append("la sección «## Fuentes» no tiene la lista generada: ejecuta «bibliografia.py lista --escribir»")
    elif actual.group(1).strip() != lista(carpeta).strip():
        errores.append("la lista de Fuentes no coincide con bibliografia.json: ejecuta «bibliografia.py lista --escribir»")
    if en_linea:
        e, a = _comprobar_en_linea(referencias)
        errores += e
        avisos += a
    return errores, avisos


def _comprobar_en_linea(referencias):
    import fuentes
    errores, avisos = [], []
    for r in referencias:
        if not r.get("pmid"):
            continue
        try:
            articulo = fuentes.pubmed(f"{r['pmid']}[uid]", maximo=1)
            for aviso in (articulo[0]["avisos"] if articulo else []):
                (errores if aviso.startswith(("RETRACTADO", "retractado")) else avisos).append(f"{r['clave']}: {aviso}")
            if r.get("tipo") == "guia":
                for c in fuentes.vigencia(r["pmid"])["posteriores"][:3]:
                    avisos.append(f"{r['clave']}: posible versión posterior: PMID {c['pmid']} ({c['anio']}), "
                                  f"{c['titulo'][:100]}")
        except RuntimeError as e:
            avisos.append(f"{r['clave']}: no se pudo consultar PubMed ({e})")
    return errores, avisos


# --- Cómo se buscó ----------------------------------------------------------------------------------------------

_BASES = {"pubmed": "PubMed", "guias": "PubMed (guías)", "vigencia": "PubMed (versiones posteriores)",
          "europepmc": "Europe PMC", "pmc_texto": "PubMed Central", "texto_completo": "texto completo (PMC y "
          "acceso abierto)", "acceso_abierto": "copias en acceso abierto (Unpaywall)", "mesh": "MeSH",
          "mondo": "MONDO", "pdf_texto": "documentos en PDF", "pagina": "páginas web", "openfda": "openFDA",
          "dailymed": "DailyMed", "cima": "CIMA (AEMPS)", "iris": "IRIS (OMS/OPS)", "binasss": "BINASSS (CCSS)",
          "reactome": "Reactome", "uniprot": "UniProt", "medlineplus": "MedlinePlus", "ema_epar": "EMA (EPAR)",
          "fda_indicaciones": "Drugs@FDA", "chembl": "ChEMBL", "pubchem": "PubChem", "cpic": "CPIC",
          "nice_guias": "NICE (guías)", "nice_guia": "NICE (recomendaciones)", "ema_medicamento": "EMA",
          "ensayos": "PubMed (ensayos)", "ensayo": "ClinicalTrials.gov", "nci_tesauro": "NCI Thesaurus",
          "livertox": "LiverTox", "lactmed": "LactMed", "ncbi_gene": "NCBI Gene", "chembl_actividad": "ChEMBL (actividades)",
          "bindingdb": "BindingDB", "openfda_eventos": "FAERS (openFDA)", "pdb_buscar": "RCSB PDB"}


def resumen_busqueda(carpeta):
    """Resumen en Markdown de busquedas.jsonl: fechas, fuentes consultadas y consultas de literatura."""
    ruta = Path(carpeta) / "busquedas.jsonl"
    if not ruta.exists():
        raise FileNotFoundError("No hay busquedas.jsonl: usa fuentes.py --registro <carpeta> al buscar")
    lineas = [json.loads(x) for x in ruta.read_text(encoding="utf-8").splitlines() if x.strip()]
    fechas = sorted(x["fecha"][:10] for x in lineas)
    cuenta = {}
    for x in lineas:
        nombre = _BASES.get(x["funcion"], x["funcion"])
        cuenta[nombre] = cuenta.get(nombre, 0) + 1
    periodo = fecha_es(fechas[0]) if fechas[0] == fechas[-1] else f"del {fecha_es(fechas[0])} al {fecha_es(fechas[-1])}"
    texto = [f"Búsqueda realizada el {periodo} con las herramientas de la skill (`fuentes.py`), "
             f"{len(lineas)} consultas en total.", "",
             "- **Fuentes consultadas:** " + "; ".join(f"{n} ({c})" for n, c in sorted(cuenta.items(),
                                                                                          key=lambda x: -x[1])) + "."]
    literatura = [x for x in lineas if x["funcion"] in ("guias", "nice_guias", "pubmed", "europepmc", "vigencia",
                                                          "ensayos")]
    if literatura:
        texto.append("- **Búsquedas de literatura:**")
        for x in literatura:
            argumento = x["argumentos"][0] if x["argumentos"] else ""
            if x["funcion"] == "vigencia":
                posteriores = len(x["resultado"].get("posteriores", []))
                cuantas = {0: "ninguna candidata", 1: "1 candidata"}.get(posteriores, f"{posteriores} candidatas")
                texto.append(f"  - {_BASES['vigencia']}: PMID {argumento} ({cuantas})")
                continue
            n = x["resultado"].get("n")
            detalle = "" if n is None else f" ({n} resultado{'' if n == 1 else 's'})"
            if x.get("opciones", {}).get("titulo") == "True":
                detalle = detalle.replace(")", ", en el título)") if detalle else " (en el título)"
            texto.append(f"  - {_BASES[x['funcion']]}: `{argumento}`{detalle}")
    texto.append("- **Criterios:** guías y consensos de los últimos 5 años, con prioridad para el texto completo; "
                 "cada cifra se comprobó en la frase original de la fuente (registro de evidencias).")
    return "\n".join(texto)


def escribir_busqueda(carpeta):
    _escribir_entre_marcas(carpeta, "Cómo se buscó", MARCAS_BUSQUEDA, resumen_busqueda(carpeta))


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    accion, carpeta, *resto = sys.argv[1:]
    if accion == "nueva":
        clave, opciones = resto[0], {}
        for nombre in ("pmid", "doi", "url", "tipo", "cita", "sello", "idioma", "version", "nota", "cima", "dailymed",
                       "ema", "nct", "nice"):
            if f"--{nombre}" in resto:
                opciones[nombre] = resto[resto.index(f"--{nombre}") + 1]
        print(json.dumps(nueva(carpeta, clave, **opciones), ensure_ascii=False, indent=1))
    elif accion == "comprobar":
        errores, avisos = comprobar(carpeta, en_linea="--en-linea" in resto)
        for e in errores:
            print(f"ERROR  {e}")
        for a in avisos:
            print(f"aviso  {a}")
        print(f"{len(errores)} errores, {len(avisos)} avisos." if errores or avisos else "Bibliografía completa.")
        sys.exit(1 if errores else 0)
    elif accion == "lista":
        escribir_lista(carpeta) if "--escribir" in resto else print(lista(carpeta))
    elif accion == "busqueda":
        escribir_busqueda(carpeta) if "--escribir" in resto else print(resumen_busqueda(carpeta))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
