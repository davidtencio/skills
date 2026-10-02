"""Casos límite de las piezas de dibujo de fisiopatologia (único test que importa código de una skill en proceso)."""
import sys
import xml.etree.ElementTree as ET

import pytest

from conftest import SKILLS_DIR

sys.path.insert(0, str(SKILLS_DIR / "fisiopatologia" / "scripts"))
from componentes import adn  # noqa: E402
from piezas import curva_fcfd  # noqa: E402
from recursos import ATRIBUCION, atribucion  # noqa: E402


def bien_formado(fragmento):
    ET.fromstring(f'<svg xmlns="http://www.w3.org/2000/svg">{fragmento}</svg>')


@pytest.mark.parametrize("indice", [None, "tiempo", "cmax", "abc"])
def test_curva_fcfd_por_indice(indice):
    s = curva_fcfd(60, 190, 700, 420, indice=indice, titulo="Prueba")
    bien_formado(s)
    assert "Esquema cualitativo" in s


def test_curva_fcfd_cmi_por_encima_de_la_curva():
    bien_formado(curva_fcfd(0, 0, 700, 420, indice="tiempo", cmi=1.5))


def test_curva_fcfd_pequena_acorta_rotulo():
    s = curva_fcfd(0, 0, 460, 200)
    assert "Concentración del fármaco" not in s and "Concentración" in s


def test_adn_admite_coordenadas_decimales():
    bien_formado(adn(10.4, 120.6, 50.2))


def test_atribucion():
    assert atribucion() == ATRIBUCION
    assert "TogoTV" in atribucion("togotv-sars-cov-2.svg") and "Servier" not in atribucion("togotv-sars-cov-2.svg")
    combinada = atribucion("servier-lung.svg", "togotv-sars-cov-2.svg")
    assert combinada.index("Servier") < combinada.index("TogoTV")
