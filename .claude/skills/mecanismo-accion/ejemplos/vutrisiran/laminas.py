"""Vutrisiran en ocho láminas (plantilla: ARN pequeño de interferencia conjugado con GalNAc).

1. Contexto: de la TTR al amiloide y dónde actúa cada fármaco.
2. Fisiología: la TTR se fabrica en el hígado; en sangre, el tetrámero se disocia y forma amiloide.
3. Mecanismo (1): cómo llega vutrisiran al hepatocito (GalNAc y ASGPR; PDB 9G76).
4. Mecanismo (2): interferencia por ARN; Ago2 corta el ARNm de TTR (PDB 9CMP).
5. Farmacocinética: horas en plasma, meses de efecto.
6. Del mecanismo al paciente.
7. Indicaciones aprobadas (FDA y UE).
8. Del ensayo a la práctica: valor y vida real.

Uso: python3 laminas.py [1 2 3 4 5 6 7 8]
"""
from pathlib import Path
import sys

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))
sys.path.insert(0, str(RAIZ / "ejemplos" / "darolutamida"))
from componentes import (COLOR, adn, arnm, bloqueo, etiqueta_farmaco, flecha, paso, ribosoma, svg,  # noqa: E402
                         texto, vesicula)
from fuentes import pdb_descargar  # noqa: E402
from recursos import ATRIBUCION, ilustracion  # noqa: E402
from superficie import RADIOS, _mezcla, como_imagen, leer_pdb, superficie_corte  # noqa: E402
from laminas import leyenda_paso, tarjeta  # noqa: E402

ANCHO, ALTO = 1600, 900
SUAVE = COLOR["texto_suave"]
VERDE, AZUL, ROJO, NARANJA = COLOR["receptor_borde"], COLOR["farmaco"], COLOR["bloqueo"], COLOR["ligando_borde"]
LILA = COLOR["coactivador_borde"]
MORADO_ARN = "#7D4E9C"
TTR = ("#BFE6D8", VERDE)

FUENTES = ("Fuentes: ficha técnica de Amvuttra (CIMA-AEMPS); FDA (Amvuttra, tafamidis, acoramidis, patisiran, "
           f"eplontersen); UniProt P02766, Q9UKV8, P07306; PMID 36345805. {ATRIBUCION}.")


def lamina(numero, etiqueta, titulo, subtitulo, contenido, extra=""):
    c = (f'<rect x="0" y="0" width="{ANCHO}" height="6" fill="{AZUL}"/>'
         + texto(40, 38, f"VUTRISIRAN · LÁMINA {numero} DE {len(LAMINAS)} · {etiqueta.upper()}", tam=14, peso="bold",
                 color=AZUL)
         + texto(40, 76, titulo, tam=32, peso="bold") + texto(40, 104, subtitulo, tam=17, color=SUAVE)
         + contenido + texto(40, ALTO - 34, FUENTES + extra, tam=12.5, color=SUAVE)
         + texto(40, ALTO - 14, "Esquema simplificado y sin escala · Prototipo pendiente de revisión farmacológica",
                 tam=12.5, color=ROJO, peso="bold"))
    return svg(ANCHO, ALTO, c, f"Vutrisiran, lámina {numero}: {titulo}", subtitulo)


# --- Piezas propias --------------------------------------------------------------------

def membrana(x1, x2, y, paso_x=9):
    """Bicapa lipídica recta (cabezas y colas)."""
    s = f'<rect x="{x1}" y="{y - 12}" width="{x2 - x1}" height="24" fill="#FFF6D6"/>'
    colas = " ".join(f"M{x},{y - 8} L{x},{y - 2} M{x},{y + 2} L{x},{y + 8}" for x in range(x1, x2, paso_x))
    s += f'<path d="{colas}" stroke="{COLOR["membrana"]}" stroke-width="1"/>'
    s += "".join(f'<circle cx="{x}" cy="{y - 11}" r="3.6" fill="#F3D27A" stroke="#B08A2E" stroke-width="0.7"/>'
                 f'<circle cx="{x}" cy="{y + 11}" r="3.6" fill="#F3D27A" stroke="#B08A2E" stroke-width="0.7"/>'
                 for x in range(x1, x2, paso_x))
    return s


def tetramero(cx, cy, s=16, t4=False, opacidad=1.0):
    """TTR: cuatro subunidades iguales alrededor de un canal central (dímero de dímeros)."""
    relleno, borde = TTR
    o = f' opacity="{opacidad}"' if opacidad < 1 else ""
    r = "".join(f'<rect x="{cx - s + i * s + 1:.1f}" y="{cy - s + j * s + 1:.1f}" width="{s - 2}" '
                f'height="{s - 2}" rx="{s * 0.25:.1f}" fill="{relleno}" stroke="{borde}" stroke-width="1.6"/>'
                for i in (0, 1) for j in (0, 1))
    if t4:
        r += f'<circle cx="{cx}" cy="{cy}" r="{s * 0.28:.1f}" fill="{COLOR["ligando"]}" stroke="{NARANJA}"/>'
    return f"<g{o}>{r}</g>"


