"""Analizadores de fuentes.py con respuestas grabadas (tests/datos/fuentes), sin red.

Las respuestas son reales, recortadas a los campos que se leen. Comprueban que cada función interpreta bien el
formato de la fuente; el monitor semanal (monitor/salud_fuentes.py) comprueba que el formato no ha cambiado.
Se prueba la copia de fisiopatologia: las funciones comunes son idénticas en las dos skills (test_paridad.py).
"""
import json
import re
import sys
import urllib.parse

import pytest

from conftest import RAIZ, SKILLS_DIR

sys.path.insert(0, str(SKILLS_DIR / "fisiopatologia" / "scripts"))
import fuentes  # noqa: E402

DATOS = RAIZ / "tests" / "datos" / "fuentes"


@pytest.fixture
def red(monkeypatch):
    """Sustituye _get: cada URL que coincide con un patrón devuelve su archivo grabado; registra las URL pedidas."""
    respuestas, pedidas = {}, []

    def falso_get(url, con_url=False, **_):
        url = fuentes._cortesia_ncbi(url)
        pedidas.append(url)
        for patron, respuesta in respuestas.items():
            if re.search(patron, url):
                if isinstance(respuesta, Exception):
                    raise respuesta
                contenido = respuesta if isinstance(respuesta, bytes) else (DATOS / respuesta).read_bytes()
                return (contenido, url) if con_url else contenido
        raise AssertionError(f"URL sin respuesta grabada: {url}")

    monkeypatch.setattr(fuentes, "_get", falso_get)
    monkeypatch.setattr(fuentes, "_REGISTRO_BUSQUEDAS", None)
    return respuestas, pedidas


def _pdf(textos):
    pymupdf = pytest.importorskip("pymupdf")
    doc = pymupdf.open()
    for texto in textos:
        doc.new_page().insert_text((72, 72), texto)
    return doc.tobytes()


# --- PubMed y Europe PMC -------------------------------------------------------------------------------------

def test_mesh_devuelve_identificador_d(red):
    respuestas, _ = red
    respuestas.update({r"esearch\.fcgi\?db=mesh": "mesh-esearch.json", r"esummary\.fcgi\?db=mesh": "mesh-esummary.json"})
    r = fuentes.mesh("Healthcare-Associated Pneumonia")
    assert r[0]["mesh"] == "D000077299" and r[0]["termino"] == "Healthcare-Associated Pneumonia"
    assert r[0]["definicion"].startswith("Infection of the lung")


def test_pubmed_metadatos_para_citar_y_avisos(red):
    respuestas, _ = red
    respuestas.update({r"esearch\.fcgi\?db=pubmed": "pubmed-esearch.json", r"efetch\.fcgi\?db=pubmed": "pubmed-efetch.xml"})
    r = {a["pmid"]: a for a in fuentes.pubmed("x", maximo=4)}
    idsa = r["27418577"]
    assert idsa["autores"][:2] == ["Kalil AC", "Metersky ML"] and idsa["revista"] == "Clin Infect Dis"
    assert idsa["anio"] == "2016" and idsa["doi"] == "10.1093/cid/ciw353"
    assert idsa["pmcid"] == "PMC4981759", "el PMCID es el del artículo, no el de una de sus referencias"
    assert "Practice Guideline" in idsa["tipos"] and idsa["estado"] == "MEDLINE"
    assert idsa["avisos"] == ["fe de erratas: PMID 28168287, PMID 29017256, PMID 29126289"]
    assert r["28890434"]["pmcid"] is None
    assert r["33378332"]["avisos"][0] == "RETRACTADO" and any(a.startswith("retractado: PMID") for a in r["33378332"]["avisos"])
    libro = r["31644035"]
    assert libro["estado"] == "libro" and libro["revista"].startswith("LiverTox") and libro["anio"] == "2012"


