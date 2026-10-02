"""Biblioteca visual de fisiopatología: células, membranas, órganos, flechas y rótulos.

Cada función devuelve un fragmento SVG (str). Las formas imitan estructuras celulares
reales (bicapa lipídica, envoltura nuclear con poros, organelos, núcleo esteroideo,
proteínas globulares), pero siempre con la misma forma y color para que el lector
reconozca cada elemento en todas las imágenes. Paleta basada en Okabe-Ito (apta para
daltonismo); cada elemento se distingue también por su forma.
"""
import math
import random
from html import escape

FUENTE = "Arial, 'Liberation Sans', Helvetica, sans-serif"

COLOR = {
    "texto": "#1F2A30",
    "texto_suave": "#56656D",
    "linea": "#3E4C55",
    "panel": "#FFFFFF",
    "borde_panel": "#D3DCE0",
    "fondo": "#F5F8F9",
    "membrana": "#5B6B73",
    "cabeza_lipido": "#A9BEC7",
    "citoplasma": "#F1F6F5",
    "nucleo": "#E7EDF7",
    "borde_nucleo": "#4A5A80",
    "ligando": "#E69F00",        # ligando endógeno (esteroide, neurotransmisor)
    "ligando_borde": "#9A6A00",
    "receptor": "#BFE6D8",       # receptor / diana
    "receptor_borde": "#00785A",
    "farmaco": "#0072B2",        # fármaco: rombo
    "farmaco_borde": "#004A75",
    "enzima": "#EBC6DA",
    "enzima_borde": "#9C4F7A",
    "bloqueo": "#D55E00",        # paso bloqueado: círculo con X
    "patogeno": "#F0E442",       # microorganismo dibujado (virus, bacteria, hongo, parásito) o su toxina
    "patogeno_borde": "#7A7000", # borde y texto del microorganismo (contraste 5:1 sobre blanco)
    "acento": "#FFF1C1",         # región destacada (p. ej., elemento de respuesta)
    "adn_1": "#5F6F86",
    "adn_2": "#A3B0C2",
    "organo": "#EEF2F4",
    "coactivador": "#DCD3F0",
    "coactivador_borde": "#6A55A0",
    "polimerasa": "#E6D8C6",
    "polimerasa_borde": "#7D6447",
    "ribosoma": "#7A858C",
    "ribosoma_borde": "#4E585E",
    "proteina": "#F3E3C8",
    "proteina_borde": "#9A6A00",
    "re": "#F3DCE6",
    "re_borde": "#B07A93",
    "golgi": "#F7E5C4",
    "golgi_borde": "#B08A4A",
    "mito": "#F6D6C8",
    "mito_borde": "#B5684A",
    "hsp": "#D9DEE1",
    "hsp_borde": "#7F8C93",
}

# Gradientes radiales (id -> (centro, borde)); dan volumen a las estructuras.
GRADIENTES = {
    "g_citoplasma": ("#F8FBFA", "#E2EEEB"),
    "g_nucleoplasma": ("#F3F6FC", "#D8E0EF"),
    "g_receptor": ("#E6F7F0", "#97D2BC"),
    "g_ligando": ("#FFD780", "#D99400"),
    "g_farmaco": ("#5AAEE0", "#0067A3"),
    "g_enzima": ("#F9E6EF", "#D6A0BE"),
    "g_hsp": ("#F2F4F5", "#B8C1C7"),
    "g_coact": ("#F1ECFA", "#C3B4E4"),
    "g_pol": ("#F5EEE4", "#CFB896"),
    "g_mito": ("#FCE9E0", "#EBB59D"),
    "g_prot": ("#FCF3E2", "#E9C88E"),
    "g_ribo": ("#A4AEB4", "#5F6A70"),
    "g_nucleolo": ("#C9D1E6", "#9DA9C9"),
    "g_organo": ("#FFFFFF", "#E6ECEF"),
}


def _f(v):
    return f"{v:.1f}"


def texto(x, y, contenido, tam=13, peso="normal", color=None, anclaje="start",
          cursiva=False, interlineado=1.3):
    """Texto con soporte para varias líneas (lista o '\\n')."""
    lineas = contenido if isinstance(contenido, list) else str(contenido).split("\n")
    estilo = ' font-style="italic"' if cursiva else ""
    partes = [
        f'<text x="{_f(x)}" y="{_f(y)}" font-family="{FUENTE}" font-size="{tam}" '
        f'font-weight="{peso}" fill="{color or COLOR["texto"]}" text-anchor="{anclaje}"{estilo}>'
    ]
    for i, linea in enumerate(lineas):
        dy = 0 if i == 0 else tam * interlineado
        partes.append(f'<tspan x="{_f(x)}" dy="{dy:.1f}">{escape(linea) or "&#160;"}</tspan>')
    partes.append("</text>")
    return "".join(partes)


