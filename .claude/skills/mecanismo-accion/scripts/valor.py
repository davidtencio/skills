"""Farmacoeconomía y estudios de vida real, con prioridad para Costa Rica y Latinoamérica.

Uso desde la línea de comandos (devuelve JSON):
    python3 scripts/valor.py economia <nombre en inglés> [latam|global]
    python3 scripts/valor.py vida-real <nombre en inglés> [latam|global]
    python3 scripts/valor.py nice <nombre en inglés>
    python3 scripts/valor.py eml <nombre en inglés>
    python3 scripts/valor.py ops <nombre en inglés>
    python3 scripts/valor.py nadac <nombre en inglés>
    python3 scripts/valor.py observacionales <nombre en inglés> [país o "latam"]
    python3 scripts/valor.py ema-rwd <nombre en inglés>
    python3 scripts/valor.py agencias <nombre>

Todos los datos económicos dependen del país, el año y la moneda: cítalos siempre con los tres.
Los estudios observacionales complementan los ensayos, no los sustituyen (sesgo de confusión).
"""

import json
import re
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fuentes import CACHE, _get, _texto_plano, pubmed  # noqa: E402

LATAM = ["Costa Rica", "Panama", "Nicaragua", "Honduras", "El Salvador", "Guatemala", "Mexico", "Colombia",
         "Brazil", "Argentina", "Chile", "Peru", "Ecuador", "Uruguay", "Paraguay", "Bolivia", "Venezuela",
         "Dominican Republic", "Cuba"]
_GEO = '("Latin America"[MeSH] OR "Central America"[MeSH] OR "South America"[MeSH] OR "Mexico"[MeSH] OR ' \
       '"Caribbean Region"[MeSH] OR "Costa Rica"[tiab] OR "Latin America"[tiab])'
_ECON = '("Cost-Benefit Analysis"[MeSH] OR "Quality-Adjusted Life Years"[MeSH] OR "Costs and Cost Analysis"[MeSH] ' \
        'OR cost-effectiveness[tiab] OR "budget impact"[tiab] OR cost-utility[tiab])'
_RWE = '("Observational Study"[pt] OR "real-world"[tiab] OR "real world"[tiab] OR registry[tiab] OR ' \
       'cohort[tiab] OR "routine clinical practice"[tiab])'


def _region(consulta, region):
    return f"{consulta} AND {_GEO}" if region == "latam" else consulta


def economia(nombre, region="latam", patron=None, maximo=30):
    """Evaluaciones económicas (coste-efectividad, coste-utilidad, impacto presupuestario) en PubMed.

    region="latam" prioriza Costa Rica y Latinoamérica; si no hay resultados, repite en global.
    """
    res = pubmed(_region(f'"{nombre}"[tiab] AND {_ECON}', region), patron, maximo=maximo)
    if not res and region == "latam":
        return {"region": "global (sin resultados en Latinoamérica)", "estudios": economia(nombre, "global",
                                                                                           patron)["estudios"]}
    return {"region": region, "estudios": res}


def vida_real(nombre, region="latam", patron=None, maximo=30):
    """Estudios observacionales y de práctica clínica real en PubMed (efectividad, seguridad, adherencia)."""
    res = pubmed(_region(f'"{nombre}"[tiab] AND {_RWE}', region), patron, maximo=maximo)
    if not res and region == "latam":
        return {"region": "global (sin resultados en Latinoamérica)", "estudios": vida_real(nombre, "global",
                                                                                            patron)["estudios"]}
    return {"region": region, "estudios": res}


def nice(nombre, patron=r"cost[- ]effective|\bQALYs?\b|\bICERs?\b|£|per quality|economic model", maximo=4):
    """Guías y evaluaciones de NICE (Reino Unido) que mencionan el fármaco, con frases de coste-efectividad."""
    html = _get(f"https://www.nice.org.uk/search?q={urllib.parse.quote(nombre)}").decode("utf-8", "ignore")
    codigos = list(dict.fromkeys(re.findall(r'href="/guidance/((?:ta|ng|cg|hst)\d+)"', html)))[:maximo]
    salida = []
    for cod in codigos:
        base = f"https://www.nice.org.uk/guidance/{cod}"
        pagina = _get(base).decode("utf-8", "ignore")
        titulo = _texto_plano((re.search(r"<title>(.*?)</title>", pagina, re.S) or [None, cod])[1]).strip()
        capitulos = list(dict.fromkeys(re.findall(rf'href="(/guidance/{cod}/chapter/[^"#]+)"', pagina)))
        frases = []
        for cap in capitulos[:8]:
            texto = _texto_plano(_get("https://www.nice.org.uk" + cap).decode("utf-8", "ignore"))
            for f in re.split(r"(?<=[.;])\s+", texto):
                if re.search(patron, f, re.I) and len(f) < 700:
                    frases.append({"capitulo": cap.rsplit("/", 1)[-1], "frase": f.strip(),
                                   "menciona_farmaco": nombre.split()[0].lower() in f.lower()})
        frases.sort(key=lambda x: not x["menciona_farmaco"])
        salida.append({"codigo": cod.upper(), "titulo": titulo, "url": base, "frases": frases[:8]})
    return salida