def test_pubmed_filtra_frases_y_orden_de_busqueda(red):
    respuestas, pedidas = red
    respuestas.update({r"esearch\.fcgi\?db=pubmed": "pubmed-esearch.json", r"efetch\.fcgi\?db=pubmed": "pubmed-efetch.xml"})
    filtrados = fuentes.pubmed("x", r"ventilat", maximo=4, orden="fecha", region="latam")
    assert filtrados and all(re.search("ventilat", f, re.I) for a in filtrados for f in a["frases"])
    consulta = urllib.parse.unquote(pedidas[0])
    assert "sort=pub_date" in consulta and '"Costa Rica"[tiab]' in consulta and "tool=skills-docencia" in consulta


def test_europepmc_campos_y_orden(red):
    respuestas, pedidas = red
    respuestas.update({r"europepmc/webservices/rest/search": "europepmc-busqueda.json"})
    r = fuentes.europepmc("x")
    assert len(r) == 3 and "CITED" not in pedidas[0], "por defecto, por relevancia y sin umbral de citas"
    assert all({"doi", "pmcid", "acceso_abierto", "tipos", "autores"} <= set(a) for a in r)
    fuentes.europepmc("x", orden="citas")
    assert "sort=CITED" in pedidas[-1]


def test_frases_no_corta_en_abreviaturas():
    texto = ("Use MRSA coverage where >10%–20% of S. aureus are resistant. Kalil et al. found it, e.g. in ICUs. "
             "Werte von 50 %, 60-70 % bzw. mindestens 40% wurden ermittelt. Siehe Fig. 2 und Tab. 3. Neue Frage.")
    assert fuentes._frases(texto) == [
        "Use MRSA coverage where >10%–20% of S. aureus are resistant.", "Kalil et al. found it, e.g. in ICUs.",
        "Werte von 50 %, 60-70 % bzw. mindestens 40% wurden ermittelt.", "Siehe Fig. 2 und Tab. 3.", "Neue Frage."]


def test_cortesia_ncbi(monkeypatch):
    monkeypatch.setenv("NCBI_API_KEY", "clave")
    url = fuentes._cortesia_ncbi("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=x")
    assert url.endswith("&tool=skills-docencia&api_key=clave")
    assert fuentes._cortesia_ncbi("https://www.ebi.ac.uk/x?y=1") == "https://www.ebi.ac.uk/x?y=1"


# --- Guías y vigencia ------------------------------------------------------------------------------------------

def _registro(pmid, titulo, anio, tipos=("Journal Article",), avisos=(), revista="J"):
    return {"pmid": pmid, "titulo": titulo, "anio": anio, "tipos": list(tipos), "avisos": list(avisos),
            "revista": revista, "autores": [], "doi": None, "pmcid": None, "estado": "MEDLINE", "frases": []}


def test_guias_dos_pasadas_orden_y_copublicaciones(monkeypatch):
    llamadas = []
    indexadas = [_registro("1", "Surviving Sepsis Campaign International Guidelines for the Management of Sepsis "
                                "in Children 2026", "2026", ("Practice Guideline",)),
                 _registro("2", "Clinical practice guideline on the management of septic shock", "2021", ("Guideline",)),
                 _registro("3", "Management of urinary stones by experts (ESD 2025)", "2025", ("Practice Guideline",))]
    sin_indexar = [_registro("4", "Surviving Sepsis Campaign: international guidelines for management of sepsis and "
                                  "septic shock 2026.", "2026", avisos=["fe de erratas: PMID 9"], revista="Intensive Care Med"),
                   _registro("5", "Surviving Sepsis Campaign: International Guidelines for Management of Sepsis and "
                                  "Septic Shock 2026", "2026", revista="Crit Care Med"),
                   _registro("6", "The 2026 Surviving Sepsis Campaign guidelines: a turning point for emergency "
                                  "medicine.", "2026"),
                   _registro("7", "Comparative performance of ChatGPT in interpreting sepsis guidelines", "2026")]

    def falso_pubmed(consulta, **opciones):
        llamadas.append((consulta, opciones))
        return [dict(r) for r in (sin_indexar if "inprocess[sb]" in consulta else indexadas)]

    monkeypatch.setattr(fuentes, "pubmed", falso_pubmed)
    r = fuentes.guias("sepsis OR septic shock", maximo=10)
    assert "practice guideline[pt]" in llamadas[0][0] and "letter[pt]" in llamadas[0][0]
    assert "(sepsis[ti]) OR (septic[ti] AND shock[ti])" in llamadas[1][0] and llamadas[1][1]["orden"] == "fecha"
    orden = [x["pmid"] for x in r]
    assert orden[:2] == ["1", "4"] or orden[:2] == ["4", "1"], orden
    adultos = next(x for x in r if x["pmid"] == "4")
    assert adultos["pasada"] == "sin indexar" and adultos["copublicaciones"] == ["5 (Crit Care Med)"]
    assert orden.index("6") > orden.index("2") and orden.index("7") > orden.index("2"), "los comentarios, al final"