def monomero(cx, cy, s=16, mal_plegado=False):
    relleno, borde = TTR
    if not mal_plegado:
        return (f'<rect x="{cx - s + 1}" y="{cy - s + 1}" width="{2 * s - 2}" height="{2 * s - 2}" rx="{s * 0.45:.1f}" '
                f'fill="{relleno}" stroke="{borde}" stroke-width="1.6"/>')
    return (f'<path d="M{cx - s},{cy} C{cx - s},{cy - s} {cx - 2},{cy - s - 6} {cx + 4},{cy - s + 4} '
            f'C{cx + s + 6},{cy - s} {cx + s},{cy + 6} {cx + s - 4},{cy + 8} C{cx + 2},{cy + s + 4} '
            f'{cx - s + 4},{cy + s} {cx - s},{cy} Z" fill="#F6D6C8" stroke="{ROJO}" stroke-width="1.6"/>')


def fibra(x, y, n=4, largo=110):
    """Fibra amiloide: láminas apiladas en zigzag."""
    s = ""
    for i in range(n):
        pts = " ".join(f"{x + j * 10},{y + i * 9 + (4 if j % 2 else -4)}" for j in range(int(largo / 10) + 1))
        s += f'<polyline points="{pts}" fill="none" stroke="{ROJO}" stroke-width="2.2" stroke-linejoin="round"/>'
    return s


def hebra(x1, x2, y, color, ancho=4.5, bases=True, abajo=True):
    s = f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="{ancho}" stroke-linecap="round"/>'
    if bases:
        d = 7 if abajo else -7
        s += "".join(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + d}" stroke="{color}" stroke-width="2"/>'
                     for x in range(int(x1) + 6, int(x2) - 2, 9))
    return s


def galnac(x, y, r=7):
    """Ligando con tres N-acetilgalactosaminas (hexágonos naranja) unido a una hebra."""
    s = f'<path d="M{x},{y} L{x - 18},{y}" stroke="{COLOR["linea"]}" stroke-width="2"/>'
    for dy in (-20, 0, 20):
        hx, hy = x - 30, y + dy
        s += f'<line x1="{x - 18}" y1="{y}" x2="{hx + r}" y2="{hy}" stroke="{COLOR["linea"]}" stroke-width="1.6"/>'
        s += (f'<path d="M{hx - r},{hy} L{hx - r / 2},{hy - r * 0.87} L{hx + r / 2},{hy - r * 0.87} L{hx + r},{hy} '
              f'L{hx + r / 2},{hy + r * 0.87} L{hx - r / 2},{hy + r * 0.87} Z" fill="{COLOR["ligando"]}" '
              f'stroke="{NARANJA}" stroke-width="1.2"/>')
    return s


def vutrisiran(x, y, w=150, etiquetas=False):
    """ARNpi bicatenario (guía azul, pasajera gris) con el ligando GalNAc en la hebra pasajera."""
    s = hebra(x, x + w, y, "#9AA9B3", abajo=True) + hebra(x + 4, x + w + 10, y + 16, AZUL, abajo=False)
    s += galnac(x, y)
    if etiquetas:
        s += texto(x + w + 18, y + 4, "hebra pasajera (sentido)", tam=13, color=SUAVE)
        s += texto(x + w + 18, y + 22, "hebra guía (antisentido)", tam=13, color=AZUL, peso="bold")
        s += texto(x - 30, y + 44, "3 × GalNAc", tam=13, color=NARANJA, peso="bold", anclaje="middle")
    return s


def asgpr(x, y_mem, abierto=True):
    """ASGPR: receptor de membrana del hepatocito, con el dominio de unión hacia la sangre (arriba)."""
    borde, relleno = "#6A55A0", "#DCD3F0"
    s = f'<rect x="{x - 3}" y="{y_mem - 46}" width="6" height="58" rx="3" fill="{borde}"/>'
    s += (f'<path d="M{x - 18},{y_mem - 40} C{x - 22},{y_mem - 70} {x + 22},{y_mem - 70} {x + 18},{y_mem - 40} '
          f'L{x + 8},{y_mem - 52} L{x - 8},{y_mem - 52} Z" fill="{relleno}" stroke="{borde}" stroke-width="1.6"/>')
    return s


def ago2(cx, cy, w=110, guia=True):
    """Ago2 (núcleo del complejo RISC): ilustración de proteína de Servier con la hebra guía."""
    h = w * 71.962 / 64.214
    s = ilustracion("enzyme-pink-3d", cx - w / 2, cy - h / 2, w, h)
    if guia:
        s += hebra(cx - w * 0.38, cx + w * 0.38, cy + h * 0.12, AZUL, ancho=4, abajo=False)
    return s


def tijera(cx, cy):
    """Corte del ARNm por Ago2."""
    return (f'<path d="M{cx - 10},{cy - 14} L{cx + 10},{cy + 14} M{cx + 10},{cy - 14} L{cx - 10},{cy + 14}" '
            f'stroke="{ROJO}" stroke-width="3" stroke-linecap="round"/>'
            f'<circle cx="{cx - 12}" cy="{cy - 17}" r="5" fill="none" stroke="{ROJO}" stroke-width="2.4"/>'
            f'<circle cx="{cx + 12}" cy="{cy - 17}" r="5" fill="none" stroke="{ROJO}" stroke-width="2.4"/>')


