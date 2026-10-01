"""Piezas comunes de las láminas de una enfermedad: marco de la lámina, pasos, tarjetas, membranas y fichas.

Uso desde ejemplos/<enfermedad>/laminas.py:
    from piezas import Lamina, leyenda_paso, tarjeta, ficha, membrana, caja, organo_ilustrado
    L = Lamina("DIABETES TIPO 2", fuentes="Fuentes: ...")
    svg = L.dibujar(1, "Contexto", "Título", "Subtítulo", contenido, total=9)
"""
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
