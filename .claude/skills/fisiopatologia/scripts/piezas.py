"""Piezas comunes de las láminas de una enfermedad: marco de la lámina, pasos, tarjetas, membranas y fichas.

Uso desde ejemplos/<enfermedad>/laminas.py:
    from piezas import Lamina, leyenda_paso, tarjeta, ficha, membrana, caja, organo_ilustrado, curva_fcfd
    L = Lamina("DIABETES TIPO 2", fuentes="Fuentes: ...")
    svg = L.dibujar(1, "Contexto", "Título", "Subtítulo", contenido, total=9)
"""
import math

from componentes import COLOR, paso, svg, texto
from recursos import ilustracion

ANCHO, ALTO = 1600, 900
SUAVE = COLOR["texto_suave"]
VERDE, AZUL, ROJO, NARANJA = COLOR["receptor_borde"], COLOR["farmaco"], COLOR["bloqueo"], COLOR["ligando_borde"]
LILA = COLOR["coactivador_borde"]


class Lamina:
    """Marco común: franja superior, cabecera «ENFERMEDAD · LÁMINA N DE TOTAL · TEMA», título, pie y aviso."""

    def __init__(self, enfermedad, fuentes, aviso="Esquema simplificado y sin escala · Prototipo pendiente de revisión clínica"):
        self.enfermedad, self.fuentes, self.aviso = enfermedad, fuentes, aviso

    def dibujar(self, numero, etiqueta, titulo, subtitulo, contenido, total, extra=""):
        c = (f'<rect x="0" y="0" width="{ANCHO}" height="6" fill="{AZUL}"/>'
             + texto(40, 38, f"{self.enfermedad} · LÁMINA {numero} DE {total} · {etiqueta.upper()}", tam=14,
                     peso="bold", color=AZUL)
             + texto(40, 76, titulo, tam=32, peso="bold") + texto(40, 104, subtitulo, tam=17, color=SUAVE)
             + contenido + texto(40, ALTO - 34, self.fuentes + extra, tam=12.5, color=SUAVE)
             + texto(40, ALTO - 14, self.aviso, tam=12.5, color=ROJO, peso="bold"))
        return svg(ANCHO, ALTO, c, f"{self.enfermedad.capitalize()}, lámina {numero}: {titulo}", subtitulo)


def leyenda_paso(x, y, n, titulo, detalle=(), fondo=True):
    """Número de paso, título en negrita y detalle opcional, sobre un fondo claro legible."""
    s = ""
    if fondo:
        ancho = 52 + max([len(titulo) * 9.6] + [len(l) * 8.2 for l in detalle])
        alto = 34 + 19.5 * len(detalle)
        s += (f'<rect x="{x - 8}" y="{y - 26}" width="{ancho:.0f}" height="{alto:.0f}" rx="10" fill="#FFFFFF" '
              f'fill-opacity="0.9" stroke="{COLOR["borde_panel"]}" stroke-width="1"/>')
    s += paso(x + 14, y - 6, n, radio=14, tam=15) + texto(x + 36, y, titulo, tam=17, peso="bold")
    if detalle:
        s += texto(x + 36, y + 22, list(detalle), tam=15, color=SUAVE, interlineado=1.3)
    return s


def tarjeta(x, y, w, h, color, titulo, lineas, icono="", tam=17):
    """Tarjeta con barra de color, título y líneas de texto."""
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#FFFFFF" stroke="{COLOR["borde_panel"]}" '
         f'stroke-width="1.4"/><rect x="{x}" y="{y}" width="8" height="{h}" rx="4" fill="{color}"/>')
    s += icono
    s += texto(x + 32, y + 46, titulo, tam=22, peso="bold", color=color)
    s += texto(x + 32, y + 84, lineas, tam=tam, interlineado=1.45)
    return s