def superficie_resaltada(ruta_pdb, grupos, delante, ancho=440, alto=330, margen=0.06):
    """Como superficie_complejo, pero las cadenas de `delante` (p. ej., ARN) se dibujan encima de la proteína."""
    atomos = []
    for cadenas, color in grupos:
        prot, _ = leer_pdb(ruta_pdb, cadenas, None)
        atomos += [(np.array(a[0]), RADIOS.get(a[1], 1.7), color, cadenas in delante) for a in prot]
    X = np.array([a[0] for a in atomos])
    centro = X.mean(0)
    Xr = np.array([a[0] for a in atomos if a[3]])
    _, _, ejes = np.linalg.svd(Xr - Xr.mean(0), full_matrices=False)
    ex = ejes[0]
    vista = ejes[2]
    ey = np.cross(vista, ex)
    sp = np.stack([(X - centro) @ ex, -((X - centro) @ ey), (X - centro) @ vista], axis=1)
    minx, maxx, miny, maxy = sp[:, 0].min() - 2, sp[:, 0].max() + 2, sp[:, 1].min() - 2, sp[:, 1].max() + 2
    escala = min(ancho * (1 - 2 * margen) / (maxx - minx), alto * (1 - 2 * margen) / (maxy - miny))
    ox, oy = ancho / 2 - escala * (minx + maxx) / 2, alto / 2 - escala * (miny + maxy) / 2
    zmin, zmax = sp[:, 2].min(), sp[:, 2].max()
    gradientes, circulos = {}, []
    orden = sorted(range(len(atomos)), key=lambda i: (atomos[i][3], sp[i, 2]))
    for i in orden:
        x, y, z = sp[i]
        nivel = round((z - zmin) / max(zmax - zmin, 1e-6) * 7) / 7
        base = atomos[i][2] if atomos[i][3] else _mezcla(atomos[i][2], "#1E3B33", 0.45 * (1 - nivel))
        if base not in gradientes:
            gid = f"r{len(gradientes)}"
            gradientes[base] = (f'<radialGradient id="{gid}" cx="0.35" cy="0.3" r="0.75">'
                                f'<stop offset="0" stop-color="{_mezcla(base, "#FFFFFF", 0.45)}"/>'
                                f'<stop offset="0.7" stop-color="{base}"/>'
                                f'<stop offset="1" stop-color="{_mezcla(base, "#000000", 0.35)}"/></radialGradient>', gid)
        op = "" if atomos[i][3] else ' fill-opacity="0.55"'
        circulos.append(f'<circle cx="{ox + escala * x:.1f}" cy="{oy + escala * y:.1f}" r="{escala * atomos[i][1]:.1f}" '
                        f'fill="url(#{gradientes[base][1]})"{op}/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" width="{ancho}" height="{alto}">'
            f'<defs>{"".join(g for g, _ in gradientes.values())}</defs>{"".join(circulos)}</svg>')


def caja(x, y, w, h, titulo, detalle, color):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#FFFFFF" stroke="{color}" '
         f'stroke-width="1.5"/>')
    s += texto(x + w / 2, y + 26, titulo, tam=15, peso="bold", anclaje="middle", color=color)
    if detalle:
        s += texto(x + w / 2, y + 46, detalle, tam=13, anclaje="middle", color=SUAVE)
    return s


# --- Lámina 1 ------------------------------------------------------------------------

def lamina_1():
    y = 330
    c = ilustracion("servier4-higado.svg", 40, 230, 190, 166)
    c += texto(135, 420, "Hígado", tam=16, peso="bold", anclaje="middle")
    c += texto(135, 440, "fabrica la TTR", tam=13, anclaje="middle", color=SUAVE)
    c += flecha([(236, y), (296, y)])
    c += arnm((310, 450), y, y, ondas=4)
    c += texto(380, y - 52, "ARNm de TTR", tam=15, peso="bold", anclaje="middle", color=MORADO_ARN)
    c += paso(380, y + 34, 1, radio=12, tam=13)
    c += flecha([(462, y), (528, y)])
    c += tetramero(590, y, s=26)
    c += texto(590, y - 70, ["TTR en sangre", "(tetrámero)"], tam=15, peso="bold", anclaje="middle", color=VERDE)
    c += paso(590, y + 52, 2, radio=12, tam=13)
    c += flecha([(640, y), (706, y)])
    c += monomero(740, y - 16, 14) + monomero(772, y + 14, 14, mal_plegado=True)
    c += texto(756, y - 70, ["se disocia y", "se pliega mal"], tam=15, peso="bold", anclaje="middle", color=ROJO)
    c += paso(756, y + 52, 3, radio=12, tam=13)
    c += flecha([(806, y), (866, y)])
    c += fibra(880, y - 14, n=4, largo=110)
    c += texto(935, y - 52, "fibras amiloides", tam=15, peso="bold", anclaje="middle", color=ROJO)
    c += paso(935, y + 52, 4, radio=12, tam=13)
    c += flecha([(1000, y - 10), (1090, y - 70)]) + flecha([(1000, y + 10), (1090, y + 80)])
    c += ilustracion("servier4-nervio.svg", 1100, 160, 260, 137)
    c += texto(1380, 222, ["Nervios:", "polineuropatía"], tam=15, peso="bold", color=COLOR["texto"])
    c += ilustracion("servier4-corazon.svg", 1130, 330, 150, 200)
    c += texto(1300, 420, ["Corazón:", "miocardiopatía"], tam=15, peso="bold", color=COLOR["texto"])
    c += paso(1080, y + 4, 5, radio=12, tam=13)
    # Fármacos
    c += etiqueta_farmaco(250, 470, "Vutrisiran, patisiran: ARN de interferencia", destacado=True, ancho=330)
    c += etiqueta_farmaco(250, 504, "Eplontersen: oligonucleótido antisentido", ancho=330)
    c += texto(415, 552, "↓ ARNm → ↓ TTR fabricada", tam=14, peso="bold", anclaje="middle", color=AZUL)
    c += etiqueta_farmaco(480, 594, "Tafamidis, acoramidis: estabilizan el tetrámero", ancho=360)
    c += texto(660, 640, "frenan la disociación (paso limitante)", tam=14, anclaje="middle", color=SUAVE)
    c += f'<line x1="415" y1="462" x2="380" y2="366" stroke="{AZUL}" stroke-width="1.6" stroke-dasharray="4 4"/>'
    c += f'<line x1="600" y1="588" x2="590" y2="378" stroke="{AZUL}" stroke-width="1.6" stroke-dasharray="4 4"/>'
    c += (f'<rect x="40" y="690" width="1520" height="122" rx="14" fill="#E3F0F8" stroke="{AZUL}" stroke-width="1.5"/>')
    c += texto(66, 726, "Idea clave", tam=18, peso="bold", color=AZUL)
    c += texto(66, 756, ["Vutrisiran no estabiliza ni repara la TTR: hace que el hígado fabrique mucha menos, tanto la variante",
                         "hereditaria como la normal (nativa). Con menos TTR en sangre, se forma menos amiloide."], tam=18,
               interlineado=1.4)
    return lamina(1, "Contexto", "De la TTR al amiloide, y dónde actúa cada fármaco",
                  "La amiloidosis por transtiretina (ATTR) daña nervios y corazón con fibras formadas a partir de la TTR.", c)


