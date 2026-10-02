"""Las reglas de revisar_lamina.py detectan los fallos de maquetación que deben detectar."""
import pytest

from conftest import SKILLS, SKILLS_DIR, ejecutar

MALA = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900">
<rect x="100" y="100" width="300" height="200" rx="16" fill="#FFFFFF" stroke="#999"/>
<text x="120" y="150" font-size="22">Este título es demasiado largo para su tarjeta</text>
<text x="700" y="400" font-size="30">Primero</text>
<text x="710" y="405" font-size="30">Segundo</text>
<text x="1500" y="600" font-size="20">Se sale por la derecha</text>
<text x="200" y="700" font-size="10">diminuto</text>
</svg>"""

BUENA = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900">
<rect x="100" y="100" width="600" height="120" rx="16" fill="#FFFFFF" stroke="#999"/>
<text x="120" y="150" font-size="22">Cabe holgado</text><text x="120" y="190" font-size="17">Segunda línea</text>
</svg>"""

ANALIZAR = """
import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from revisar_lamina import revisar
print(json.dumps({Path(k).name: v for k, v in revisar(sys.argv[2:]).items()}, ensure_ascii=False))
"""


@pytest.mark.chromium
@pytest.mark.parametrize("skill", SKILLS)
def test_detecta_errores_y_acepta_lamina_correcta(skill, tmp_path):
    import json
    (tmp_path / "mala.svg").write_text(MALA, encoding="utf-8")
    (tmp_path / "buena.svg").write_text(BUENA, encoding="utf-8")
    r = ejecutar("-c", ANALIZAR, SKILLS_DIR / skill / "scripts", tmp_path / "mala.svg", tmp_path / "buena.svg")
    assert r.returncode == 0, r.stderr[-2000:]
    informe = json.loads(r.stdout.strip().splitlines()[-1])
    errores, avisos = informe["mala.svg"]
    assert any("demasiado largo" in e and "recuadro" in e for e in errores)
    assert any("Primero" in e and "Segundo" in e and "pisan" in e for e in errores)
    assert any("derecha" in e and "lámina" in e for e in errores)
    assert any("diminuto" in a for a in avisos)
    assert informe["buena.svg"] == [[], []]


@pytest.mark.parametrize("skill", SKILLS)
def test_partir_respeta_el_ancho(skill):
    codigo = """
import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from componentes import ancho_texto, partir, texto
frase = "La ventilación mecánica rompe las barreras del huésped y permite la microaspiración"
lineas = partir(frase, 300, 17)
print(json.dumps({"lineas": lineas, "anchos": [ancho_texto(l, 17) for l in lineas],
                  "igual_sin_ancho": texto(0, 0, ["a b", "c"]) == texto(0, 0, "a b\\nc")}))
"""
    import json
    r = ejecutar("-c", codigo, SKILLS_DIR / skill / "scripts")
    assert r.returncode == 0, r.stderr[-2000:]
    d = json.loads(r.stdout.strip().splitlines()[-1])
    assert len(d["lineas"]) > 1 and all(a <= 300 for a in d["anchos"])
    assert " ".join(d["lineas"]).startswith("La ventilación mecánica rompe")
    assert d["igual_sin_ancho"]
