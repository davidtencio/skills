"""Hoja de comparación de candidatos (ilustraciones o estructuras) para elegir el mejor.

Uso: python3 hoja_comparacion.py salida.png archivo1.svg archivo2.png ...
Cada candidato se muestra en una celda con su nombre; luego se revisa la imagen con Read.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from renderizar import ejecutable


def hoja(salida, archivos, columnas=5, celda=260):
    celdas = "".join(
        f'<div style="display:inline-block;width:{celda}px;height:{celda + 30}px;margin:4px;border:1px solid #ccc;'
        f'text-align:center;font:12px Arial;vertical-align:top;background:#fff">'
        f'<img src="{Path(a).resolve().as_uri()}" style="max-width:{celda - 10}px;max-height:{celda - 10}px"><br>'
        f'{Path(a).name}</div>' for a in archivos)
    html = Path(salida).with_suffix(".html")
    html.write_text(f'<html><body style="margin:0;width:{columnas * (celda + 10)}px;background:#eee">{celdas}</body></html>')
    with sync_playwright() as p:
        navegador = p.chromium.launch(executable_path=ejecutable())
        pagina = navegador.new_page(viewport={"width": columnas * (celda + 10), "height": 400})
        pagina.goto(html.resolve().as_uri())
        pagina.wait_for_timeout(800)
        pagina.screenshot(path=str(salida), full_page=True)
        navegador.close()
    return salida


if __name__ == "__main__":
    print(hoja(sys.argv[1], sys.argv[2:]))
