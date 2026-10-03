#!/usr/bin/env python3
"""Mapa muscular esquemático (frente y espalda) con los músculos de un ejercicio resaltados.

Dibujo propio, sin escala anatómica: cada grupo muscular es una forma simple que se colorea en rojo (principal)
o en rosa (secundario). Las formas del lado izquierdo de la figura se reflejan para el derecho.

Uso:
    python3 musculos.py cuadriceps,gluteos --secundarios isquiotibiales,aductores > mapa.svg
"""
import argparse
import sys

# Nombre visible de cada grupo (clave → texto). Las claves son las que usa assets/ejercicios/catalogo.json.
NOMBRES = {
    "pecho": "Pectoral",
    "hombros": "Deltoides",
    "deltoides-posterior": "Deltoides posterior",
    "biceps": "Bíceps",
    "triceps": "Tríceps",
    "antebrazo": "Antebrazo",
    "abdomen": "Recto abdominal",
    "oblicuos": "Oblicuos",
    "trapecio": "Trapecio y romboides",
    "dorsal": "Dorsal ancho",
    "lumbares": "Erectores lumbares",
    "gluteos": "Glúteo mayor",
    "gluteo-medio": "Glúteo medio",
    "cuadriceps": "Cuádriceps",
    "aductores": "Aductores",
    "isquiotibiales": "Isquiotibiales",
    "gemelos": "Gemelos y sóleo",
}

COLOR = {"principal": "#d1495b", "secundario": "#f4a9a8", "musculo": "#dfe3e8", "borde": "#8b95a1", "piel": "#f1f2f4"}

# (clave o None para piel, trazado SVG del lado izquierdo de la figura, ¿reflejar?)
FRENTE = [
    (None, "M100 11 C112 11 118 22 118 33 C118 46 110 54 100 54 C90 54 82 46 82 33 C82 22 88 11 100 11 Z", False),
    (None, "M92 50 L108 50 L109 64 L91 64 Z", False),
    ("trapecio", "M91 58 L76 66 L92 67 Z", True),
    ("hombros", "M77 66 C62 64 53 76 54 92 L60 101 C63 89 70 80 81 75 Z", True),
    ("pecho", "M99 71 L99 108 C88 113 72 109 64 100 C62 88 68 76 81 71 Z", True),
    ("biceps", "M56 99 C50 110 47 126 49 139 L59 141 C64 128 64 112 62 102 Z", True),
    ("antebrazo", "M49 143 C43 160 39 177 39 192 L47 194 C54 178 60 160 60 145 Z", True),
    (None, "M37 196 C33 204 35 214 41 218 C47 216 50 206 48 197 Z", True),
    ("abdomen", "M88 111 L112 111 L112 186 C106 193 94 193 88 186 Z", False),
    ("oblicuos", "M86 111 L69 106 C65 126 67 160 73 179 L86 187 Z", True),
    (None, "M73 181 L87 189 C92 196 97 198 100 198 L100 206 L72 200 Z", True),
    ("cuadriceps", "M72 199 C65 232 66 270 74 297 L91 299 C95 271 95 232 92 205 Z", True),
    ("aductores", "M94 205 L99 207 L99 248 L93 262 C94 242 95 224 94 205 Z", True),
    (None, "M74 299 C72 306 76 314 84 315 C92 314 95 306 92 299 Z", True),
    ("gemelos", "M75 317 C70 340 73 368 79 392 L88 392 C93 368 95 340 92 317 Z", True),
    (None, "M78 394 L89 394 C93 400 95 406 92 410 L72 410 C71 404 74 398 78 394 Z", True),
]