def test_guias_normas_por_capitulos_y_estudios_sobre_guias(monkeypatch):
    llamadas = []
    normas = [_registro(str(100 + n), f"{n}. {tema}: Standards of Care in Diabetes-2026.", "2026",
                        ("Journal Article", "Review"))
              for n, tema in ((9, "Pharmacologic Approaches to Glycemic Treatment"),
                              (2, "Diagnosis and Classification of Diabetes"), (6, "Glycemic Goals"))]
    normas.append(_registro("200", "9. Pharmacologic Approaches to Glycemic Treatment: Standards of Care in "
                                   "Diabetes-2025.", "2025", ("Journal Article", "Review")))
    indexadas = [_registro("1", "Algorithm for Management of Adults With Type 2 Diabetes: AACE Consensus Statement.",
                           "2026", ("Consensus Statement", "Practice Guideline"))]
    sin_indexar = [_registro("2", "Continuous Glucose Monitoring in Type 2 Diabetes: A Narrative Review of Evidence "
                                  "and Recommendations.", "2026"),
                   _registro("3", "Euglycemic ketoacidosis in a patient with type 2 diabetes: a case report and "
                                  "guideline recommendations.", "2026")]

    def falso_pubmed(consulta, **opciones):
        llamadas.append(consulta)
        if "inprocess[sb]" in consulta:
            return [dict(r) for r in sin_indexar]
        return [dict(r) for r in (normas if '"standards of care"[ti] OR' in consulta else indexadas)]

    monkeypatch.setattr(fuentes, "pubmed", falso_pubmed)
    r = fuentes.guias("type 2 diabetes")
    assert "(diabetes[ti]) AND" in llamadas[2], "la pasada de normas busca la enfermedad sin el subtipo"
    ada = next(x for x in r if x["pmid"] == "109")
    assert ada["serie"] == "Standards of Care in Diabetes-2026" and len(ada["secciones"]) == 2
    assert ada["anteriores"] == ["200: Standards of Care in Diabetes-2025"]
    assert {x["pmid"] for x in r} == {"1", "109", "2", "3"}, "los capítulos y la edición anterior, agrupados"
    orden = [x["pmid"] for x in r]
    assert orden.index("2") > orden.index("109") and orden.index("3") > orden.index("1"), \
        "las revisiones y los casos clínicos que citan guías, detrás de las guías"


def test_vigencia_busca_versiones_posteriores(monkeypatch):
    llamadas = []
    original = _registro("34599691", "Surviving sepsis campaign: international guidelines for management of sepsis "
                                     "and septic shock 2021.", "2021")
    posteriores = [_registro("41870560", "Surviving Sepsis Campaign: international guidelines for management of "
                                         "sepsis and septic shock 2026.", "2026"),
                   _registro("42786551", "Revisiting diastolic arterial pressure in the 2026 Surviving Sepsis Campaign "
                                         "septic shock guidelines.", "2026"),
                   _registro("1", "Sepsis campaign shock surviving septic: unrelated survey", "2023")]

    def falso_pubmed(consulta, **opciones):
        llamadas.append(consulta)
        return [original] if consulta.endswith("[uid]") else posteriores

    monkeypatch.setattr(fuentes, "pubmed", falso_pubmed)
    r = fuentes.vigencia("34599691")
    assert "surviving[ti]" in llamadas[1] and "2022:3000[dp]" in llamadas[1]
    assert [c["pmid"] for c in r["posteriores"]] == ["41870560"]


