"""La biblioteca de ilustraciones de cada skill está registrada y tiene licencias reutilizables."""
import json
import re

import pytest

from conftest import SKILLS, SKILLS_DIR

EXTENSIONES = {".svg", ".png", ".jpg", ".jpeg", ".webp"}


def biblioteca(skill):
    carpeta = SKILLS_DIR / skill / "assets" / "ilustraciones"
    registro = json.loads((carpeta / "registro.json").read_text(encoding="utf-8"))
    archivos = {p.name for p in carpeta.iterdir() if p.suffix.lower() in EXTENSIONES}
    return registro, archivos


@pytest.mark.parametrize("skill", SKILLS)
def test_cada_archivo_registrado(skill):
    registro, archivos = biblioteca(skill)
    assert not sorted(archivos - set(registro)), "Ilustraciones sin entrada en registro.json (usa fuentes.registrar)"
    assert not sorted(set(registro) - archivos), "Entradas de registro.json sin archivo"


@pytest.mark.parametrize("skill", SKILLS)
def test_licencias_reutilizables(skill):
    registro, _ = biblioteca(skill)
    for nombre, datos in registro.items():
        for campo in ("fuente", "licencia", "origen", "fecha"):
            assert datos.get(campo), f"{nombre}: falta «{campo}»"
        assert not re.search(r"\bN[CD]\b|NonCommercial|NoDeriv", datos["licencia"], re.I), \
            f"{nombre}: licencia no reutilizable ({datos['licencia']})"
