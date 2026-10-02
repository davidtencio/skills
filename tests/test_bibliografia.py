"""Bibliografía estructurada (bibliografia.py) y citas numeradas y enlazadas del PDF (pdf.py), sin red.

Se prueba la copia de fisiopatologia: bibliografia.py es idéntico en las dos skills (test_paridad.py).
"""
import json
import sys

import pytest

from conftest import SKILLS_DIR, versionados

sys.path.insert(0, str(SKILLS_DIR / "fisiopatologia" / "scripts"))
import bibliografia  # noqa: E402

pytest.importorskip("markdown")
import pdf  # noqa: E402

REFERENCIAS = [
    {"clave": "idsa-2016", "tipo": "guia", "cita": "Kalil AC, Metersky ML. Management of Adults. Clin Infect Dis. "
     "2016;63(5):e61-e111.", "pmid": "27418577", "pmcid": "PMC4981759", "doi": "10.1093/cid/ciw353",
     "sello": "IDSA/ATS"},
    {"clave": "s3-2024", "tipo": "guia", "cita": "Rademacher J, et al. Nosokomiale Pneumonie. S3-Leitlinie; 2024",
     "url": "https://register.awmf.org/x.pdf", "idioma": "de", "version": "3.0", "consultado": "2026-10-02"},
]
MATERIAL = """# Tema

Primera afirmación. *[@s3-2024, rec. 21; traducción propia]*
Segunda. *[@idsa-2016, p. e63; @s3-2024]*

## Fuentes

texto previo que se conserva
"""


@pytest.fixture
def carpeta(tmp_path):
    (tmp_path / "material.md").write_text(MATERIAL, encoding="utf-8")
    bibliografia.guardar(tmp_path, REFERENCIAS)
    return tmp_path


def test_citas_con_localizador():
    assert bibliografia.citas("x *[@s3-2024, rec. 21; traducción propia]* y *[@idsa-2016; @ers-2017, p. 3]*") == [
        ("s3-2024", "rec. 21; traducción propia"), ("idsa-2016", ""), ("ers-2017", "p. 3")]


def test_numeracion_por_orden_de_primera_cita(carpeta):
    assert bibliografia.numeracion(carpeta) == {"s3-2024": 1, "idsa-2016": 2}


def test_lista_vancouver_con_enlaces_idioma_y_fecha(carpeta):
    lineas = bibliografia.lista(carpeta).splitlines()
    assert lineas[0].startswith("1. Rademacher J") and "En alemán; traducción propia" in lineas[0]
    assert "Versión 3.0" in lineas[0] and "Consultado el 2 de octubre de 2026" in lineas[0]
    assert lineas[1].startswith("2. Kalil AC") and "PMID [27418577](https://pubmed.ncbi.nlm.nih.gov/27418577/)" in lineas[1]
    assert "doi:[10.1093/cid/ciw353](https://doi.org/10.1093/cid/ciw353)" in lineas[1]


def test_comprobar_detecta_claves_huerfanas_y_lista_desactualizada(carpeta):
    errores, _ = bibliografia.comprobar(carpeta)
    assert any("no tiene la lista generada" in e for e in errores)
    bibliografia.escribir_lista(carpeta)
    material = (carpeta / "material.md").read_text(encoding="utf-8")
    assert "texto previo que se conserva" in material
    assert bibliografia.comprobar(carpeta) == ([], [])
    (carpeta / "material.md").write_text(material + "\nOtra. *[@inexistente]*\n", encoding="utf-8")
    bibliografia.guardar(carpeta, REFERENCIAS + [{"clave": "sin-citar", "tipo": "web", "cita": "X", "url": "https://x"}])
    errores, _ = bibliografia.comprobar(carpeta)
    assert "cita a una clave inexistente: @inexistente" in errores and "sin-citar: no se cita en el material" in errores


def test_vancouver_desde_csl():
    csl = {"author": [{"family": f"Autor{k}", "given": "Ana María"} for k in range(7)]
           + [{"family": "Committee for Diabetes*"}],
           "title": "Resistance in <i>Staphylococcus aureus</i>.", "container-title-short": "J Ejemplo",
           "issued": {"date-parts": [[2026]]}, "volume": "49", "issue": "Supplement_1", "page": "S1-S9"}
    assert bibliografia.vancouver(csl) == ("Autor0 AM, Autor1 AM, Autor2 AM, Autor3 AM, Autor4 AM, Autor5 AM, et al. "
                                          "Resistance in *Staphylococcus aureus*. J Ejemplo. 2026;49(Suppl 1):S1-S9.")


def test_resumen_de_la_busqueda(carpeta):
    lineas = [{"fecha": "2026-10-02T10:00:00+00:00", "funcion": "guias", "argumentos": ["type 2 diabetes"],
               "opciones": {"titulo": "True"}, "resultado": {"n": 10}},
              {"fecha": "2026-10-02T10:01:00+00:00", "funcion": "vigencia", "argumentos": ["36151309"],
               "opciones": {}, "resultado": {"posteriores": ["42825450"]}},
              {"fecha": "2026-10-02T10:02:00+00:00", "funcion": "pubmed", "argumentos": ["x"], "opciones": {},
               "resultado": {"n": 1}}]
    (carpeta / "busquedas.jsonl").write_text("\n".join(json.dumps(x) for x in lineas), encoding="utf-8")
    texto = bibliografia.resumen_busqueda(carpeta)
    assert "el 2 de octubre de 2026" in texto and "3 consultas" in texto
    assert "`type 2 diabetes` (10 resultados, en el título)" in texto
    assert "PMID 36151309 (1 candidata)" in texto and "`x` (1 resultado)" in texto


def test_pdf_citas_numeradas_y_enlaces():
    html, _ = pdf.cuerpo_html("Dato. *[@idsa-2016, p. e63; @s3-2024]*\n\nVer PMID 27418577 y PMC4981759.\n",
                              {"s3-2024": 1, "idsa-2016": 2})
    assert '<a href="#ref-2">2</a>, p. e63; <a href="#ref-1">1</a>' in html
    assert '<a href="https://pubmed.ncbi.nlm.nih.gov/27418577/">PMID 27418577</a>' in html
    assert '<a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC4981759/">PMC4981759</a>' in html
    ya = pdf.enlazar_identificadores('<a href="https://doi.org/10.1093/x">doi: 10.1093/x</a> y doi: 10.1183/y.')
    assert ya.count("<a ") == 2 and 'href="https://doi.org/10.1183/y"' in ya


@pytest.mark.parametrize("bib", versionados(".claude/skills/*/ejemplos/*/bibliografia.json"),
                         ids=lambda p: p.parent.name)
def test_bibliografia_de_los_ejemplos(bib):
    errores, _ = bibliografia.comprobar(bib.parent)
    assert not errores, errores
