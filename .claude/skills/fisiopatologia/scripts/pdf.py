"""Genera el PDF final de una enfermedad: portada, índice, glosario, láminas y ficha de la enfermedad.

Uso:
    python3 scripts/pdf.py ejemplos/<enfermedad>            # crea ejemplos/<enfermedad>/<enfermedad>.pdf
    python3 scripts/pdf.py ejemplos/<enfermedad> --portada 3  # lámina que ilustra la portada

Lee `material.md` y todas las `lamina-N.png` de la carpeta (sin límite de número). El diseño es
A4: portada, índice con números de página, glosario de siglas, una lámina por página en horizontal y la ficha en
vertical con tipografía editorial (Source Serif 4 para títulos, Inter para el texto).
"""

import argparse
import html
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

import markdown

sys.path.insert(0, str(Path(__file__).parent))
from renderizar import ejecutable  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
FUENTES_CSS = RAIZ / "assets" / "fuentes" / "fuentes.css"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
         "noviembre", "diciembre"]

# Secciones del material con tratamiento visual propio (por el comienzo del título).
DESTACADAS = {"puntos clave": "clave", "error frecuente": "error", "pregunta de autoevaluación": "pregunta",
              "no verificado": "pendiente", "fuentes": "fuentes", "simplificaciones": "simplificaciones",
              "lista de verificación": "pendiente"}
# Fuentes que se reconocen en el material para resumirlas en la portada.
SELLOS = [("CIMA", "Ficha técnica AEMPS (CIMA)"), ("FDA", "Fichas de la FDA"), ("EMA", "EMA"),
          ("ChEMBL", "ChEMBL"), ("UniProt", "UniProt"), ("NCBI Gene", "NCBI Gene"),
          ("NCI Thesaurus", "NCI Thesaurus"), ("Reactome", "Reactome"), ("PMID", "PubMed / Europe PMC"),
          ("LiverTox", "LiverTox"), ("MedlinePlus", "MedlinePlus"), ("PDB", "RCSB PDB"),
          ("AlphaFold", "AlphaFold"), ("PubChem", "PubChem"), ("BindingDB", "BindingDB"), ("CPIC", "CPIC"), ("LactMed", "LactMed"),
          ("openFDA", "openFDA"), ("ADA", "ADA (diabetes.org)"), ("EASD", "Consenso ADA/EASD"), ("NIDDK", "NIDDK (NIH)"),
          ("OMS", "OMS"), ("OPS", "OPS"), ("MeSH", "MeSH"), ("MONDO", "MONDO"), ("ESC", "Guías ESC"),
          ("KDIGO", "KDIGO"),
          # Fuentes en otros idiomas (traducidas al español)
          ("Käypä hoito", "Käypä hoito (Finlandia)"), ("AWMF", "AWMF (Alemania)"),
          ("VersorgungsLeitlinie", "NVL (Alemania)"), ("IQWiG", "IQWiG (Alemania)"),
          ("Helsedirektoratet", "Helsedirektoratet (Noruega)"), ("Felleskatalogen", "Felleskatalogen (Noruega)"),
          ("pro.medicin.dk", "pro.medicin.dk (Dinamarca)"), ("FASS", "FASS (Suecia)"), ("Janusinfo", "Janusinfo (Suecia)"),
          ("Farmacotherapeutisch Kompas", "Farmacotherapeutisch Kompas (Países Bajos)"), ("HAS", "HAS (Francia)"),
          ("AIFA", "AIFA (Italia)")]


