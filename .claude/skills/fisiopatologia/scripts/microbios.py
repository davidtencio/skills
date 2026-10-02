"""Microorganismos esquemáticos para las láminas de infecciones: bacterias en corte y sus estructuras.

Dibujos propios en el color de patógeno de la paleta (COLOR["patogeno"]), sin escala. Se combinan con
etiqueta_farmaco para el mapa de antibióticos y con los rótulos en bermellón para los mecanismos de resistencia.
Ejemplo de uso: ejemplos/neumonia-nosocomial/laminas.py (láminas 7 y 8).
"""
from componentes import COLOR, adn, flecha, ribosoma, texto

PAT, PAT_B = COLOR["patogeno"], COLOR["patogeno_borde"]
VERDE, ROJO = COLOR["receptor_borde"], COLOR["bloqueo"]


def bacilo_gramnegativo(x, y, w, h):
    """Bacilo gramnegativo en corte: membrana externa, periplasma con peptidoglucano y membrana interna."""
    r = h / 2
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#FBF3B8" stroke="{PAT_B}" stroke-width="5"/>'
         f'<rect x="{x + 12}" y="{y + 12}" width="{w - 24}" height="{h - 24}" rx="{r - 12}" fill="none" stroke="#B9A94A" '
         f'stroke-width="4" stroke-dasharray="3 3"/>'
         f'<rect x="{x + 22}" y="{y + 22}" width="{w - 44}" height="{h - 44}" rx="{r - 22}" fill="#FEFBE6" stroke="{PAT_B}" '
         f'stroke-width="3"/>')
    s += adn(round(x + w * 0.30), round(x + w * 0.62), y + h * 0.55)
    for i, (dx, dy) in enumerate([(0.24, 0.32), (0.70, 0.36), (0.76, 0.66), (0.36, 0.76), (0.56, 0.30)]):
        s += ribosoma(x + w * dx, y + h * dy)
    return s


def coco_grampositivo(cx, cy, r):
    """Coco grampositivo en corte: pared gruesa de peptidoglucano y membrana citoplasmática."""
    s = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#EFE3A0" stroke="{PAT_B}" stroke-width="3"/>'
         f'<circle cx="{cx}" cy="{cy}" r="{r - 9}" fill="none" stroke="#B9A94A" stroke-width="12" stroke-dasharray="3 3"/>'
         f'<circle cx="{cx}" cy="{cy}" r="{r - 18}" fill="#FEFBE6" stroke="{PAT_B}" stroke-width="3"/>')
    s += adn(round(cx - r * 0.45), round(cx + r * 0.15), cy + r * 0.2)
    for dx, dy in [(-0.35, -0.35), (0.35, -0.3), (0.42, 0.35)]:
        s += ribosoma(cx + r * dx, cy + r * dy)
    return s


def porina(x, y, cerrada=False):
    """Canal de porina en la membrana externa (y = borde superior del bacilo)."""
    color = ROJO if cerrada else VERDE
    s = (f'<rect x="{x - 9}" y="{y - 8}" width="7" height="26" rx="3" fill="#BFE6D8" stroke="{color}" stroke-width="1.5"/>'
         f'<rect x="{x + 2}" y="{y - 8}" width="7" height="26" rx="3" fill="#BFE6D8" stroke="{color}" stroke-width="1.5"/>')
    if cerrada:
        s += f'<rect x="{x - 2}" y="{y - 2}" width="4" height="14" fill="{ROJO}"/>'
    return s


def bomba(x, y):
    """Bomba de expulsión que atraviesa las dos membranas (y = borde superior del bacilo)."""
    return (f'<rect x="{x - 10}" y="{y - 10}" width="20" height="40" rx="6" fill="#F6D6C8" stroke="{ROJO}" stroke-width="1.6"/>'
            + flecha([(x, y + 24), (x, y - 26)]))


def pbp(cx, cy, color=VERDE, relleno="#BFE6D8", etiqueta="PBP"):
    """Proteína fijadora de penicilina (PBP) en la membrana interna."""
    return (f'<path d="M{cx - 14},{cy + 6} C{cx - 16},{cy - 16} {cx + 16},{cy - 16} {cx + 14},{cy + 6} Z" fill="{relleno}" '
            f'stroke="{color}" stroke-width="1.6"/>' + texto(cx, cy + 24, etiqueta, tam=13, peso="bold", anclaje="middle",
                                                                 color=color))


def enzima_bl(cx, cy, etiqueta="β-lactamasa"):
    """Betalactamasa en el periplasma; el rótulo va por fuera del bacilo, debajo."""
    return (f'<path d="M{cx - 10},{cy} L{cx},{cy - 10} L{cx + 10},{cy} L{cx},{cy + 10} Z" fill="#F6D6C8" stroke="{ROJO}" '
            f'stroke-width="1.6"/>' + (texto(cx, cy + 34, etiqueta, tam=14, peso="bold", color=ROJO, anclaje="middle")
                                       if etiqueta else ""))


def bacteria_pequena(x, y, ang=0, escala=1.0):
    """Bacilo pequeño en color de patógeno, para escenas."""
    return (f'<rect x="{x - 9 * escala}" y="{y - 4 * escala}" width="{18 * escala}" height="{8 * escala}" rx="{4 * escala}" '
            f'fill="{PAT}" stroke="{PAT_B}" stroke-width="1.2" transform="rotate({ang} {x} {y})"/>')