def ficha(x, y, w, titulo, lineas, fuente, color):
    """Hallazgo con título, texto y fuente en una franja de color. Devuelve (svg, alto + margen)."""
    alto = 46 + 21 * len(lineas) + 24
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{alto}" rx="10" fill="#FFFFFF" stroke="{COLOR["borde_panel"]}"/>'
         f'<rect x="{x}" y="{y}" width="6" height="{alto}" rx="3" fill="{color}"/>')
    s += texto(x + 22, y + 28, titulo, tam=16, peso="bold", color=color)
    s += texto(x + 22, y + 52, lineas, tam=15, interlineado=1.4)
    s += texto(x + 22, y + alto - 12, fuente, tam=12.5, color=SUAVE, cursiva=True)
    return s, alto + 10


def caja(x, y, w, h, titulo, detalle, color, fondo="#FFFFFF"):
    """Recuadro con título centrado y detalle opcional."""
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fondo}" stroke="{color}" '
         f'stroke-width="1.5"/>')
    s += texto(x + w / 2, y + 26, titulo, tam=15, peso="bold", anclaje="middle", color=color)
    if detalle:
        s += texto(x + w / 2, y + 46, detalle, tam=13, anclaje="middle", color=SUAVE)
    return s


def membrana(x1, x2, y, paso_x=9):
    """Bicapa lipídica recta (cabezas y colas)."""
    s = f'<rect x="{x1}" y="{y - 12}" width="{x2 - x1}" height="24" fill="#FFF6D6"/>'
    colas = " ".join(f"M{x},{y - 8} L{x},{y - 2} M{x},{y + 2} L{x},{y + 8}" for x in range(x1, x2, paso_x))
    s += f'<path d="{colas}" stroke="{COLOR["membrana"]}" stroke-width="1"/>'
    s += "".join(f'<circle cx="{x}" cy="{y - 11}" r="3.6" fill="#F3D27A" stroke="#B08A2E" stroke-width="0.7"/>'
                 f'<circle cx="{x}" cy="{y + 11}" r="3.6" fill="#F3D27A" stroke="#B08A2E" stroke-width="0.7"/>'
                 for x in range(x1, x2, paso_x))
    return s


def organo_ilustrado(nombre_svg, x, y, w, h, titulo, detalle=None, color=None):
    """Ilustración de un órgano con su rótulo debajo."""
    s = ilustracion(nombre_svg, x, y, w, h)
    s += texto(x + w / 2, y + h + 20, titulo, tam=15, peso="bold", anclaje="middle", color=color or COLOR["texto"])
    if detalle:
        s += texto(x + w / 2, y + h + 40, detalle, tam=13, anclaje="middle", color=SUAVE)
    return s


