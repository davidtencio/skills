"""Extracción de cifras y comprobaciones sin red de verificar_evidencias.py."""
import json

import pytest

from conftest import SKILLS, SKILLS_DIR, ejecutar

LAMINA = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900">
<text x="40" y="40"><tspan>NEUMONÍA · LÁMINA 2 DE 9 · CLÍNICA</tspan></text>
<text x="40" y="200"><tspan>Fiebre &gt; 38,3 °C y leucocitos &gt; 10 000/µl</tspan><tspan>Duración: 7–8 días (lámina 9)</tspan></text>
<text x="40" y="300"><tspan>1</tspan></text>
<text x="40" y="400"><tspan>Recomendación 21; PMID 28890434; tobramicina 6 mg/kg</tspan></text>
<text x="40" y="860"><tspan>Fuentes: guía S3 2024; 95 % de algo</tspan></text>
</svg>"""

CODIGO = """
import json, sys
sys.path.insert(0, sys.argv[1])
from verificar_evidencias import cifras_lamina, revisar
print(json.dumps({"cifras": cifras_lamina(sys.argv[2] + "/lamina-2.svg"), "revision": revisar(sys.argv[2])},
                 ensure_ascii=False))
"""


def _ejecutar(skill, carpeta):
    r = ejecutar("-c", CODIGO, SKILLS_DIR / skill / "scripts", carpeta)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


@pytest.mark.parametrize("skill", SKILLS)
def test_extrae_cifras_sin_cabecera_pie_ni_referencias(skill, tmp_path):
    (tmp_path / "lamina-2.svg").write_text(LAMINA, encoding="utf-8")
    d = _ejecutar(skill, tmp_path)
    assert d["cifras"] == ["> 38,3 °C", "> 10 000/µl", "7–8 días", "6 mg/kg"]
    errores, pendientes = d["revision"]
    assert errores == [] and pendientes == {"2": d["cifras"]}


@pytest.mark.parametrize("skill", SKILLS)
def test_detecta_cifra_que_no_esta_en_la_frase(skill, tmp_path):
    (tmp_path / "lamina-2.svg").write_text(LAMINA, encoding="utf-8")
    (tmp_path / "evidencias.json").write_text(json.dumps({"evidencias": [
        {"cifras": ["> 38,3 °C", "> 10 000/µl"], "laminas": [2], "fuente": "S3", "frase": "Fieber > 38,3 °C, Leukozyten > 10 000"},
        {"cifras": ["7–8 días"], "laminas": [2], "fuente": "S3", "frase": "sieben bis acht Tage"},
        {"cifras": ["6 mg/kg"], "laminas": [2], "fuente": "S3", "frase": "Tobramycin 1x 5 mg/kg"}]}), encoding="utf-8")
    errores, pendientes = _ejecutar(skill, tmp_path)["revision"]
    assert pendientes == {}
    assert len(errores) == 1 and "6" in errores[0] and "no aparece" in errores[0]