def defs():
    """Marcadores de flecha y gradientes. Incluir una vez dentro de <svg>."""
    partes = ["<defs>"]
    for ident, color in (("flecha", COLOR["linea"]), ("flecha_bloqueada", COLOR["bloqueo"])):
        partes.append(f'<marker id="{ident}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
                      f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
                      f'fill="{color}"/></marker>')
    for ident, (centro, borde) in GRADIENTES.items():
        partes.append(f'<radialGradient id="{ident}" cx="0.4" cy="0.35" r="0.75">'
                      f'<stop offset="0" stop-color="{centro}"/><stop offset="1" stop-color="{borde}"/>'
                      f'</radialGradient>')
    partes.append("</defs>")
    return "".join(partes)


def panel(x, y, w, h, numero, titulo, subtitulo):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{COLOR["panel"]}" '
        f'stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
        + paso(x + 30, y + 34, numero, radio=15, tam=15)
        + texto(x + 54, y + 40, titulo, tam=20, peso="bold")
        + texto(x + 24, y + 66, subtitulo, tam=13, color=COLOR["texto_suave"])
    )


# --- Utilidades geométricas -------------------------------------------------

def _camino(puntos, cerrado=True):
    d = "M" + " L".join(f"{_f(x)},{_f(y)}" for x, y in puntos)
    return d + (" Z" if cerrado else "")


def _contorno_celula(cx, cy, a, b, semilla, n=720):
    """Superelipse con pequeñas irregularidades: contorno orgánico de una célula."""
    fase = semilla * 1.7
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        c, s = math.cos(t), math.sin(t)
        ex = 0.42
        f = 1 + 0.012 * math.sin(3 * t + fase) + 0.008 * math.sin(5 * t + 2 * fase)
        pts.append((cx + a * f * math.copysign(abs(c) ** ex, c), cy + b * f * math.copysign(abs(s) ** ex, s)))
    return pts


def _a_lo_largo(pts, centro, espaciado):
    """Puntos equiespaciados a lo largo de un contorno cerrado, con su normal hacia fuera."""
    cx, cy = centro
    resultado, acumulado, siguiente = [], 0.0, 0.0
    for i in range(len(pts)):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
        seg = math.hypot(x1 - x0, y1 - y0)
        while siguiente <= acumulado + seg and seg > 0:
            t = (siguiente - acumulado) / seg
            px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            nx, ny = -(y1 - y0) / seg, (x1 - x0) / seg
            if nx * (px - cx) + ny * (py - cy) < 0:
                nx, ny = -nx, -ny
            resultado.append((px, py, nx, ny))
            siguiente += espaciado
        acumulado += seg
    return resultado


# --- Célula y compartimentos -------------------------------------------------

def bicapa(pts, centro, espaciado=7.5, cabeza=2.6, grosor=6.0):
    """Bicapa de fosfolípidos: cabezas hidrofílicas (círculos) y colas (líneas)."""
    colas, cabezas = [], []
    for px, py, nx, ny in _a_lo_largo(pts, centro, espaciado):
        for signo in (1, -1):
            hx, hy = px + signo * nx * grosor, py + signo * ny * grosor
            tx0, ty0 = px + signo * nx * (grosor - cabeza), py + signo * ny * (grosor - cabeza)
            tx1, ty1 = px + signo * nx * 0.6, py + signo * ny * 0.6
            colas.append(f"M{_f(tx0)},{_f(ty0)} L{_f(tx1)},{_f(ty1)}")
            cabezas.append(f'<circle cx="{_f(hx)}" cy="{_f(hy)}" r="{cabeza}"/>')
    return (f'<path d="{" ".join(colas)}" stroke="{COLOR["membrana"]}" stroke-width="0.9" fill="none"/>'
            f'<g fill="{COLOR["cabeza_lipido"]}" stroke="{COLOR["membrana"]}" stroke-width="0.7">'
            + "".join(cabezas) + "</g>")


def celula(x, y, w, h, etiqueta="Célula", semilla=1):
    """Célula con citoplasma y membrana plasmática representada como bicapa lipídica."""
    cx, cy = x + w / 2, y + h / 2
    pts = _contorno_celula(cx, cy, w / 2 - 7, h / 2 - 7, semilla)
    return (
        f'<path d="{_camino(pts)}" fill="url(#g_citoplasma)"/>'
        + bicapa(pts, (cx, cy))
        + texto(x + w - 80, y + 60, etiqueta, tam=12, color=COLOR["texto_suave"], anclaje="end", cursiva=True)
    )


