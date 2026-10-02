"""Regresión de los ejemplos: las láminas, el glosario y el PDF siguen saliendo como los versionados.

Si un cambio en los scripts altera un ejemplo a propósito, regenera en el mismo PR sus láminas y la huella de su PDF
(`pdf.py <carpeta> --huella`); el PDF solo se versiona en los ejemplos que ya lo guardan (uno por skill).
"""
import json
import xml.etree.ElementTree as ET

import pytest

from conftest import RAIZ, ejecutar, ejemplos, versionados

EJEMPLOS = ejemplos()
IDS = [f"{skill}/{carpeta.name}" for skill, carpeta in EJEMPLOS]

COMPARAR_SVG = """
import importlib.util, json, sys
from pathlib import Path
f = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("laminas_ejemplo", f)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
print(json.dumps([n for n, fn in m.LAMINAS.items()
                  if fn() != f.with_name(f"lamina-{n}.svg").read_text(encoding="utf-8")]))
"""


@pytest.mark.parametrize("skill, carpeta", EJEMPLOS, ids=IDS)
def test_laminas_identicas(skill, carpeta):
    r = ejecutar("-c", COMPARAR_SVG, carpeta / "laminas.py")
    assert r.returncode == 0, r.stderr[-2000:]
    distintas = json.loads(r.stdout.strip().splitlines()[-1])
    assert not distintas, f"Las láminas {distintas} ya no coinciden con las versionadas: regenera el ejemplo"


@pytest.mark.parametrize("skill, carpeta", EJEMPLOS, ids=IDS)
def test_svg_bien_formados(skill, carpeta):
    for svg in sorted(carpeta.glob("lamina-*.svg")):
        ET.parse(svg)


@pytest.mark.parametrize("skill, carpeta", EJEMPLOS, ids=IDS)
def test_glosario_completo(skill, carpeta):
    r = ejecutar(carpeta.parents[1] / "scripts" / "glosario.py", carpeta)
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]


@pytest.mark.chromium
@pytest.mark.parametrize("skill, carpeta", EJEMPLOS, ids=IDS)
def test_maquetacion_sin_errores(skill, carpeta):
    """Ningún texto se pisa con otro ni se sale de la lámina o de su recuadro (revisar_lamina.py)."""
    r = ejecutar(carpeta.parents[1] / "scripts" / "revisar_lamina.py", carpeta)
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-2000:]


HUELLA = """
import json, sys
sys.path.insert(0, sys.argv[1])
from pdf import huella
print(json.dumps(huella(sys.argv[2]), ensure_ascii=False))
"""
REGENERAR = ("regenera el PDF y su huella: python3 scripts/pdf.py ejemplos/<nombre> --huella "
             "(y versiona el PDF solo si el ejemplo ya lo guardaba)")


def _comparar_huellas(nueva, guardada):
    assert nueva["paginas"] == guardada["paginas"], f"{nueva['paginas']} páginas en lugar de {guardada['paginas']}; {REGENERAR}"
    assert nueva["indice"] == guardada["indice"], f"El índice de marcadores cambió; {REGENERAR}"
    distintas = [k + 1 for k, (a, b) in enumerate(zip(nueva["texto"], guardada["texto"])) if a != b]
    assert not distintas, f"Las páginas {distintas} ya no tienen el mismo texto; {REGENERAR}"


def _huella(carpeta, pdf):
    r = ejecutar("-c", HUELLA, carpeta.parents[1] / "scripts", pdf)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


@pytest.mark.parametrize("skill, carpeta", EJEMPLOS, ids=IDS)
def test_huella_y_pdf_guardado_coinciden(skill, carpeta):
    """Cada ejemplo guarda la huella de su PDF; si además guarda el PDF (uno por skill), es el de esa huella."""
    ruta = carpeta / "huella-pdf.json"
    assert ruta.exists(), f"Falta {ruta.name}; {REGENERAR}"
    guardado = carpeta / f"{carpeta.name}.pdf"
    if guardado in versionados(str(guardado.relative_to(RAIZ))):
        _comparar_huellas(_huella(carpeta, guardado), json.loads(ruta.read_text(encoding="utf-8")))


@pytest.mark.pdf
@pytest.mark.parametrize("skill, carpeta", EJEMPLOS, ids=IDS)
def test_pdf_misma_estructura(skill, carpeta, tmp_path):
    """El PDF regenerado tiene la huella guardada: mismas páginas, mismo índice de marcadores y mismo texto en cada
    página (material.md fija la portada y la fecha). No se comparan bytes: Chromium añade la fecha de creación."""
    salida = tmp_path / f"{carpeta.name}.pdf"
    r = ejecutar(carpeta.parents[1] / "scripts" / "pdf.py", carpeta, "--salida", salida, timeout=900)
    assert r.returncode == 0, r.stderr[-2000:]
    _comparar_huellas(_huella(carpeta, salida),
                      json.loads((carpeta / "huella-pdf.json").read_text(encoding="utf-8")))


CON_EVIDENCIAS = [(s, c) for s, c in EJEMPLOS if (c / "evidencias.json").exists()]


@pytest.mark.parametrize("skill, carpeta", CON_EVIDENCIAS, ids=[f"{s}/{c.name}" for s, c in CON_EVIDENCIAS])
def test_evidencias_completas(skill, carpeta):
    """Cada cifra de las láminas está en evidencias.json, con una frase de la fuente que contiene su número."""
    r = ejecutar(carpeta.parents[1] / "scripts" / "verificar_evidencias.py", carpeta)
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-2000:]
