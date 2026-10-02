"""El SKILL.md de cada skill es válido y lo que menciona existe."""
import re

import pytest

from conftest import SKILLS, SKILLS_DIR

LIMITE_DESCRIPCION = 1024  # especificación de Agent Skills; claude.ai rechaza descripciones más largas


def frontmatter(skill):
    texto = (SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8")
    bloque = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    assert bloque, "SKILL.md sin frontmatter"
    return dict(re.findall(r"^(\w+): (.*)$", bloque.group(1), re.M))


def documentos(skill):
    raiz = SKILLS_DIR / skill
    return [raiz / "SKILL.md", *sorted((raiz / "references").glob("*.md"))]


@pytest.mark.parametrize("skill", SKILLS)
def test_frontmatter(skill):
    datos = frontmatter(skill)
    assert datos.get("name") == skill
    descripcion = datos.get("description", "")
    assert descripcion, "Falta la descripción"
    assert len(descripcion) <= LIMITE_DESCRIPCION, f"Descripción de {len(descripcion)} caracteres"


@pytest.mark.parametrize("skill", SKILLS)
def test_rutas_citadas_existen(skill):
    raiz = SKILLS_DIR / skill
    faltan = []
    for doc in documentos(skill):
        for ruta in re.findall(r"`((?:scripts|references|assets)/[^`<>*\s]+)`", doc.read_text(encoding="utf-8")):
            if not (raiz / ruta).exists():
                faltan.append(f"{doc.name}: {ruta}")
    assert not faltan, faltan


@pytest.mark.parametrize("skill", SKILLS)
def test_comandos_de_fuentes_existen(skill):
    """Cada `fuentes.py <comando>` citado en la documentación existe en el despachador del script."""
    raiz = SKILLS_DIR / skill
    codigo = (raiz / "scripts" / "fuentes.py").read_text(encoding="utf-8")
    despachador = codigo[codigo.index("funciones = {"):]
    disponibles = set(re.findall(r'"([a-z][\w-]*)":', despachador))
    citados = {c for doc in documentos(skill)
               for c in re.findall(r"fuentes\.py ([a-z][\w-]*)", doc.read_text(encoding="utf-8"))}
    assert not sorted(citados - disponibles), f"Comandos citados que no existen: {sorted(citados - disponibles)}"