def nucleo(cx, cy, rx, ry, etiqueta="Núcleo", poros=(-90, -56.6, -123.4, -20, -160, 20, 160, 60, 120),
           nucleolo=None, semilla=3):
    """Envoltura nuclear (doble membrana con complejos de poro), cromatina y nucléolo.

    poros: ángulos en grados (0 = derecha, -90 = arriba). nucleolo: (dx, dy) desde el centro.
    """
    rnd = random.Random(semilla)
    partes = [
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#D4DCEB" stroke="{COLOR["borde_nucleo"]}" stroke-width="2"/>',
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx - 7}" ry="{ry - 7}" fill="url(#g_nucleoplasma)" '
        f'stroke="{COLOR["borde_nucleo"]}" stroke-width="1.6"/>',
    ]
    # Cromatina: hebras finas y tenues
    hebras = []
    for _ in range(70):
        ang, rad = rnd.uniform(0, 2 * math.pi), math.sqrt(rnd.uniform(0, 0.8))
        x0, y0 = cx + (rx - 20) * rad * math.cos(ang), cy + (ry - 20) * rad * math.sin(ang)
        d = f"M{_f(x0)},{_f(y0)}"
        for _ in range(3):
            d += f" q{_f(rnd.uniform(-8, 8))},{_f(rnd.uniform(-8, 8))} {_f(rnd.uniform(-12, 12))},{_f(rnd.uniform(-8, 8))}"
        hebras.append(d)
    partes.append(f'<path d="{" ".join(hebras)}" fill="none" stroke="#8E88B8" stroke-width="1.1" opacity="0.35"/>')
    if nucleolo:
        nx, ny = cx + nucleolo[0], cy + nucleolo[1]
        partes.append(f'<ellipse cx="{nx}" cy="{ny}" rx="30" ry="20" fill="url(#g_nucleolo)" stroke="#7D89AE" stroke-width="1"/>')
        granos = "".join(f'<circle cx="{_f(nx + rnd.uniform(-20, 20))}" cy="{_f(ny + rnd.uniform(-12, 12))}" r="1.6"/>'
                         for _ in range(18))
        partes.append(f'<g fill="#6F7BA0" opacity="0.6">{granos}</g>')
        partes.append(texto(nx, ny + 34, "Nucléolo", tam=10, anclaje="middle", color=COLOR["borde_nucleo"], cursiva=True))
    # Complejos de poro nuclear
    for grados in poros:
        t = math.radians(grados)
        px, py = cx + (rx - 3.5) * math.cos(t), cy + (ry - 3.5) * math.sin(t)
        nx_, ny_ = math.cos(t) / rx, math.sin(t) / ry
        giro = math.degrees(math.atan2(ny_, nx_)) + 90
        partes.append(
            f'<g transform="translate({_f(px)},{_f(py)}) rotate({_f(giro)})">'
            f'<rect x="-6" y="-7" width="12" height="14" fill="url(#g_nucleoplasma)"/>'
            f'<rect x="-9" y="-7" width="5" height="14" rx="2" fill="#8C9AC0" stroke="{COLOR["borde_nucleo"]}" stroke-width="0.8"/>'
            f'<rect x="4" y="-7" width="5" height="14" rx="2" fill="#8C9AC0" stroke="{COLOR["borde_nucleo"]}" stroke-width="0.8"/>'
            f'</g>')
    partes.append(texto(cx - rx * 0.62, cy - ry * 0.62, etiqueta, tam=12, color=COLOR["borde_nucleo"], cursiva=True))
    return "".join(partes)