# --- Lámina 2 ------------------------------------------------------------------------

_TTR = superficie_corte(pdb_descargar("1ICT"), "ABCD", "T44", cadena_ligando="C", color_ligando="#E69F00",
                        colores_cadena={"A": "#7FC8A9", "B": "#9CB8D9", "C": "#7FC8A9", "D": "#9CB8D9"})[0]


def lamina_2():
    c = texto(40, 160, "A · En el hepatocito: del gen a la proteína", tam=21, peso="bold")
    c += ilustracion("emptycell-3d-1", 40, 176, 720, 560, ajustar="none")
    c += ilustracion("nucleus", 110, 330, 280, 200, ajustar="none")
    c += adn(150, 350, 392, region=(220, 300), etiqueta_region="gen TTR")
    c += arnm((300, 560), 400, 380, ondas=5)
    c += texto(560, 360, "ARNm", tam=14, peso="bold", color=MORADO_ARN)
    c += ribosoma(470, 382) + ribosoma(530, 378)
    c += monomero(580, 450, 12) + monomero(612, 450, 12)
    c += flecha([(630, 470), (640, 520)])
    c += tetramero(640, 560, s=20)
    c += flecha([(660, 590), (700, 660)])
    c += texto(610, 650, "secreción", tam=14, peso="bold", anclaje="middle", color=VERDE)
    c += leyenda_paso(60, 772, 1, "Transcripción", ["gen TTR → ARNm   "], fondo=True)
    c += leyenda_paso(300, 772, 2, "Traducción", ["ARNm → subunidad   "], fondo=True)
    c += leyenda_paso(540, 772, 3, "Ensamblaje y secreción", ["4 subunidades = tetrámero  "], fondo=True)
    c += f'<line x1="800" y1="140" x2="800" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    c += texto(830, 160, "B · En la sangre: transporte y amiloide", tam=21, peso="bold")
    c += como_imagen(_TTR, 830, 176, 330, 240)
    c += texto(995, 432, ["Tetrámero de TTR con tiroxina", "(naranja) en el canal · PDB 1ICT"], tam=13,
               anclaje="middle", color=SUAVE, cursiva=True)
    c += texto(1190, 200, "Funciones de la TTR", tam=16, peso="bold", color=VERDE)
    c += texto(1190, 226, ["• Transporta tiroxina (T4).",
                           "• Se une a RBP4, que lleva el",
                           "  retinol (vitamina A): así",
                           "  evita que se filtre en el riñón."], tam=15, interlineado=1.4)
    c += tetramero(880, 560, s=22)
    c += flecha([(916, 560), (976, 560)])
    c += monomero(1010, 540, 13) + monomero(1010, 580, 13)
    c += flecha([(1036, 560), (1096, 560)])
    c += monomero(1130, 560, 15, mal_plegado=True)
    c += flecha([(1160, 560), (1220, 560)])
    c += fibra(1236, 546, n=4, largo=100)
    c += leyenda_paso(830, 690, 1, "El tetrámero se disocia", ["es el paso limitante"])
    c += leyenda_paso(1080, 690, 2, "Monómero mal plegado", ["se agrega en fibras"])
    c += leyenda_paso(1320, 690, 3, "Depósito", ["en nervios y corazón"])
    c += texto(830, 790, ["ATTRh: variante hereditaria del gen TTR · ATTRwt (nativa): TTR sin variante."], tam=14,
               color=SUAVE, cursiva=True)
    return lamina(2, "Fisiología normal", "La TTR: del hígado a la sangre, y de ahí al amiloide",
                  "La TTR circulante se fabrica sobre todo en el hígado; el problema empieza cuando el tetrámero se separa.",
                  c, " PDB 1ICT (CC0). Reactome R-HSA-2404134.")


# --- Lámina 3 ------------------------------------------------------------------------

_ASGPR = superficie_corte(pdb_descargar("9G76"), "A", "A2G", color="#C9B3DD", color_ligando="#E69F00")[0]