def eml(nombre):
    """Lista Modelo de Medicamentos Esenciales de la OMS: si el fármaco está y en qué sección e indicación."""
    html = _get(f"https://list.essentialmeds.org/?query={urllib.parse.quote(nombre)}").decode("utf-8", "ignore")
    texto = _texto_plano(html)
    i = texto.find("Found ")
    return {"url": f"https://list.essentialmeds.org/?query={urllib.parse.quote(nombre)}",
            "resumen": texto[i:i + 1500] if i >= 0 else "Sin resultados en la Lista de la OMS."}


def ops(nombre):
    """Productos del Fondo Estratégico de la OPS (compra conjunta para las Américas) y su rango de precio."""
    import pymupdf
    pagina = _get("https://www.paho.org/en/documents/strategic-funds-reference-prices-eligible-products").decode(
        "utf-8", "ignore")
    pdf = re.search(r'href="([^"]+prsfreferenceprices[^"]*\.pdf)"', pagina)
    if not pdf:
        return {"error": "No se encontró el PDF de precios de referencia del Fondo Estratégico."}
    url = urllib.parse.urljoin("https://www.paho.org", pdf.group(1))
    destino = CACHE / Path(url).name
    if not destino.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(_get(url, timeout=120))
    texto = re.sub(r"\s+", " ", " ".join(p.get_text() for p in pymupdf.open(destino)))
    filas = re.findall(rf"\d{{8}} ({re.escape(nombre.upper())}[^|]*?) (Yes|No) (.*?) (Box|Tablet|Vial|Ampoule|"
                       r"Bottle|Capsule|Unit|Each|Kit|Pack)\b", texto, re.I)
    return {"url": url, "productos": [{"producto": p.strip(), "listo_para_comprar": l,
                                       "rango_precio_usd": r.strip(), "unidad": u} for p, l, r, u in filas]}


def nadac(nombre, maximo=12):
    """Precio de adquisición por unidad en EE. UU. (NADAC, Medicaid). Referencia de precio de genéricos."""
    busq = json.loads(_get("https://data.medicaid.gov/api/1/search?fulltext=NADAC%20National%20Average%20Drug"
                           "%20Acquisition%20Cost&page-size=30"))["results"].values()
    anuales = [d for d in busq if re.fullmatch(r"NADAC \(National Average Drug Acquisition Cost\) \d{4}", d["title"])]
    ultimo = max(anuales, key=lambda d: d["title"])
    q = urllib.parse.urlencode({"conditions[0][property]": "ndc_description",
                                "conditions[0][value]": f"{nombre.upper()}%", "conditions[0][operator]": "LIKE",
                                "sorts[0][property]": "effective_date", "sorts[0][order]": "desc", "limit": 200})
    filas = json.loads(_get(f"https://data.medicaid.gov/api/1/datastore/query/{ultimo['identifier']}/0?{q}"))["results"]
    por_producto = {}
    for f in filas:
        por_producto.setdefault(f["ndc_description"], f)
    return {"conjunto": ultimo["title"], "moneda": "USD", "productos": [
        {"producto": k, "usd_por_unidad": float(v["nadac_per_unit"]), "unidad": v["pricing_unit"],
         "fecha": v["effective_date"], "generico": v["classification_for_rate_setting"] == "G"}
        for k, v in list(por_producto.items())[:maximo]]}


