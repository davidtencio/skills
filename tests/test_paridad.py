"""Paridad del código común entre las skills: lo que tienen en común debe ser idéntico.

Las dos skills llevan sus propias copias de los módulos comunes (cada skill se instala sola). Para que un arreglo
en una no se quede sin aplicar en la otra:
- los módulos de IDENTICOS deben ser iguales byte a byte;
- en el resto de los módulos con el mismo nombre, cada función o clase que exista en las dos copias debe tener el
  mismo código. Pueden diferir el docstring del módulo, las constantes (textos, paletas, listas de fuentes) y las
  funciones que solo tiene una de las skills.
Si este test falla, copia el cambio a la otra skill.
"""
import ast

import pytest

from conftest import SKILLS, SKILLS_DIR

IDENTICOS = ["renderizar.py", "hoja_comparacion.py", "estructuras.py", "superficie.py", "revisar_lamina.py",
             "glosario.py"]


def _modulos_comunes():
    if len(SKILLS) < 2:
        return []
    conjuntos = [{p.name for p in (SKILLS_DIR / s / "scripts").glob("*.py")} for s in SKILLS]
    return sorted(set.intersection(*conjuntos))


def _definiciones(ruta):
    codigo = ruta.read_text(encoding="utf-8")
    arbol = ast.parse(codigo)
    return {n.name: ast.get_source_segment(codigo, n) for n in arbol.body
            if isinstance(n, (ast.FunctionDef, ast.ClassDef))}


@pytest.mark.parametrize("modulo", IDENTICOS)
def test_modulos_identicos(modulo):
    copias = {s: (SKILLS_DIR / s / "scripts" / modulo).read_bytes() for s in SKILLS
              if (SKILLS_DIR / s / "scripts" / modulo).exists()}
    assert len(copias) == len(SKILLS), f"{modulo} falta en alguna skill"
    assert len(set(copias.values())) == 1, f"{modulo} difiere entre {sorted(copias)}"


@pytest.mark.parametrize("modulo", _modulos_comunes())
def test_funciones_comunes_iguales(modulo):
    copias = [_definiciones(SKILLS_DIR / s / "scripts" / modulo) for s in SKILLS]
    comunes = set.intersection(*(set(c) for c in copias))
    distintas = sorted(n for n in comunes if len({c[n] for c in copias}) > 1)
    assert not distintas, f"{modulo}: estas funciones difieren entre las skills: {distintas}"