def test_vigencia_admite_un_cambio_de_palabra_y_no_mezcla_subtipos(monkeypatch):
    llamadas = []
    original = _registro("36151309", "Management of hyperglycaemia in type 2 diabetes, 2022. A consensus report by "
                                     "the American Diabetes Association (ADA) and the European Association for the "
                                     "Study of Diabetes (EASD).", "2022")
    posteriores = [_registro("42825450", "Management of Type 2 Diabetes, 2026. A Consensus Report by the American "
                                         "Diabetes Association (ADA) and the European Association for the Study of "
                                         "Diabetes (EASD).", "2026"),
                   _registro("42747450", "The management of type 1 diabetes in adults. The updated 2026 consensus "
                                         "report by the ADA and the EASD.", "2026")]

    def falso_pubmed(consulta, **opciones):
        llamadas.append(consulta)
        return [original] if consulta.endswith("[uid]") else posteriores

    monkeypatch.setattr(fuentes, "pubmed", falso_pubmed)
    r = fuentes.vigencia("36151309")
    assert ") OR (" in llamadas[1], "todas las palabras distintivas menos una"
    assert [c["pmid"] for c in r["posteriores"]] == ["42825450"]


# --- Texto completo --------------------------------------------------------------------------------------------

def test_pmc_texto_secciones_y_respaldo_de_europe_pmc(red):
    respuestas, pedidas = red
    respuestas.update({r"eutils\.ncbi": RuntimeError("No se pudo consultar eutils.ncbi.nlm.nih.gov"),
                       r"europepmc/webservices/rest/PMC6018155/fullTextXML": "europepmc-fulltext.xml"})
    r = fuentes.pmc_texto("PMC6018155", ("48 h", "ERTAPENEM"))
    assert r["texto_completo"] and r["fuente"] == "Europe PMC"
    assert r["fragmentos"]["48 h"][0]["seccion"] == "Background"
    assert "after 48 h of admission" in r["fragmentos"]["48 h"][0]["texto"]
    assert r["fragmentos"]["ERTAPENEM"][0]["seccion"] == "Table 2 Empirical treatment", "sin distinguir mayúsculas"
    assert any("eutils" in u for u in pedidas)


def test_pmc_texto_sin_texto_completo_lo_dice(red):
    respuestas, _ = red
    respuestas.update({r"eutils\.ncbi": b"<pmc-articleset><article>The publisher of this article does not allow "
                                        b"downloading of the full text in XML form.</article></pmc-articleset>",
                       r"europepmc": RuntimeError("No se pudo consultar www.ebi.ac.uk")})
    r = fuentes.pmc_texto("PMC1", ("x",))
    assert r["texto_completo"] is False and "NCBI PMC" in r["detalle"]


def test_acceso_abierto_doi_aun_sin_unpaywall(red):
    respuestas, _ = red
    respuestas.update({r"api\.unpaywall\.org": RuntimeError("No se pudo consultar api.unpaywall.org: HTTP Error 404")})
    r = fuentes.acceso_abierto("10.2337/dci26-0141", ("x",))
    assert r["texto_completo"] is False and "aún no tiene" in r["detalle"]


