"""Consulta de fuentes abiertas para el material de fisiopatología de una enfermedad.

Cada función devuelve datos verificables y registra la procedencia en
`assets/ilustraciones/registro.json` cuando guarda un archivo.

Uso rápido desde la terminal:
  python3 fuentes.py pubchem darolutamida
  python3 fuentes.py chembl darolutamide
  python3 fuentes.py pdb-buscar "androgen receptor darolutamide"
  python3 fuentes.py pdb-ligandos 2AMA
  python3 fuentes.py bioicons testis
  python3 fuentes.py servier-kits
  python3 fuentes.py servier-diapositivas Endocrinology
  python3 fuentes.py servier-extraer Endocrinology 11 "Group 641" testiculo
  python3 fuentes.py cima atorvastatina          # ficha técnica en español (AEMPS)
  python3 fuentes.py dailymed atorvastatin       # ficha técnica de la FDA
  python3 fuentes.py uniprot SREBF2
  python3 fuentes.py reactome "SREBP cholesterol"
  python3 fuentes.py europepmc "SREBP-2 AND LDL receptor AND statin" "SREBP-?2.*(LDLR|LDL receptor)"
  python3 fuentes.py pdf <URL del PDF> "<regex>"   # frases de un PDF público con su página
  python3 fuentes.py uniprot-proteina "beta-lactamase" 1280   # proteína de S. aureus (taxón 1280)

Si una fuente no responde (red bloqueada), las funciones lanzan RuntimeError con el
nombre del dominio para avisar a la persona usuaria; no inventan datos.
"""
import html
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ILUSTRACIONES = RAIZ / "assets" / "ilustraciones"
REGISTRO = ILUSTRACIONES / "registro.json"
CACHE = Path("/tmp/fisiopatologia-cache")
CACHE.mkdir(exist_ok=True)
AGENTE = "fisiopatologia/1.0"  # User-Agent de las consultas

LICENCIAS = {
    "servier": "CC BY 4.0 (Servier Medical Art, smart.servier.com)",
    "servier-bioicons": "CC BY 3.0 (Servier Medical Art vía Bioicons)",
    "pubchem": "Dominio público (NCBI PubChem)",
    "chembl": "CC BY-SA 3.0 (EMBL-EBI ChEMBL)",
    "pdb": "CC0 (RCSB Protein Data Bank)",
    "alphafold": "CC BY 4.0 (AlphaFold DB, EMBL-EBI/Google DeepMind)",
    "nih-bioart": "Dominio público salvo indicación (NIH BioArt, bioart.niaid.nih.gov)",
    "bioicons": "Según carpeta de licencia del icono (Bioicons)",
    "togotv": "CC BY 4.0 (© DBCLS TogoTV, togotv.dbcls.jp)",
    "commons": "Según la ficha del archivo en Wikimedia Commons",
}


def _get(url, timeout=60, datos=None, cabeceras=None, intentos=4):
    """Descarga una URL. Reintenta con espera creciente si el servidor limita la frecuencia (429), falla (5xx)
    o se corta la conexión; ante un 429 respeta la cabecera Retry-After (hasta 30 s)."""
    import time
    import urllib.error
    req = urllib.request.Request(url, data=datos, headers=cabeceras or {"User-Agent": AGENTE})
    for intento in range(intentos):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if (e.code == 429 or e.code >= 500) and intento < intentos - 1:
                espera = e.headers.get("Retry-After", "") if e.headers else ""
                time.sleep(min(int(espera), 30) if espera.isdigit() else 2 ** intento)
                continue
            error = e
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            if intento < intentos - 1:  # corte de red o túnel cerrado: suele ser pasajero
                time.sleep(2 ** intento)
                continue
            error = e
        except Exception as e:  # noqa: BLE001
            error = e
        break
    dominio = urllib.parse.urlparse(url).netloc
    raise RuntimeError(f"No se pudo consultar {dominio}: {error}. Puede que la red del entorno lo bloquee.") from error


def registrar(archivo, fuente, origen, notas=""):
    """Anota procedencia y licencia de un archivo incorporado a la biblioteca."""
    registro = json.loads(REGISTRO.read_text()) if REGISTRO.exists() else {}
    registro[Path(archivo).name] = {"fuente": fuente, "licencia": LICENCIAS.get(fuente, fuente), "origen": origen,
                                   "fecha": date.today().isoformat(), "notas": notas}
    REGISTRO.write_text(json.dumps(registro, indent=2, ensure_ascii=False))


# --- Química -------------------------------------------------------------------

def pubchem(nombre):
    """SMILES, fórmula y CID de un compuesto por nombre (inglés o DCI)."""
    q = urllib.parse.quote(nombre)
    url = (f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{q}/property/"
           "IsomericSMILES,CanonicalSMILES,MolecularFormula,IUPACName/JSON")
    p = json.loads(_get(url))["PropertyTable"]["Properties"][0]
    smiles = p.get("IsomericSMILES") or p.get("SMILES") or p.get("CanonicalSMILES") or p.get("ConnectivitySMILES")
    return {"cid": p["CID"], "smiles": smiles, "formula": p["MolecularFormula"], "iupac": p.get("IUPACName"),
            "fuente": f"PubChem CID {p['CID']}"}


def chembl(nombre):
    """Mecanismo de acción y diana documentados en ChEMBL.

    Busca primero por nombre exacto y, si no, por texto; usa la molécula «padre» porque
    las sales (p. ej., atorvastatina cálcica) no tienen mecanismos asociados.
    """
    q = urllib.parse.quote(nombre)
    base = "https://www.ebi.ac.uk/chembl/api/data"
    mols = json.loads(_get(f"{base}/molecule.json?pref_name__iexact={q}&limit=1"))["molecules"]
    mols += json.loads(_get(f"{base}/molecule/search.json?q={q}&limit=5"))["molecules"]
    ids = []
    for m in mols:
        padre = (m.get("molecule_hierarchy") or {}).get("parent_chembl_id") or m["molecule_chembl_id"]
        if padre not in ids:
            ids.append(padre)
    for chembl_id in ids:
        # El mecanismo puede estar registrado en una sal (molécula hija); se busca por la molécula padre.
        mecs = json.loads(_get(f"{base}/mechanism.json?parent_molecule_chembl_id={chembl_id}"))["mechanisms"]
        if not mecs:
            continue
        salida = []
        for m in mecs:
            diana = json.loads(_get(f"{base}/target/{m['target_chembl_id']}.json"))
            salida.append({"chembl_id": chembl_id, "mecanismo": m["mechanism_of_action"], "accion": m["action_type"],
                           "diana": diana["pref_name"], "tipo_diana": diana["target_type"],
                           "referencias": [r.get("ref_url") for r in m.get("mechanism_refs", [])]})
        return salida
    return []