def adn(x1, x2, y, region=None, etiqueta_region=None):
    """Doble hélice horizontal; `region` = (xa, xb) destaca un elemento de respuesta."""
    x1, x2 = round(x1), round(x2)  # el paso de 3 px y los pares de bases necesitan enteros
    partes = []
    if region:
        xa, xb = region
        partes.append(f'<rect x="{xa}" y="{y - 15}" width="{xb - xa}" height="30" rx="6" '
                      f'fill="{COLOR["acento"]}" stroke="{COLOR["ligando_borde"]}" '
                      f'stroke-width="1.2" stroke-dasharray="4 3"/>')
    hebras, pares = ([], []), []
    x = x1
    while x <= x2:
        fase = (x - x1) / 38 * 2 * math.pi
        y_a, y_b = y + 9 * math.sin(fase), y - 9 * math.sin(fase)
        hebras[0].append(f"{x},{_f(y_a)}")
        hebras[1].append(f"{x},{_f(y_b)}")
        if (x - x1) % 6 == 0:
            color = ("#E69F00", "#56B4E9", "#009E73", "#CC79A7")[((x - x1) // 6) % 4]
            pares.append(f'<line x1="{x}" y1="{_f(y_a)}" x2="{x}" y2="{_f(y)}" stroke="{color}" stroke-width="1.6" opacity="0.7"/>'
                         f'<line x1="{x}" y1="{_f(y)}" x2="{x}" y2="{_f(y_b)}" stroke="#A3B0C2" stroke-width="1.6" opacity="0.7"/>')
        x += 3
    partes += pares
    partes.append(f'<polyline points="{" ".join(hebras[1])}" fill="none" stroke="{COLOR["adn_2"]}" stroke-width="3.2" stroke-linecap="round"/>')
    partes.append(f'<polyline points="{" ".join(hebras[0])}" fill="none" stroke="{COLOR["adn_1"]}" stroke-width="3.2" stroke-linecap="round"/>')
    partes.append(texto(x1, y + 32, "ADN", tam=11, color=COLOR["texto_suave"], peso="bold"))
    if region and etiqueta_region:
        partes.append(texto((region[0] + region[1]) / 2, y + 32, etiqueta_region, tam=11,
                            color=COLOR["ligando_borde"], peso="bold", anclaje="middle"))
    return "".join(partes)


# --- Organelos ----------------------------------------------------------------

def reticulo_rugoso(x, y, w, sacos=3, separacion=13, semilla=5):
    """Retículo endoplásmico rugoso: cisternas onduladas con ribosomas adheridos."""
    rnd = random.Random(semilla)
    partes, ribos = [], []
    for k in range(sacos):
        y0 = y + k * separacion
        arriba, abajo = [], []
        for i in range(41):
            t = i / 40
            px = x + w * t + k * 6
            ond = 3 * math.sin(t * 2 * math.pi * 1.5 + k)
            arriba.append((px, y0 + ond - 3.5))
            abajo.append((px, y0 + ond + 3.5))
        contorno = arriba + abajo[::-1]
        partes.append(f'<path d="{_camino(contorno)}" fill="{COLOR["re"]}" stroke="{COLOR["re_borde"]}" '
                      f'stroke-width="1.2" stroke-linejoin="round"/>')
        for px, py in arriba[1:-1:3] + abajo[2:-1:3]:
            desplazamiento = -2.6 if (px, py) in arriba else 2.6
            ribos.append(f'<circle cx="{_f(px + rnd.uniform(-1, 1))}" cy="{_f(py + desplazamiento)}" r="2"/>')
    partes.append(f'<g fill="{COLOR["ribosoma"]}">{"".join(ribos)}</g>')
    return "".join(partes)


def golgi(cx, cy, ancho=70, cisternas=4):
    """Aparato de Golgi: cisternas curvas apiladas y vesículas en los extremos."""
    partes = []
    for k in range(cisternas):
        w = ancho - k * 9
        yk = cy + k * 9
        partes.append(
            f'<path d="M{_f(cx - w / 2)},{_f(yk)} Q{_f(cx)},{_f(yk - 14)} {_f(cx + w / 2)},{_f(yk)} '
            f'Q{_f(cx + w / 2 + 3)},{_f(yk + 4)} {_f(cx + w / 2 - 2)},{_f(yk + 5)} '
            f'Q{_f(cx)},{_f(yk - 8)} {_f(cx - w / 2 + 2)},{_f(yk + 5)} '
            f'Q{_f(cx - w / 2 - 3)},{_f(yk + 4)} {_f(cx - w / 2)},{_f(yk)} Z" '
            f'fill="{COLOR["golgi"]}" stroke="{COLOR["golgi_borde"]}" stroke-width="1.2"/>')
    for dx, dy in ((-ancho / 2 - 6, 6), (ancho / 2 + 6, 4), (ancho / 2 + 2, -10)):
        partes.append(vesicula(cx + dx, cy + dy, 4.5))
    return "".join(partes)


def vesicula(cx, cy, r=9, carga=0):
    """Vesícula con membrana y, opcionalmente, proteínas de carga (puntos)."""
    s = (f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{r}" fill="#FBF3E6" stroke="{COLOR["golgi_borde"]}" stroke-width="1.6"/>'
         f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{r - 2.2}" fill="none" stroke="{COLOR["golgi_borde"]}" stroke-width="0.6"/>')
    for i in range(carga):
        a = 2 * math.pi * i / carga
        s += f'<circle cx="{_f(cx + r * 0.4 * math.cos(a))}" cy="{_f(cy + r * 0.4 * math.sin(a))}" r="1.8" fill="{COLOR["proteina_borde"]}"/>'
    return s


def mitocondria(cx, cy, largo=58, ancho=26, angulo=0):
    """Mitocondria: membrana externa y crestas de la membrana interna."""
    l, a = largo / 2, ancho / 2
    crestas = "M" + " L".join(
        f"{_f(-l + 8 + i * (largo - 16) / 8)},{_f((a - 6) * (1 if i % 2 else -1))}" for i in range(9))
    return (
        f'<g transform="translate({_f(cx)},{_f(cy)}) rotate({angulo})">'
        f'<rect x="{-l}" y="{-a}" width="{largo}" height="{ancho}" rx="{a}" fill="url(#g_mito)" '
        f'stroke="{COLOR["mito_borde"]}" stroke-width="1.6"/>'
        f'<rect x="{-l + 4}" y="{-a + 4}" width="{largo - 8}" height="{ancho - 8}" rx="{a - 4}" fill="none" '
        f'stroke="{COLOR["mito_borde"]}" stroke-width="0.7" opacity="0.7"/>'
        f'<path d="{crestas}" fill="none" stroke="{COLOR["mito_borde"]}" stroke-width="1.3" stroke-linejoin="round"/>'
        f'</g>')


# --- Moléculas y proteínas ----------------------------------------------------

def _esteroide(cx, cy, lado):
    """Núcleo esteroideo (ciclopentanoperhidrofenantreno): tres hexágonos y un pentágono."""
    a, r3 = lado, math.sqrt(3)
    hexs = [(0, 0), (r3 * a, 0), (1.5 * r3 * a, -1.5 * a)]

    def hexagono(hx, hy):
        return [(hx + a * math.cos(math.radians(30 + 60 * k)), hy + a * math.sin(math.radians(30 + 60 * k))) for k in range(6)]

    poligonos = [hexagono(*h) for h in hexs]
    c = hexs[2]
    medio = (c[0] + r3 / 2 * a + 0.688 * a, c[1])
    R = 0.8507 * a
    poligonos.append([(medio[0] + R * math.cos(math.radians(g)), medio[1] + R * math.sin(math.radians(g)))
                      for g in (144, 216, 288, 0, 72)])
    xs = [x for p in poligonos for x, _ in p]
    ys = [y for p in poligonos for _, y in p]
    dx, dy = cx - (min(xs) + max(xs)) / 2, cy - (min(ys) + max(ys)) / 2
    return "".join(
        f'<path d="{_camino([(x + dx, y + dy) for x, y in p])}" fill="url(#g_ligando)" '
        f'stroke="{COLOR["ligando_borde"]}" stroke-width="1.4" stroke-linejoin="round"/>' for p in poligonos)


def ligando(cx, cy, etiqueta=None, r=16):
    """Andrógeno u otra hormona esteroidea: núcleo de cuatro anillos, con su sigla debajo."""
    s = _esteroide(cx, cy, r * 0.42)
    if etiqueta:
        s += texto(cx, cy + r * 0.7 + 11, etiqueta, tam=10.5, peso="bold", anclaje="middle", color=COLOR["ligando_borde"])
    return s


def farmaco(cx, cy, etiqueta="D", s=17):
    """Fármaco: rombo azul (símbolo convencional, no su estructura química)."""
    return (
        f'<path d="M{_f(cx)},{_f(cy - s)} L{_f(cx + s)},{_f(cy)} L{_f(cx)},{_f(cy + s)} L{_f(cx - s)},{_f(cy)} Z" '
        f'fill="url(#g_farmaco)" stroke="{COLOR["farmaco_borde"]}" stroke-width="2"/>'
        + (texto(cx, cy + 4, etiqueta, tam=11, peso="bold", anclaje="middle", color="#FFFFFF") if etiqueta else "")
    )


def receptor(cx, cy, etiqueta="RA", ocupante=None, chaperonas=False, escala=1.0):
    """Receptor como proteína globular con un bolsillo de unión al ligando en la parte superior.

    ocupante: None, ("ligando", ...) o ("farmaco", "D"). chaperonas: pinza de HSP90.
    """
    s = escala

    def p(x, y):
        return f"{_f(cx + x * s)},{_f(cy + y * s)}"

    partes = []
    if chaperonas:
        for lado in (-1, 1):
            partes.append(f'<ellipse cx="{_f(cx + lado * 52 * s)}" cy="{_f(cy + 2 * s)}" rx="{_f(11 * s)}" ry="{_f(24 * s)}" '
                          f'transform="rotate({lado * -16} {_f(cx + lado * 52 * s)} {_f(cy + 2 * s)})" '
                          f'fill="url(#g_hsp)" stroke="{COLOR["hsp_borde"]}" stroke-width="1.4"/>')
        partes.append(f'<ellipse cx="{_f(cx)}" cy="{_f(cy + 30 * s)}" rx="{_f(46 * s)}" ry="{_f(8 * s)}" '
                      f'fill="url(#g_hsp)" stroke="{COLOR["hsp_borde"]}" stroke-width="1.4"/>')
        partes.append(texto(cx, cy + 33 * s, "HSP90", tam=8.5, anclaje="middle", color=COLOR["texto_suave"], peso="bold"))
    d = (f"M{p(-38, -6)} C{p(-42, -20)} {p(-28, -26)} {p(-14, -22)} Q{p(-14, -2)} {p(0, -2)} "
         f"Q{p(14, -2)} {p(14, -22)} C{p(28, -26)} {p(44, -18)} {p(40, -4)} C{p(46, 8)} {p(38, 24)} {p(22, 22)} "
         f"C{p(10, 28)} {p(-10, 28)} {p(-22, 22)} C{p(-40, 24)} {p(-46, 8)} {p(-38, -6)} Z")
    partes.append(f'<path d="{d}" fill="url(#g_receptor)" stroke="{COLOR["receptor_borde"]}" stroke-width="2"/>')
    # Surcos que sugieren plegamiento en dominios
    partes.append(f'<path d="M{p(-26, 4)} Q{p(-18, 10)} {p(-24, 18)} M{p(24, 2)} Q{p(30, 10)} {p(22, 16)}" '
                  f'fill="none" stroke="{COLOR["receptor_borde"]}" stroke-width="1" opacity="0.5"/>')
    if s >= 0.6 and etiqueta:
        partes.append(texto(cx, cy + 15 * s, etiqueta, tam=12 * s, peso="bold", anclaje="middle", color=COLOR["receptor_borde"]))
    if ocupante:
        tipo, nombre = ocupante
        oy = cy - 12 * s
        partes.append(ligando(cx, oy, None, r=max(16 * s, 12)) if tipo == "ligando" else farmaco(cx, oy, nombre, s=14 * s))
    return "".join(partes)


def enzima(cx, cy, etiqueta, r=20, membrana=False):
    """Enzima globular con sitio activo; `membrana` la muestra anclada a un segmento de retículo."""
    s = ""
    if membrana:
        s += (f'<path d="M{_f(cx - 2.2 * r)},{_f(cy + r * 0.55)} Q{_f(cx)},{_f(cy + r * 0.85)} {_f(cx + 2.2 * r)},{_f(cy + r * 0.55)} '
              f'L{_f(cx + 2.2 * r)},{_f(cy + r * 0.55 + 8)} Q{_f(cx)},{_f(cy + r * 0.85 + 8)} {_f(cx - 2.2 * r)},{_f(cy + r * 0.55 + 8)} Z" '
              f'fill="{COLOR["re"]}" stroke="{COLOR["re_borde"]}" stroke-width="1.2"/>')
    a = math.radians(32)
    x1, y1 = cx + r * math.cos(a), cy - r * math.sin(a)
    x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a)
    s += (f'<path d="M{_f(cx + 4)},{_f(cy)} L{_f(x1)},{_f(y1)} A{r},{r} 0 1 0 {_f(x2)},{_f(y2)} Z" '
          f'fill="url(#g_enzima)" stroke="{COLOR["enzima_borde"]}" stroke-width="2" stroke-linejoin="round"/>')
    if etiqueta:
        s += texto(cx, cy + r + (26 if membrana else 16), etiqueta, tam=11, anclaje="middle", color=COLOR["enzima_borde"], peso="bold")
    return s


def flecha(puntos, bloqueada=False, discontinua=False):
    """Flecha por una lista de puntos [(x, y), ...]."""
    color = COLOR["bloqueo"] if bloqueada else COLOR["linea"]
    marcador = "flecha_bloqueada" if bloqueada else "flecha"
    guion = ' stroke-dasharray="6 5"' if (discontinua or bloqueada) else ""
    pts = " ".join(f"{_f(x)},{_f(y)}" for x, y in puntos)
    return (f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.2"{guion} '
            f'marker-end="url(#{marcador})"/>')


def bloqueo(cx, cy, r=13):
    """Paso bloqueado: círculo con X."""
    k = r * 0.5
    return (
        f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{r}" fill="#FFFFFF" stroke="{COLOR["bloqueo"]}" stroke-width="2.6"/>'
        f'<path d="M{_f(cx - k)},{_f(cy - k)} L{_f(cx + k)},{_f(cy + k)} M{_f(cx + k)},{_f(cy - k)} L{_f(cx - k)},{_f(cy + k)}" '
        f'stroke="{COLOR["bloqueo"]}" stroke-width="2.8" stroke-linecap="round"/>'
    )


def paso(cx, cy, numero, radio=11, tam=12):
    """Número de paso dentro de un círculo oscuro."""
    return (
        f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{radio}" fill="{COLOR["texto"]}"/>'
        + texto(cx, cy + tam * 0.36, str(numero), tam=tam, peso="bold", anclaje="middle", color="#FFFFFF")
    )


def recuadro(x, y, w, h, titulo, lineas, color_borde, tam=13):
    """Caja de texto con barra lateral de color."""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#FFFFFF" '
        f'stroke="{COLOR["borde_panel"]}" stroke-width="1.2"/>'
        f'<rect x="{x}" y="{y}" width="6" height="{h}" rx="3" fill="{color_borde}"/>'
        + texto(x + 20, y + 26, titulo, tam=14, peso="bold", color=color_borde)
        + texto(x + 20, y + 50, lineas, tam=tam, interlineado=1.4)
    )


def atenuado(contenido, opacidad=0.3):
    """Elementos que ya no ocurren (p. ej., bajo el efecto del fármaco)."""
    return f'<g opacity="{opacidad}">{contenido}</g>'


# --- Órganos (esquema del eje hormonal) --------------------------------------

def icono_organo(tipo, cx, cy):
    """Iconos anatómicos simplificados para esquemas de ejes hormonales."""
    if tipo == "cerebro":
        contorno = (f"M{cx - 22},{cy + 6} C{cx - 30},{cy - 6} {cx - 20},{cy - 20} {cx - 8},{cy - 18} "
                    f"C{cx - 2},{cy - 26} {cx + 14},{cy - 24} {cx + 18},{cy - 14} C{cx + 30},{cy - 10} {cx + 28},{cy + 8} "
                    f"{cx + 18},{cy + 10} C{cx + 10},{cy + 16} {cx - 2},{cy + 12} {cx - 6},{cy + 10} "
                    f"C{cx - 12},{cy + 14} {cx - 20},{cy + 12} {cx - 22},{cy + 6} Z")
        surcos = (f"M{cx - 14},{cy - 10} q6,6 0,12 M{cx - 2},{cy - 16} q-4,8 4,14 M{cx + 10},{cy - 14} q6,6 0,14 "
                  f"M{cx + 20},{cy - 2} q-6,2 -4,8")
        return (f'<path d="{contorno}" fill="#F3D9DE" stroke="#A0606E" stroke-width="1.5"/>'
                f'<path d="{surcos}" fill="none" stroke="#A0606E" stroke-width="1.1"/>'
                f'<circle cx="{cx - 2}" cy="{cy + 8}" r="4" fill="{COLOR["ligando"]}" stroke="{COLOR["ligando_borde"]}"/>')
    if tipo == "hipofisis":
        return (f'<path d="M{cx - 20},{cy - 14} Q{cx},{cy - 22} {cx + 20},{cy - 14}" fill="none" stroke="#A0606E" stroke-width="1.5"/>'
                f'<line x1="{cx}" y1="{cy - 18}" x2="{cx}" y2="{cy - 4}" stroke="#A0606E" stroke-width="2.5"/>'
                f'<ellipse cx="{cx - 4}" cy="{cy + 6}" rx="9" ry="9" fill="#F3D9DE" stroke="#A0606E" stroke-width="1.5"/>'
                f'<ellipse cx="{cx + 7}" cy="{cy + 6}" rx="6" ry="7" fill="#EAC3CB" stroke="#A0606E" stroke-width="1.5"/>')
    if tipo == "testiculo":
        return (f'<path d="M{cx},{cy - 24} L{cx},{cy - 14}" stroke="#A0606E" stroke-width="2.5"/>'
                f'<ellipse cx="{cx - 2}" cy="{cy + 2}" rx="11" ry="15" fill="#F3D9DE" stroke="#A0606E" stroke-width="1.5"/>'
                f'<path d="M{cx + 6},{cy - 14} C{cx + 18},{cy - 10} {cx + 16},{cy + 14} {cx + 6},{cy + 16}" fill="none" '
                f'stroke="#A0606E" stroke-width="4" stroke-linecap="round" opacity="0.7"/>')
    if tipo == "suprarrenal":
        return (f'<path d="M{cx - 6},{cy - 10} C{cx - 20},{cy - 10} {cx - 20},{cy + 22} {cx - 4},{cy + 22} '
                f'C{cx + 8},{cy + 22} {cx + 10},{cy + 12} {cx + 4},{cy + 6} C{cx + 10},{cy} {cx + 8},{cy - 10} {cx - 6},{cy - 10} Z" '
                f'fill="#E7B3A8" stroke="#9A5A4E" stroke-width="1.5"/>'
                f'<path d="M{cx - 14},{cy - 10} L{cx - 4},{cy - 24} L{cx + 6},{cy - 10} Z" fill="#F6D66F" stroke="#A88618" stroke-width="1.5" stroke-linejoin="round"/>')
    if tipo == "vaso":
        s = (f'<path d="M{cx - 24},{cy - 11} L{cx + 24},{cy - 11} M{cx - 24},{cy + 11} L{cx + 24},{cy + 11}" '
             f'stroke="#B4534B" stroke-width="3"/>'
             f'<rect x="{cx - 24}" y="{cy - 9.5}" width="48" height="19" fill="#FBE4E1"/>')
        for dx, dy, g in ((-14, -2, 20), (0, 3, -15), (14, -1, 10)):
            s += (f'<ellipse cx="{cx + dx}" cy="{cy + dy}" rx="6" ry="4.5" transform="rotate({g} {cx + dx} {cy + dy})" '
                  f'fill="#D9665C" stroke="#9E3A32" stroke-width="1"/>')
        return s
    if tipo == "nucleo":
        return (f'<ellipse cx="{cx}" cy="{cy}" rx="22" ry="16" fill="url(#g_nucleoplasma)" stroke="{COLOR["borde_nucleo"]}" stroke-width="1.6"/>'
                f'<path d="M{cx - 14},{cy} q4,-6 8,0 t8,0 t8,0" fill="none" stroke="{COLOR["adn_1"]}" stroke-width="2"/>')
    return ""


def organo(x, y, w, h, titulo, subtitulo=None, icono=None):
    """Órgano o compartimento del organismo en un esquema de eje hormonal."""
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="url(#g_organo)" '
         f'stroke="{COLOR["membrana"]}" stroke-width="1.4"/>')
    tx = x + w / 2
    if icono:
        s += icono_organo(icono, x + 34, y + h / 2)
        tx = x + 62 + (w - 62) / 2
    ty = y + (h / 2 + 5 if not subtitulo else h / 2 - 4)
    s += texto(tx, ty, titulo, tam=14, peso="bold", anclaje="middle")
    if subtitulo:
        s += texto(tx, ty + 18, subtitulo, tam=11, anclaje="middle", color=COLOR["texto_suave"])
    return s