def _slug(texto):
    t = texto.lower()
    for a, b in zip("áéíóúüñ", "aeiouun"):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def leer_material(carpeta):
    """Separa el material en título, lista de láminas y cuerpo (sin la lista ni el aviso inicial)."""
    texto = (carpeta / "material.md").read_text(encoding="utf-8")
    titulo = re.search(r"^# (.+)$", texto, re.M).group(1).strip()
    titulos = {int(n): t for t, n in re.findall(r"^\s*\d+\.\s*\[(.+?)\]\(lamina-(\d+)\.png\)", texto, re.M)}
    cuerpo = re.sub(r"^# .+\n", "", texto, count=1, flags=re.M)
    cuerpo = re.sub(r"^\s*\d+\.\s*\[.+?\]\(lamina-\d+\.png\)\s*$\n?", "", cuerpo, flags=re.M)
    cuerpo = re.sub(r"^>.*\n", "", cuerpo, flags=re.M)
    cuerpo = re.sub(r"^(Serie de .*láminas.*|Versión anterior.*)\n", "", cuerpo, flags=re.M)
    cuerpo = re.sub(r"\]\((lamina-\d+|[\w-]+)\.png\)", "]", cuerpo)  # enlaces a PNG sueltos
    return titulo, titulos, cuerpo.strip()


def laminas(carpeta, titulos):
    numeradas = [(int(m.group(1)), p) for p in carpeta.glob("lamina-*.png")
                 if (m := re.fullmatch(r"lamina-(\d+)", p.stem))]
    return [(n, titulos.get(n, f"Lámina {n}"), p) for n, p in sorted(numeradas)]


def _normalizar_listas(md):
    """Ajusta el Markdown de estilo GitHub a Python-Markdown: sangría de 4 espacios y línea en blanco antes de listas."""
    salida, previa = [], ""
    for linea in md.splitlines():
        sangria = len(linea) - len(linea.lstrip(" "))
        if 0 < sangria < 4 and linea.strip():
            linea = "    " + linea.lstrip(" ")
        es_lista = re.match(r"\s*([-*]|\d+\.) ", linea)
        if es_lista and previa.strip() and not re.match(r"\s*([-*]|\d+\.) ", previa):
            salida.append("")
        salida.append(linea)
        previa = linea
    return "\n".join(salida)


def cuerpo_html(md):
    """Convierte el material en HTML con secciones, citas y recuadros."""
    md = _normalizar_listas(md)
    md = re.sub(r"<details>\s*<summary>(.*?)</summary>(.*?)</details>",
                lambda m: f'<div class="respuesta" markdown="1">\n<p class="respuesta-titulo">{m.group(1)}</p>\n'
                          f'{m.group(2)}\n</div>', md, flags=re.S)
    md = re.sub(r"^- \[ \] ", "- ☐ ", md, flags=re.M)
    cuerpo = markdown.markdown(md, extensions=["tables", "md_in_html", "sane_lists"])
    cuerpo = re.sub(r"<em>\[(.+?)\]</em>", r'<span class="cita">\1</span>', cuerpo)
    cuerpo = re.sub(r"<p><span class=\"cita\">(.+?)</span></p>", r'<p class="cita-sola"><span class="cita">\1</span></p>',
                    cuerpo)
    partes = re.split(r"<h2>(.*?)</h2>", cuerpo)
    secciones, html_secciones = [], [partes[0]]
    for i in range(1, len(partes), 2):
        nombre = re.sub(r"<[^>]+>", "", re.sub(r'<span class="cita">.*?</span>', "", partes[i])).strip()
        clase = next((v for k, v in DESTACADAS.items() if nombre.lower().startswith(k)), "")
        ident = "s-" + _slug(nombre)
        n = len(secciones) + 1
        secciones.append((ident, nombre))
        citas = re.findall(r'<span class="cita">.*?</span>', partes[i])
        titulo_h2 = re.sub(r'\s*<span class="cita">.*?</span>', "", partes[i]).strip()
        bajo_titulo = f'<p class="cita-titulo">{" ".join(citas)}</p>' if citas else ""
        html_secciones.append(
            f'<section class="seccion {clase}" id="{ident}"><h2><span class="num">{n:02d}</span>{titulo_h2}</h2>'
            f'{bajo_titulo}<div class="contenido">{partes[i + 1]}</div></section>')
    return "".join(html_secciones), secciones


