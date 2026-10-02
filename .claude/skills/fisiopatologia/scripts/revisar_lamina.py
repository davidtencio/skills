"""Revisión automática de la maquetación de una lámina SVG, medida en Chromium tal como se renderiza.

Uso: python3 revisar_lamina.py lamina-1.svg [lamina-2.svg ...]   (o una carpeta de ejemplo)

Errores (código de salida 1):
- textos que se pisan entre sí;
- texto que se sale de la lámina;
- texto que nace dentro de un recuadro y se sale de él (tarjetas, cajas, celdas).
Avisos (no cambian el código de salida):
- letra de menos de 14 px fuera del pie (las etiquetas pequeñas de los componentes son a veces intencionadas);
- tarjetas con mucho espacio vacío debajo del texto.

No sustituye mirar el PNG: no ve flechas mal dirigidas ni ilustraciones tapadas. Sí encuentra lo que más rondas costaba.
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from renderizar import ejecutable

TOLERANCIA = 2.0        # px que se perdonan en solapes y desbordes (rasgos de las letras, redondeos)
LETRA_MINIMA = 14.0
ALTO_PIE = 60           # franja inferior del pie, donde se admite letra de 12,5 px

MEDIR = """
() => {
  const svg = document.querySelector('svg');
  const caja = svg.getBoundingClientRect();
  const escala = caja.width / svg.viewBox.baseVal.width;
  const rel = r => ({x: (r.left - caja.left) / escala, y: (r.top - caja.top) / escala,
                     w: r.width / escala, h: r.height / escala});
  const textos = [...svg.querySelectorAll('text')].map((t, i) => {
    const primero = t.querySelector('tspan') || t;
    return {i, texto: t.textContent.trim().slice(0, 60), caja: rel(t.getBoundingClientRect()),
            tam: parseFloat(getComputedStyle(t).fontSize),
            ancla: {x: parseFloat(primero.getAttribute('x') || t.getAttribute('x') || 0),
                    y: parseFloat(primero.getAttribute('y') || t.getAttribute('y') || 0)},
            girado: !!t.getAttribute('transform')};
  }).filter(t => t.texto);
  const recuadros = [...svg.querySelectorAll('rect')].map(r => ({caja: rel(r.getBoundingClientRect()),
      relleno: (r.getAttribute('fill') || '').toLowerCase(), rx: parseFloat(r.getAttribute('rx') || 0)}))
    .filter(r => r.caja.w >= 60 && r.caja.h >= 30 && r.caja.w < 1590);
  return {ancho: svg.viewBox.baseVal.width, alto: svg.viewBox.baseVal.height, textos, recuadros};
}
"""


def _dentro(p, c, margen=0):
    return c["x"] - margen <= p["x"] <= c["x"] + c["w"] + margen and c["y"] - margen <= p["y"] <= c["y"] + c["h"] + margen


def _interseccion(a, b):
    w = min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"])
    h = min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"])
    return (w, h) if w > 0 and h > 0 else (0, 0)


def analizar(datos):
    """Aplica las reglas a las medidas de una lámina. Devuelve (errores, avisos) como listas de frases."""
    errores, avisos = [], []
    textos, recuadros = datos["textos"], datos["recuadros"]
    for t in textos:
        c = t["caja"]
        if c["x"] < -TOLERANCIA or c["y"] < -TOLERANCIA or c["x"] + c["w"] > datos["ancho"] + TOLERANCIA \
                or c["y"] + c["h"] > datos["alto"] + TOLERANCIA:
            errores.append(f"«{t['texto']}» se sale de la lámina")
        en_pie = c["y"] > datos["alto"] - ALTO_PIE
        if t["tam"] < LETRA_MINIMA and not (en_pie and t["tam"] >= 12.5):
            avisos.append(f"«{t['texto']}» tiene letra de {t['tam']:g} px")
        # recuadro que contiene el ancla del texto: el más pequeño
        contenedores = [r for r in recuadros if _dentro(t["ancla"], r["caja"])]
        if contenedores and not t["girado"]:
            r = min(contenedores, key=lambda r: r["caja"]["w"] * r["caja"]["h"])["caja"]
            if c["x"] + c["w"] > r["x"] + r["w"] + TOLERANCIA or c["x"] < r["x"] - TOLERANCIA \
                    or c["y"] + c["h"] > r["y"] + r["h"] + TOLERANCIA:
                errores.append(f"«{t['texto']}» se sale de su recuadro")
    for k, a in enumerate(textos):
        for b in textos[k + 1:]:
            w, h = _interseccion(a["caja"], b["caja"])
            if w > TOLERANCIA * 2 and h > TOLERANCIA * 2:
                errores.append(f"«{a['texto']}» y «{b['texto']}» se pisan")
    for r in recuadros:  # tarjetas con mucho hueco debajo del texto
        c = r["caja"]
        if r["rx"] < 8 or r["relleno"] not in ("#ffffff", "white") or c["h"] < 120:
            continue
        dentro = [t["caja"] for t in textos if _dentro(t["ancla"], c)]
        if dentro:
            fondo = max(t["y"] + t["h"] for t in dentro)
            hueco = c["y"] + c["h"] - fondo
            if hueco > max(90, 0.45 * c["h"]):
                avisos.append(f"recuadro en ({c['x']:.0f}, {c['y']:.0f}) con {hueco:.0f} px vacíos bajo el texto")
    return errores, avisos


def medir(svgs):
    """Mide todas las láminas con un solo navegador. Devuelve {ruta: datos}."""
    resultado = {}
    with sync_playwright() as p:
        navegador = p.chromium.launch(executable_path=ejecutable())
        pagina = navegador.new_page(viewport={"width": 1600, "height": 900})
        for svg in svgs:
            pagina.set_content(f'<html><body style="margin:0">{Path(svg).read_text(encoding="utf-8")}</body></html>')
            resultado[str(svg)] = pagina.evaluate(MEDIR)
        navegador.close()
    return resultado


def revisar(rutas):
    svgs = []
    for ruta in map(Path, rutas):
        svgs += sorted(ruta.glob("lamina-*.svg"), key=lambda p: int(p.stem.split("-")[1])) if ruta.is_dir() else [ruta]
    return {svg: analizar(datos) for svg, datos in medir(svgs).items()}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    informe = revisar(sys.argv[1:])
    total = 0
    for svg, (errores, avisos) in informe.items():
        if errores or avisos:
            print(f"\n{Path(svg).name}")
        for e in errores:
            print(f"  ERROR  {e}")
        for a in avisos:
            print(f"  aviso  {a}")
        total += len(errores)
    print(f"\n{len(informe)} láminas revisadas, {total} errores." if total else f"\n{len(informe)} láminas sin errores.")
    if "--json" in sys.argv:
        print(json.dumps({k: {"errores": e, "avisos": a} for k, (e, a) in informe.items()}, ensure_ascii=False))
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
