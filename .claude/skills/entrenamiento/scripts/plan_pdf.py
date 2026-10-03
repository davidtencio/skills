#!/usr/bin/env python3
"""Convierte un plan en Markdown en un PDF A4 ilustrado.

Uso:
    python3 plan_pdf.py planes/<nombre>/plan.md [--salida plan.pdf]
    python3 plan_pdf.py --lista            # ejercicios del catálogo con su clave

Además del Markdown normal (tablas incluidas), el plan admite dos marcas, cada una en su propia línea:

    {{ejercicio: press-banca-mancuernas | 3 × 8–12 · RIR 2 · 2 min}}
        Tarjeta del ejercicio: las dos fases ilustradas (Everkinetic, CC BY-SA 4.0), el mapa de músculos
        principales y secundarios, el equipo, la prescripción (texto libre tras «|») y las claves de técnica.

    {{musculos: sentadilla-mancuernas, press-banca-mancuernas, remo-polea-baja | Sesión A}}
        Mapa de todos los músculos que trabaja una sesión (principales de cualquier ejercicio en rojo).

Al final se añade la página de créditos de las imágenes. Las claves salen de `assets/ejercicios/catalogo.json`;
una clave desconocida detiene el proceso con la lista de claves válidas.
"""
import argparse
import html
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

import markdown

sys.path.insert(0, str(Path(__file__).resolve().parent))
import musculos  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
EJERCICIOS = RAIZ / "assets" / "ejercicios"
FUENTES = RAIZ / "assets" / "fuentes" / "fuentes.css"

MARCA = re.compile(r"^\{\{\s*(ejercicio|musculos)\s*:\s*(.+?)\s*\}\}\s*$", re.M)

CSS = """
@page { size: A4; margin: 16mm 15mm 18mm 15mm; }
:root { --texto: #1f2933; --suave: #52606d; --linea: #d9e2ec; --acento: #d1495b; --fondo: #f5f7fa; }
* { box-sizing: border-box; }
body { font-family: Inter, Helvetica, Arial, sans-serif; color: var(--texto); font-size: 10pt; line-height: 1.45;
       margin: 0; background: #fff; }
h1 { font-size: 21pt; margin: 0 0 2mm; letter-spacing: -0.01em; }
h1 + p { color: var(--suave); margin-top: 0; }
h2 { font-size: 14pt; margin: 8mm 0 3mm; padding-bottom: 1.5mm; border-bottom: 2px solid var(--acento);
     break-after: avoid; }
h3 { font-size: 11.5pt; margin: 5mm 0 2mm; break-after: avoid; }
p, ul, ol { margin: 0 0 2.5mm; }
blockquote { margin: 3mm 0; padding: 2.5mm 4mm; background: #fff4f4; border-left: 3px solid var(--acento);
             color: var(--texto); }
blockquote p { margin: 0; }
table { border-collapse: collapse; width: 100%; margin: 2mm 0 4mm; font-size: 9pt; break-inside: auto; }
th, td { border: 1px solid var(--linea); padding: 1.6mm 2.2mm; text-align: left; vertical-align: top; }
th { background: var(--fondo); font-weight: 600; }
tr { break-inside: avoid; }
code { font-size: 9pt; }
.ejercicio { border: 1px solid var(--linea); border-radius: 3mm; padding: 3mm 4mm; margin: 3mm 0;
             break-inside: avoid; }
.ej-cab { display: flex; justify-content: space-between; align-items: baseline; gap: 4mm; }
.ej-cab h4 { margin: 0; font-size: 11.5pt; }
.presc { font-weight: 600; color: var(--acento); white-space: nowrap; }
.ej-cuerpo { display: flex; align-items: center; gap: 4mm; margin: 2mm 0; }
.ej-fotos { flex: 1; display: flex; align-items: center; justify-content: center; gap: 2mm; min-height: 38mm; }
.ej-fotos img { height: 40mm; max-width: 46%; object-fit: contain; }
.flecha { color: var(--suave); font-size: 14pt; }
.sin-img { flex: 1; text-align: center; color: var(--suave); font-size: 9pt; background: var(--fondo);
           border-radius: 2mm; padding: 14mm 2mm; }
.ej-mapa svg { display: block; }
.ej-datos { font-size: 9pt; color: var(--suave); margin-bottom: 1mm; }
.ej-datos b { color: var(--texto); font-weight: 600; }
.claves { margin: 1mm 0 0; padding-left: 5mm; font-size: 9pt; }
.sesion { display: flex; align-items: center; gap: 6mm; border: 1px solid var(--linea); border-radius: 3mm;
          padding: 3mm 4mm; margin: 3mm 0; break-inside: avoid; }
.sesion h4 { margin: 0 0 1.5mm; font-size: 11pt; }
.sesion ul { font-size: 9pt; padding-left: 5mm; }
.creditos { font-size: 8.5pt; color: var(--suave); break-before: page; }
.creditos h2 { color: var(--texto); }
"""