def lamina_3():
    c = texto(40, 160, "La molécula", tam=21, peso="bold")
    c += vutrisiran(120, 220, w=190, etiquetas=True)
    c += texto(40, 296, ["ARN pequeño de interferencia (ARNpi) bicatenario,",
                         "estabilizado químicamente y unido a un ligando",
                         "con tres N-acetilgalactosaminas (GalNAc)."], tam=15, interlineado=1.4)
    c += como_imagen(_ASGPR, 40, 380, 300, 250)
    c += texto(190, 648, ["GalNAc (naranja) en el bolsillo", "del ASGPR · PDB 9G76"], tam=13, anclaje="middle",
               color=SUAVE, cursiva=True)
    c += texto(370, 430, ["ASGPR: receptor del", "hepatocito que reconoce", "la galactosa y la GalNAc", "de las glucoproteínas",
                          "y las internaliza."], tam=15, interlineado=1.4)
    c += texto(370, 580, ["La GalNAc es la «dirección»:", "lleva el ARNpi al hígado."], tam=15, peso="bold",
               color=NARANJA, interlineado=1.4)
    # Escena
    c += f'<line x1="800" y1="140" x2="800" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    c += texto(830, 160, "Del tejido subcutáneo al hepatocito", tam=21, peso="bold")
    c += ilustracion("servier-syringe.svg", 830, 180, 150, 50)
    c += paso(1000, 206, 1, radio=13, tam=14)
    c += texto(1022, 212, "Inyección subcutánea → sangre → hígado", tam=15)
    y_m = 340
    c += texto(1550, 300, "sangre", tam=14, cursiva=True, color=SUAVE, anclaje="end")
    c += membrana(820, 1560, y_m)
    c += texto(1550, 384, "hepatocito", tam=14, cursiva=True, color=SUAVE, anclaje="end")
    c += asgpr(900, y_m) + asgpr(1090, y_m)
    c += vutrisiran(930, 280, w=70)
    c += paso(1060, 266, 2, radio=13, tam=14)
    # Endocitosis
    c += (f'<path d="M1150,{y_m} C1150,{y_m + 60} 1250,{y_m + 60} 1250,{y_m}" fill="none" stroke="{COLOR["membrana"]}" '
          f'stroke-width="3"/>')
    c += vutrisiran(1188, y_m + 22, w=40)
    c += paso(1270, y_m + 40, 3, radio=13, tam=14)
    c += vesicula(1220, 500, 44)
    c += vutrisiran(1208, 492, w=34)
    c += texto(1220, 568, "endosoma", tam=13, anclaje="middle", color=SUAVE, cursiva=True)
    c += flecha([(1214, y_m + 50), (1218, 452)])
    c += flecha([(1266, 506), (1340, 540)])
    c += hebra(1350, 1420, 552, AZUL, abajo=False) + hebra(1346, 1412, 536, "#9AA9B3")
    c += paso(1450, 546, 4, radio=13, tam=14)
    c += flecha([(1180, 470), (1060, y_m + 26)], discontinua=True)
    c += texto(1050, 490, ["el receptor", "vuelve a la", "membrana"], tam=13, color=SUAVE, cursiva=True)
    c += leyenda_paso(830, 650, 1, "Inyección subcutánea", ["cada 3 meses"])
    c += leyenda_paso(1090, 650, 2, "GalNAc se une al ASGPR", ["en la cara sanguínea"])
    c += leyenda_paso(830, 750, 3, "Endocitosis", ["el complejo entra"])
    c += leyenda_paso(1090, 750, 4, "El ARNpi llega al citoplasma", ["listo para la lámina 4"])
    return lamina(3, "Mecanismo de acción (1)", "Cómo llega vutrisiran al hepatocito",
                  "El ligando GalNAc dirige el ARNpi al receptor ASGPR, que lo introduce en el hepatocito.",
                  c, " PDB 9G76 (CC0). NCI C152919.")


# --- Lámina 4 ------------------------------------------------------------------------

_AGO2 = superficie_resaltada(pdb_descargar("9CMP"), [("A", "#C9D3DC"), ("G", "#0072B2"), ("T", "#E69F00")],
                             delante=("G", "T"))