def test_acceso_abierto_lee_la_copia_del_repositorio(red, tmp_path, monkeypatch):
    respuestas, pedidas = red
    monkeypatch.setattr(fuentes, "CACHE", tmp_path)
    respuestas.update({
        r"api\.unpaywall\.org/v2/10\.1093": "unpaywall-ciw353.json",
        r"academic\.oup\.com": RuntimeError("No se pudo consultar academic.oup.com: HTTP Error 403"),
        r"hdl\.handle\.net/2445/118988": b'<html><a href="/bitstreams/abc-123/download">PDF</a>'
                                         b'<a href="https://x.fe.cpd.local:4000/bitstreams/abc-123/download">x</a></html>',
        r"bitstreams/abc-123/download": _pdf(["Portada.", "Units where >10%-20% of S. aureus isolates are MRSA."]),
    })
    r = fuentes.acceso_abierto("10.1093/cid/ciw353", (r">10%-20%",))
    assert r["texto_completo"] and r["tipo"] == "repository" and r["version"] == "publishedVersion"
    assert r["fragmentos"][r">10%-20%"][0]["pagina"] == 2
    assert not any("ncbi.nlm.nih.gov/pmc" in u for u in pedidas), "PMC lo intenta pmc_texto, no Unpaywall"


def test_texto_completo_prueba_pmc_y_luego_acceso_abierto(monkeypatch):
    llamadas = []
    monkeypatch.setattr(fuentes, "pubmed", lambda consulta, **o: [_registro("27418577", "t", "2016") |
                                                                  {"pmcid": "PMC4981759", "doi": "10.1093/cid/ciw353"}])
    monkeypatch.setattr(fuentes, "pmc_texto", lambda p, *a, **o: llamadas.append(("pmc", p)) or
                        {"texto_completo": False, "detalle": "NCBI PMC: sin texto completo"})
    monkeypatch.setattr(fuentes, "acceso_abierto", lambda d, *a, **o: llamadas.append(("oa", d)) or
                        {"texto_completo": True, "tipo": "repository", "version": "publishedVersion", "fragmentos": {}})
    r = fuentes.texto_completo("27418577", ("x",))
    assert llamadas == [("pmc", "PMC4981759"), ("oa", "10.1093/cid/ciw353")]
    assert r["texto_completo"] and r["via"].startswith("acceso abierto") and r["pmid"] == "27418577"


def test_ids(red):
    respuestas, _ = red
    respuestas.update({r"idconv": "idconv.json"})
    r = fuentes.ids("27418577", "28890434")
    assert r[0] == {"pmid": "27418577", "pmcid": "PMC4981759", "doi": "10.1093/cid/ciw353", "pedido": "27418577"}
    assert r[1]["pmcid"] is None


def test_pdf_texto_da_la_pagina_y_rechaza_lo_que_no_es_pdf(red, tmp_path, monkeypatch):
    respuestas, _ = red
    monkeypatch.setattr(fuentes, "CACHE", tmp_path)
    respuestas.update({r"ejemplo\.org/guia\.pdf": _pdf(["Einleitung. Keine Zahlen.",
                                                        "Die Therapiedauer sollte 7-8 Tage betragen. Andere Frage."]),
                       r"ejemplo\.org/aviso": b"<html>Acepte las cookies</html>"})
    r = fuentes.pdf_texto("https://ejemplo.org/guia.pdf", ("7-8 Tage",))
    assert r["paginas"] == 2 and r["aviso"] is None
    assert r["fragmentos"]["7-8 Tage"] == [{"pagina": 2, "texto": "Die Therapiedauer sollte 7-8 Tage betragen."}]
    with pytest.raises(ValueError):
        fuentes.pdf_texto("https://ejemplo.org/aviso", ("x",))
    assert not list(tmp_path.glob("*")) or len(list(tmp_path.glob("*"))) == 1, "lo que no es PDF no se guarda"


def test_enlace_pdf():
    base = "https://diposit.ub.edu/items/x"
    assert fuentes._enlace_pdf('<meta name="citation_pdf_url" content="https://r.org/a.pdf">', base) == "https://r.org/a.pdf"
    assert fuentes._enlace_pdf('<a href="https://h.fe.cpd.local:4000/bitstreams/1/download"></a>'
                               '<a href="/bitstreams/1/download"></a>', base) == "https://diposit.ub.edu/bitstreams/1/download"
    assert fuentes._enlace_pdf("<p>sin enlaces</p>", base) is None