def catalogo():
    datos = json.loads((EJERCICIOS / "catalogo.json").read_text(encoding="utf-8"))
    return {e["id"]: e for e in datos}


def _buscar(cat, clave):
    if clave not in cat:
        raise ValueError(f"Ejercicio desconocido: «{clave}». Claves válidas: {', '.join(sorted(cat))}")
    return cat[clave]


def _nombres(claves):
    return ", ".join(musculos.NOMBRES[m] for m in claves)


def tarjeta(cat, argumento):
    clave, _, prescripcion = (x.strip() for x in argumento.partition("|"))
    e = _buscar(cat, clave)
    if e["imagenes"]:
        a, b = ((EJERCICIOS / i).resolve().as_uri() for i in e["imagenes"])
        fotos = (f'<div class="ej-fotos"><img src="{a}" alt="{html.escape(e["nombre"])}: posición inicial">'
                 f'<span class="flecha">→</span><img src="{b}" alt="{html.escape(e["nombre"])}: posición final"></div>')
    else:
        fotos = '<div class="sin-img">Sin ilustración en la biblioteca: guíate por las claves de técnica.</div>'
    mapa = musculos.mapa(e["principales"], e["secundarios"], ancho=165)
    secundarios = f' · <b>Secundarios:</b> {_nombres(e["secundarios"])}' if e["secundarios"] else ""
    claves = "".join(f"<li>{html.escape(c)}</li>" for c in e["claves"])
    return (f'<div class="ejercicio"><div class="ej-cab"><h4>{html.escape(e["nombre"])}</h4>'
            f'<span class="presc">{html.escape(prescripcion)}</span></div>'
            f'<div class="ej-cuerpo">{fotos}<div class="ej-mapa">{mapa}</div></div>'
            f'<div class="ej-datos"><b>Equipo:</b> {html.escape(e["equipo"])} · '
            f'<b>Principales:</b> {_nombres(e["principales"])}{secundarios}</div>'
            f'<ul class="claves">{claves}</ul></div>')


def sesion(cat, argumento):
    lista, _, titulo = argumento.partition("|")
    ejercicios = [_buscar(cat, c.strip()) for c in lista.split(",") if c.strip()]
    principales = {m for e in ejercicios for m in e["principales"]}
    secundarios = {m for e in ejercicios for m in e["secundarios"]} - principales
    mapa = musculos.mapa(sorted(principales), sorted(secundarios), ancho=230)
    titulo = html.escape(titulo.strip() or "Músculos de la sesión")
    filas = "".join(f"<li>{html.escape(e['nombre'])}</li>" for e in ejercicios)
    return (f'<div class="sesion"><div>{mapa}</div><div><h4>{titulo}</h4>'
            f'<p class="ej-datos"><b>Principales:</b> {_nombres(sorted(principales))}</p><ul>{filas}</ul></div></div>')