def lamina_4():
    c = texto(40, 160, "Ago2: la enzima que corta", tam=21, peso="bold")
    c += como_imagen(_AGO2, 40, 176, 440, 330)
    c += texto(260, 524, ["Ago2 humana (gris) con ARN guía (azul) y ARNm", "complementario (naranja) · PDB 9CMP"],
               tam=13, anclaje="middle", color=SUAVE, cursiva=True)
    c += texto(260, 562, "Secuencias de ejemplo, no las de vutrisiran.", tam=13, anclaje="middle", color=SUAVE,
               cursiva=True)
    c += texto(500, 220, ["Ago2 es el núcleo", "del complejo RISC.", "", "Con un ARN guía", "perfectamente",
                          "complementario, corta", "el ARNm diana."], tam=15, interlineado=1.4)
    c += (f'<rect x="40" y="610" width="730" height="110" rx="14" fill="#E3F0F8" stroke="{AZUL}" stroke-width="1.4"/>')
    c += texto(62, 642, "Interferencia por ARN (ARNi)", tam=17, peso="bold", color=AZUL)
    c += texto(62, 668, ["Mecanismo natural de la célula para silenciar genes. Vutrisiran",
                         "lo aprovecha: aporta la guía que apunta al ARNm de TTR."], tam=15, interlineado=1.4)
    # Escena en el citoplasma
    c += f'<line x1="800" y1="140" x2="800" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    c += texto(830, 160, "En el citoplasma del hepatocito", tam=21, peso="bold")
    c += hebra(840, 920, 230, AZUL, abajo=False) + hebra(836, 912, 214, "#9AA9B3")
    c += flecha([(930, 222), (990, 240)])
    c += ago2(1060, 250, w=110)
    c += texto(1060, 330, "RISC con la hebra guía", tam=13, anclaje="middle", color=SUAVE, cursiva=True)
    c += hebra(1130, 1190, 200, "#9AA9B3") + texto(1200, 205, "la pasajera se descarta", tam=13, color=SUAVE)
    c += paso(980, 200, 1, radio=13, tam=14)
    c += arnm((900, 1300), 430, 430, ondas=7)
    c += texto(900, 410, "ARNm de TTR", tam=14, peso="bold", color=MORADO_ARN)
    c += ago2(1100, 400, w=96)
    c += paso(1170, 360, 2, radio=13, tam=14)
    c += tijera(1100, 470)
    c += paso(1140, 490, 3, radio=13, tam=14)
    c += arnm((920, 1060), 560, 560, ondas=3) + arnm((1140, 1280), 560, 560, ondas=3)
    c += texto(1100, 590, "fragmentos degradados", tam=13, anclaje="middle", color=SUAVE, cursiva=True)
    c += flecha([(1200, 400), (1340, 300)], discontinua=True)
    c += texto(1350, 290, ["RISC queda libre", "y corta otro ARNm"], tam=13, color=AZUL, peso="bold")
    c += paso(1440, 330, 4, radio=13, tam=14)
    c += ribosoma(1420, 560) + bloqueo(1460, 560, r=12)
    c += texto(1440, 600, ["sin ARNm:", "↓ TTR"], tam=13, anclaje="middle", color=ROJO, peso="bold")
    c += leyenda_paso(830, 670, 1, "Carga en RISC", ["queda la hebra guía  "])
    c += leyenda_paso(1080, 670, 2, "Apareamiento", ["guía + ARNm de TTR    "])
    c += leyenda_paso(1320, 670, 3, "Corte", ["Ago2 corta el ARNm    "])
    c += leyenda_paso(830, 770, 4, "Ciclo catalítico", ["una guía, muchos cortes  "])
    c += texto(1080, 770, ["Resultado: TTR sérica ↓ 83–88 % con dosis", "cada 3 meses, variante y nativa por igual."],
               tam=15, peso="bold", color=VERDE, interlineado=1.4)
    return lamina(4, "Mecanismo de acción (2)", "Interferencia por ARN: el ARNm de TTR se corta",
                  "La hebra guía lleva a Ago2 (RISC) hasta el ARNm de TTR, que se corta y degrada: el hígado fabrica menos TTR.",
                  c, " PDB 9CMP (CC0). PMID 22233755.")


# --- Lámina 5 ------------------------------------------------------------------------

def lamina_5():
    x0, y0, w, h = 110, 200, 660, 420
    c = texto(40, 160, "Dos relojes distintos (esquema cualitativo)", tam=21, peso="bold")
    c += f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 + h}" stroke="{COLOR["linea"]}" stroke-width="2"/>'
    c += f'<line x1="{x0}" y1="{y0 + h}" x2="{x0 + w}" y2="{y0 + h}" stroke="{COLOR["linea"]}" stroke-width="2"/>'
    c += texto(x0 + w, y0 + h + 52, "tiempo →", tam=14, anclaje="end", color=SUAVE)
    for i, m in enumerate(("dosis", "3 meses", "6 meses")):
        xx = x0 + 20 + i * 300
        c += f'<line x1="{xx}" y1="{y0 + h}" x2="{xx}" y2="{y0 + h + 8}" stroke="{COLOR["linea"]}" stroke-width="2"/>'
        c += texto(xx, y0 + h + 26, m, tam=13, anclaje="middle", color=SUAVE)
        c += f'<path d="M{xx},{y0 + h} L{xx + 4},{y0 + 40} L{xx + 14},{y0 + h - 2}" fill="{AZUL}" fill-opacity="0.18" ' \
             f'stroke="{AZUL}" stroke-width="2.4"/>'
    c += texto(x0 + 44, y0 + 34, "vutrisiran en plasma: horas", tam=14, peso="bold", color=AZUL)
    pts = [(x0 + 20, y0 + 90)] + [(x0 + 20 + t, y0 + 90 + 230 * (1 - np.exp(-t / 45))) for t in range(10, 641, 10)]
    c += f'<polyline points="{" ".join(f"{a:.0f},{b:.0f}" for a, b in pts)}" fill="none" stroke="{VERDE}" ' \
         f'stroke-width="3.4"/>'
    c += texto(x0 + 40, y0 + 362, ["TTR en suero:", "se mantiene baja"], tam=14, peso="bold", color=VERDE)
    c += texto(x0 + w, y0 - 14, "Eje: TTR (verde). Picos azules sin escala.", tam=12.5, anclaje="end", color=SUAVE, cursiva=True)
    c += texto(x0 - 14, y0 + 96, "basal", tam=12.5, anclaje="end", color=SUAVE)
    c += texto(x0 - 14, y0 + 326, "−80 %", tam=12.5, anclaje="end", color=SUAVE)
    c += texto(40, 690, ["El efecto depende de la cantidad de vutrisiran en el hígado, no en el plasma:",
                         "por eso basta una inyección cada 3 meses."], tam=17, peso="bold", interlineado=1.4)
    c += f'<line x1="800" y1="140" x2="800" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    c += tarjeta(830, 150, 730, 300, AZUL, "El fármaco", [
        "• Absorción subcutánea rápida: tmáx ≈ 3 h.",
        "• Se distribuye sobre todo al hígado; unión a",
        "  proteínas > 80 %.",
        "• Nucleasas lo cortan en fragmentos; no lo",
        "  metaboliza el CYP450.",
        "• Semivida plasmática ≈ 5 h; 15–25 % sale",
        "  intacto por la orina. No se acumula en plasma."])
    c += tarjeta(830, 480, 730, 300, VERDE, "El efecto", [
        "• TTR sérica: −73 % a la semana 6, −83 % a los",
        "  9 meses y −88 % a los 18 meses (HELIOS-A).",
        "• Vitamina A sérica: −62 a −70 %, porque baja",
        "  su transportador (TTR–RBP4).",
        "• Sin interacciones previstas (ni CYP ni",
        "  transportadores); sin ajuste en insuficiencia",
        "  renal o hepática leve a moderada."])
    return lamina(5, "Farmacocinética", "Horas en el plasma, meses de efecto",
                  "Vutrisiran desaparece del plasma en un día, pero la TTR sigue baja durante todo el intervalo de 3 meses.",
                  c, " Curvas: esquema, no datos.")