def etiqueta_farmaco(x, y, contenido, destacado=False, ancho=None):
    """Etiqueta de un fármaco que actúa en ese punto; rombo lleno = fármaco protagonista."""
    w = ancho or (len(contenido) * 6.4 + 40)
    relleno = COLOR["farmaco"] if destacado else "#FFFFFF"
    color_texto = "#FFFFFF" if destacado else COLOR["farmaco_borde"]
    rombo_relleno = "#FFFFFF" if destacado else "none"
    rombo_borde = "#FFFFFF" if destacado else COLOR["farmaco"]
    cx, cy = x + 16, y + 13
    return (
        f'<rect x="{x}" y="{y}" width="{w:.0f}" height="26" rx="13" fill="{relleno}" '
        f'stroke="{COLOR["farmaco"]}" stroke-width="1.6"/>'
        f'<path d="M{cx},{cy - 7} L{cx + 7},{cy} L{cx},{cy + 7} L{cx - 7},{cy} Z" fill="{rombo_relleno}" '
        f'stroke="{rombo_borde}" stroke-width="1.6"/>'
        + texto(x + 30, y + 17.5, contenido, tam=12, peso="bold", color=color_texto)
    )


def coactivador(cx, cy, etiqueta="Coact."):
    return (
        f'<path d="M{cx - 22},{cy} C{cx - 24},{cy - 20} {cx - 2},{cy - 22} {cx + 4},{cy - 14} '
        f'C{cx + 20},{cy - 22} {cx + 28},{cy - 2} {cx + 20},{cy + 8} C{cx + 14},{cy + 20} {cx - 18},{cy + 18} '
        f'{cx - 22},{cy} Z" fill="url(#g_coact)" stroke="{COLOR["coactivador_borde"]}" stroke-width="1.8"/>'
        + (texto(cx, cy + 4, etiqueta, tam=9.5, peso="bold", anclaje="middle", color=COLOR["coactivador_borde"]) if etiqueta else "")
    )