# --- Repositorios y Costa Rica ---------------------------------------------------------------------------------

def test_iris_documento_con_su_pdf(red):
    respuestas, _ = red
    respuestas.update({r"discover/search/objects": "iris-busqueda.json", r"/items/[^/]+/bundles": "iris-paquetes.json",
                       r"/bundles/[^/]+/bitstreams": "iris-archivos.json"})
    r = fuentes.iris("AWaRe antibiotic book")
    assert r[0]["titulo"].startswith("The WHO AWaRe") and r[0]["fecha"].startswith("2022")
    assert r[0]["url"] == "https://iris.who.int/handle/10665/365237" and r[0]["pdf"].endswith("/content")


def test_binasss_filtra_por_termino_sin_tildes(red):
    respuestas, _ = red
    respuestas.update({r"binasss\.sa\.cr/\?s=": b"<html></html>", r"protocolos/protocolos\.htm": "binasss-protocolos.html"})
    r = fuentes.binasss("infeccion")
    assert r and all("infecci" in x["titulo"].lower() for x in r)
    assert all(x["url"].startswith("https://www.binasss.sa.cr/protocolos/") and x["pdf"] for x in r)


def test_openfda_prefiere_la_ficha_con_las_secciones_pedidas(red):
    respuestas, _ = red
    respuestas.update({r"api\.fda\.gov/drug/label": "openfda-piperacillin.json"})
    fichas = json.loads((DATOS / "openfda-piperacillin.json").read_text())["results"]
    assert "microbiology" not in fichas[0], "la grabación debe empezar por una ficha sin 12.4 para que el test valga"
    r = fuentes.openfda("piperacillin")
    assert r.get("microbiology") and r["set_id"] != fichas[0]["set_id"]


def test_openfda_prefiere_el_principio_activo_solo():
    combinada = {"openfda": {"generic_name": ["PIPERACILLIN AND TAZOBACTAM"]}, "microbiology": ["x"],
                 "mechanism_of_action": ["x"], "effective_time": "20260101"}
    sola = {"openfda": {"generic_name": ["MEROPENEM"]}, "effective_time": "20200101"}
    secciones = ("microbiology", "mechanism_of_action")
    assert fuentes._puntuar_ficha(sola, "meropenem", secciones) > fuentes._puntuar_ficha(combinada, "meropenem",
                                                                                         secciones)


def test_uniprot_por_gen_se_queda_con_el_gen_exacto(red):
    respuestas, pedidas = red
    respuestas.update({r"rest\.uniprot\.org": "uniprot-klk3.tsv"})
    r = fuentes.uniprot("KLK3")
    assert [x["uniprot"] for x in r] == ["P07288"] and r[0]["organismo"].startswith("Homo sapiens")
    assert "taxonomy_id%3A9606" in pedidas[0]


def test_uniprot_por_proteina_sin_organismo(red):
    respuestas, pedidas = red
    respuestas.update({r"rest\.uniprot\.org": b"Entry\tGene Names (primary)\tProtein names\tOrganism\tFunction [CC]\t"
                                              b"Subcellular location [CC]\nP00807\tblaZ\tBeta-lactamase\tStaphylococcus "
                                              b"aureus\tFUNCTION: x\t\n"})
    r = fuentes.uniprot(proteina="beta-lactamase", organismo=None)
    assert r[0]["gen"] == "blaZ" and r[0]["localizacion"] == ""
    consulta = urllib.parse.unquote(pedidas[0])
    assert 'protein_name:"beta-lactamase"' in consulta and "taxonomy_id" not in consulta
    with pytest.raises(ValueError):
        fuentes.uniprot()