# --- Lámina 6 ------------------------------------------------------------------------

def lamina_6():
    w, h = 752, 336
    x1, x2, y1, y2 = 40, 808, 136, 488
    c = tarjeta(x1, y1, w, h, VERDE, "Efecto terapéutico", [
        "• Polineuropatía (HELIOS-A): a los 18 meses, mNIS+7",
        "  28,5 puntos mejor que un placebo externo.",
        "• Miocardiopatía (HELIOS-B): −28 % de muerte y",
        "  eventos CV recurrentes frente a placebo; −35 % de",
        "  mortalidad total hasta el mes 42.",
        "• Iniciar pronto, para evitar que se acumule discapacidad."],
        ilustracion("servier4-corazon.svg", x1 + w - 120, y1 + 18, 90, 120))
    c += tarjeta(x2, y1, w, h, ROJO, "Error frecuente", [
        "«Vutrisiran edita el gen TTR.»",
        "Falso: no cambia el ADN. Destruye el ARNm de TTR,",
        "por eso hay que repetir la dosis cada 3 meses.",
        "Tampoco es un estabilizador como tafamidis: este",
        "protege la TTR que ya circula; vutrisiran reduce",
        "la que se fabrica.",
        "",
        "Para pensar: ¿por qué hay que dar vitamina A?"])
    c += tarjeta(x1, y2, w, h, AZUL, "Vitamina A y embarazo", [
        "• Al bajar la TTR baja el retinol: suplemento de",
        "  2 500–3 000 UI/día (no más).",
        "• Vigilar síntomas oculares (ceguera nocturna).",
        "• Excluir embarazo antes de iniciar y usar",
        "  anticoncepción: la vitamina A alta o baja es",
        "  teratogénica. Puede seguir baja > 12 meses tras",
        "  la última dosis."], "")
    c += tarjeta(x2, y2, w, h, COLOR["enzima_borde"], "Efectos adversos", [
        "• Frecuentes (1–10 %): reacción en la zona de",
        "  inyección (leve, transitoria), ALT elevada y",
        "  fosfatasa alcalina elevada.",
        "• HELIOS-B: ALT levemente elevada en 30 % frente a",
        "  24 % con placebo, asintomática.",
        "• Anticuerpos antifármaco: raros y transitorios.",
        "• Contraindicado si hubo anafilaxia."], "")
    return lamina(6, "Aplicación clínica", "Del mecanismo al paciente",
                  "Qué significa fabricar menos TTR: eficacia en nervio y corazón, vitamina A y seguridad.", c)


# --- Lámina 7 ------------------------------------------------------------------------

def lamina_7():
    x0, x1, y = 260, 1340, 300
    c = f'<line x1="{x0 - 120}" y1="{y}" x2="{x1 + 120}" y2="{y}" stroke="{COLOR["borde_panel"]}" stroke-width="6" ' \
        f'stroke-linecap="round"/>'
    for x, fecha, lineas in ((x0, "06/2022", ["Polineuropatía de la", "ATTR hereditaria (adultos)"]),
                             (x1, "03/2025", ["Miocardiopatía de la ATTR", "nativa o hereditaria (adultos)"])):
        c += f'<circle cx="{x}" cy="{y}" r="14" fill="#FFFFFF" stroke="{AZUL}" stroke-width="4"/>'
        c += texto(x, y - 70, fecha, tam=20, peso="bold", anclaje="middle", color=AZUL)
        c += (f'<rect x="{x - 44}" y="{y - 56}" width="88" height="24" rx="12" fill="{AZUL}" fill-opacity="0.16"/>')
        c += texto(x, y - 39, "UE: sí", tam=12.5, peso="bold", anclaje="middle", color=AZUL)
        c += texto(x, y + 44, lineas, tam=16, anclaje="middle", interlineado=1.35)
    c += texto(800, y - 16, "FDA", tam=15, peso="bold", anclaje="middle", color=SUAVE)
    c += tarjeta(40, 430, 740, 220, VERDE, "HELIOS-A (polineuropatía)", [
        "Abierto, frente a patisiran y un placebo externo (APOLLO);",
        "122 pacientes con vutrisiran, 22 variantes de TTR.",
        "mNIS+7 a 18 meses: −0,5 frente a +28,1 puntos.",
        "UE: solo estadio 1 o 2 de polineuropatía."])
    c += tarjeta(820, 430, 740, 220, VERDE, "HELIOS-B (miocardiopatía)", [
        "Doble ciego frente a placebo, 654 pacientes; 89 % ATTRwt,",
        "40 % ya tomaba tafamidis. Muerte y eventos CV:",
        "HR 0,72 (global) y 0,67 (sin tafamidis).",
        "FDA: para reducir mortalidad CV y hospitalizaciones."])
    c += tarjeta(40, 670, 1520, 150, AZUL, "Cómo leer esta lámina", [
        "La FDA y la EMA aprueban por separado; ambas incluyen hoy las dos indicaciones. En Costa Rica rige el registro",
        "sanitario nacional."])
    return lamina(7, "Indicaciones", "Indicaciones aprobadas: de los nervios al corazón",
                  "Aprobaciones de la FDA (Drugs@FDA, NDA 215515) y su presencia en la ficha europea (CIMA 4.1).",
                  c, " Drugs@FDA.")