ESPALDA = [
    (None, "M100 11 C112 11 118 22 118 33 C118 46 110 54 100 54 C90 54 82 46 82 33 C82 22 88 11 100 11 Z", False),
    ("dorsal", "M80 78 C70 98 71 126 84 150 L100 160 L100 122 L90 80 Z", True),
    ("trapecio", "M100 50 L91 54 L77 67 L89 76 L100 120 Z", True),
    ("deltoides-posterior", "M77 66 C62 64 53 76 54 92 L60 101 C63 89 70 80 81 75 Z", True),
    ("triceps", "M56 99 C50 110 47 126 49 139 L59 141 C64 128 64 112 62 102 Z", True),
    ("antebrazo", "M49 143 C43 160 39 177 39 192 L47 194 C54 178 60 160 60 145 Z", True),
    (None, "M37 196 C33 204 35 214 41 218 C47 216 50 206 48 197 Z", True),
    ("lumbares", "M100 150 L88 146 L87 181 L100 186 Z", True),
    ("gluteo-medio", "M73 180 C69 188 69 197 71 205 L84 195 L86 181 Z", True),
    ("gluteos", "M99 187 L85 184 C72 195 69 213 75 228 C85 236 95 234 99 228 Z", True),
    ("isquiotibiales", "M75 232 C71 256 73 282 79 299 L93 299 C96 276 98 252 97 236 Z", True),
    ("aductores", "M97 236 L99 237 L99 258 L96 262 Z", True),
    (None, "M78 300 C76 306 79 313 85 314 C92 313 95 306 93 300 Z", True),
    ("gemelos", "M76 315 C69 333 71 352 79 368 L92 368 C97 352 97 332 93 315 Z", True),
    (None, "M80 370 L91 370 L90 394 C93 400 95 406 92 410 L72 410 C71 404 75 398 80 394 Z", True),
]


# Líneas de detalle (sin color propio): línea alba e intersecciones tendinosas del recto abdominal.
DETALLES_FRENTE = ('<path d="M100 112 V190 M89 132 H111 M89 152 H111 M89 170 H111" fill="none" '
                   'stroke="#8b95a1" stroke-width="1" opacity="0.7"/>')


def _formas(trazados, principales, secundarios):
    partes = []
    for clave, d, reflejar in trazados:
        if clave is None:
            relleno, clase = COLOR["piel"], "piel"
        elif clave in principales:
            relleno, clase = COLOR["principal"], f"m-{clave} principal"
        elif clave in secundarios:
            relleno, clase = COLOR["secundario"], f"m-{clave} secundario"
        else:
            relleno, clase = COLOR["musculo"], f"m-{clave}"
        comun = f'fill="{relleno}" stroke="{COLOR["borde"]}" stroke-width="1.2" stroke-linejoin="round" class="{clase}"'
        partes.append(f'<path d="{d}" {comun}/>')
        if reflejar:
            partes.append(f'<path d="{d}" transform="translate(200 0) scale(-1 1)" {comun}/>')
    return "".join(partes)


def mapa(principales, secundarios=(), ancho=220, leyenda=True):
    """SVG con la vista de frente y de espalda. Lanza ValueError si una clave no existe."""
    principales, secundarios = set(principales), set(secundarios) - set(principales)
    desconocidas = sorted((principales | secundarios) - set(NOMBRES))
    if desconocidas:
        raise ValueError(f"Músculos desconocidos: {desconocidas}. Válidos: {sorted(NOMBRES)}")
    alto_figura = 420
    alto = alto_figura + (34 if leyenda else 0)
    texto = 'font-family="Inter, Helvetica, Arial, sans-serif" font-size="17" fill="#4a5560" text-anchor="middle"'
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 {alto}" width="{ancho}" '
           f'role="img" aria-label="Músculos trabajados">',
           f'<g>{_formas(FRENTE, principales, secundarios)}{DETALLES_FRENTE}</g>',
           f'<g transform="translate(200 0)">{_formas(ESPALDA, principales, secundarios)}</g>',
           f'<text x="100" y="{alto_figura + 6}" {texto}>Frente</text>',
           f'<text x="300" y="{alto_figura + 6}" {texto}>Espalda</text>']
    if leyenda:
        y = alto_figura + 24
        svg.append(f'<rect x="78" y="{y - 10}" width="12" height="12" rx="2" fill="{COLOR["principal"]}"/>'
                   f'<text x="96" y="{y}" {texto} text-anchor="start">Principal</text>'
                   f'<rect x="218" y="{y - 10}" width="12" height="12" rx="2" fill="{COLOR["secundario"]}"/>'
                   f'<text x="236" y="{y}" {texto} text-anchor="start">Secundario</text>')
    svg.append("</svg>")
    return "".join(svg).replace(' text-anchor="middle" text-anchor="start"', ' text-anchor="start"')


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("principales", help="claves separadas por comas")
    p.add_argument("--secundarios", default="")
    a = p.parse_args(argv)
    lista = lambda s: [x.strip() for x in s.split(",") if x.strip()]
    try:
        print(mapa(lista(a.principales), lista(a.secundarios)))
    except ValueError as e:
        p.error(str(e))


if __name__ == "__main__":
    sys.exit(main())
