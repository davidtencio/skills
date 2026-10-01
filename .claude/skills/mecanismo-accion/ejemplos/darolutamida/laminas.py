"""Darolutamida en cuatro láminas para estudiantes de farmacia (16:9, para proyectar o imprimir).

1. Origen de los andrógenos y dónde actúa cada fármaco.
2. Cómo se activa el receptor de andrógenos (fisiología normal).
3. Cómo actúa darolutamida.
4. Del mecanismo al paciente.

Uso: python3 laminas.py [1 2 3 4]  ->  lamina-N.svg (y PNG con ../../scripts/renderizar.py).
"""
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))
from componentes import (COLOR, adn, arnm, atenuado, bloqueo, dominios, etiqueta_farmaco,  # noqa: E402
                         farmaco, flecha, icono_organo, ligando, paso, svg, texto, vesicula)
from estructuras import estructura, formula, molecula  # noqa: E402
from recursos import ATRIBUCION, ilustracion  # noqa: E402
from superficie import como_imagen, superficie_corte  # noqa: E402
from fuentes import pdb_descargar  # noqa: E402

ANCHO, ALTO = 1600, 900
SUAVE = COLOR["texto_suave"]

# SMILES verificados por fórmula. Darolutamida: derivado del registro PubChem CID 67171867
# (scripts/molecular/data/darolutamide.json del proyecto); es una mezcla de diastereómeros,
# por eso se dibuja sin estereoquímica.
TESTOSTERONA = molecula("C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1CC[C@@H]2O", "C19H28O2")
DHT = molecula("C[C@]12CC[C@H]3[C@@H](CC[C@@H]4CC(=O)CC[C@]34C)[C@@H]1CC[C@@H]2O", "C19H30O2")
DAROLUTAMIDA = molecula("CC(Cn1ccc(-c2ccc(C#N)c(Cl)c2)n1)NC(=O)c1cc(C(C)O)[nH]n1", "C19H19ClN6O2")

FUENTES = ("Fuentes: ficha técnica de Nubeqa (CIMA-AEMPS); FDA (abiraterona, finasterida, dutasterida, leuprorelina, "
           f"degarelix); UniProt P10275, P31213. {ATRIBUCION}. Estructuras: RDKit/PubChem.")


# --- Utilidades ----------------------------------------------------------------

def lamina(numero, etiqueta, titulo, subtitulo, contenido, fuentes_extra=""):
    c = (f'<rect x="0" y="0" width="{ANCHO}" height="6" fill="{COLOR["farmaco"]}"/>'
         + texto(40, 38, f"DAROLUTAMIDA · LÁMINA {numero} DE {len(LAMINAS)} · {etiqueta.upper()}", tam=14, peso="bold",
                 color=COLOR["farmaco"])
         + texto(40, 76, titulo, tam=32, peso="bold")
         + texto(40, 104, subtitulo, tam=17, color=SUAVE)
         + contenido
         + texto(40, ALTO - 34, FUENTES + fuentes_extra, tam=12.5, color=SUAVE)
         + texto(40, ALTO - 14, "Esquema simplificado y sin escala · Prototipo pendiente de revisión farmacológica",
                 tam=12.5, color=COLOR["bloqueo"], peso="bold"))
    return svg(ANCHO, ALTO, c, f"Darolutamida, lámina {numero}: {titulo}", subtitulo)


def leyenda_paso(x, y, n, titulo, detalle=(), fondo=True):
    """Número de paso, título en negrita y detalle opcional, sobre un fondo claro legible."""
    s = ""
    if fondo:
        ancho = 44 + max([len(titulo) * 9.6] + [len(l) * 7.7 for l in detalle])
        alto = 34 + 19.5 * len(detalle)
        s += (f'<rect x="{x - 8}" y="{y - 26}" width="{ancho:.0f}" height="{alto:.0f}" rx="10" fill="#FFFFFF" '
              f'fill-opacity="0.86" stroke="{COLOR["borde_panel"]}" stroke-width="1"/>')
    s += paso(x + 14, y - 6, n, radio=14, tam=15) + texto(x + 36, y, titulo, tam=17, peso="bold")
    if detalle:
        s += texto(x + 36, y + 22, list(detalle), tam=15, color=SUAVE, interlineado=1.3)
    return s


