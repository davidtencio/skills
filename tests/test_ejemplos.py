"""Regresión de los ejemplos: las láminas, el glosario y el PDF siguen saliendo como los versionados.

Si un cambio en los scripts altera un ejemplo a propósito, regenera sus láminas y su PDF en el mismo PR.
"""
import json
import xml.etree.ElementTree as ET

import pytest

from conftest import ejecutar, ejemplos

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


@pytest.mark.pdf
@pytest.mark.parametrize("skill, carpeta", EJEMPLOS, ids=IDS)
def test_pdf_misma_estructura(skill, carpeta, tmp_path):
    """El PDF regenerado tiene las mismas páginas y el mismo índice de marcadores que el versionado.
    No se comparan píxeles: la portada lleva la fecha de generación."""
    pymupdf = pytest.importorskip("pymupdf")
    versionado = carpeta / f"{carpeta.name}.pdf"
    salida = tmp_path / versionado.name
    r = ejecutar(carpeta.parents[1] / "scripts" / "pdf.py", carpeta, "--salida", salida, timeout=900)
    assert r.returncode == 0, r.stderr[-2000:]
    nuevo, viejo = pymupdf.open(salida), pymupdf.open(versionado)
    assert len(nuevo) == len(viejo), f"{len(nuevo)} páginas en lugar de {len(viejo)}"
    assert nuevo.get_toc() == viejo.get_toc()
