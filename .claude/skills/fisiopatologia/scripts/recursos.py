"""Ilustraciones externas (Servier Medical Art, CC BY 3.0) insertadas como imágenes SVG.

Cada archivo se incrusta como data URI para que la lámina final sea un único SVG
autocontenido y sin conflictos de identificadores entre ilustraciones.
"""
import base64
from functools import lru_cache
from pathlib import Path

CARPETA = Path(__file__).resolve().parent.parent / "assets" / "ilustraciones"
ATRIBUCION = "Ilustraciones: Servier Medical Art (CC BY 3.0 y 4.0)"


@lru_cache(maxsize=None)
def _data_uri(nombre):
    ruta = CARPETA / nombre
    if not ruta.exists():
        ruta = CARPETA / f"servier-{nombre}.svg"
    return "data:image/svg+xml;base64," + base64.b64encode(ruta.read_bytes()).decode()


def ilustracion(nombre, x, y, w, h, girar=0, opacidad=1.0, espejo=False, ajustar="xMidYMid meet"):
    """Inserta la ilustración `nombre` en la caja (x, y, w, h).

    girar: grados alrededor del centro de la caja. espejo: refleja horizontalmente.
    ajustar: valor de preserveAspectRatio ("none" permite deformarla para llenar la caja).
    """
    cx, cy = x + w / 2, y + h / 2
    transformaciones = []
    if girar:
        transformaciones.append(f"rotate({girar} {cx:.1f} {cy:.1f})")
    if espejo:
        transformaciones.append(f"translate({2 * cx:.1f} 0) scale(-1 1)")
    t = f' transform="{" ".join(transformaciones)}"' if transformaciones else ""
    o = f' opacity="{opacidad}"' if opacidad < 1 else ""
    return (f'<image href="{_data_uri(nombre)}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'preserveAspectRatio="{ajustar}"{t}{o}/>')