def test_pagina_quita_html_y_da_fragmentos(red):
    respuestas, _ = red
    respuestas.update({r"ejemplo\.org": '<html lang="fi"><head><title>Diabetes &amp; hoito</title><script>var x=1;'
                                        '</script></head><body><p>Metformiini on <b>ensisijainen</b> lääke.</p>'
                                        '</body></html>'.encode()})
    r = fuentes.pagina("https://ejemplo.org/x", ("ensisijainen",))
    assert r["idioma"] == "fi" and r["titulo"] == "Diabetes & hoito"
    fragmento, = r["fragmentos"]["ensisijainen"]
    assert fragmento.endswith("Metformiini on ensisijainen lääke.") and "var x" not in fragmento
    assert r["aviso"]  # texto corto: puede requerir JavaScript


# --- Registro de búsquedas -------------------------------------------------------------------------------------

def test_registro_anota_solo_las_consultas_de_primer_nivel(red, tmp_path, monkeypatch):
    respuestas, _ = red
    respuestas.update({r"esearch\.fcgi\?db=pubmed": "pubmed-esearch.json", r"efetch\.fcgi\?db=pubmed": "pubmed-efetch.xml",
                       r"idconv": "idconv.json"})
    ruta = fuentes.registrar_busquedas(tmp_path)
    try:
        fuentes.pubmed("sepsis guideline", maximo=4)
        fuentes.texto_completo("27418577", ("x",))  # llama por dentro a pubmed: no se anota dos veces
    except Exception:  # noqa: BLE001  (texto_completo puede fallar al no tener grabado el texto: da igual aquí)
        pass
    finally:
        monkeypatch.setattr(fuentes, "_REGISTRO_BUSQUEDAS", None)
    lineas = [json.loads(x) for x in ruta.read_text(encoding="utf-8").splitlines()]
    assert lineas[0]["funcion"] == "pubmed" and lineas[0]["argumentos"] == ["sepsis guideline"]
    assert lineas[0]["resultado"]["n"] == 4 and "27418577" in lineas[0]["resultado"]["ids"]
    assert [x["funcion"] for x in lineas].count("pubmed") == 1


# --- Medicamentos: fichas, EMA y ensayos ---------------------------------------------------------------------------

def test_openfda_prefiere_el_principio_activo_solo_aunque_lleve_sal():
    solo = {"openfda": {"generic_name": ["METFORMIN HYDROCHLORIDE"]}, "mechanism_of_action": ["x"], "effective_time": "2024"}
    combinada = {"openfda": {"generic_name": ["EMPAGLIFLOZIN AND METFORMIN HYDROCHLORIDE"]}, "mechanism_of_action": ["x"],
                 "effective_time": "2026"}
    assert max([combinada, solo], key=lambda f: fuentes._puntuar_ficha(f, "metformin", ("mechanism_of_action",))) is solo


def test_dailymed_elige_la_ficha_sin_combinar(red):
    respuestas, pedidas = red
    respuestas.update({
        r"spls\.json": json.dumps({"data": [
            {"title": "SYNJARDY (EMPAGLIFLOZIN AND METFORMIN HYDROCHLORIDE) TABLET [BI]", "setid": "combo", "spl_version": 23,
             "published_date": "Aug 27, 2026"},
            {"title": "JARDIANCE (EMPAGLIFLOZIN) TABLET, FILM COATED [REENVASADOR]", "setid": "reenvase", "spl_version": 2,
             "published_date": "Jan 01, 2025"},
            {"title": "JARDIANCE (EMPAGLIFLOZIN) TABLET, FILM COATED [BI]", "setid": "original", "spl_version": 31,
             "published_date": "Feb 02, 2026"}]}).encode(),
        r"spls/original\.xml": b"<document>12.1 Mechanism of Action Empagliflozin is an inhibitor of SGLT2.</document>"})
    r = fuentes.dailymed("empagliflozin", secciones=("12.1 Mechanism of Action",))
    assert r["setid"] == "original" and r["version"] == 31 and r["fecha"] == "Feb 02, 2026"
    assert "inhibitor of SGLT2" in r["12.1 Mechanism of Action"]