def creditos(usados):
    lineas = ["<h2>Créditos de las imágenes</h2>"]
    if usados:
        nombres = ", ".join(sorted(usados))
        lineas.append(
            "<p>Ilustraciones de ejercicios: <b>Everkinetic</b> (everkinetic.com, Greg Priday), "
            "<a href=\"https://github.com/everkinetic/data\">github.com/everkinetic/data</a>, con licencia "
            "<a href=\"https://creativecommons.org/licenses/by-sa/4.0/deed.es\">Creative Commons Atribución-"
            f"CompartirIgual 4.0</a>. Sin modificaciones. Ejercicios ilustrados en este plan: {html.escape(nombres)}.</p>")
    lineas.append("<p>Mapas musculares: dibujo esquemático propio de la skill <i>entrenamiento</i>, sin escala "
                  "anatómica. Tipografía Inter (SIL Open Font License 1.1).</p>")
    return f'<section class="creditos">{"".join(lineas)}</section>'


def a_html(texto_md, titulo="Plan"):
    cat = catalogo()
    piezas, usados = [], set()

    def sustituir(m):
        tipo, argumento = m.groups()
        if tipo == "ejercicio":
            e = _buscar(cat, argumento.partition("|")[0].strip())
            if e["imagenes"]:
                usados.add(e["nombre"])
            piezas.append(tarjeta(cat, argumento))
        else:
            piezas.append(sesion(cat, argumento))
        return f"\n\n<div data-pieza=\"{len(piezas) - 1}\"></div>\n\n"

    cuerpo = markdown.markdown(MARCA.sub(sustituir, texto_md), extensions=["tables", "sane_lists"])
    cuerpo = re.sub(r'<div data-pieza="(\d+)"></div>', lambda m: piezas[int(m.group(1))], cuerpo)
    fuentes = FUENTES.read_text(encoding="utf-8")
    base = FUENTES.parent.resolve().as_uri() + "/"
    fuentes = re.sub(r"url\(([^)]+)\)", lambda m: f"url({base}{m.group(1)})", fuentes)
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{html.escape(titulo)}</title>'
            f"<style>{fuentes}{CSS}</style></head><body>{cuerpo}{creditos(usados)}</body></html>")


def _ejecutable():
    if os.environ.get("CHROMIUM_PATH"):
        return os.environ["CHROMIUM_PATH"]
    for candidato in ("/opt/pw-browsers/chromium", "/usr/bin/chromium", "/usr/bin/chromium-browser"):
        if Path(candidato).is_file():
            return candidato
    return None


def generar(ruta_md, salida=None):
    from playwright.sync_api import sync_playwright

    ruta_md = Path(ruta_md)
    texto = ruta_md.read_text(encoding="utf-8")
    titulo = next(iter(re.findall(r"^# (.+)$", texto, re.M)), ruta_md.stem)
    ruta_html = ruta_md.with_suffix(".html")
    ruta_html.write_text(a_html(texto, titulo), encoding="utf-8")
    salida = Path(salida) if salida else ruta_md.with_suffix(".pdf")
    pie = ('<div style="font-family:Helvetica,Arial,sans-serif;font-size:7pt;color:#7b8794;width:100%;'
           'padding:0 15mm;display:flex;justify-content:space-between">'
           f'<span>{html.escape(titulo)} · {date.today().isoformat()}</span>'
           '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
    with sync_playwright() as p:
        navegador = p.chromium.launch(executable_path=_ejecutable())
        pagina = navegador.new_page()
        pagina.goto(ruta_html.resolve().as_uri())
        pagina.wait_for_load_state("networkidle")
        pagina.evaluate("document.fonts.ready")
        pagina.pdf(path=str(salida), prefer_css_page_size=True, print_background=True, outline=True, tagged=True,
                   display_header_footer=True, header_template="<span></span>", footer_template=pie)
        navegador.close()
    return salida


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("plan", nargs="?", help="plan en Markdown")
    p.add_argument("--salida")
    p.add_argument("--lista", action="store_true", help="muestra las claves del catálogo de ejercicios")
    a = p.parse_args(argv)
    if a.lista:
        for e in catalogo().values():
            marca = "" if e["imagenes"] else "  (sin ilustración)"
            print(f"{e['id']:30} {e['nombre']} · {e['equipo']}{marca}")
        return 0
    if not a.plan:
        p.error("falta la ruta del plan")
    try:
        print(generar(a.plan, a.salida))
    except ValueError as e:
        p.error(str(e))
    return 0


if __name__ == "__main__":
    sys.exit(main())