def observacionales(nombre, region="latam", maximo=20):
    """Estudios observacionales registrados en ClinicalTrials.gov (registros, cohortes, vida real)."""
    params = {"query.intr": nombre, "filter.advanced": "AREA[StudyType]OBSERVATIONAL", "pageSize": maximo,
              "countTotal": "true"}
    if region == "latam":
        params["query.locn"] = " OR ".join(LATAM)
    elif region and region != "global":
        params["query.locn"] = region
    r = json.loads(_get("https://clinicaltrials.gov/api/v2/studies?" + urllib.parse.urlencode(params)))
    estudios = []
    for s in r.get("studies", []):
        p = s["protocolSection"]
        paises = sorted({l.get("country") for l in p.get("contactsLocationsModule", {}).get("locations", [])
                         if l.get("country")})
        estudios.append({"nct": p["identificationModule"]["nctId"], "titulo": p["identificationModule"]["briefTitle"],
                         "estado": p["statusModule"]["overallStatus"],
                         "inicio": p["statusModule"].get("startDateStruct", {}).get("date"),
                         "participantes": p.get("designModule", {}).get("enrollmentInfo", {}).get("count"),
                         "modelo": p.get("designModule", {}).get("designInfo", {}).get("observationalModelInfo"),
                         "paises": paises})
    return {"total": r.get("totalCount"), "region": region, "estudios": estudios}


def ema_rwd(nombre, maximo=10):
    """Catálogo de estudios con datos de vida real de la EMA (antes EU PAS Register; incluye DARWIN EU)."""
    html = _get(f"https://catalogues.ema.europa.eu/search?search_api_fulltext={urllib.parse.quote(nombre)}"
                ).decode("utf-8", "ignore")
    enlaces = re.findall(r'<a class="article-title" href="(/study/\d+)"[^>]*>(.*?)</a>', html, re.S)
    texto = _texto_plano(html)
    total = re.search(r"Results \((\d+)\)", texto)
    return {"total": int(total.group(1)) if total else 0,
            "estudios": [{"titulo": _texto_plano(t).strip(), "url": "https://catalogues.ema.europa.eu" + u}
                         for u, t in enlaces if len(_texto_plano(t).strip()) > 30][:maximo]}


# Agencias cuyo buscador no se puede leer de forma automática desde este entorno: se dan las rutas para
# la persona usuaria y la skill solo cita lo que haya podido leer.
AGENCIAS = [
    ("Costa Rica", "CCSS: Lista Oficial de Medicamentos y Comité Central de Farmacoterapia",
     "https://www.ccss.sa.cr/lom", "el sitio corta las conexiones desde la nube: consultar con el navegador"),
    ("Américas", "BRISA/RedETSA (OPS): informes de evaluación de tecnologías de la región",
     "https://redetsa.bvsalud.org", "BRISA (pesquisa.bvsalud.org/brisa) rechaza consultas automáticas (403): consultar con el navegador"),
    ("Brasil", "CONITEC: relatorios de recomendación con coste-efectividad e impacto presupuestario",
     "https://www.gov.br/conitec", "buscador dinámico; leer el relatorio en PDF si se tiene el enlace"),
    ("Colombia", "IETS: evaluaciones de efectividad, seguridad y económicas", "https://www.iets.org.co",
     "buscador dinámico"),
    ("Argentina", "CONETEC: informes de evaluación", "https://www.argentina.gob.ar/salud/conetec", "buscador dinámico"),
    ("México", "CENETEC", "https://www.gob.mx/salud/cenetec", "buscador dinámico"),
    ("Perú", "IETSI-EsSalud: dictámenes", "https://ietsi.essalud.gob.pe", "buscador dinámico"),
    ("Francia", "HAS: beneficio clínico (SMR) y beneficio añadido (ASMR)", "https://www.has-sante.fr",
     "buscador dinámico"),
    ("Alemania", "G-BA / IQWiG: beneficio añadido (AMNOG)", "https://www.g-ba.de", "buscador dinámico"),
    ("EE. UU.", "ICER: coste-efectividad y precio basado en valor", "https://icer.org", "informes en PDF"),
    ("Australia", "PBAC: resúmenes públicos de decisiones", "https://www.pbs.gov.au", "buscador dinámico"),
    ("Canadá", "CDA-AMC (antes CADTH): revisiones de reembolso", "https://www.cda-amc.ca",
     "bloquea consultas automáticas"),
]


def agencias(nombre=""):
    return [{"ambito": a, "agencia": n, "url": u, "acceso": e} for a, n, u, e in AGENCIAS]


if __name__ == "__main__":
    accion, *args = sys.argv[1:]
    funciones = {"economia": economia, "vida-real": vida_real, "nice": nice, "eml": eml, "ops": ops,
                 "nadac": nadac, "observacionales": observacionales, "ema-rwd": ema_rwd, "agencias": agencias}
    if accion in ("nice", "eml", "ops", "nadac", "ema-rwd", "agencias"):
        args = [" ".join(args)]
    print(json.dumps(funciones[accion](*args), indent=2, ensure_ascii=False, default=str))