def test_pubmed_numero_de_ensayo_y_revision_de_monografia(red):
    respuestas, _ = red
    respuestas.update({r"esearch": json.dumps({"esearchresult": {"idlist": ["1", "2"]}}).encode(), r"efetch": b"""
<PubmedArticleSet>
 <PubmedArticle><MedlineCitation Status="MEDLINE"><PMID>1</PMID><Article><ArticleTitle>Empagliflozin, Cardiovascular
  Outcomes.</ArticleTitle><Abstract><AbstractText>Funded; EMPA-REG OUTCOME NCT01131676.</AbstractText></Abstract>
  <DataBankList><DataBank><DataBankName>ClinicalTrials.gov</DataBankName><AccessionNumberList>
  <AccessionNumber>NCT01131676</AccessionNumber></AccessionNumberList></DataBank></DataBankList></Article>
  </MedlineCitation></PubmedArticle>
 <PubmedBookArticle><BookDocument><PMID>2</PMID><Book><BookTitle>LiverTox</BookTitle></Book>
  <ArticleTitle>Sodium-Glucose Cotransporter-2 (SGLT2) Inhibitors</ArticleTitle>
  <ContributionDate><Year>2023</Year><Month>2</Month><Day>10</Day></ContributionDate></BookDocument>
 </PubmedBookArticle>
</PubmedArticleSet>"""})
    articulo, libro = fuentes.pubmed("x", maximo=2)
    assert articulo["ensayos"] == ["NCT01131676"] and articulo["revisado"] is None
    assert libro["estado"] == "libro" and libro["revisado"] == "2023-02-10"


def test_ensayos_pone_primero_los_pivotales(monkeypatch):
    def reg(pmid, titulo, tipos, revista="J", nct=()):
        return {**_registro(pmid, titulo, "2020", tipos, revista=revista), "ensayos": list(nct)}
    candidatos = [reg("1", "Empagliflozin in heart failure: a post hoc analysis of EMPEROR-Reduced",
                      ("Randomized Controlled Trial",), "N Engl J Med", ["NCT03057977"]),
                  reg("2", "Empagliflozin and liver fat: a pilot trial", ("Randomized Controlled Trial",)),
                  reg("3", "Cardiovascular and Renal Outcomes with Empagliflozin in Heart Failure",
                      ("Randomized Controlled Trial", "Multicenter Study"), "N Engl J Med", ["NCT03057977"])]
    monkeypatch.setattr(fuentes, "pubmed", lambda consulta, **_: [dict(c) for c in candidatos])
    orden = [r["pmid"] for r in fuentes.ensayos("empagliflozin")]
    assert orden[0] == "3" and orden.index("1") > orden.index("3"), "el análisis post hoc, detrás del principal"


def test_ema_medicamento_lee_los_datos_publicos(red, tmp_path, monkeypatch):
    respuestas, _ = red
    monkeypatch.setattr(fuentes, "CACHE", tmp_path)
    comun = {"category": "Human", "active_substance": "empagliflozin", "medicine_status": "Authorised",
             "international_non_proprietary_name_common_name": "empagliflozin", "biosimilar": "No"}
    respuestas.update({r"medicines_json-report": json.dumps({"data": [
        {**comun, "name_of_medicine": "Empagliflozin Genérico", "generic": "Yes"},
        {**comun, "name_of_medicine": "Jardiance", "generic": "No", "ema_product_number": "EMEA/H/C/002677",
         "revision_number": "33", "last_updated_date": "24/03/2026",
         "medicine_url": "https://www.ema.europa.eu/en/medicines/human/EPAR/jardiance"}]}).encode()})
    r = fuentes.ema_medicamento("empagliflozin")
    assert r[0]["nombre"] == "Jardiance" and r[0]["revision"] == "33" and r[1]["generico"]