def fecha_es(d):
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def separar_glosario(md):
    """Saca la sección «## Glosario» del material: el PDF la muestra tras el índice, no al final."""
    m = re.search(r"^## Glosario\s*$(.*?)(?=^## |\Z)", md, re.M | re.S)
    if not m:
        return md, ""
    lista = markdown.markdown(_normalizar_listas(m.group(1).strip()), extensions=["sane_lists"])
    return md[:m.start()] + md[m.end():], lista


def documento(farmaco, subtitulo, lams, cuerpo, secciones, sellos, portada, paginas=None, glosario=""):
    paginas = paginas or {}
    total = len(lams)
    num = lambda ident: paginas.get(ident, "")  # noqa: E731
    indice_laminas = "".join(
        f'<li><a href="#l-{n}"><span class="n">{n}</span><span class="t">{html.escape(t)}</span>'
        f'<span class="pag">{num(f"l-{n}")}</span></a></li>' for n, t, _ in lams)
    indice_ficha = "".join(
        f'<li><a href="#{i}"><span class="n">{k:02d}</span><span class="t">{html.escape(t)}</span>'
        f'<span class="pag">{num(i)}</span></a></li>' for k, (i, t) in enumerate(secciones, 1))
    paginas_laminas = "".join(
        f'<section class="lamina" id="l-{n}"><header><span class="etq">Lámina {n} de {total}</span>'
        f'<span class="tit">{html.escape(t)}</span></header>'
        f'<div class="imagen" role="img" aria-label="{html.escape(t)}" '
        f'style="background-image:url({p.resolve().as_uri()})"></div></section>' for n, t, p in lams)
    indice_glosario = (f'<h3>Antes de empezar</h3><ol><li><a href="#glosario"><span class="n">G</span>'
                       f'<span class="t">Glosario de siglas y abreviaturas</span><span class="pag">{num("glosario")}'
                       f'</span></a></li></ol>') if glosario else ""
    pagina_glosario = (f'<section class="glosario" id="glosario"><h1>Glosario</h1><p class="intro">Siglas y '
                       f'abreviaturas que aparecen en las láminas y en la ficha de la enfermedad.</p>{glosario}'
                       f'</section>') if glosario else ""
    heroe = next((p for n, _, p in lams if n == portada), lams[0][2] if lams else None)
    sellos_html = "".join(f"<li>{html.escape(s)}</li>" for s in sellos)
    hoy = fecha_es(date.today())
    nombre_pie = html.escape(farmaco).replace('"', "")
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>{html.escape(farmaco)} · Fisiopatología y tratamiento</title>
<link rel="stylesheet" href="{FUENTES_CSS.as_uri()}">
<style>
:root {{ --tinta:#1d2733; --suave:#5b6773; --linea:#d9e0e6; --azul:#0b5d99; --azul-osc:#0a2f4d;
        --verde:#007a5e; --naranja:#c4520a; --morado:#8a3f7a; --fondo:#f3f6f9; }}
@page {{ size: A4; margin: 22mm 20mm 20mm 20mm;
  @top-right {{ content: "{nombre_pie} · Fisiopatología y tratamiento"; font: 500 7.5pt Inter, sans-serif;
               color: #7d8893; letter-spacing: .04em; }}
  @bottom-left {{ content: "Material profesional · Prototipo pendiente de revisión clínica";
                 font: 7.5pt Inter, sans-serif; color: #7d8893; }}
  @bottom-right {{ content: counter(page) " / " counter(pages); font: 600 8pt Inter, sans-serif; color: #5b6773; }} }}
@page portada {{ margin: 0; @top-right {{ content: none; }} @bottom-left {{ content: none; }}
                 @bottom-right {{ content: none; }} }}
@page apaisada {{ size: A4 landscape; margin: 14mm 14mm 14mm 14mm;
  @top-right {{ content: none; }}
  @bottom-left {{ content: "{nombre_pie} · Fisiopatología y tratamiento"; font: 7.5pt Inter, sans-serif; color: #7d8893; }}
  @bottom-right {{ content: counter(page) " / " counter(pages); font: 600 8pt Inter, sans-serif; color: #5b6773; }} }}
* {{ box-sizing: border-box; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ margin: 0; font-family: Inter, 'Liberation Sans', sans-serif; font-size: 9.6pt; line-height: 1.55;
        color: var(--tinta); font-feature-settings: "cv11", "ss01"; hyphens: auto; }}
h1, h2, h3 {{ font-family: 'Source Serif 4', 'Liberation Serif', serif; color: var(--azul-osc); }}
a {{ color: inherit; text-decoration: none; }}

/* Portada */
.portada {{ page: portada; height: 296mm; position: relative; overflow: hidden; break-after: page;
           background: #fff; }}
.portada .banda {{ background: linear-gradient(160deg, #0a2f4d 0%, #0b4d80 60%, #0b5d99 100%); color: #fff;
                  padding: 30mm 22mm 70mm; position: relative; }}
.portada .banda::after {{ content: ""; position: absolute; inset: 0;
  background: radial-gradient(circle at 85% 20%, rgba(255,255,255,.10) 0, rgba(255,255,255,0) 45%); }}
.portada .marca {{ font: 600 8.5pt Inter; letter-spacing: .22em; text-transform: uppercase; color: #9cc8ea; }}
.portada h1 {{ color: #fff; font-size: 40pt; line-height: 1.05; margin: 9mm 0 5mm; font-weight: 700;
              letter-spacing: -.01em; }}
.portada .sub {{ font: 400 14pt 'Source Serif 4', serif; color: #d7e7f4; max-width: 140mm; }}
.portada .regla {{ width: 22mm; height: 1.2mm; background: #e69f00; margin-top: 9mm; border-radius: 1mm; }}
.portada .heroe {{ position: absolute; left: 22mm; right: 22mm; top: 112mm; border-radius: 2.5mm; overflow: hidden;
                  box-shadow: 0 6mm 14mm rgba(10,47,77,.28), 0 0 0 .3mm rgba(10,47,77,.15); background: #fff; }}
.portada .heroe img {{ display: block; width: 100%; }}
.portada .datos {{ position: absolute; left: 22mm; right: 22mm; bottom: 20mm; display: grid;
                  grid-template-columns: 1fr 1fr 1fr; gap: 6mm; }}
.portada .datos div {{ border-top: .5mm solid var(--azul); padding-top: 2.5mm; }}
.portada .datos b {{ display: block; font: 600 7pt Inter; letter-spacing: .14em; text-transform: uppercase;
                    color: var(--suave); margin-bottom: 1mm; }}
.portada .datos span {{ font-size: 9.5pt; }}
.portada .sellos {{ list-style: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: 1.2mm; }}
.portada .sellos li {{ font-size: 7.4pt; background: var(--fondo); border: .25mm solid var(--linea);
                      border-radius: 4mm; padding: .4mm 2.2mm; }}
.portada .verificado {{ position: absolute; left: 22mm; right: 22mm; bottom: 48mm; }}
.portada .verificado b {{ display: block; font: 600 7pt Inter; letter-spacing: .14em; text-transform: uppercase;
                         color: var(--suave); margin-bottom: 2.5mm; }}
.portada .aviso {{ position: absolute; left: 22mm; right: 22mm; bottom: 9mm; font-size: 7.6pt; color: var(--naranja); }}

/* Índice */
.indice {{ break-after: page; }}
.indice h1 {{ font-size: 26pt; margin: 0 0 2mm; }}
.indice .intro {{ color: var(--suave); margin: 0 0 4mm; }}
.indice h3 {{ font: 600 8pt Inter; letter-spacing: .16em; text-transform: uppercase; color: var(--azul);
             margin: 5mm 0 1.2mm; border-bottom: .3mm solid var(--linea); padding-bottom: 1.2mm; }}
.indice ol {{ list-style: none; padding: 0; margin: 0; font-size: 9.5pt; }}
.indice li a {{ display: flex; align-items: baseline; gap: 4mm; padding: 1mm 0; border-bottom: .2mm dotted #c6ced6; }}
.indice .n {{ font: 600 9pt Inter; color: var(--azul); width: 7mm; }}
.indice .t {{ flex: 1; }}
.indice .pag {{ font-weight: 600; color: var(--suave); font-variant-numeric: tabular-nums; }}

/* Láminas */
.lamina {{ page: apaisada; break-before: page; }}
.lamina header {{ display: flex; align-items: baseline; gap: 4mm; margin-bottom: 3.5mm; }}
.lamina .etq {{ font: 600 7.5pt Inter; letter-spacing: .16em; text-transform: uppercase; color: #fff;
               background: var(--azul); padding: 1mm 2.6mm; border-radius: 1mm; }}
.lamina .tit {{ font: 600 13pt 'Source Serif 4', serif; color: var(--azul-osc); }}
/* Fondo y no <img>: Chromium 141 manda a la página siguiente las imágenes de páginas con nombre. */
.lamina .imagen {{ width: 269mm; height: 151.3mm; background: center / contain no-repeat; border-radius: 1.5mm; box-shadow: 0 0 0 .3mm var(--linea); }}

/* Ficha */
.ficha-cabecera {{ break-before: page; margin-bottom: 8mm; padding-bottom: 5mm; border-bottom: .6mm solid var(--azul); }}
.ficha-cabecera .marca {{ font: 600 8pt Inter; letter-spacing: .2em; text-transform: uppercase; color: var(--azul); }}
.ficha-cabecera h1 {{ font-size: 25pt; margin: 2mm 0 0; line-height: 1.15; }}
.seccion {{ margin: 0 0 7mm; }}
.seccion h2 {{ font-size: 14.5pt; margin: 0 0 3mm; display: flex; align-items: baseline; gap: 3mm;
              break-after: avoid; }}
.seccion h2 .num {{ font: 600 8.5pt Inter; color: var(--azul); letter-spacing: .05em; }}
h3 {{ font-size: 11pt; margin: 4mm 0 1.5mm; break-after: avoid; }}
p {{ margin: 0 0 2.4mm; orphans: 3; widows: 3; }}
ul, ol {{ margin: 0 0 2.6mm; padding-left: 5mm; }}
li {{ margin-bottom: 1.1mm; }}
li > p {{ margin: 0; }}
strong {{ font-weight: 600; color: #101a24; }}
.cita {{ font-size: 7.4pt; color: var(--azul); background: #e8f1f8; border-radius: 1mm; padding: .15mm 1.3mm;
        white-space: nowrap; font-style: normal; font-weight: 500; }}
.cita-sola {{ margin-top: -1mm; }}
.cita-titulo {{ margin: -1.5mm 0 3mm 8.5mm; }}
.cita-titulo .cita {{ white-space: normal; }}
table {{ width: 100%; border-collapse: collapse; margin: 2mm 0 4mm; font-size: 8.8pt; break-inside: avoid; }}
th {{ text-align: left; font: 600 7.4pt Inter; letter-spacing: .1em; text-transform: uppercase; color: #fff;
     background: var(--azul-osc); padding: 2mm 2.5mm; }}
td {{ padding: 1.8mm 2.5mm; border-bottom: .25mm solid var(--linea); vertical-align: top; }}
tr:nth-child(even) td {{ background: #f6f8fa; }}
.clave .contenido > ol {{ list-style: none; padding: 0; counter-reset: k; }}
.clave .contenido > ol > li {{ counter-increment: k; position: relative; padding: 3mm 4mm 3mm 13mm;
  background: var(--fondo); border-radius: 1.5mm; margin-bottom: 2mm; break-inside: avoid; }}
.clave .contenido > ol > li::before {{ content: counter(k); position: absolute; left: 3.5mm; top: 2.8mm;
  width: 6mm; height: 6mm; border-radius: 50%; background: var(--azul); color: #fff; font: 700 8.5pt/6mm Inter;
  text-align: center; }}
.error .contenido, .pregunta .contenido, .pendiente .contenido {{ border-radius: 1.5mm; padding: 4mm 5mm 2mm;
  break-inside: avoid; }}
.error .contenido {{ background: #fdf2ea; border-left: 1.2mm solid var(--naranja); }}
.pregunta .contenido {{ background: #eef5fb; border-left: 1.2mm solid var(--azul); }}
.pendiente .contenido {{ background: #eef7f3; border-left: 1.2mm solid var(--verde); }}
.respuesta {{ background: #fff; border: .25mm solid var(--linea); border-radius: 1.2mm; padding: 3mm 4mm 1mm;
             margin: 3mm 0 2mm; }}
.respuesta-titulo {{ font: 600 7.4pt Inter; letter-spacing: .14em; text-transform: uppercase; color: var(--azul); }}
.simplificaciones .contenido {{ color: var(--suave); font-size: 9pt; }}
.fuentes .contenido {{ font-size: 8.4pt; color: #3a4652; columns: 2; column-gap: 8mm; }}
.fuentes .contenido li {{ break-inside: avoid; }}
.glosario {{ break-before: page; }}
.glosario h1 {{ font-size: 26pt; margin: 0 0 2mm; }}
.glosario .intro {{ color: var(--suave); margin: 0 0 6mm; }}
.glosario ul {{ list-style: none; padding: 0; margin: 0; columns: 2; column-gap: 8mm; font-size: 9pt; }}
.glosario li {{ break-inside: avoid; margin: 0 0 1.8mm; padding-left: 0; line-height: 1.35; }}
.glosario li::before {{ content: none; }}
.glosario strong {{ color: var(--azul); }}
.cierre {{ margin-top: 8mm; padding-top: 3mm; border-top: .3mm solid var(--linea); font-size: 7.8pt;
          color: var(--suave); }}
</style></head><body>

<section class="portada">
  <div class="banda">
    <div class="marca">Fisiopatología · Material profesional</div>
    <h1>{html.escape(farmaco)}</h1>
    <div class="sub">{html.escape(subtitulo)}</div>
    <div class="regla"></div>
  </div>
  {f'<div class="heroe"><img src="{heroe.resolve().as_uri()}"></div>' if heroe else ''}
  <div class="verificado"><b>Datos verificados en</b><ul class="sellos">{sellos_html}</ul></div>
  <div class="datos">
    <div><b>Dirigido a</b><span>Profesionales de salud</span></div>
    <div><b>Contenido</b><span>{total} láminas · ficha de la enfermedad</span></div>
    <div><b>Fecha</b><span>{hoy}</span></div>
  </div>
  <div class="aviso">Prototipo pendiente de revisión clínica. No sustituye las guías de práctica clínica vigentes.</div>
</section>

<section class="indice">
  <h1>Contenido</h1>
  <p class="intro">Láminas para proyectar o imprimir y ficha de la enfermedad con la fuente de cada dato.</p>
  {indice_glosario}
  <h3>Láminas</h3><ol>{indice_laminas}</ol>
  <h3>Ficha de la enfermedad</h3><ol>{indice_ficha}</ol>
</section>

{pagina_glosario}

{paginas_laminas}

<header class="ficha-cabecera"><div class="marca">Ficha de la enfermedad</div><h1>{html.escape(farmaco)}</h1></header>
{cuerpo}
<p class="cierre">Generado el {hoy}. Ilustraciones: Servier Medical Art (CC BY 3.0 y 4.0). Prototipo pendiente de revisión clínica;
no sustituye las guías de práctica clínica vigentes ni el juicio clínico.</p>
</body></html>"""


def _imprimir(pagina, ruta_html, ruta_pdf):
    pagina.goto(ruta_html.as_uri(), timeout=120000)
    pagina.wait_for_load_state("load", timeout=120000)  # todo es local: no hace falta esperar la red
    pagina.evaluate("document.fonts.ready")
    pagina.pdf(path=str(ruta_pdf), prefer_css_page_size=True, outline=True, tagged=True)


def _paginas(ruta_pdf, lams, secciones):
    """Busca en qué página quedó el glosario, cada lámina y cada sección (para el índice)."""
    import pymupdf
    doc = pymupdf.open(ruta_pdf)
    textos = [p.get_text() for p in doc]
    res, desde = {}, 2
    plano = [re.sub(r"\s+", " ", t).lower() for t in textos]
    for i in range(desde, len(textos)):
        if "siglas y abreviaturas que aparecen" in plano[i]:
            res["glosario"], desde = i + 1, i + 1
            break
    for n, titulo, _ in lams:
        for i in range(desde, len(textos)):
            if re.sub(r"\s+", " ", titulo).lower()[:40] in plano[i]:
                res[f"l-{n}"], desde = i + 1, i + 1
                break
    for ident, nombre in secciones:
        clave = re.sub(r"\s+", " ", nombre).strip()[:30]
        for i in range(desde, len(textos)):
            if clave.lower() in re.sub(r"\s+", " ", textos[i]).lower():
                res[ident], desde = i + 1, i
                break
    return res


def generar(carpeta, portada=None, salida=None):
    from playwright.sync_api import sync_playwright
    carpeta = Path(carpeta).resolve()
    titulo, titulos, md = leer_material(carpeta)
    farmaco = titulo.split(":")[0].strip()
    lams = laminas(carpeta, titulos)
    if portada is None:  # por defecto, la primera lámina de fisiopatología
        portada = next((n for n, t, _ in lams if re.search(r"fisiopatolog|resistencia|falla|daño", t, re.I)), lams[0][0])
    subtitulo = "De la fisiopatología al tratamiento"
    md, glosario = separar_glosario(md)
    cuerpo, secciones = cuerpo_html(md)
    seccion = re.search(r"^## Fuentes\s*$(.*?)(?=^## |\Z)", md, re.M | re.S)  # solo lo citado como fuente
    texto_fuentes = seccion.group(1) if seccion else md
    sellos = [nombre for clave, nombre in SELLOS if re.search(rf"\b{re.escape(clave)}\b", texto_fuentes)]
    salida = Path(salida) if salida else carpeta / f"{carpeta.name}.pdf"
    with tempfile.TemporaryDirectory() as tmp, sync_playwright() as p:
        ruta_html = Path(tmp) / "documento.html"
        navegador = p.chromium.launch(executable_path=ejecutable())
        pagina = navegador.new_page()
        ruta_html.write_text(documento(farmaco, subtitulo, lams, cuerpo, secciones, sellos, portada,
                                       glosario=glosario), encoding="utf-8")
        _imprimir(pagina, ruta_html, salida)  # primera pasada: medir páginas
        paginas = _paginas(salida, lams, secciones)
        ruta_html.write_text(documento(farmaco, subtitulo, lams, cuerpo, secciones, sellos, portada, paginas,
                                       glosario), encoding="utf-8")
        _imprimir(pagina, ruta_html, salida)
        navegador.close()
    import pymupdf
    doc = pymupdf.open(salida)
    doc.set_metadata({"title": f"{farmaco} · Fisiopatología y tratamiento", "author": "Skill fisiopatologia",
                      "subject": "Material educativo para profesionales de salud",
                      "keywords": f"{farmaco}, fisiopatología, diagnóstico, tratamiento"})
    doc.saveIncr()
    return salida


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("carpeta")
    ap.add_argument("--portada", type=int, help="número de la lámina de la portada")
    ap.add_argument("--salida")
    a = ap.parse_args()
    print(generar(a.carpeta, a.portada, a.salida))