def halo(x, y, w, h, color):
    """Fondo suave detrás de una estructura química para identificar su papel por color."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{color}" fill-opacity="0.16" '
            f'stroke="{color}" stroke-opacity="0.55" stroke-width="1.5"/>')


def receptor_ra(x, y, w=80, girar_bolsillo="izquierda", opacidad=1.0):
    """Receptor de andrógenos: proteína con bolsillo de unión (ilustración Servier)."""
    h = w * 208.063 / 142.98
    return ilustracion("enzyme-green-3d", x, y, w, h, espejo=(girar_bolsillo == "izquierda"), opacidad=opacidad)


def hsp90(x, y, h=70, opacidad=1.0):
    return ilustracion("protein-2", x, y, h * 0.5, h, opacidad=opacidad)


def nombre(x, y, contenido, color=COLOR["texto"], tam=15):
    return texto(x, y, contenido, tam=tam, peso="bold", anclaje="middle", color=color)


# --- Lámina 2: activación del receptor -------------------------------------------

def lamina_2():
    c = ilustracion("emptycell-3d-1", 200, 112, 1375, 752, ajustar="none")
    c += texto(560, 272, "Célula prostática", tam=15, color=SUAVE, cursiva=True)
    c += ilustracion("mitochondrium-1", 300, 640, 112, 60, girar=18)
    c += ilustracion("mitochondrium-1", 440, 708, 104, 56, girar=-12)
    # 1. La testosterona llega desde la sangre
    c += texto(30, 200, "Sangre", tam=15, color=SUAVE, cursiva=True)
    c += halo(24, 276, 160, 112, COLOR["ligando"])
    c += estructura(TESTOSTERONA, 30, 280, 148, 96)
    c += nombre(104, 410, "Testosterona", COLOR["ligando_borde"])
    c += flecha([(184, 332), (372, 350)])
    c += leyenda_paso(22, 470, 1, "Entra a la célula", ["Es lipofílica:", "atraviesa la", "membrana"], fondo=False)
    # 2. 5α-reductasa en el retículo endoplásmico
    c += ilustracion("endoplasmatic-reticulum-rough-3d", 320, 398, 240, 92)
    c += ilustracion("enzyme-pink-3d", 384, 318, 58, 86, girar=-90)
    c += flecha([(446, 350), (494, 334)])
    c += halo(496, 284, 150, 100, COLOR["ligando"])
    c += estructura(DHT, 502, 288, 138, 92)
    c += nombre(571, 404, "DHT", COLOR["ligando_borde"])
    c += leyenda_paso(320, 528, 2, "5α-reductasa (RE)", ["convierte la testosterona", "en DHT, más potente"])
    # 3. La DHT se une al RA, que suelta la HSP90
    c += flecha([(648, 330), (724, 326)])
    c += hsp90(812, 250, 64) + hsp90(818, 326, 56)
    c += receptor_ra(728, 260, 82)
    c += nombre(769, 394, "RA + HSP90", COLOR["receptor_borde"])
    c += flecha([(862, 314), (928, 314)])
    c += receptor_ra(938, 260, 82)
    c += ligando(944, 316, None, r=22)
    c += hsp90(1030, 226, 44, opacidad=0.45) + hsp90(1056, 258, 38, opacidad=0.45)
    c += nombre(979, 394, "RA activo (con DHT)", COLOR["receptor_borde"])
    c += leyenda_paso(640, 444, 3, "La DHT se une al RA", ["cambia de forma y", "suelta la HSP90"])
    # 4. Dímero y entrada al núcleo
    c += receptor_ra(1108, 278, 62) + receptor_ra(1166, 278, 62, girar_bolsillo="derecha")
    c += ligando(1112, 320, None, r=16) + ligando(1222, 320, None, r=16)
    c += flecha([(1166, 376), (1166, 420), (1104, 498)])
    c += leyenda_paso(900, 438, 4, "Dímero al núcleo", ["entra por un poro", "nuclear"])
    # Núcleo y transcripción
    c += ilustracion("nucleus", 640, 486, 600, 336, ajustar="none")
    c += texto(745, 580, "Núcleo", tam=15, color=COLOR["borde_nucleo"], cursiva=True)
    c += adn(700, 1180, 704, region=(808, 936), etiqueta_region="ARE")
    c += receptor_ra(820, 614, 54) + receptor_ra(872, 614, 54, girar_bolsillo="derecha")
    c += ilustracion("protein-20", 946, 628, 70, 56)
    c += texto(981, 620, "Coactivadores", tam=13, anclaje="middle", color=COLOR["coactivador_borde"], peso="bold")
    c += ilustracion("protein-12", 1030, 612, 92, 80)
    c += texto(1076, 606, "ARN pol II", tam=13, anclaje="middle", color="#1F5F8B", peso="bold")
    c += leyenda_paso(744, 768, 5, "Se une al ARE del ADN", ["y recluta coactivadores y la ARN pol II"])
    # 6. ARNm, RE rugoso, Golgi y secreción de PSA
    c += arnm((1112, 1290), 624, 476, ondas=5)
    c += texto(1300, 500, "ARNm", tam=13, peso="bold", color="#7D4E9C")
    c += ilustracion("endoplasmatic-reticulum-rough-3d", 1236, 392, 210, 84)
    c += flecha([(1352, 390), (1366, 368)])
    c += ilustracion("golgi-3d-1", 1288, 270, 152, 98)
    c += vesicula(1440, 296, 10, carga=3) + vesicula(1466, 266, 9, carga=3)
    c += "".join(f'<circle cx="{1508 + dx}" cy="{226 + dy}" r="3.4" fill="{COLOR["proteina_borde"]}"/>'
                 for dx, dy in ((0, 0), (10, 14), (-4, 26)))
    c += texto(1500, 206, "PSA", tam=14, peso="bold", color=COLOR["proteina_borde"])
    c += leyenda_paso(1236, 584, 6, "Síntesis de proteínas", ["ARNm → ribosomas del RE", "→ Golgi → se secreta", "el PSA. También se",
                                                            "producen proteínas", "de crecimiento."])
    return lamina(2, "Fisiología normal", "Cómo se activa el receptor de andrógenos (RA)",
                  "Sin fármaco: de la testosterona en sangre a la síntesis de proteínas en la célula prostática.", c)


# --- Lámina 1: origen de los andrógenos ------------------------------------------

def guia(puntos):
    pts = " ".join(f"{x},{y}" for x, y in puntos)
    return (f'<polyline points="{pts}" fill="none" stroke="{COLOR["farmaco"]}" stroke-width="1.6" '
            f'stroke-dasharray="4 4"/>')


def nota_farmaco(x, y, contenido):
    return texto(x, y, contenido, tam=15, color=SUAVE, interlineado=1.3)


def lamina_1():
    c = ""
    # Hipotálamo e hipófisis
    c += ilustracion("brain-2", 46, 170, 200, 168)
    c += f'<circle cx="150" cy="292" r="7" fill="{COLOR["ligando"]}" stroke="#FFFFFF" stroke-width="2"/>'
    c += nombre(146, 366, "Hipotálamo → Hipófisis") + texto(146, 388, "GnRH → LH", tam=15, anclaje="middle", color=SUAVE)
    c += flecha([(250, 262), (348, 262)]) + texto(299, 250, "LH", tam=15, peso="bold", anclaje="middle")
    # Testículos
    c += ilustracion("servier4-testiculo.svg", 360, 184, 100, 166)
    c += nombre(410, 366, "Testículos") + texto(410, 388, "fuente principal", tam=15, anclaje="middle", color=SUAVE)
    c += flecha([(470, 262), (586, 262)]) + texto(528, 250, "testosterona", tam=14, peso="bold", anclaje="middle",
                                                 color=COLOR["ligando_borde"])
    # Suprarrenales
    c += ilustracion("servier4-rinon-suprarrenal.svg", 362, 444, 96, 154)
    c += nombre(410, 614, "Suprarrenales") + texto(410, 636, "precursores (DHEA)", tam=15, anclaje="middle", color=SUAVE)
    c += flecha([(470, 520), (646, 342)])
    # Sangre
    c += (f'<rect x="590" y="196" width="270" height="136" rx="68" fill="#FBE4E1" stroke="#B4534B" stroke-width="3"/>')
    for i, (ex, ey, g) in enumerate(((622, 222, 10), (690, 280, -20), (770, 214, 30), (812, 276, 0), (650, 300, 40))):
        c += ilustracion("erythrocyte", ex, ey, 40, 34, girar=g)
    c += ligando(726, 236, None, r=16) + ligando(760, 300, None, r=14)
    c += nombre(725, 366, "Sangre") + texto(725, 388, "T libre y unida a SHBG", tam=15, anclaje="middle", color=SUAVE)
    c += flecha([(864, 264), (912, 264)])
    # Próstata y célula prostática
    c += ilustracion("servier4-vejiga-prostata.svg", 914, 176, 104, 146)
    c += texto(966, 344, "próstata", tam=13, color=SUAVE, cursiva=True, anclaje="middle")
    c += guia([(1004, 282), (1072, 222)]) + guia([(1004, 300), (1072, 330)])
    c += ilustracion("normal-cell-1", 1066, 206, 120, 116)
    c += nombre(1066, 380, "Célula prostática") + texto(1066, 402, "T → DHT → activa el RA", tam=15, anclaje="middle",
                                                        color=SUAVE)
    c += flecha([(1190, 264), (1226, 264)])
    c += ilustracion("cancerous-cell-1", 1232, 180, 170, 168)
    c += nombre(1318, 366, "Crecimiento celular") + texto(1318, 388, "de la próstata y del tumor", tam=15,
                                                          anclaje="middle", color=SUAVE)
    # Dónde actúa cada fármaco
    c += guia([(150, 396), (150, 470)]) + etiqueta_farmaco(40, 470, "TPA: análogos o antagonistas de GnRH")
    c += nota_farmaco(52, 520, ["↓ LH → ↓ testosterona testicular"])
    c += guia([(466, 566), (560, 633)])
    c += etiqueta_farmaco(560, 620, "Abiraterona: inhibe CYP17A1")
    c += nota_farmaco(572, 670, ["↓ síntesis de andrógenos en testículo,", "suprarrenal y tumor"])
    c += guia([(1000, 410), (1000, 470)]) + etiqueta_farmaco(900, 470, "Finasterida, dutasterida")
    c += nota_farmaco(912, 520, ["inhiben la 5α-reductasa", "(uso en hiperplasia prostática benigna)"])
    c += guia([(1100, 410), (1100, 430), (1250, 430), (1250, 600)])
    c += etiqueta_farmaco(1180, 600, "Darolutamida: bloquea el RA", destacado=True)
    c += nota_farmaco(1192, 650, ["también apalutamida, enzalutamida", "y bicalutamida"])
    # Idea clave
    c += (f'<rect x="40" y="716" width="1520" height="96" rx="14" fill="#E3F0F8" stroke="{COLOR["farmaco"]}" '
          f'stroke-width="1.5"/>')
    c += texto(66, 754, "Idea clave", tam=18, peso="bold", color=COLOR["farmaco"])
    c += texto(66, 784, "La TPA reduce la producción de testosterona; darolutamida impide que los andrógenos que quedan "
                        "activen el receptor. Por eso se usan juntas.", tam=18)
    return lamina(1, "Contexto", "¿De dónde vienen los andrógenos y dónde actúa cada fármaco?",
                  "El eje hipotálamo–hipófisis–testículo produce la testosterona que activa el receptor de andrógenos (RA).", c)


# --- Lámina 3: acción de darolutamida ----------------------------------------------

def lamina_3():
    c = texto(40, 160, "En el sitio de unión del RA", tam=21, peso="bold")
    # Fila A: sin fármaco
    c += texto(40, 196, "SIN FÁRMACO", tam=14, peso="bold", color=COLOR["ligando_borde"])
    c += halo(40, 212, 210, 128, COLOR["ligando"])
    c += estructura(DHT, 48, 218, 194, 104)
    c += texto(145, 334, f"DHT · {formula(DHT)} · esteroide", tam=13, anclaje="middle", color=COLOR["ligando_borde"],
               peso="bold")
    c += flecha([(256, 276), (300, 276)])
    sup, (lx, ly), _ = SUPERFICIE_CON_DHT
    c += como_imagen(sup, 300, 186, 240, 180)
    c += texto(420, 382, "Estructura real: PDB 2AMA", tam=12.5, anclaje="middle", color=SUAVE, cursiva=True)
    c += texto(560, 240, ["La DHT encaja en el", "bolsillo del dominio de", "unión al ligando (LBD):"], tam=17)
    c += texto(560, 306, "el RA se activa", tam=17, peso="bold", color=COLOR["receptor_borde"])
    # Fila B: con darolutamida
    c += texto(40, 420, "CON DAROLUTAMIDA", tam=14, peso="bold", color=COLOR["farmaco"])
    c += halo(30, 436, 296, 136, COLOR["farmaco"])
    c += estructura(DAROLUTAMIDA, 40, 438, 270, 110, rotar=90)
    c += texto(178, 566, f"Darolutamida · {formula(DAROLUTAMIDA)} · no esteroideo", tam=13, anclaje="middle",
               color=COLOR["farmaco"], peso="bold")
    vacio, (vx, vy), _ = SUPERFICIE_VACIA
    escala = min(240 / 420, 180 / 320)
    px, py = 300 + (240 - 420 * escala) / 2 + vx * escala, 406 + (180 - 320 * escala) / 2 + vy * escala
    c += como_imagen(vacio, 300, 406, 240, 180)
    c += farmaco(px, py, "D", s=19)
    c += flecha([(340, 500), (px - 24, py)])
    c += ligando(512, 418, None, r=15) + bloqueo(538, 446, r=11)
    c += texto(420, 602, "Esquema: posición del fármaco no cristalográfica", tam=12.5, anclaje="middle", color=SUAVE,
               cursiva=True)
    c += texto(560, 466, ["Ocupa el LBD con alta", "afinidad y compite con", "la DHT:"], tam=17)
    c += texto(560, 532, "el RA no se activa", tam=17, peso="bold", color=COLOR["bloqueo"])
    # Dominios del RA
    c += texto(40, 650, "La diana: dominios del RA (~920 aminoácidos)", tam=17, peso="bold")
    segs = [(0.60, "NTD", "#DDEFE8", False), (0.075, "DBD", "#BFE6D8", False),
            (0.045, "", "#E9F4EF", False), (0.28, "LBD", "#BFE6D8", True)]
    c += dominios(40, 664, 720, segs, alto=36)
    c += farmaco(40 + 720 * 0.86, 662, "", s=10)
    c += texto(40, 728, ["NTD: activa la transcripción · DBD: se une al ADN · bisagra: señal nuclear",
                         "LBD: une los andrógenos; aquí se une darolutamida"], tam=14.5, color=SUAVE)
    c += f'<line x1="800" y1="140" x2="800" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    # Panel derecho: la célula
    c += texto(830, 160, "En la célula: tres puntos de bloqueo", tam=21, peso="bold")
    c += ilustracion("emptycell-3d-1", 826, 176, 740, 520, ajustar="none")
    c += ilustracion("mitochondrium-1", 900, 560, 90, 50, girar=20)
    c += atenuado(ilustracion("endoplasmatic-reticulum-rough-3d", 1340, 330, 170, 68)
                  + ilustracion("golgi-3d-1", 1386, 260, 120, 76), 0.3)
    c += texto(1420, 428, "↓ PSA", tam=16, peso="bold", color=COLOR["receptor_borde"], anclaje="middle")
    c += halo(912, 290, 98, 70, COLOR["ligando"]) + estructura(DHT, 915, 293, 92, 64)
    c += flecha([(1008, 324), (1062, 324)], bloqueada=True) + bloqueo(1034, 324, r=12)
    c += paso(1034, 294, 1, radio=13, tam=14)
    c += receptor_ra(1068, 270, 78)
    c += farmaco(1076, 326, "D", s=15)
    c += texto(1108, 404, "RA + darolutamida", tam=14, peso="bold", anclaje="middle", color=COLOR["farmaco"])
    c += flecha([(1150, 330), (1210, 330), (1250, 448)], bloqueada=True) + bloqueo(1220, 382, r=12)
    c += paso(1194, 372, 2, radio=13, tam=14)
    c += ilustracion("nucleus", 1060, 446, 420, 230, ajustar="none")
    c += adn(1104, 1440, 590, region=(1190, 1290), etiqueta_region="ARE libre")
    c += bloqueo(1240, 548, r=13) + paso(1210, 540, 3, radio=13, tam=14)
    c += atenuado(ilustracion("protein-20", 1300, 530, 52, 42) + ilustracion("protein-12", 1360, 516, 66, 58), 0.3)
    # Pasos
    c += leyenda_paso(834, 734, 1, "Bloquea la unión", ["compite con los", "andrógenos por el LBD"])
    c += leyenda_paso(1066, 734, 2, "Bloquea la entrada", ["el RA no se transloca", "al núcleo"])
    c += leyenda_paso(1290, 734, 3, "Bloquea la transcripción", ["el ARE queda libre: no", "se activan los genes"])
    c += texto(830, 838, "Resultado: ↓ proteínas de crecimiento · ↓ proliferación tumoral · ↓ PSA", tam=17,
               peso="bold", color=COLOR["receptor_borde"])
    return lamina(3, "Mecanismo de acción", "Cómo actúa darolutamida",
                  "Antagonista no esteroideo del RA: se une al dominio de unión al ligando y bloquea la señal en tres puntos.", c,
                  " Receptor: RCSB PDB 2AMA (CC0).")


# --- Lámina 4: del mecanismo al paciente -------------------------------------------

def tarjeta(x, y, w, h, color, titulo, lineas, icono=""):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#FFFFFF" stroke="{COLOR["borde_panel"]}" '
         f'stroke-width="1.4"/><rect x="{x}" y="{y}" width="8" height="{h}" rx="4" fill="{color}"/>')
    s += icono
    s += texto(x + 32, y + 46, titulo, tam=22, peso="bold", color=color)
    s += texto(x + 32, y + 84, lineas, tam=17, interlineado=1.45)
    return s


def lamina_4():
    w, h = 752, 336
    x1, x2, y1, y2 = 40, 808, 136, 488
    c = tarjeta(x1, y1, w, h, COLOR["receptor_borde"], "Efecto terapéutico", [
        "• Menor proliferación de las células del cáncer",
        "  de próstata que dependen de los andrógenos.",
        "• Disminución del PSA en sangre, útil para",
        "  el seguimiento del tratamiento.",
        "• Se usa junto con la terapia de privación de",
        "  andrógenos (TPA)."], ilustracion("cancerous-cell-1", x1 + w - 150, y1 + 20, 120, 118))
    c += tarjeta(x2, y1, w, h, COLOR["bloqueo"], "Error frecuente", [
        "«Darolutamida baja la testosterona.»",
        "Falso: bloquea el receptor sobre el que actúa.",
        "La testosterona la reduce la TPA. Las dos actúan",
        "en puntos distintos de la misma vía.",
        "",
        "Para pensar: ¿por qué se combinan si ambas",
        "«bloquean los andrógenos»?"],
        halo(x2 + w - 186, y1 + 24, 160, 104, COLOR["ligando"])
        + estructura(TESTOSTERONA, x2 + w - 182, y1 + 28, 152, 96))
    c += tarjeta(x1, y2, w, h, COLOR["farmaco"], "Farmacocinética e interacciones", [
        "• Vía oral, con alimentos: la biodisponibilidad",
        "  aumenta de 2 a 2,5 veces. Dos tomas al día.",
        "• CYP3A4 y UGT1A9/1A1; ceto-darolutamida (metabolito",
        "  principal) tiene actividad similar. Semivida 18–20 h.",
        "• Inductores de CYP3A4/P-gp (rifampicina): ↓ 72 % su",
        "  exposición; no se recomiendan.",
        "• Inhibe BCRP y OATP1B1/1B3: evitar la rosuvastatina."],
        ilustracion("cc0-pill_blue.svg", x1 + w - 150, y2 + 26, 120, 60, girar=-20))
    c += tarjeta(x2, y2, w, h, COLOR["enzima_borde"], "Efectos adversos y dato distintivo", [
        "• Muy frecuente: fatiga o astenia; en análisis,",
        "  ↓ neutrófilos y ↑ bilirrubina, ALT y AST.",
        "• Frecuentes: erupción, dolor en extremidades,",
        "  fracturas, cardiopatía isquémica, insuf. cardíaca.",
        "• Dato distintivo: en ratas y ratones la exposición",
        "  cerebral fue muy baja (1,9–4,5 % de la plasmática)."],
        ilustracion("brain-2", x2 + w - 150, y2 + 22, 120, 100))
    return lamina(4, "Aplicación clínica", "Del mecanismo al paciente",
                  "Qué significa el bloqueo del receptor para el tratamiento, la seguridad y las interacciones.", c)


_PDB = pdb_descargar("2AMA")
SUPERFICIE_CON_DHT = superficie_corte(_PDB, "A", "DHT")
SUPERFICIE_VACIA = superficie_corte(_PDB, "A", "DHT", mostrar_ligando=False)

LAMINAS = {1: lamina_1, 2: lamina_2, 3: lamina_3, 4: lamina_4}

if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or sorted(LAMINAS):
        salida = Path(__file__).with_name(f"lamina-{n}.svg")
        salida.write_text(LAMINAS[n](), encoding="utf-8")
        print(salida)