def polimerasa(cx, cy):
    """ARN polimerasa II: complejo grande con una hendidura donde pasa el ADN."""
    return (
        f'<path d="M{cx - 34},{cy + 14} C{cx - 40},{cy - 18} {cx - 16},{cy - 34} {cx + 6},{cy - 30} '
        f'C{cx + 34},{cy - 28} {cx + 42},{cy - 4} {cx + 34},{cy + 14} L{cx + 12},{cy + 14} '
        f'Q{cx},{cy + 4} {cx - 12},{cy + 14} Z" fill="url(#g_pol)" '
        f'stroke="{COLOR["polimerasa_borde"]}" stroke-width="1.8"/>'
        + texto(cx, cy - 10, ["ARN", "pol II"], tam=9.5, peso="bold", anclaje="middle",
                color=COLOR["polimerasa_borde"], interlineado=1.15)
    )


def arnm(puntos_x, y0, y1, ondas=5):
    """ARNm: una sola hebra ondulada de (x0, y0) a (x1, y1)."""
    x0, x1 = puntos_x
    pts = []
    n = 40
    for i in range(n + 1):
        t = i / n
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        largo = math.hypot(x1 - x0, y1 - y0) or 1
        nx, ny = -(y1 - y0) / largo, (x1 - x0) / largo
        off = 5 * math.sin(t * ondas * 2 * math.pi)
        pts.append(f"{_f(x + nx * off)},{_f(y + ny * off)}")
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="#7D4E9C" stroke-width="2.4" stroke-linecap="round"/>'


