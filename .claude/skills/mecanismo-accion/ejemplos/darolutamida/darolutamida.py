"""Mecanismo de acción de darolutamida, versión detallada (plantilla: receptor nuclear).

Secciones: A) eje hormonal y sitios de acción de fármacos; 1) fisiología normal en la
célula prostática; 2) acción de darolutamida; fila inferior con estructura del receptor,
consecuencias, farmacocinética y efectos adversos.

Uso: python3 darolutamida.py  ->  escribe darolutamida.svg junto a este archivo.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from componentes import (COLOR, adn, arnm, atenuado, bloqueo, celula, coactivador, dominios,  # noqa: E402
                         enzima, etiqueta_farmaco, farmaco, flecha, golgi, ligando, mitocondria, nucleo,
                         organo, panel, paso, polimerasa, receptor, recuadro, reticulo_rugoso, svg, texto,
                         vesicula)

ANCHO, ALTO = 1800, 1580
MARGEN = 24
YA, HA = 112, 292                  # sección A
YP, HP, WP = 420, 776, 868         # paneles 1 y 2
X1, X2 = MARGEN, MARGEN + WP + 16
YF, HF = 1212, 248                 # fila inferior
SUAVE = COLOR["texto_suave"]


def nota(x, y, contenido, **kw):
    kw.setdefault("tam", 12)
    kw.setdefault("color", SUAVE)
    return texto(x, y, contenido, **kw)


def guia(x1, y1, x2, y2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{COLOR["farmaco"]}" '
            f'stroke-width="1.4" stroke-dasharray="3 3"/>')


# --- Sección A: eje hormonal -------------------------------------------------

def seccion_eje():
    ox, oy, w = MARGEN, YA, ANCHO - 2 * MARGEN
    s = panel(ox, oy, w, HA, "A", "Origen de los andrógenos y dónde actúa cada fármaco",
              "La testosterona se produce sobre todo en los testículos; una parte menor proviene de "
              "precursores de las glándulas suprarrenales.")
    fy, fh = oy + 92, 62
    s += organo(ox + 26, fy, 170, fh, "Hipotálamo", icono="cerebro")
    s += flecha([(ox + 196, fy + 31), (ox + 266, fy + 31)]) + nota(ox + 231, fy + 22, "GnRH", anclaje="middle", peso="bold")
    s += organo(ox + 270, fy, 170, fh, "Hipófisis", icono="hipofisis")
    s += flecha([(ox + 440, fy + 31), (ox + 510, fy + 31)]) + nota(ox + 475, fy + 22, "LH", anclaje="middle", peso="bold")
    s += organo(ox + 514, fy, 190, fh, "Testículos", "fuente principal", icono="testiculo")
    s += flecha([(ox + 704, fy + 31), (ox + 790, fy + 31)])
    s += ligando(ox + 747, fy + 14, None, r=11) + nota(ox + 747, fy - 2, "T", anclaje="middle", peso="bold")
    s += organo(ox + 794, fy, 210, fh, "Sangre", "T libre y unida a SHBG", icono="vaso")
    s += organo(ox + 514, fy + 92, 190, 54, "Suprarrenales", "precursores (DHEA)", icono="suprarrenal")
    s += flecha([(ox + 704, fy + 119), (ox + 899, fy + 119), (ox + 899, fy + 64)])
    s += flecha([(ox + 1004, fy + 31), (ox + 1068, fy + 31)])
    # Célula prostática en miniatura: T -> DHT -> RA
    s += celula(ox + 1072, fy - 6, 330, fh + 12, "", semilla=4)
    s += nota(ox + 1237, fy - 14, "Célula prostática", anclaje="middle", cursiva=True)
    cy = fy + 33
    s += ligando(ox + 1104, cy - 6, "T", r=12) + flecha([(ox + 1120, cy - 6), (ox + 1150, cy - 6)])
    s += enzima(ox + 1170, cy - 6, "", r=12) + flecha([(ox + 1186, cy - 6), (ox + 1218, cy - 6)])
    s += ligando(ox + 1240, cy - 6, "DHT", r=12) + flecha([(ox + 1258, cy - 6), (ox + 1302, cy - 6)])
    s += receptor(ox + 1345, cy + 4, escala=0.6, ocupante=("ligando", "DHT"))
    s += flecha([(ox + 1402, fy + 31), (ox + 1446, fy + 31)])
    s += organo(ox + 1450, fy, 276, fh, "Transcripción de genes", "crecimiento prostático y tumoral", icono="nucleo")
    # Sitios de acción de fármacos
    ty = fy + 82
    s += guia(ox + 355, fy + fh, ox + 355, ty) + etiqueta_farmaco(ox + 230, ty, "Análogos o antagonistas de GnRH (TPA)")
    s += nota(ox + 230, ty + 44, "↓ LH  →  ↓ testosterona testicular")
    s += etiqueta_farmaco(ox + 740, ty + 44, "Abiraterona: inhibe CYP17A1")
    s += nota(ox + 740, ty + 88, "↓ síntesis de andrógenos (testículo, suprarrenal y tumor)")
    s += guia(ox + 1172, fy + fh, ox + 1172, ty) + etiqueta_farmaco(ox + 960, ty, "Finasterida, dutasterida: inhiben 5α-reductasa")
    s += nota(ox + 960, ty + 44, "uso en hiperplasia prostática benigna")
    s += guia(ox + 1345, fy + fh, ox + 1345, ty + 62)
    s += etiqueta_farmaco(ox + 1290, ty + 62, "Darolutamida: bloquea el RA", destacado=True)
    s += nota(ox + 1290, ty + 104, "(también apalutamida, enzalutamida, bicalutamida)")
    return s


# --- Panel 1: fisiología normal ---------------------------------------------

def nucleo_base(ox, activo):
    """Núcleo, ADN con ARE y maquinaria de transcripción."""
    s = nucleo(ox + 520, YP + 600, 292, 140, nucleolo=(215, -24))
    s += adn(ox + 262, ox + 782, YP + 632, region=(ox + 362, ox + 470),
             etiqueta_region="ARE" if activo else "ARE (libre)")
    maquinaria = (coactivador(ox + 502, YP + 600) + polimerasa(ox + 580, YP + 614)
                  + arnm((ox + 616, ox + 690), YP + 598, YP + 472, ondas=4))
    s += maquinaria if activo else atenuado(maquinaria)
    return s


def panel_fisiologia(ox):
    s = panel(ox, YP, WP, HP, 1, "Fisiología normal", "Cómo se activa el receptor de andrógenos (RA) sin fármaco")
    s += celula(ox + 20, YP + 136, WP - 40, 624, "Célula prostática (citoplasma)")
    s += mitocondrias(ox)
    # 1. Testosterona atraviesa la membrana
    s += ligando(ox + 110, YP + 108, "T")
    s += nota(ox + 134, YP + 104, ["Testosterona libre", "(lipofílica)"])
    s += flecha([(ox + 110, YP + 136), (ox + 110, YP + 200)])
    s += paso(ox + 136, YP + 168, 1) + nota(ox + 152, YP + 172, "atraviesa la membrana (difusión)", tam=11)
    # 2. 5α-reductasa: T -> DHT
    s += enzima(ox + 110, YP + 224, ["5α-reductasa tipo 2", "(retículo endoplásmico)"], membrana=True)
    s += flecha([(ox + 136, YP + 224), (ox + 202, YP + 224)])
    s += ligando(ox + 224, YP + 224, "DHT")
    s += paso(ox + 168, YP + 202, 2)
    s += nota(ox + 186, YP + 322, ["La DHT se une al RA", "con mayor afinidad", "que la testosterona."], tam=11)
    # 3. Unión al RA y liberación de HSP90
    s += flecha([(ox + 246, YP + 224), (ox + 342, YP + 224)])
    s += nota(ox + 294, YP + 214, "se une al LBD", anclaje="middle", tam=11)
    s += receptor(ox + 420, YP + 232, chaperonas=True, escala=0.9)
    s += nota(ox + 490, YP + 226, ["RA inactivo,", "unido a HSP90"], tam=11)
    s += flecha([(ox + 420, YP + 270), (ox + 420, YP + 322)])
    s += paso(ox + 396, YP + 290, 3)
    s += nota(ox + 382, YP + 286, ["cambio de forma:", "se libera HSP90"], tam=11, anclaje="end")
    # 4. Dímero y translocación
    s += receptor(ox + 390, YP + 350, escala=0.72, ocupante=("ligando", "DHT"))
    s += receptor(ox + 450, YP + 350, escala=0.72, ocupante=("ligando", "DHT"))
    s += flecha([(ox + 420, YP + 370), (ox + 420, YP + 410), (ox + 510, YP + 456)])
    s += paso(ox + 330, YP + 400, 4)
    s += nota(ox + 312, YP + 424, ["Forma un dímero y", "entra al núcleo por", "un poro nuclear"],
              tam=11, anclaje="end")
    # 5. Unión al ADN y reclutamiento de la maquinaria
    s += nucleo_base(ox, activo=True)
    s += receptor(ox + 388, YP + 604, escala=0.62, ocupante=("ligando", "DHT"))
    s += receptor(ox + 444, YP + 604, escala=0.62, ocupante=("ligando", "DHT"))
    s += paso(ox + 300, YP + 682, 5)
    s += texto(ox + 318, YP + 686, ["El dímero se une al ARE y recluta", "coactivadores y la ARN polimerasa II"],
               tam=12, peso="bold")
    # 6. Traducción y vía secretora
    s += vias_secretoras(ox)
    s += paso(ox + 506, YP + 296, 6)
    s += nota(ox + 524, YP + 300, ["El ARNm sale al citoplasma:", "ribosomas del RE rugoso →", "Golgi → vesículas.",
                                   "Se producen proteínas de", "crecimiento y PSA, que se", "secreta a la sangre."],
              tam=11, color=COLOR["texto"])
    return s


def vias_secretoras(ox, activo=True):
    """ARNm saliendo del poro, RE rugoso, Golgi, vesículas y exocitosis de PSA."""
    s = arnm((ox + 690, ox + 706), YP + 472, YP + 432, ondas=1)
    s += reticulo_rugoso(ox + 640, YP + 398, 150)
    s += flecha([(ox + 742, YP + 390), (ox + 756, YP + 366)])
    s += golgi(ox + 762, YP + 340)
    s += vesicula(ox + 796, YP + 296, 9, carga=3)
    s += flecha([(ox + 806, YP + 286), (ox + 822, YP + 270)])
    s += vesicula(ox + 828, YP + 258, 8, carga=3)
    s += "".join(f'<circle cx="{ox + 852 + dx}" cy="{YP + 250 + dy}" r="2.2" fill="{COLOR["proteina_borde"]}"/>'
                 for dx, dy in ((0, 0), (4, 10), (-2, 18)))
    s += nota(ox + 806, YP + 252, "PSA", tam=11, peso="bold", anclaje="end", color=COLOR["proteina_borde"])
    if activo:
        s += nota(ox + 718, YP + 548, "ARNm", tam=11, peso="bold")
        return s
    return atenuado(s)


def mitocondrias(ox):
    return (mitocondria(ox + 96, YP + 560, angulo=72) + mitocondria(ox + 150, YP + 690, angulo=-18)
            + mitocondria(ox + 78, YP + 690, 44, 22, angulo=40))


# --- Panel 2: con darolutamida ----------------------------------------------

def panel_farmaco(ox):
    s = panel(ox, YP, WP, HP, 2, "Con darolutamida", "Bloquea al receptor en tres puntos de la misma vía")
    s += celula(ox + 20, YP + 136, WP - 40, 624, "Célula prostática (citoplasma)")
    s += mitocondrias(ox)
    # La DHT se sigue produciendo
    s += ligando(ox + 110, YP + 108, "T")
    s += nota(ox + 134, YP + 104, ["La T y la DHT se", "siguen produciendo"])
    s += flecha([(ox + 110, YP + 136), (ox + 110, YP + 200)])
    s += enzima(ox + 110, YP + 224, ["5α-reductasa tipo 2", "(retículo endoplásmico)"], membrana=True)
    s += flecha([(ox + 136, YP + 224), (ox + 202, YP + 224)])
    s += ligando(ox + 224, YP + 224, "DHT")
    # Darolutamida ocupa el LBD
    s += farmaco(ox + 420, YP + 108)
    s += nota(ox + 446, YP + 104, ["Darolutamida (vía oral) y su", "metabolito activo ceto-darolutamida"])
    s += flecha([(ox + 420, YP + 128), (ox + 420, YP + 196)])
    s += receptor(ox + 420, YP + 232, escala=0.9, ocupante=("farmaco", "D"))
    s += nota(ox + 490, YP + 226, ["RA ocupado: alta afinidad", "por el dominio de unión", "al ligando (LBD)"], tam=11)
    # 1. Compite con la DHT
    s += flecha([(ox + 246, YP + 224), (ox + 368, YP + 224)], bloqueada=True)
    s += bloqueo(ox + 306, YP + 224)
    s += paso(ox + 72, YP + 322, 1)
    s += texto(ox + 92, YP + 326, ["Inhibe de forma competitiva", "la unión de los andrógenos"], tam=12, peso="bold")
    # 2. No hay translocación
    s += flecha([(ox + 420, YP + 262), (ox + 420, YP + 410), (ox + 510, YP + 456)], bloqueada=True)
    s += bloqueo(ox + 420, YP + 360)
    s += paso(ox + 330, YP + 400, 2)
    s += texto(ox + 312, YP + 424, ["Inhibe la translocación", "del RA al núcleo"], tam=12, peso="bold", anclaje="end")
    # 3. No hay transcripción
    s += nucleo_base(ox, activo=False)
    s += bloqueo(ox + 416, YP + 600)
    s += paso(ox + 300, YP + 682, 3)
    s += texto(ox + 318, YP + 686, ["Inhibe la transcripción mediada por el RA:", "ARE libre, sin coactivadores ni ARN pol II"],
               tam=12, peso="bold")
    # Consecuencia
    s += vias_secretoras(ox, activo=False)
    s += nota(ox + 524, YP + 300, ["↓ proteínas de crecimiento", "↓ proliferación tumoral", "↓ PSA en sangre"],
              tam=12, color=COLOR["receptor_borde"], peso="bold")
    return s


# --- Fila inferior -----------------------------------------------------------

def fila_inferior():
    w = (ANCHO - 2 * MARGEN - 3 * 16) / 4
    xs = [MARGEN + i * (w + 16) for i in range(4)]
    # Estructura del RA
    x = xs[0]
    s = (f'<rect x="{x}" y="{YF}" width="{w}" height="{HF}" rx="10" fill="#FFFFFF" '
         f'stroke="{COLOR["borde_panel"]}" stroke-width="1.2"/>'
         f'<rect x="{x}" y="{YF}" width="6" height="{HF}" rx="3" fill="{COLOR["receptor_borde"]}"/>')
    s += texto(x + 20, YF + 26, "La diana: dominios del RA", tam=14, peso="bold", color=COLOR["receptor_borde"])
    s += nota(x + 20, YF + 48, "Proteína de ~920 aminoácidos", tam=12)
    bx, bw, by = x + 20, w - 40, YF + 70
    segs = [(0.60, "NTD", "#DDEFE8", False), (0.075, "DBD", "#BFE6D8", False),
            (0.045, "", "#E9F4EF", False), (0.28, "LBD", "#BFE6D8", True)]
    s += dominios(bx, by, bw, segs)
    s += farmaco(bx + bw * 0.86, by - 2, s=9, etiqueta="")
    filas = [
        (bx + bw * 0.30, "NTD: dominio N-terminal; activa la transcripción (AF-1)"),
        (bx + bw * 0.6375, "DBD: dominio de unión al ADN (dedos de zinc)"),
        (bx + bw * 0.7025, "Bisagra (entre DBD y LBD): señal nuclear"),
        (bx + bw * 0.86, "LBD: une andrógenos; aquí se une darolutamida"),
    ]
    for i, (_, contenido) in enumerate(filas):
        s += texto(bx, by + 70 + i * 30, contenido, tam=12, color=COLOR["farmaco"] if i == 3 else COLOR["texto"],
                   peso="bold" if i == 3 else "normal")
    # Consecuencias
    s += recuadro(xs[1], YF, w, HF, "Efecto terapéutico", [
        "• ↓ proliferación de las células del cáncer",
        "  de próstata dependientes de andrógenos.",
        "• ↓ PSA en sangre (útil para el seguimiento).",
        "",
        "",
        "No disminuye la testosterona: bloquea su",
        "receptor. Por eso se usa junto con la TPA,",
        "que sí reduce la producción de andrógenos.",
    ], COLOR["receptor_borde"])
    # Farmacocinética
    s += recuadro(xs[2], YF, w, HF, "Farmacocinética e interacciones", [
        "• Vía oral; se toma con alimentos",
        "  (aumentan su absorción).",
        "• Metabolismo: CYP3A4 y UGT1A9/1A1;",
        "  ceto-darolutamida también es activa.",
        "• Inductores potentes de CYP3A4 y P-gp",
        "  (p. ej., rifampicina): ↓ su concentración.",
        "• Inhibe BCRP y OATP1B1/1B3:",
        "  ↑ concentración de rosuvastatina.",
    ], COLOR["farmaco"])
    # Efectos adversos y dato distintivo
    s += recuadro(xs[3], YF, w, HF, "Efectos adversos frecuentes", [
        "• Fatiga.",
        "• Erupción cutánea; dolor en extremidades.",
        "• Fracturas (bloqueo androgénico sostenido).",
        "Lista completa: ficha técnica.",
        "",
        "",
        "Estructura polar: en estudios preclínicos",
        "atraviesa poco la barrera hematoencefálica.",
    ], COLOR["enzima_borde"])
    # Subtítulos internos en negrita
    s += texto(xs[1] + 20, YF + 50 + 4 * 13 * 1.4, "Error frecuente", tam=13, peso="bold", color=COLOR["bloqueo"])
    s += texto(xs[3] + 20, YF + 50 + 5 * 13 * 1.4, "Dato distintivo", tam=13, peso="bold", color=COLOR["farmaco"])
    return s


def leyenda(y):
    l = texto(MARGEN, y, "Leyenda", tam=13, peso="bold")
    items = [
        (ligando(0, -5, None, r=12), "Andrógeno (núcleo esteroideo)"),
        (receptor(0, -2, escala=0.45, etiqueta=None), "RA: receptor de andrógenos"),
        (farmaco(0, -5, s=11), "Darolutamida"),
        (enzima(0, -5, "", r=10), "Enzima"),
        (f'<g transform="scale(0.6)">{coactivador(0, -8, "")}</g>', "Coactivador"),
        (reticulo_rugoso(-16, -10, 30, sacos=2, separacion=9), "RE rugoso con ribosomas"),
        (mitocondria(0, -5, 32, 15), "Mitocondria"),
        (bloqueo(0, -5, r=10), "Paso bloqueado"),
    ]
    x = 110
    for icono, etiqueta in items:
        l += f'<g transform="translate({x},{y})">{icono}</g>' + texto(x + 30, y, etiqueta, tam=12)
        x += 30 + len(etiqueta) * 6.6 + 36
    l += texto(MARGEN, y + 26, "Siglas: ARE, elemento de respuesta a andrógenos; HSP90, proteína de choque térmico 90; "
               "LBD, dominio de unión al ligando; PSA, antígeno prostático específico; SHBG, globulina fijadora de "
               "hormonas sexuales; TPA, terapia de privación de andrógenos.", tam=11.5, color=SUAVE)
    return l


def construir():
    c = texto(MARGEN, 52, "Darolutamida: ¿cómo actúa?", tam=32, peso="bold")
    c += texto(MARGEN, 86, "Antagonista no esteroideo del receptor de andrógenos (RA) · Cáncer de próstata · "
               "Material para estudiantes de farmacia", tam=16, color=SUAVE)
    c += seccion_eje() + panel_fisiologia(X1) + panel_farmaco(X2) + fila_inferior()
    c += leyenda(YF + HF + 40)
    c += texto(MARGEN, ALTO - 30, "Esquema simplificado y sin escala. Fuentes: Nubeqa (darolutamida), ficha técnica, "
               "Agencia Europea de Medicamentos (EMA); Goodman & Gilman, capítulo de andrógenos.", tam=11.5, color=SUAVE)
    c += texto(MARGEN, ALTO - 12, "PROTOTIPO · pendiente de revisión farmacológica", tam=11.5, peso="bold",
               color=COLOR["bloqueo"])
    return svg(ANCHO, ALTO, c, "Mecanismo de acción de darolutamida",
               "A: eje hipotálamo-hipófisis-testículo y sitios de acción de TPA, abiraterona, inhibidores de "
               "5α-reductasa y antiandrógenos. 1: la testosterona entra a la célula, se convierte en DHT, que se "
               "une al RA, libera HSP90, forma un dímero, entra al núcleo, se une al ARE y activa la "
               "transcripción de proteínas de crecimiento y PSA. 2: darolutamida ocupa el LBD e inhibe la unión "
               "de andrógenos, la translocación nuclear y la transcripción. Abajo: dominios del RA, efecto "
               "terapéutico, farmacocinética e interacciones y efectos adversos.")


if __name__ == "__main__":
    salida = Path(__file__).with_suffix(".svg")
    salida.write_text(construir(), encoding="utf-8")
    print(salida)