# --- Lámina 8 -----------------------------------------------------------------------

def ficha(x, y, w, titulo, lineas, fuente, color):
    """Hallazgo con título, texto y fuente (país y año) en una franja de color."""
    alto = 46 + 21 * len(lineas) + 24
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{alto}" rx="10" fill="#FFFFFF" stroke="{COLOR["borde_panel"]}"/>'
         f'<rect x="{x}" y="{y}" width="6" height="{alto}" rx="3" fill="{color}"/>')
    s += texto(x + 22, y + 28, titulo, tam=16, peso="bold", color=color)
    s += texto(x + 22, y + 52, lineas, tam=15, interlineado=1.4)
    s += texto(x + 22, y + alto - 12, fuente, tam=12.5, color=SUAVE, cursiva=True)
    return s, alto + 10


def lamina_8():
    c = texto(40, 160, "¿Vale lo que cuesta? · Farmacoeconomía", tam=21, peso="bold", color=VERDE)
    y = 178
    for titulo, lineas, fuente in [
        ("Reino Unido (NICE): polineuropatía",
         ["Recomendado en estadio 1–2 con acuerdo comercial. Precio de lista:", "£95 862 por jeringa (≈ £383 449 al año)."],
         "NICE TA868, 2023"),
        ("Reino Unido (NICE): miocardiopatía",
         ["Puede usarse con acuerdo comercial; elegir la opción más barata", "entre vutrisiran y tafamidis."],
         "NICE TA1115, 2025"),
        ("Canadá (CDA-AMC): miocardiopatía",
         ["Reembolso con condiciones, entre ellas que su costo no supere", "al de tafamidis y que no se combinen."],
         "Recomendación de reembolso · PMID 42118893, 2026"),
    ]:
        f, alto = ficha(40, y, 740, titulo, lineas, fuente, VERDE)
        c += f
        y += alto
    c += f'<line x1="800" y1="140" x2="800" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    c += texto(830, 160, "¿Funciona igual fuera del ensayo? · Vida real", tam=21, peso="bold", color=AZUL)
    y = 178
    for titulo, lineas, fuente in [
        ("EE. UU.: reclamaciones de seguros, 111 pacientes",
         ["Seguimiento medio de 1,5 años: el 37 % fue hospitalizado. En 12", "meses, el 12 % murió y otro 12 % suspendió el tratamiento."],
         "Estudio retrospectivo (Optum) · PMID 42455256, 2026"),
        ("Metaanálisis: terapias dirigidas en miocardiopatía",
         ["Ensayos y estudios comparativos (5 203 pacientes): −39 % de", "mortalidad con el conjunto de tratamientos dirigidos."],
         "10 estudios · PMID 41311351, 2025"),
    ]:
        f, alto = ficha(830, y, 730, titulo, lineas, fuente, AZUL)
        c += f
        y += alto
    c += (f'<rect x="830" y="{y + 4}" width="730" height="160" rx="12" fill="#FFF4EE" stroke="{NARANJA}" '
          f'stroke-width="1.4"/>')
    c += texto(852, y + 34, "Cómo leer estos datos", tam=16, peso="bold", color=NARANJA)
    c += texto(852, y + 58, ["• Precio, umbral y comparador cambian con el país y el año.",
                             "• Los estudios observacionales muestran asociaciones, no causas.",
                             "• Latinoamérica: no se hallaron evaluaciones económicas ni",
                             "  estudios de vida real publicados en PubMed."], tam=15, interlineado=1.4)
    return lamina(8, "Valor y vida real", "Del ensayo a la práctica: valor y vida real",
                  "Qué dicen las evaluaciones económicas y los estudios en la práctica clínica, con prioridad para Latinoamérica.",
                  c)


LAMINAS = {1: lamina_1, 2: lamina_2, 3: lamina_3, 4: lamina_4, 5: lamina_5, 6: lamina_6, 7: lamina_7, 8: lamina_8}

if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or sorted(LAMINAS):
        salida = Path(__file__).with_name(f"lamina-{n}.svg")
        salida.write_text(LAMINAS[n](), encoding="utf-8")
        print(salida)