def ribosoma(cx, cy):
    """Ribosoma: subunidad mayor y menor."""
    return (
        f'<ellipse cx="{cx}" cy="{cy - 6}" rx="13" ry="9" fill="url(#g_ribo)" stroke="{COLOR["ribosoma_borde"]}" stroke-width="1.2"/>'
        f'<ellipse cx="{cx}" cy="{cy + 6}" rx="9" ry="5.5" fill="url(#g_ribo)" stroke="{COLOR["ribosoma_borde"]}" stroke-width="1.2"/>'
    )


def proteina(cx, cy, etiqueta, r=14):
    """Proteína producida: glóbulo irregular."""
    return (
        f'<path d="M{cx - r},{cy} C{cx - r},{cy - r} {cx - 2},{cy - r - 4} {cx + 3},{cy - r + 2} '
        f'C{cx + r + 4},{cy - r} {cx + r + 2},{cy + 4} {cx + r - 2},{cy + 6} C{cx + r - 4},{cy + r + 2} '
        f'{cx - r + 2},{cy + r} {cx - r},{cy} Z" fill="url(#g_prot)" '
        f'stroke="{COLOR["proteina_borde"]}" stroke-width="1.6"/>'
        + (texto(cx, cy + 3.5, etiqueta, tam=9.5, peso="bold", anclaje="middle", color="#5A3E00") if etiqueta else "")
    )


