"""El monitor de fuentes solo llama a funciones que existen en cada skill (sin red)."""
import re

import pytest

from conftest import RAIZ, ejecutar

COMPROBAR = """
import importlib, importlib.util, json, re, sys
from pathlib import Path
raiz, skill = Path(sys.argv[1]), sys.argv[2]
spec = importlib.util.spec_from_file_location("salud", raiz / "monitor" / "salud_fuentes.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
sys.path.insert(0, str(raiz / ".claude" / "skills" / skill / "scripts"))
modulos = {"f": importlib.import_module("fuentes")}
if (raiz / ".claude" / "skills" / skill / "scripts" / "valor.py").exists():
    modulos["v"] = importlib.import_module("valor")
faltan = [f"{nombre}: {alias}.{func}" for nombre, _, expr, _ in m.COMPROBACIONES[skill]
          for alias, func in re.findall(r"\\b([fv])\\.(\\w+)\\(", expr)
          if alias not in modulos or not hasattr(modulos[alias], func)]
prohibidas = [nombre for nombre, _, expr, _ in m.COMPROBACIONES[skill] if re.search(r"_descargar|servier_extraer", expr)]
print(json.dumps({"faltan": faltan, "prohibidas": prohibidas}))
"""


def skills_del_monitor():
    codigo = (RAIZ / "monitor" / "salud_fuentes.py").read_text(encoding="utf-8")
    return re.findall(r'^    "([\w-]+)": \[$', codigo, re.M)


@pytest.mark.parametrize("skill", skills_del_monitor())
def test_monitor_usa_funciones_existentes_y_sin_descargas(skill):
    import json
    r = ejecutar("-c", COMPROBAR, RAIZ, skill)
    assert r.returncode == 0, r.stderr[-2000:]
    resultado = json.loads(r.stdout.strip().splitlines()[-1])
    assert not resultado["faltan"], f"Funciones inexistentes: {resultado['faltan']}"
    assert not resultado["prohibidas"], f"Comprobaciones que escribirían en assets/: {resultado['prohibidas']}"
