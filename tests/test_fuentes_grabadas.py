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

    def falso_get(url, **_):
        pedidas.append(url)
        for patron, respuesta in respuestas.items():
            if re.search(patron, url):
                if isinstance(respuesta, Exception):
                    raise respuesta
                return respuesta if isinstance(respuesta, bytes) else (DATOS / respuesta).read_bytes()
        raise AssertionError(f"URL sin respuesta grabada: {url}")

    monkeypatch.setattr(fuentes, "_get", falso_get)
    return respuestas, pedidas


def test_mesh_devuelve_identificador_d(red):
    respuestas, _ = red
    respuestas.update({r"esearch\.fcgi\?db=mesh": "mesh-esearch.json", r"esummary\.fcgi\?db=mesh": "mesh-esummary.json"})
    r = fuentes.mesh("Healthcare-Associated Pneumonia")
    assert r[0]["mesh"] == "D000077299" and r[0]["termino"] == "Healthcare-Associated Pneumonia"
    assert r[0]["definicion"].startswith("Infection of the lung")


def test_pubmed_extrae_articulos_y_filtra_frases(red):
    respuestas, _ = red
    respuestas.update({r"esearch\.fcgi\?db=pubmed": "pubmed-esearch.json", r"efetch\.fcgi\?db=pubmed": "pubmed-efetch.xml"})
    todos = fuentes.pubmed("hospital-acquired pneumonia guideline", maximo=3)
    assert {a["pmid"] for a in todos} >= {"28890434"}
    assert all(a["titulo"] and re.fullmatch(r"\d{4}", a["anio"]) for a in todos)
    filtrados = fuentes.pubmed("x", r"ventilat", maximo=3)
    assert filtrados and all(re.search("ventilat", f, re.I) for a in filtrados for f in a["frases"])


def test_guias_titulo_exige_cada_palabra_en_el_titulo(red):
    respuestas, pedidas = red
    respuestas.update({r"esearch\.fcgi\?db=pubmed": b'{"esearchresult": {"idlist": []}}'})
    assert fuentes.guias("hospital-acquired pneumonia", titulo=True) == []
    consulta = urllib.parse.unquote(pedidas[0])
    assert "(hospital-acquired[ti] AND pneumonia[ti])" in consulta and "guideline[pt]" in consulta


def test_pmc_texto_recurre_a_europe_pmc(red):
    respuestas, pedidas = red
    respuestas.update({r"eutils\.ncbi": RuntimeError("No se pudo consultar eutils.ncbi.nlm.nih.gov"),
                       r"europepmc/webservices/rest/PMC6018155/fullTextXML": "europepmc-fulltext.xml"})
    r = fuentes.pmc_texto("PMC6018155", ("48 h",))
    assert r["texto_completo"] and r["fuente"] == "Europe PMC"
    assert "after 48 h of admission" in r["fragmentos"]["48 h"][0]
    assert any("eutils" in u for u in pedidas)


def test_pmc_texto_sin_texto_completo_lo_dice(red):
    respuestas, _ = red
    respuestas.update({r"eutils\.ncbi": b"<pmc-articleset><article>The publisher of this article does not allow "
                                        b"downloading of the full text in XML form.</article></pmc-articleset>",
                       r"europepmc": RuntimeError("No se pudo consultar www.ebi.ac.uk")})
    r = fuentes.pmc_texto("PMC1", ("x",))
    assert r["texto_completo"] is False and "NCBI PMC" in r["detalle"]


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


def test_pdf_texto_da_la_pagina_de_cada_frase(tmp_path):
    pymupdf = pytest.importorskip("pymupdf")
    doc = pymupdf.open()
    for texto in ("Einleitung. Keine Zahlen hier.", "Die Therapiedauer sollte 7-8 Tage betragen. Andere Frage."):
        doc.new_page().insert_text((72, 72), texto)
    ruta = tmp_path / "guia.pdf"
    doc.save(ruta)
    r = fuentes.pdf_texto(str(ruta), ("7-8 Tage",))
    assert r["paginas"] == 2 and r["aviso"] is None
    assert r["fragmentos"]["7-8 Tage"] == [{"pagina": 2, "texto": "Die Therapiedauer sollte 7-8 Tage betragen."}]
