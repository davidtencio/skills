"""Convierte un SVG en PNG (2x) con Chromium vía Playwright.

Uso: python3 renderizar.py imagen.svg [salida.png]
Requiere: pip install playwright. Si el navegador no está instalado,
definir CHROMIUM_PATH o ejecutar `playwright install chromium`.
"""
import os
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def ejecutable():
    if os.environ.get("CHROMIUM_PATH"):
        return os.environ["CHROMIUM_PATH"]
    for candidato in ("/opt/pw-browsers/chromium", "/usr/bin/chromium", "/usr/bin/chromium-browser"):
        if Path(candidato).is_file():
            return candidato
    return None


def renderizar(svg_path, png_path=None, escala=2):
    svg_path = Path(svg_path)
    png_path = Path(png_path) if png_path else svg_path.with_suffix(".png")
    contenido = svg_path.read_text(encoding="utf-8")
    ancho, alto = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', contenido).groups())
    html = f'<html><body style="margin:0">{contenido}</body></html>'
    with sync_playwright() as p:
        navegador = p.chromium.launch(executable_path=ejecutable())
        pagina = navegador.new_page(viewport={"width": int(ancho), "height": int(alto)}, device_scale_factor=escala)
        pagina.set_content(html)
        pagina.locator("svg").screenshot(path=str(png_path))
        navegador.close()
    return png_path


if __name__ == "__main__":
    print(renderizar(*sys.argv[1:3]))