def dominios(x, y, w, segmentos, alto=34):
    """Barra de dominios de una proteína. segmentos = [(fraccion, sigla, color, destacado), ...]."""
    partes, cx = [], x
    for fraccion, sigla, color, destacado in segmentos:
        ancho = w * fraccion
        borde = COLOR["farmaco"] if destacado else COLOR["receptor_borde"]
        grosor = 3 if destacado else 1.5
        partes.append(f'<rect x="{_f(cx)}" y="{y}" width="{_f(ancho)}" height="{alto}" fill="{color}" '
                      f'stroke="{borde}" stroke-width="{grosor}"/>')
        if ancho > 26:
            partes.append(texto(cx + ancho / 2, y + alto / 2 + 4.5, sigla, tam=12, peso="bold", anclaje="middle",
                                color=COLOR["receptor_borde"]))
        cx += ancho
    return "".join(partes)


def svg(ancho, alto, contenido, titulo, descripcion):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" width="{ancho}" height="{alto}" '
        f'role="img" aria-labelledby="titulo desc">'
        f'<title id="titulo">{escape(titulo)}</title><desc id="desc">{escape(descripcion)}</desc>'
        + defs()
        + f'<rect width="{ancho}" height="{alto}" fill="{COLOR["fondo"]}"/>'
        + contenido
        + "</svg>"
    )