# --- Estructuras de proteínas -------------------------------------------------

def pdb_buscar(texto, filas=10):
    consulta = {"query": {"type": "terminal", "service": "full_text", "parameters": {"value": texto}},
                "return_type": "entry", "request_options": {"paginate": {"start": 0, "rows": filas}}}
    r = json.loads(_get("https://search.rcsb.org/rcsbsearch/v2/query", datos=json.dumps(consulta).encode(),
                        cabeceras={"Content-Type": "application/json"}))
    salida = []
    for e in r.get("result_set", []):
        d = json.loads(_get(f"https://data.rcsb.org/rest/v1/core/entry/{e['identifier']}"))
        salida.append({"pdb": e["identifier"], "titulo": d["struct"]["title"]})
    return salida


def pdb_ligandos(pdb_id):
    d = json.loads(_get(f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"))
    ids = d["rcsb_entry_container_identifiers"].get("non_polymer_entity_ids") or []
    salida = []
    for e in ids:
        n = json.loads(_get(f"https://data.rcsb.org/rest/v1/core/nonpolymer_entity/{pdb_id}/{e}"))["pdbx_entity_nonpoly"]
        salida.append({"codigo": n["comp_id"], "nombre": n["name"]})
    return salida


def pdb_descargar(pdb_id):
    destino = CACHE / f"{pdb_id.upper()}.pdb"
    if not destino.exists():
        destino.write_bytes(_get(f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb", timeout=120))
    return destino


def alphafold_descargar(uniprot):
    destino = CACHE / f"AF-{uniprot}.pdb"
    if not destino.exists():
        info = json.loads(_get(f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot}"))[0]
        destino.write_bytes(_get(info["pdbUrl"], timeout=120))
    return destino


# --- Ilustraciones -------------------------------------------------------------

def bioicons(termino, repo=CACHE / "bioicons"):
    """Busca iconos en Bioicons (GitHub). Devuelve rutas con su carpeta de licencia."""
    if not repo.exists():
        subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--sparse",
                        "https://github.com/duerrsimon/bioicons.git", str(repo)], check=True, timeout=600)
        subprocess.run(["git", "-C", str(repo), "sparse-checkout", "set", "static/icons"], check=True, timeout=600)
    base = repo / "static" / "icons"
    return [str(p.relative_to(base)) for p in base.rglob("*.svg") if termino.lower() in p.name.lower()]


def togopic(termino, maximo=30):
    """Busca en la galería de TogoTV (DBCLS, Japón; CC BY 4.0). La búsqueda mira el nombre y las etiquetas:
    en inglés solo encuentra por el nombre; en japonés también por la etiqueta (感染症, 細菌, ウイルス, 真菌…)."""
    q = urllib.parse.urlencode({"target": "pictures", "text": termino})
    datos = json.loads(_get(f"https://togotv-api.dbcls.jp/api/search?{q}"))["data"][:maximo]
    return [{"nombre": d.get("name_en"), "nombre_ja": d.get("name"), "svg": d.get("svg"), "doi": d.get("id"),
             "licencia": d.get("license"), "autoria": d.get("author_str"), "fecha": d.get("uploadDate"),
             "etiquetas": d.get("other_tags_comma_en")} for d in datos if d.get("svg")]


def togopic_descargar(svg, nombre, doi=""):
    """Descarga un SVG de TogoTV a assets/ilustraciones/togotv-<nombre>.svg y lo registra.
    svg: el campo «svg» de togopic(); doi: el campo «doi» (identifica la imagen en el registro)."""
    destino = ILUSTRACIONES / f"togotv-{nombre}.svg"
    destino.write_bytes(_get("https://dbarchive.biosciencedbc.jp/data/togo-pic/image/" + urllib.parse.quote(svg),
                             timeout=120))
    registrar(destino, "togotv", f"TogoTV {svg} {doi}".strip())
    return destino


def _commons_info(paginas):
    salida = []
    for pagina_ in paginas:
        info = pagina_["imageinfo"][0]
        meta = info.get("extmetadata", {})
        licencia = meta.get("LicenseShortName", {}).get("value", "")
        if re.search(r"\bN[CD]\b|NonCommercial|NoDeriv", licencia, re.I):
            continue
        salida.append({"titulo": pagina_["title"], "url": info["url"].split("?")[0], "licencia": licencia,
                       "autoria": _texto_plano(meta.get("Artist", {}).get("value", "")).strip()[:120],
                       "aviso": "CC BY-SA: avisa antes de usarla" if "SA" in licencia else None})
    return salida


def _commons_api(parametros):
    q = urllib.parse.urlencode({"action": "query", "format": "json", "prop": "imageinfo",
                                "iiprop": "url|extmetadata", **parametros})
    datos = json.loads(_get(f"https://commons.wikimedia.org/w/api.php?{q}", cabeceras=COMMONS_UA))
    return list(datos.get("query", {}).get("pages", {}).values())


COMMONS_UA = {"User-Agent": "skills-docencia/1.0 (https://github.com/davidtencio/skills; material educativo)"}


def commons(termino, maximo=20):
    """Busca dibujos y diagramas en Wikimedia Commons, en cualquier idioma (p. ej., «Pharmakokinetik»,
    «pharmacocinétique»). Devuelve la licencia y la autoría de cada archivo; descarta las licencias NC y ND."""
    return _commons_info(_commons_api({"generator": "search", "gsrnamespace": 6,
                                       "gsrsearch": f"{termino} filetype:drawing", "gsrlimit": maximo}))


def commons_descargar(titulo, nombre):
    """Descarga un archivo de Wikimedia Commons («File:…») a assets/ilustraciones/commons-<nombre>.<ext>
    y lo registra con su licencia y autoría. Rechaza las licencias NC y ND."""
    archivos = _commons_info(_commons_api({"titles": titulo}))
    if not archivos:
        raise ValueError(f"{titulo}: no existe o su licencia no permite reutilizarlo (NC o ND)")
    r = archivos[0]
    destino = ILUSTRACIONES / f"commons-{nombre}{Path(r['url']).suffix}"
    destino.write_bytes(_get(r["url"], timeout=120, cabeceras=COMMONS_UA))
    registrar(destino, "commons", f"Wikimedia Commons, {r['titulo']}", f"{r['licencia']}; autoría: {r['autoria']}")
    return destino


def servier_kits():
    """Kits de PowerPoint de Servier Medical Art por categoría (vectoriales, CC BY 4.0)."""
    html = _get("https://smart.servier.com/image-kits-by-category/").decode("utf-8", "ignore")
    return sorted(set(re.findall(r"https://smart\.servier\.com/wp-content/uploads/[^\"]+\.pptx", html)))


def _kit(nombre):
    pptx = CACHE / f"SMART-{nombre}.pptx"
    if not pptx.exists():
        url = next(u for u in servier_kits() if u.endswith(f"SMART-{nombre}.pptx"))
        pptx.write_bytes(_get(url, timeout=300))
    return pptx


def servier_diapositivas(kit):
    """Lista diapositivas y grupos de dibujo de un kit, con sus títulos."""
    from pptx import Presentation
    p = Presentation(str(_kit(kit)))
    salida = []
    for i, s in enumerate(p.slides, 1):
        textos = [sh.text_frame.text.strip() for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
        grupos = [sh.name for sh in s.shapes if sh.shape_type == 6]
        if grupos:
            salida.append({"diapositiva": i, "textos": textos[:4], "grupos": grupos})
    return salida


def servier_extraer(kit, diapositiva, grupo, nombre, recorte=None):
    """Extrae un dibujo de un kit de Servier como SVG vectorial sin el fondo de la diapositiva.

    Requiere LibreOffice Impress (soffice), python-pptx y pymupdf.
    recorte: (x0, y0, x1, y1) en puntos de la diapositiva para quedarse con una parte del grupo.
    """
    import pymupdf
    from pptx import Presentation
    ns = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
    p = Presentation(str(_kit(kit)))
    for m in p.slide_masters:
        for contenedor in [m] + list(m.slide_layouts):
            for sh in list(contenedor.shapes):
                sh._element.getparent().remove(sh._element)
            fondo = contenedor._element.find(f".//{ns}bg")
            if fondo is not None:
                fondo.getparent().remove(fondo)
    s = p.slides[diapositiva - 1]
    caja = None
    for sh in list(s.shapes):
        if sh.name == grupo:
            caja = (sh.left / 12700, sh.top / 12700, (sh.left + sh.width) / 12700, (sh.top + sh.height) / 12700)
        else:
            sh._element.getparent().remove(sh._element)
    if caja is None:
        raise ValueError(f"No existe el grupo {grupo!r} en la diapositiva {diapositiva}")
    tmp = CACHE / f"extraer-{nombre}.pptx"
    p.save(str(tmp))
    subprocess.run(["soffice", "--headless", "--norestore", "-env:UserInstallation=file:///tmp/lo_profile",
                    "--convert-to", "pdf", "--outdir", str(CACHE), str(tmp)], check=True, capture_output=True,
                   timeout=600)
    svg = pymupdf.open(str(tmp.with_suffix(".pdf")))[diapositiva - 1].get_svg_image(text_as_path=True)
    # Quita el rectángulo blanco de fondo que LibreOffice añade a cada página
    svg = re.sub(r'<path[^>]*d="M0 [\d.]+H[\d.]+V[\d.]+H0V[\d.]+Z" fill="#ffffff"[^>]*/>', "", svg)
    x0, y0, x1, y1 = recorte or caja
    svg = re.sub(r'viewBox="[^"]*"', f'viewBox="{x0 - 2:.1f} {y0 - 2:.1f} {x1 - x0 + 4:.1f} {y1 - y0 + 4:.1f}"', svg, 1)
    svg = re.sub(r'width="[^"]*" height="[^"]*"', f'width="{x1 - x0 + 4:.0f}" height="{y1 - y0 + 4:.0f}"', svg, 1)
    destino = ILUSTRACIONES / f"servier4-{nombre}.svg"
    destino.write_text(svg)
    registrar(destino, "servier", f"Kit SMART-{kit}.pptx, diapositiva {diapositiva}, {grupo}",
              f"recorte {recorte}" if recorte else "")
    return destino


# --- Verificación: fichas técnicas, biología curada y literatura ------------------

def _texto_plano(contenido):
    import html as _html
    contenido = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", contenido, flags=re.S)
    return _html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", contenido)))


def dailymed(nombre, secciones=("12.1 Mechanism of Action", "12.3 Pharmacokinetics", "12.4 Microbiology", "5.1 ",
                                 "7.1 "), largo=1200):
    """Ficha técnica de la FDA (DailyMed): devuelve fragmentos de las secciones pedidas.
    En los antimicrobianos, el mecanismo, la resistencia y la sensibilidad están en 12.4 Microbiology."""
    q = urllib.parse.quote(nombre)
    datos = json.loads(_get(f"https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name={q}&pagesize=1"))
    if not datos["data"]:
        return {}
    spl = datos["data"][0]
    texto = _texto_plano(_get(f"https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{spl['setid']}.xml",
                              timeout=120).decode("utf-8", "ignore"))
    salida = {"fuente": f"DailyMed, {spl['title'][:120]} (setid {spl['setid']})"}
    for sec in secciones:
        i = texto.find(sec)
        if i >= 0:
            salida[sec.strip()] = texto[i:i + largo]
    return salida


def cima(nombre, secciones=("4.1", "4.2", "4.5", "4.8", "5.1", "5.2", "5.3"), largo=1500):
    """Ficha técnica española (CIMA, AEMPS), en español. Prefiere monofármacos."""
    q = urllib.parse.quote(nombre)
    res = json.loads(_get(f"https://cima.aemps.es/cima/rest/medicamentos?nombre={q}"))["resultados"]
    res = sorted(res, key=lambda r: ("/" in r["nombre"], len(r["nombre"])))
    for r in res:
        ficha = next((d for d in r.get("docs", []) if d["tipo"] == 1 and d.get("urlHtml")), None)
        if not ficha:
            continue
        texto = _texto_plano(_get(ficha["urlHtml"], timeout=120).decode("utf-8", "ignore"))
        salida = {"fuente": f"CIMA (AEMPS), ficha técnica de {r['nombre']} (n.º registro {r['nregistro']})",
                  "url": ficha["urlHtml"]}
        for sec in secciones:
            m = re.search(rf"\b{re.escape(sec)}\.? [A-ZÁÉÍÓÚ][^0-9]{{3,60}}", texto)
            if m:
                salida[sec] = texto[m.start():m.start() + largo]
        return salida
    return {}


def uniprot(gen=None, organismo=9606, proteina=None, maximo=10):
    """Función de una proteína revisada en UniProt (con PMID de respaldo), por gen o por nombre de proteína.

    Por gen, se queda con la entrada cuyo nombre de gen principal coincide exactamente: algunos símbolos
    (p. ej., KLK3) también aparecen como sinónimos de otros genes. Por proteína (p. ej., «penicillin-binding
    protein 2a»), sirve también para bacterias, hongos y virus: organismo=None busca en todos, o pasa el
    identificador de taxonomía de NCBI (1280 = Staphylococcus aureus; 287 = Pseudomonas aeruginosa).
    """
    if not gen and not proteina:
        raise ValueError("Indica gen o proteina")
    partes = [f"gene:{gen}" if gen else f'protein_name:"{proteina}"', "reviewed:true"]
    if organismo:
        partes.append(f"taxonomy_id:{organismo}")  # incluye las cepas del taxón
    q = urllib.parse.quote(" AND ".join(partes))
    tsv = _get(f"https://rest.uniprot.org/uniprotkb/search?query={q}&fields=accession,gene_primary,protein_name,"
               f"organism_name,cc_function,cc_subcellular_location&format=tsv&size={maximo}").decode()
    filas = [f.split("\t") + [""] * 6 for f in tsv.strip().split("\n")[1:] if f]
    if gen:
        filas = [f for f in filas if f[1].upper() == gen.upper()] or filas
    return [{"uniprot": f[0], "gen": f[1], "proteina": f[2], "organismo": f[3], "funcion": f[4],
             "localizacion": f[5]} for f in filas]


def reactome(texto, especie="Homo sapiens"):
    """Vías de Reactome que coinciden con el texto, con su resumen."""
    q = urllib.parse.quote(texto)
    r = json.loads(_get(f"https://reactome.org/ContentService/search/query?query={q}&species="
                        f"{urllib.parse.quote(especie)}&types=Pathway"))
    salida = []
    for grupo in r.get("results", []):
        for e in grupo["entries"][:5]:
            d = json.loads(_get(f"https://reactome.org/ContentService/data/query/{e['stId']}"))
            resumen = re.sub(r"<[^>]+>", "", (d.get("summation") or [{}])[0].get("text", ""))
            salida.append({"reactome": e["stId"], "via": re.sub(r"<[^>]+>", "", e["name"]), "resumen": resumen[:1500]})
    return salida


def europepmc(consulta, patron=None, maximo=60, citas_minimas=20):
    """Busca en Europe PMC y devuelve frases de resúmenes que respaldan una afirmación.

    patron: expresión regular que debe cumplir la frase (p. ej., r"SREBP-?2.*LDL"). Ordena por citas.
    """
    q = urllib.parse.quote(consulta)
    r = json.loads(_get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}&format=json"
                        f"&pageSize={maximo}&resultType=core&sort=CITED%20desc"))
    salida = []
    for a in r["resultList"]["result"]:
        if (a.get("citedByCount") or 0) < citas_minimas:
            continue
        resumen = re.sub(r"<[^>]+>", "", a.get("abstractText", ""))
        frases = [f for f in re.split(r"(?<=\.) ", resumen) if not patron or re.search(patron, f, re.I)]
        if frases:
            salida.append({"pmid": a.get("pmid"), "titulo": a["title"], "revista": a.get("journalTitle"),
                           "anio": a.get("pubYear"), "citas": a.get("citedByCount"), "frases": frases[:2]})
    return salida


EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def pubmed(consulta, patron=None, maximo=40, revisiones=False, completo=False):
    """Busca en PubMed (NCBI, NIH) y devuelve frases de resúmenes que respaldan una afirmación.

    Complementa a europepmc: PubMed ordena por relevancia e incluye revisiones y guías recientes.
    patron: expresión regular que debe cumplir la frase. revisiones=True limita a revisiones.
    """
    termino = consulta + (" AND review[pt]" if revisiones else "")
    q = urllib.parse.quote(termino)
    ids = json.loads(_get(f"{EUTILS}/esearch.fcgi?db=pubmed&term={q}&retmax={maximo}&sort=relevance"
                          f"&retmode=json"))["esearchresult"]["idlist"]
    if not ids:
        return []
    xml = _get(f"{EUTILS}/efetch.fcgi?db=pubmed&id={','.join(ids)}&retmode=xml", timeout=120).decode("utf-8", "ignore")
    salida = []
    for art in re.findall(r"<Pubmed(?:Book)?Article>.*?</Pubmed(?:Book)?Article>", xml, re.S):
        pmid = re.search(r"<PMID[^>]*>(\d+)</PMID>", art).group(1)
        titulo = re.sub(r"<[^>]+>", "", (re.search(r"<ArticleTitle[^>]*>(.*?)</ArticleTitle>", art, re.S) or [None, ""])[1])
        revista = (re.search(r"<ISOAbbreviation>(.*?)</ISOAbbreviation>", art)
                   or re.search(r"<BookTitle[^>]*>(.*?)</BookTitle>", art) or [None, ""])[1]
        anio = (re.search(r"<PubDate>.*?<Year>(\d{4})</Year>", art, re.S) or [None, ""])[1]
        resumen = " ".join(re.sub(r"<[^>]+>", "", t) for t in re.findall(r"<AbstractText[^>]*>(.*?)</AbstractText>", art, re.S))
        frases = [f for f in re.split(r"(?<=\.) ", resumen) if not patron or re.search(patron, f, re.I)]
        if frases:
            salida.append({"pmid": pmid, "titulo": titulo, "revista": revista, "anio": anio,
                           "frases": frases if completo else frases[:2]})
    return salida


def ncbi_gene(gen, organismo=9606):
    """Resumen curado del gen en NCBI Gene (NIH): función, nombres alternativos y localización."""
    q = urllib.parse.quote(f"{gen}[sym] AND {organismo}[taxid]")
    ids = json.loads(_get(f"{EUTILS}/esearch.fcgi?db=gene&term={q}&retmode=json"))["esearchresult"]["idlist"]
    if not ids:
        return None
    d = json.loads(_get(f"{EUTILS}/esummary.fcgi?db=gene&id={ids[0]}&retmode=json"))["result"][ids[0]]
    return {"gene_id": ids[0], "simbolo": d["name"], "nombre": d["description"], "alias": d.get("otheraliases"),
            "cromosoma": d.get("maplocation"), "resumen": d.get("summary")}


def nci_tesauro(nombre):
    """Definición del fármaco en el NCI Thesaurus (Instituto Nacional del Cáncer, NIH).

    Útil sobre todo en oncología: describe mecanismo, diana y clase con lenguaje revisado.
    """
    q = urllib.parse.quote(nombre)
    r = json.loads(_get(f"https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/search?term={q}"
                        f"&type=match&include=definitions,synonyms&pageSize=3"))
    salida = []
    for c in r.get("concepts", []):
        defs = [d["definition"] for d in c.get("definitions", []) if d.get("source") in ("NCI", "NCI-GLOSS")]
        salida.append({"codigo": c["code"], "nombre": c["name"], "definiciones": defs})
    return salida


def _monografia_nih(nombre, editor, libro, patron=None):
    """Monografías del NIH indexadas en PubMed como libro (LiverTox, LactMed): texto completo del resumen."""
    import html as _html
    res = pubmed(f'"{nombre}"[ti] AND "{editor}"[pb]', patron, maximo=5, completo=True)
    for r in res:
        r["revista"] = _html.unescape(r["revista"])
    return [r for r in res if libro in r["revista"]]


def livertox(nombre, patron=None):
    """Hepatotoxicidad del fármaco según LiverTox (NIDDK, NIH), con PMID. nombre en inglés."""
    return _monografia_nih(nombre, "National Institute of Diabetes and Digestive and Kidney Diseases", "LiverTox", patron)


def lactmed(nombre, patron=None):
    """Paso a la leche y seguridad en la lactancia según LactMed (NICHD, NIH), con PMID. nombre en inglés."""
    return _monografia_nih(nombre, "National Institute of Child Health and Human Development", "LactMed", patron)


def medlineplus(nombre):
    """Información para pacientes en MedlinePlus (NLM, NIH), en español, a partir del RxCUI."""
    q = urllib.parse.quote(nombre)
    rx = json.loads(_get(f"https://rxnav.nlm.nih.gov/REST/rxcui.json?name={q}&search=2"))
    rxcui = (rx.get("idGroup", {}).get("rxnormId") or [None])[0]
    if not rxcui:
        return None
    r = json.loads(_get("https://connect.medlineplus.gov/service?mainSearchCriteria.v.cs=2.16.840.1.113883.6.88"
                        f"&mainSearchCriteria.v.c={rxcui}&informationRecipient.languageCode.c=es"
                        "&knowledgeResponseType=application/json"))
    entradas = r.get("feed", {}).get("entry", [])
    return [{"rxcui": rxcui, "titulo": e["title"]["_value"], "url": e["link"][0]["href"],
             "resumen": _texto_plano(e.get("summary", {}).get("_value", ""))[:800]} for e in entradas]


def chembl_actividad(nombre, diana=None, tipos=("IC50", "Ki", "Kd", "EC50"), maximo=200):
    """Potencia y selectividad del fármaco en ChEMBL: actividades medidas, agrupadas por diana.

    Devuelve por diana la mediana y el rango (nM) de cada tipo de medida y el número de ensayos.
    diana: filtra por texto en el nombre de la diana (p. ej., "HMG-CoA"). Útil para mostrar con
    números la afinidad por la diana frente a otras proteínas (selectividad).
    """
    from statistics import median
    info = chembl(nombre)
    if not info:
        return None
    base = "https://www.ebi.ac.uk/chembl/api/data"
    acts = json.loads(_get(f"{base}/activity.json?molecule_chembl_id={info[0]['chembl_id']}"
                           f"&standard_type__in={','.join(tipos)}&standard_units=nM&target_organism=Homo%20sapiens"
                           f"&limit={maximo}", timeout=120))["activities"]
    grupos = {}
    for a in acts:
        if a.get("standard_value") is None or (diana and diana.lower() not in (a.get("target_pref_name") or "").lower()):
            continue
        clave = (a["target_pref_name"], a["standard_type"])
        grupos.setdefault(clave, []).append((float(a["standard_value"]), a.get("document_chembl_id")))
    salida = [{"diana": d, "tipo": t, "mediana_nM": round(median(v for v, _ in vals), 3),
               "min_nM": min(v for v, _ in vals), "max_nM": max(v for v, _ in vals), "n": len(vals),
               "documentos": sorted({doc for _, doc in vals if doc})[:5]}
              for (d, t), vals in grupos.items()]
    return sorted(salida, key=lambda x: x["mediana_nM"])


def bindingdb(uniprot, smiles, corte_nM=100000):
    """Afinidades del fármaco por una diana en BindingDB (segunda fuente para las cifras de ChEMBL).

    Compara los ligandos de la diana con el SMILES del fármaco (de PubChem) sin estereoquímica.
    """
    from rdkit import Chem
    def clave(smi):
        m = Chem.MolFromSmiles(smi)
        if m is None:
            return None
        Chem.RemoveStereochemistry(m)
        return Chem.MolToSmiles(m)
    objetivo = clave(smiles)
    r = json.loads(_get(f"https://www.bindingdb.org/rest/getLigandsByUniprots?uniprot={uniprot}&cutoff={corte_nM}"
                        "&response=application/json", timeout=180))
    afinidades = r.get("getLindsByUniprotsResponse", r.get("getLigandsByUniprotsResponse", {})).get("affinities", [])
    return [{"tipo": a["affinity_type"], "valor_nM": a["affinity"], "pmid": a.get("pmid"), "doi": a.get("doi")}
            for a in afinidades if clave(a["smile"]) == objetivo]


def ema_epar(nombre, patron, documento="public-assessment-report", contexto=1):
    """Frases del informe público de evaluación de la EMA (EPAR) que cumplen un patrón, con su página.

    Solo existe para medicamentos autorizados por procedimiento centralizado (la mayoría de los nuevos,
    biológicos y oncológicos). nombre: marca comercial (p. ej., "enhertu"). El EPAR detalla
    farmacocinética, metabolitos, transportadores, exposición-respuesta y poblaciones especiales.
    """
    slug = re.sub(r"[^a-z0-9]+", "-", nombre.lower()).strip("-")
    destino = CACHE / f"epar-{slug}-{documento}.pdf"
    if not destino.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(_get(f"https://www.ema.europa.eu/en/documents/assessment-report/"
                                 f"{slug}-epar-{documento}_en.pdf", timeout=300))
    return _frases_pdf(destino, patron, contexto)


def _frases_pdf(ruta, patron, contexto=1, maximo=None):
    """Frases de un PDF que cumplen el patrón (regex, sin distinguir mayúsculas), con su página y las
    `contexto - 1` frases vecinas a cada lado."""
    import pymupdf
    salida = []
    for n, pagina_ in enumerate(pymupdf.open(ruta), 1):
        frases = re.split(r"(?<=[.;])\s+", re.sub(r"\s+", " ", pagina_.get_text()))
        for i, f in enumerate(frases):
            if re.search(patron, f, re.I):
                salida.append({"pagina": n, "texto": " ".join(frases[max(0, i - contexto + 1):i + contexto])})
                if maximo and len(salida) >= maximo:
                    return salida
    return salida


def pdf_texto(url, patrones=(), contexto=1, maximo=8):
    """Frases de un PDF público (guía nacional, documento de posición, informe técnico) que cumplen cada patrón,
    con el número de página para citarlas. url: dirección del PDF o ruta local. El PDF se guarda en la caché.
    Si el PDF es una imagen escaneada no tiene texto: lo indica en «aviso»."""
    import hashlib
    import pymupdf
    if Path(url).exists():
        ruta = Path(url)
    else:
        ruta = CACHE / f"pdf-{hashlib.sha1(url.encode()).hexdigest()[:16]}.pdf"
        if not ruta.exists():
            ruta.write_bytes(_get(url, timeout=300, cabeceras={"User-Agent": "Mozilla/5.0 (compatible; "
                                                                             "skills-docencia/1.0)"}))
    documento = pymupdf.open(ruta)
    caracteres = sum(len(p.get_text()) for p in documento)
    return {"url": url, "titulo": (documento.metadata or {}).get("title") or None, "paginas": len(documento),
            "aviso": "sin texto extraíble: puede ser un escaneo" if caracteres < 20 * len(documento) else None,
            "fragmentos": {p: _frases_pdf(ruta, p, contexto, maximo) for p in patrones}}


def openfda(nombre, secciones=("clinical_pharmacology", "mechanism_of_action", "microbiology", "pharmacokinetics",
                               "drug_interactions", "pharmacogenomics", "use_in_specific_populations"), largo=2500):
    """Ficha de la FDA ya separada por secciones (openFDA). nombre: genérico en inglés.
    En los antimicrobianos, 12.1 suele remitir a 12.4 («microbiology»): ahí están el mecanismo y la resistencia.
    Las fichas antiguas sin formato PLR no tienen ese campo; su «Microbiology» va dentro de clinical_pharmacology."""
    q = urllib.parse.quote(f'openfda.generic_name:"{nombre}"')
    fichas = json.loads(_get(f"https://api.fda.gov/drug/label.json?search={q}&limit=25", timeout=90))["results"]
    r = max(fichas, key=lambda f: _puntuar_ficha(f, nombre, secciones))
    salida = {"set_id": r.get("set_id"), "fecha": r.get("effective_time")}
    for s in secciones:
        if r.get(s):
            salida[s] = " ".join(r[s])[:largo]
    return salida


def _puntuar_ficha(ficha, nombre, secciones):
    """Orden de preferencia entre fichas de openFDA: primero la del principio activo solo (no una combinación),
    después la que tiene más secciones de las pedidas y, a igualdad, la más reciente."""
    genericos = [g.strip().upper() for g in ficha.get("openfda", {}).get("generic_name", [])]
    solo = any(g == nombre.strip().upper() for g in genericos)
    return solo, sum(bool(ficha.get(s)) for s in secciones), ficha.get("effective_time", "")


def openfda_eventos(nombre, maximo=15):
    """Reacciones más notificadas en FAERS (FDA). Son notificaciones espontáneas: no dan frecuencias
    ni causalidad; sirven solo para orientar qué buscar en la ficha técnica."""
    q = urllib.parse.quote(f'patient.drug.openfda.generic_name:"{nombre}"')
    r = json.loads(_get(f"https://api.fda.gov/drug/event.json?search={q}"
                        f"&count=patient.reaction.reactionmeddrapt.exact&limit={maximo}", timeout=90))
    return r["results"]


def cpic(nombre):
    """Pares gen-fármaco de CPIC (farmacogenética) con nivel de evidencia y recomendaciones.

    Niveles A y B: hay recomendación de prescripción. Devuelve los pares A/B con sus recomendaciones
    por fenotipo, y la lista de pares C/D sin recomendación. nombre: genérico en inglés, en minúsculas.
    """
    base = "https://api.cpicpgx.org/v1"
    q = urllib.parse.quote(nombre.lower())
    pares = json.loads(_get(f"{base}/pair_view?drugname=eq.{q}&select=genesymbol,cpiclevel,guidelinename,"
                            "guidelineurl,clinpgxlevel,pmids,usedforrecommendation"))
    recs = json.loads(_get(f"{base}/recommendation_view?drugname=eq.{q}&select=lookupkey,drugrecommendation,"
                           "classification,implications,population"))
    fuertes = [p for p in pares if p.get("cpiclevel") in ("A", "B")]
    for p in fuertes:
        p["recomendaciones"] = [r for r in recs if p["genesymbol"] in (r.get("lookupkey") or {})]
    return {"con_recomendacion": fuertes,
            "sin_recomendacion": [(p["genesymbol"], p["cpiclevel"]) for p in pares if p not in fuertes]}


def fda_indicaciones(nombre, ultimas=6, cartas=True):
    """Indicaciones aprobadas por la FDA: texto vigente de la ficha y aprobaciones recientes con fecha.

    - Ficha vigente (openFDA): sección 1 completa, fecha y «Recent Major Changes».
    - Historial (Drugs@FDA): suplementos de eficacia aprobados (nuevas indicaciones o cambios de uso),
      del más reciente al más antiguo, con la frase de la carta de aprobación que dice qué se aprobó.
    Usa la solicitud del innovador (NDA o BLA), no las de genéricos (ANDA). nombre: genérico en inglés.
    """
    import pymupdf
    palabras = [w for w in re.split(r"[\s-]+", nombre.lower()) if len(w) > 2]
    q = "+AND+".join(f"openfda.generic_name:{urllib.parse.quote(w)}" for w in palabras)
    apps = json.loads(_get(f"https://api.fda.gov/drug/drugsfda.json?search={q}&limit=50", timeout=90))["results"]
    apps = [a for a in apps if a["application_number"].startswith(("NDA", "BLA"))]
    if not apps:
        return None
    # El innovador suele ser la solicitud con más suplementos de eficacia.
    app = max(apps, key=lambda a: sum(s.get("submission_class_code") == "EFFICACY" for s in a.get("submissions", [])))
    subs = sorted((s for s in app.get("submissions", []) if s.get("submission_status") == "AP"
                   and (s.get("submission_class_code") == "EFFICACY" or s.get("submission_type") == "ORIG")),
                  key=lambda s: s["submission_status_date"], reverse=True)
    historial, vistas = [], set()
    for sub in subs[:ultimas]:
        docs = {d["type"]: d["url"] for d in sub.get("application_docs", [])}
        fecha = sub["submission_status_date"]
        item = {"fecha": f"{fecha[:4]}-{fecha[4:6]}-{fecha[6:]}", "tipo": sub["submission_type"],
                "numero": sub["submission_number"], "carta": docs.get("Letter"), "ficha": docs.get("Label")}
        if cartas and item["carta"] and (item["carta"], item["numero"]) not in vistas:
            vistas.add((item["carta"], item["numero"]))
            try:
                destino = CACHE / ("fda-" + re.sub(r"[^\w.]+", "_", item["carta"].rsplit("/", 1)[-1]))
                if not destino.exists():
                    CACHE.mkdir(parents=True, exist_ok=True)
                    destino.write_bytes(_get(item["carta"].replace(" ", "%20"), timeout=120,
                                             cabeceras={"User-Agent": "Mozilla/5.0"}))
                texto = re.sub(r"\s+", " ", " ".join(p.get_text() for p in pymupdf.open(destino)))
                fin = r"(?=Prior Approval|We have completed|APPROVAL &|This information will|CONTENT OF LABELING|$)"
                verbo = r"(?:provides?|provided|proposes)(?: for)? (.{20,900}?)"
                m = (re.search(rf"S-?0*{int(item['numero'])}\b[^.]{{0,40}}?{verbo}{fin}", texto)
                     or re.search(verbo + fin, texto)
                     or re.search(r"is indicated (for .{20,600}?\.)", texto))
                item["aprobado"] = m.group(1).strip() if m else None
            except Exception as e:  # noqa: BLE001
                item["aprobado"] = f"(no se pudo leer la carta: {e})"
        historial.append(item)
    ficha = {}
    try:
        etiqueta = json.loads(_get(f"https://api.fda.gov/drug/label.json?search={q}+AND+openfda.application_number:"
                                   f"{app['application_number']}&sort=effective_time:desc&limit=1", timeout=90))
        r = etiqueta["results"][0]
        ficha = {"fecha": r.get("effective_time"), "cambios_recientes": " ".join(r.get("recent_major_changes", [])),
                 "indicaciones": " ".join(r.get("indications_and_usage", []))}
    except Exception as e:  # noqa: BLE001
        ficha = {"error": str(e)}
    return {"solicitud": app["application_number"], "titular": app.get("sponsor_name"),
            "marcas": sorted({p.get("brand_name") for p in app.get("products", [])}),
            "ficha_vigente": ficha, "aprobaciones_recientes": historial}


# --- Enfermedades: definiciones, ontologías y guías ------------------------------------

def mesh(termino):
    """Definición curada de MeSH (NLM) y su identificador. termino: en inglés.
    «mesh» es el identificador que se cita (D…, p. ej., D003924); «uid» es el número interno de Entrez."""
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    q = urllib.parse.quote(termino)
    ids = json.loads(_get(f"{base}/esearch.fcgi?db=mesh&term={q}&retmode=json"))["esearchresult"]["idlist"][:3]
    salida = []
    for uid in ids:
        r = json.loads(_get(f"{base}/esummary.fcgi?db=mesh&id={uid}&retmode=json"))["result"][uid]
        salida.append({"mesh": r.get("ds_meshui"), "uid": uid, "termino": (r.get("ds_meshterms") or [""])[0],
                       "definicion": r.get("ds_scopenote", "").strip()})
    return salida


def mondo(termino):
    """Enfermedad en la ontología MONDO (EBI OLS): identificador, definición y sinónimos. termino: en inglés."""
    q = urllib.parse.quote(termino)
    d = json.loads(_get(f"https://www.ebi.ac.uk/ols4/api/search?q={q}&ontology=mondo&rows=3"))
    return [{"id": x.get("obo_id"), "nombre": x.get("label"), "definicion": " ".join(x.get("description") or [])}
            for x in d["response"]["docs"]]


def guias(enfermedad, maximo=10, titulo=False):
    """Guías de práctica clínica y consensos recientes en PubMed (filtro de tipo de publicación).
    Cada resultado lleva su PMCID si el texto completo está en PMC (léelo con pmc_texto).
    titulo=True exige que cada palabra de `enfermedad` esté en el título: menos ruido cuando el nombre
    de la enfermedad aparece de pasada en guías de otros temas (p. ej., «hospital-acquired pneumonia»)."""
    if titulo:
        enfermedad = " AND ".join(f"{palabra}[ti]" for palabra in re.findall(r"[\w-]+", enfermedad))
    consulta = (f"({enfermedad}) AND (practice guideline[pt] OR guideline[pt] OR consensus[ti] OR "
                f'"standards of care"[ti]) AND ("last 5 years"[dp])')
    resultados = pubmed(consulta, maximo=maximo)
    for r in resultados:
        r["pmcid"] = pmcid(r["pmid"])
    return resultados


def pmcid(pmid):
    """PMCID de un artículo de PubMed, o None si no está en PMC."""
    d = json.loads(_get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pmc"
                        f"&linkname=pubmed_pmc&id={pmid}&retmode=json"))
    enlaces = [l for c in d.get("linksets", []) for l in c.get("linksetdbs", []) if l.get("linkname") == "pubmed_pmc"]
    return f"PMC{enlaces[0]['links'][0]}" if enlaces and enlaces[0].get("links") else None


def pmc_texto(pmcid, patrones=(), contexto=350):
    """Texto completo de un artículo de PMC cuando la editorial lo permite (p. ej., acceso abierto).

    Devuelve los fragmentos que contienen cada patrón (regex). Lo pide a NCBI y, si NCBI no lo da (la editorial
    no permite descargarlo, o el servicio falla), a Europe PMC; «fuente» dice cuál respondió. Si ninguno lo
    tiene, lo indica: en ese caso, usa el resumen de PubMed o busca una versión en acceso abierto.
    """
    numero = str(pmcid).upper().replace("PMC", "")
    intentos = (("NCBI PMC", f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={numero}"
                              "&retmode=xml"),
                ("Europe PMC", f"https://www.ebi.ac.uk/europepmc/webservices/rest/PMC{numero}/fullTextXML"))
    errores = []
    for fuente, url in intentos:
        try:
            xml = _get(url, timeout=180, intentos=2).decode("utf-8", "ignore")
        except RuntimeError as e:
            errores.append(str(e))
            continue
        texto = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", xml)))
        if "does not allow downloading of the full text" in xml or "<body" not in xml:
            errores.append(f"{fuente}: sin texto completo")
            continue
        fragmentos = {p: [texto[max(0, m.start() - contexto):m.end() + contexto]
                          for m in re.finditer(p, texto)][:3] for p in patrones}
        return {"pmcid": f"PMC{numero}", "texto_completo": True, "fuente": fuente, "caracteres": len(texto),
                "fragmentos": fragmentos}
    return {"pmcid": f"PMC{numero}", "texto_completo": False, "detalle": "; ".join(errores)}


def pagina(url, patrones=(), contexto=300):
    """Texto de una página web pública (guía, ficha técnica nacional, página de un instituto), en cualquier idioma.
    Quita el HTML y devuelve, para cada patrón (regex en el idioma de la página), los fragmentos donde aparece.
    Si el texto es muy corto, la página probablemente se genera con JavaScript: búscala en otra fuente."""
    crudo = _get(url, cabeceras={"User-Agent": "Mozilla/5.0 (compatible; skills-docencia/1.0)",
                                 "Accept-Language": "es,en;q=0.8,*;q=0.5"}).decode("utf-8", "ignore")
    titulo = re.search(r"<title[^>]*>(.*?)</title>", crudo, re.S | re.I)
    idioma = re.search(r'<html[^>]*\blang="([^"]+)"', crudo, re.I)
    texto = re.sub(r"<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>", " ", crudo, flags=re.S | re.I)
    texto = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", texto))).strip()
    fragmentos = {p: [texto[max(0, m.start() - contexto):m.end() + contexto]
                      for m in list(re.finditer(p, texto, re.I))[:3]] for p in patrones}
    return {"url": url, "titulo": html.unescape(titulo.group(1).strip()) if titulo else None,
            "idioma": idioma.group(1) if idioma else None, "caracteres": len(texto),
            "aviso": "texto muy corto: puede requerir JavaScript" if len(texto) < 2000 else None,
            "fragmentos": fragmentos}


if __name__ == "__main__":
    accion, *args = sys.argv[1:]
    if accion in ("pubchem", "chembl", "pdb-buscar", "bioicons", "dailymed", "cima", "reactome", "nci", "livertox",
                  "medlineplus", "lactmed", "openfda", "openfda-eventos", "cpic", "fda-indicaciones", "mesh", "mondo",
                  "guias", "guias-titulo", "togopic", "commons"):
        args = [" ".join(args)]
    funciones = {"pubchem": pubchem, "chembl": chembl, "pdb-buscar": pdb_buscar, "pdb-ligandos": pdb_ligandos,
                 "bioicons": bioicons, "servier-kits": servier_kits, "servier-diapositivas": servier_diapositivas,
                 "servier-extraer": lambda k, d, g, n: servier_extraer(k, int(d), g, n),
                 "dailymed": dailymed, "cima": cima, "uniprot": uniprot, "reactome": reactome,
                 "uniprot-proteina": lambda nombre, organismo=None: uniprot(
                     proteina=nombre, organismo=int(organismo) if organismo else None),
                 "pdf": lambda url, *patrones: pdf_texto(url, patrones),
                 "europepmc": lambda consulta, patron=None: europepmc(consulta, patron),
                 "pubmed": lambda consulta, patron=None: pubmed(consulta, patron),
                 "gen": ncbi_gene, "nci": nci_tesauro, "livertox": livertox, "medlineplus": medlineplus,
                 "lactmed": lactmed, "openfda": openfda, "openfda-eventos": openfda_eventos, "cpic": cpic,
                 "actividad": lambda nombre, diana=None: chembl_actividad(nombre, diana),
                 "bindingdb": bindingdb, "epar": ema_epar, "fda-indicaciones": fda_indicaciones,
                 "mesh": mesh, "mondo": mondo, "guias": guias,
                 "guias-titulo": lambda enfermedad: guias(enfermedad, titulo=True),
                 "togopic": togopic, "togopic-descargar": togopic_descargar, "commons": commons,
                 "commons-descargar": commons_descargar,
                 "pmc": lambda pmcid, *patrones: pmc_texto(pmcid, patrones),
                 "pagina": lambda url, *patrones: pagina(url, patrones)}
    resultado = funciones[accion](*args)
    print(json.dumps(resultado, indent=2, ensure_ascii=False, default=str))