def curva_fcfd(x, y, w, h, indice=None, dosis=3, cmi=0.32, titulo=None):
    """Curva cualitativa concentración-tiempo de un antimicrobiano con dosis intermitentes y la CMI.

    indice: "tiempo" (T > CMI), "cmax" (Cmáx/CMI), "abc" (ABC/CMI) o None (los tres a la vez).
    dosis: número de dosis en el intervalo dibujado. cmi: altura de la CMI como fracción de la Cmáx.
    La curva no tiene datos: lleva el rótulo «Esquema cualitativo: curva sin escala».
    Tamaño recomendado: al menos 600 × 320 px (por debajo de 300 de alto, el eje se queda corto para los rótulos).
    """
    ox, oy, aw, ah = x + 34, y + h - 50, w - 54, h - 96          # origen y tamaño de los ejes
    tau, subida, k = 1 / dosis, 0.035, 9.0                        # intervalo, infusión y eliminación (relativos)

    def conc(t):
        c = 0.0
        for i in range(dosis):
            d = t - i * tau
            if 0 <= d < subida:
                c += 0.88 * d / subida * math.exp(-k * d)
            elif d >= subida:
                c += 0.88 * math.exp(-k * d)
        return c

    ts = [i / 400 for i in range(401)]
    cs = [conc(t) for t in ts]
    escala = max(cs)
    px = lambda t: ox + t * aw                                    # noqa: E731
    py = lambda c: oy - c / escala * ah * 0.92                    # noqa: E731
    puntos = " ".join(f"{px(t):.1f},{py(c):.1f}" for t, c in zip(ts, cs))
    ycmi = py(cmi * escala)
    azul, borde_cmi = COLOR["farmaco"], COLOR["patogeno_borde"]
    s = ""
    if indice in ("abc", None):                                   # área bajo la curva
        s += (f'<polygon points="{px(0):.1f},{oy:.1f} {puntos} {px(1):.1f},{oy:.1f}" fill="{azul}" '
              f'fill-opacity="0.13"/>')
    if indice in ("tiempo", None):                                # tramos con concentración por encima de la CMI
        tramos, inicio = [], None
        for t, c in zip(ts, cs):
            if c > cmi * escala and inicio is None:
                inicio = t
            elif c <= cmi * escala and inicio is not None:
                tramos.append((inicio, t))
                inicio = None
        if inicio is not None:
            tramos.append((inicio, 1.0))
        for a, b in tramos:
            s += (f'<rect x="{px(a):.1f}" y="{oy + 8:.1f}" width="{px(b) - px(a):.1f}" height="10" rx="3" '
                  f'fill="{COLOR["receptor_borde"]}"/>')
        s += texto(px(tramos[0][0] if tramos else 0), oy + 40, "T > CMI: tiempo por encima de la CMI", tam=14,
                   peso="bold", color=COLOR["receptor_borde"])
    s += f'<polyline points="{puntos}" fill="none" stroke="{azul}" stroke-width="3"/>'
    s += (f'<line x1="{ox:.1f}" y1="{ycmi:.1f}" x2="{ox + aw:.1f}" y2="{ycmi:.1f}" stroke="{borde_cmi}" '
          f'stroke-width="2.2" stroke-dasharray="8 6"/>')
    s += texto(ox + aw, ycmi - 8, "CMI", tam=15, peso="bold", color=borde_cmi, anclaje="end")
    if indice in ("cmax", None):                                  # pico y cociente Cmáx/CMI
        tp = max(range(len(cs) // dosis), key=lambda i: cs[i]) / 400
        xp, yp = px(tp), py(conc(tp))
        s += (f'<circle cx="{xp:.1f}" cy="{yp:.1f}" r="6" fill="{azul}"/>'
              f'<line x1="{xp + 16:.1f}" y1="{yp:.1f}" x2="{xp + 16:.1f}" y2="{ycmi:.1f}" stroke="{azul}" '
              f'stroke-width="1.6" marker-start="url(#flecha)" marker-end="url(#flecha)"/>')
        s += texto(xp + 26, yp + 18, ["Cmáx/CMI"], tam=15, peso="bold", color=azul)
    if indice in ("abc", None):
        s += texto(px(0.04), py(0.07 * escala), "ABC/CMI", tam=15, peso="bold", color=azul)  # bajo el primer pico
    s += (f'<path d="M{ox:.1f},{oy - ah:.1f} L{ox:.1f},{oy:.1f} L{ox + aw:.1f},{oy:.1f}" fill="none" '
          f'stroke="{COLOR["linea"]}" stroke-width="1.6"/>')
    s += texto(ox + aw, oy + 22, "Tiempo", tam=14, color=SUAVE, anclaje="end")
    s += (f'<text transform="translate({ox - 14:.1f} {oy - ah / 2:.1f}) rotate(-90)" font-family="Arial, sans-serif" '
          f'font-size="14" fill="{SUAVE}" text-anchor="middle">{"Concentración del fármaco" if ah > 200 else "Concentración"}'
          '</text>')
    for i in range(dosis):
        s += texto(px(i * tau), oy - ah - 6, "dosis", tam=13, color=SUAVE, anclaje="middle")
    s += texto(x + w, y + h - 4, "Esquema cualitativo: curva sin escala", tam=13, color=SUAVE, anclaje="end",
               cursiva=True)
    if titulo:
        s = texto(x, y - 10, titulo, tam=17, peso="bold") + s
    return s
