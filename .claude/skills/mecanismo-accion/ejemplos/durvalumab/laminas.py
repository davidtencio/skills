"""Durvalumab en seis láminas (plantilla: anticuerpo bloqueante de un punto de control inmunitario).

1. Puntos de control: los frenos del linfocito T y dónde actúa cada fármaco.
2. Fisiología: cómo PD-L1 frena al linfocito T que reconoce el tumor.
3. Cómo actúa durvalumab (estructuras reales PDB 4ZQK y 5X8M).
4. Del mecanismo al paciente.
5. Indicaciones aprobadas por la FDA, comparadas con la UE (CIMA).
6. Del ensayo a la práctica: valor y vida real.

Uso: python3 laminas.py [1 2 3 4 5 6]
"""
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))
sys.path.insert(0, str(RAIZ / "ejemplos" / "darolutamida"))
from componentes import COLOR, bloqueo, enzima, etiqueta_farmaco, flecha, paso, svg, texto  # noqa: E402
from fuentes import pdb_descargar  # noqa: E402
from recursos import ATRIBUCION, ilustracion  # noqa: E402
from superficie import como_imagen, superficie_complejo  # noqa: E402
from laminas import leyenda_paso, tarjeta  # noqa: E402

ANCHO, ALTO = 1600, 900
SUAVE = COLOR["texto_suave"]
VERDE, AZUL, ROJO, NARANJA = COLOR["receptor_borde"], COLOR["farmaco"], COLOR["bloqueo"], COLOR["ligando_borde"]
LILA = COLOR["coactivador_borde"]
GRIS = "#7F8C93"

# Colores de las proteínas de la sinapsis (iguales en todas las láminas).
PDL1 = ("#BFE6D8", VERDE)            # diana: verde
PD1 = ("#F6D6C8", "#B5684A")         # receptor inhibidor del linfocito
CD80 = ("#F3E3C8", "#9A6A00")
TCR = ("#DCD3F0", LILA)
MHC = ("#D9DEE1", GRIS)

FUENTES = ("Fuentes: ficha técnica de Imfinzi (CIMA-AEMPS); FDA (Imfinzi, atezolizumab, nivolumab, pembrolizumab, "
           f"cemiplimab, tremelimumab, ipilimumab); UniProt Q9NZQ7, Q15116; Reactome R-HSA-389948. {ATRIBUCION}.")


def lamina(numero, etiqueta, titulo, subtitulo, contenido, extra=""):
    c = (f'<rect x="0" y="0" width="{ANCHO}" height="6" fill="{AZUL}"/>'
         + texto(40, 38, f"DURVALUMAB · LÁMINA {numero} DE {len(LAMINAS)} · {etiqueta.upper()}", tam=14, peso="bold",
                 color=AZUL)
         + texto(40, 76, titulo, tam=32, peso="bold") + texto(40, 104, subtitulo, tam=17, color=SUAVE)
         + contenido + texto(40, ALTO - 34, FUENTES + extra, tam=12.5, color=SUAVE)
         + texto(40, ALTO - 14, "Esquema simplificado y sin escala · Prototipo pendiente de revisión farmacológica",
                 tam=12.5, color=ROJO, peso="bold"))
    return svg(ANCHO, ALTO, c, f"Durvalumab, lámina {numero}: {titulo}", subtitulo)


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


def ig(x, y_mem, y_punta, colores, n=1, etiqueta=None, lado="derecha", rx=15, ry=18):
    """Proteína de membrana con n dominios de inmunoglobulina; el último toca y_punta.

    La proteína sale de la membrana en y_mem hacia y_punta (arriba o abajo).
    """
    relleno, borde = colores
    sentido = 1 if y_punta > y_mem else -1
    y_dom = y_punta - sentido * 2 * ry * n            # borde del primer dominio
    s = f'<rect x="{x - 3}" y="{min(y_mem, y_dom) - 12 if sentido < 0 else y_mem - 12}" width="6" ' \
        f'height="{abs(y_dom - y_mem) + 12}" rx="3" fill="{borde}"/>'
    for i in range(n):
        cy = y_dom + sentido * (ry + 2 * ry * i)
        s += f'<ellipse cx="{x}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{relleno}" stroke="{borde}" stroke-width="1.6"/>'
    if etiqueta:
        tx = x + rx + 8 if lado == "derecha" else x - rx - 8
        ty = (y_mem + y_dom) / 2 + 5
        s += texto(tx, ty, etiqueta, tam=13, peso="bold", color=borde, anclaje="start" if lado == "derecha" else "end")
    return s


def mhc(x, y_mem, y_punta, etiqueta=True):
    """MHC de clase I con el péptido tumoral (punto naranja) en la punta."""
    s = ig(x, y_mem, y_punta, MHC, n=2)
    s += f'<circle cx="{x}" cy="{y_punta - 1}" r="6.5" fill="{COLOR["ligando"]}" stroke="{NARANJA}" stroke-width="1.4"/>'
    if etiqueta:
        s += texto(x + 22, (y_mem + y_punta) / 2 + 22, ["MHC +", "péptido"], tam=13, peso="bold", color=GRIS)
    return s


def tcr(x, y_mem, y_punta, etiqueta=True):
    """Receptor del linfocito T (cadenas α y β)."""
    s = ig(x - 9, y_mem, y_punta, TCR, n=2, rx=9) + ig(x + 9, y_mem, y_punta, TCR, n=2, rx=9)
    if etiqueta:
        s += texto(x - 26, (y_mem + y_punta) / 2 + 5, "TCR", tam=13, peso="bold", color=LILA, anclaje="end")
    return s


def anticuerpo(x, y, w=60, invertido=False, opacidad=1.0, girar=0):
    """Anticuerpo IgG (Servier). invertido=True: brazos (Fab) hacia abajo, como al unirse a su diana."""
    h = w * 82 / 66.935
    return ilustracion("servier-antibody-3-recortado.svg", x - w / 2, y - h / 2, w, h, opacidad=opacidad,
                       girar=180 + girar if invertido else girar)


def durvalumab_sobre(x, y_punta, w=58):
    """Durvalumab unido por un brazo a la punta de PD-L1 (que sube desde abajo)."""
    h = w * 82 / 66.935
    return anticuerpo(x + w * 0.24, y_punta - h * 0.36, w, invertido=True)


def lado_celula(x, y, nombre, icono, subtitulo=None, color=COLOR["texto"]):
    s = ilustracion(icono, x, y - 30, 44, 44) + texto(x + 54, y - 4, nombre, tam=16, peso="bold", color=color)
    if subtitulo:
        s += texto(x + 54, y + 16, subtitulo, tam=13, color=SUAVE, cursiva=True)
    return s


def granulos(x, y, n=3):
    """Gránulos de perforina y granzimas."""
    return "".join(f'<circle cx="{x + 13 * i}" cy="{y + (i % 2) * 9}" r="5.5" fill="#D55E00" fill-opacity="0.75" '
                   f'stroke="#8A3D00" stroke-width="1"/>' for i in range(n))


def ifng(x, y):
    """Molécula de IFN-γ (citocina): pequeño hexágono naranja."""
    return (f'<path d="M{x - 7},{y} L{x - 3.5},{y - 6} L{x + 3.5},{y - 6} L{x + 7},{y} L{x + 3.5},{y + 6} '
            f'L{x - 3.5},{y + 6} Z" fill="{COLOR["ligando"]}" stroke="{NARANJA}" stroke-width="1.2"/>')


# --- Lámina 1 ------------------------------------------------------------------------

def lamina_1():
    yt, yb = 300, 580
    c = membrana(40, 1560, yt) + membrana(40, 1560, yb)
    c += lado_celula(50, 190, "Linfocito T citotóxico", "servier-t-lymphocyte.svg", "citoplasma", LILA)
    c += lado_celula(50, 680, "Célula tumoral", "cancerous-cell-1", "citoplasma", COLOR["texto"])
    c += texto(1550, 344, "Espacio entre las dos células (sinapsis inmunitaria)", tam=14, color=SUAVE,
               cursiva=True, anclaje="end")
    # 1) Reconocimiento
    c += tcr(330, yt, 440) + mhc(330, yb, 440)
    c += texto(330, 236, "1 · Reconoce el tumor", tam=17, peso="bold", anclaje="middle", color=LILA)
    c += texto(330, 258, "(señal de activación)", tam=14, anclaje="middle", color=SUAVE)
    # 2) Freno PD-1/PD-L1, con los fármacos que lo bloquean
    c += ig(780, yt, 430, PD1, n=1, etiqueta="PD-1", lado="izquierda")
    c += ig(780, yb, 430, PDL1, n=2, etiqueta="PD-L1", lado="izquierda")
    c += texto(780, 236, "2 · Freno PD-1 / PD-L1", tam=17, peso="bold", anclaje="middle", color=ROJO)
    c += texto(780, 258, "(apaga al linfocito)", tam=14, anclaje="middle", color=SUAVE)
    c += etiqueta_farmaco(812, 399, "Anti-PD-1: nivolumab, pembrolizumab, cemiplimab", ancho=350)
    c += etiqueta_farmaco(812, 452, "Anti-PD-L1: durvalumab", destacado=True, ancho=200)
    c += etiqueta_farmaco(1022, 452, "atezolizumab", ancho=130)
    # 3) CTLA-4, en otra sinapsis
    c += (f'<rect x="1190" y="380" width="370" height="150" rx="14" fill="#FFFFFF" stroke="{COLOR["borde_panel"]}" '
          f'stroke-width="1.4"/>')
    c += texto(1210, 412, "Otro freno: CTLA-4", tam=17, peso="bold", color=ROJO)
    c += texto(1210, 436, ["Se une a CD80/CD86 de la célula", "presentadora de antígeno, no a la tumoral."],
               tam=14, color=SUAVE)
    c += etiqueta_farmaco(1210, 486, "Anti-CTLA-4: tremelimumab, ipilimumab", ancho=330)
    c += (f'<rect x="40" y="716" width="1520" height="96" rx="14" fill="#E3F0F8" stroke="{AZUL}" stroke-width="1.5"/>')
    c += texto(66, 754, "Idea clave", tam=18, peso="bold", color=AZUL)
    c += texto(66, 784, "Durvalumab no ataca al tumor: bloquea PD-L1, la señal con la que el tumor «apaga» al linfocito T "
                        "que ya lo había reconocido.", tam=18)
    return lamina(1, "Contexto", "Puntos de control: los frenos del linfocito T",
                  "Los inhibidores de puntos de control no matan células: quitan frenos a la respuesta inmunitaria.", c)


# --- Lámina 2 ------------------------------------------------------------------------

def lamina_2():
    yt, yb = 420, 650
    x2 = 1050
    c = membrana(40, x2, yt) + membrana(40, x2, yb)
    c += lado_celula(50, 160, "Linfocito T citotóxico", "servier-t-lymphocyte.svg", None, LILA)
    c += lado_celula(50, 720, "Célula tumoral", "cancerous-cell-1", None)
    # Señal de activación (izquierda)
    c += tcr(300, yt, 535) + mhc(300, yb, 535)
    c += (f'<rect x="220" y="300" width="190" height="56" rx="12" fill="#FFFFFF" stroke="{LILA}" stroke-width="1.5"/>')
    c += texto(315, 324, "CD3ζ y ZAP70", tam=15, peso="bold", anclaje="middle", color=LILA)
    c += texto(315, 344, "fosforilados", tam=13, anclaje="middle", color=SUAVE)
    c += flecha([(300, 396), (300, 362)])
    c += (f'<rect x="200" y="196" width="300" height="74" rx="12" fill="#EAF6F1" stroke="{VERDE}" stroke-width="1.5"/>')
    c += texto(350, 222, "Linfocito activado", tam=16, peso="bold", anclaje="middle", color=VERDE)
    c += texto(350, 242, ["proliferación, citocinas,", "perforina y granzimas"], tam=13, anclaje="middle", color=SUAVE)
    c += flecha([(315, 298), (322, 276)])
    # IFN-γ hacia el tumor e inducción de PD-L1
    c += "".join(ifng(470 + dx, 470 + dy) for dx, dy in ((0, 0), (22, 30), (8, 64), (34, 96), (52, 130)))
    c += texto(560, 488, "IFN-γ", tam=14, peso="bold", color=NARANJA)
    c += ilustracion("nucleus", 470, 690, 230, 130, ajustar="none")
    c += texto(710, 770, ["↑ gen de", "PD-L1"], tam=14, peso="bold", color=VERDE)
    c += flecha([(530, 610), (560, 686)], discontinua=True)
    c += flecha([(660, 700), (735, 668)])
    # Freno: PD-1 y CD80 con PD-L1
    c += ig(760, yt, 540, PD1, n=1, etiqueta="PD-1", lado="izquierda")
    c += ig(760, yb, 540, PDL1, n=2)
    c += ig(950, yt, 540, CD80, n=2, etiqueta="CD80", lado="derecha")
    c += ig(950, yb, 540, PDL1, n=2)
    c += texto(855, 620, "PD-L1", tam=14, peso="bold", anclaje="middle", color=VERDE)
    c += enzima(760, 296, "SHP-2", r=22)
    c += flecha([(760, 396), (760, 348)])
    c += flecha([(734, 296), (416, 326)], bloqueada=True)
    c += texto(575, 296, "desfosforila", tam=13, anclaje="middle", color=ROJO, peso="bold")
    c += bloqueo(350, 286, r=11)
    # Pasos (derecha)
    c += f'<line x1="1080" y1="140" x2="1080" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    c += leyenda_paso(1100, 180, 1, "Reconoce el antígeno", ["El TCR se une al MHC con un", "péptido tumoral y se activa."])
    c += leyenda_paso(1100, 290, 2, "Libera IFN-γ", ["y el tumor responde fabricando", "más PD-L1 en su membrana."])
    c += leyenda_paso(1100, 400, 3, "PD-L1 se une a PD-1", ["y también a CD80 (B7.1)."])
    c += leyenda_paso(1100, 490, 4, "PD-1 recluta SHP-2", ["que desfosforila CD3ζ y ZAP70:", "se corta la señal del TCR."])
    c += leyenda_paso(1100, 600, 5, "Linfocito «agotado»", ["↓ citotoxicidad, proliferación", "y citocinas: el tumor escapa."])
    c += texto(1100, 740, ["En tejidos sanos, este freno evita", "la autoinmunidad (tolerancia)."], tam=15,
               color=SUAVE, cursiva=True)
    return lamina(2, "Fisiología normal", "Cómo PD-L1 frena al linfocito T que reconoce el tumor",
                  "PD-L1 es una respuesta adaptativa del tumor: aparece cuando el linfocito ya lo está atacando.", c)


# --- Lámina 3 ------------------------------------------------------------------------

_PD1 = superficie_complejo(pdb_descargar("4ZQK"), [("A", "#7FC8A9"), ("B", "#E8A98E")])
_DUR = superficie_complejo(pdb_descargar("5X8M"), [("A", "#7FC8A9"), ("BC", "#7DB7E0")])


def lamina_3():
    c = texto(40, 160, "Durvalumab ocupa el sitio de PD-1", tam=21, peso="bold")
    c += como_imagen(_PD1, 40, 180, 340, 230)
    c += texto(210, 430, ["PD-L1 (verde) + PD-1 (salmón)", "PDB 4ZQK"], tam=13, anclaje="middle", color=SUAVE,
               cursiva=True)
    c += como_imagen(_DUR, 400, 180, 370, 230)
    c += texto(585, 430, ["PD-L1 (verde) + Fab de durvalumab (azul)", "PDB 5X8M"], tam=13, anclaje="middle",
               color=SUAVE, cursiva=True)
    c += (f'<rect x="40" y="476" width="730" height="96" rx="14" fill="#E3F0F8" stroke="{AZUL}" stroke-width="1.4"/>')
    c += texto(62, 508, "Misma cara de PD-L1", tam=17, peso="bold", color=AZUL)
    c += texto(62, 534, ["11 de los 18 aminoácidos de PD-L1 que tocan PD-1 también", "los toca durvalumab: PD-1 ya no cabe."],
               tam=15)
    c += anticuerpo(110, 700, 84)
    c += texto(170, 650, "IgG1κ humana anti-PD-L1", tam=16, peso="bold", color=AZUL)
    c += texto(170, 674, ["• Bloquea PD-L1 frente a PD-1 y frente a CD80.",
                          "• Fc modificado: no induce citotoxicidad celular",
                          "  dependiente de anticuerpos (CCDA).",
                          "• No actúa sobre PD-L2 (anti-PD-1 sí lo bloquea)."], tam=15, interlineado=1.4)
    # Escena en la sinapsis
    c += f'<line x1="800" y1="140" x2="800" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    yt, yb = 300, 590
    c += texto(830, 160, "En la sinapsis", tam=21, peso="bold")
    c += membrana(820, 1560, yt) + membrana(820, 1560, yb)
    c += texto(1550, 270, "Linfocito T", tam=15, peso="bold", anclaje="end", color=LILA)
    c += texto(1550, 630, "Célula tumoral", tam=15, peso="bold", anclaje="end")
    c += tcr(900, yt, 445, etiqueta=False) + mhc(900, yb, 445, etiqueta=False)
    c += texto(900, 248, "TCR–MHC", tam=13, peso="bold", anclaje="middle", color=LILA)
    c += ig(1080, yt, 372, PD1, n=1) + texto(1080, 396, "PD-1 libre", tam=13, peso="bold", anclaje="middle", color=PD1[1])
    c += ig(1080, yb, 480, PDL1, n=2) + durvalumab_sobre(1080, 480)
    c += ig(1280, yt, 392, CD80, n=2) + texto(1280, 416, "CD80 libre", tam=13, peso="bold", anclaje="middle", color=CD80[1])
    c += ig(1280, yb, 480, PDL1, n=2) + durvalumab_sobre(1280, 480)
    c += texto(1180, 560, "PD-L1 + durvalumab", tam=13, peso="bold", anclaje="middle", color=AZUL)
    c += paso(1030, 440, 1, radio=12, tam=13) + paso(1230, 440, 2, radio=12, tam=13)
    c += granulos(1440, 340) + flecha([(1452, 362), (1452, 540)])
    c += paso(1478, 450, 3, radio=12, tam=13)
    c += texto(1478, 342, ["perforina y", "granzimas"], tam=13, color=ROJO, peso="bold")
    c += leyenda_paso(830, 690, 1, "Bloquea PD-L1–PD-1", ["SHP-2 no se activa: el TCR", "sigue enviando su señal."])
    c += leyenda_paso(1080, 690, 2, "Bloquea PD-L1–CD80", ["se retira el segundo freno", "de PD-L1."])
    c += leyenda_paso(1320, 690, 3, "El linfocito ataca", ["libera perforina y granzimas:", "apoptosis del tumor."])
    return lamina(3, "Mecanismo de acción", "Cómo actúa durvalumab",
                  "Anticuerpo IgG1κ humano que se une a PD-L1 y le impide unirse a PD-1 y a CD80.",
                  c, " PDB 4ZQK, 5X8M (CC0).")


# --- Lámina 4 ------------------------------------------------------------------------

def lamina_4():
    w, h = 752, 336
    x1, x2, y1, y2 = 40, 808, 136, 488
    c = tarjeta(x1, y1, w, h, VERDE, "Efecto terapéutico", [
        "• Reactiva linfocitos T que ya reconocían el tumor:",
        "  ↑ activación y respuesta antitumoral.",
        "• No mata por sí mismo: en modelos animales, su",
        "  efecto desaparece sin linfocitos T.",
        "• Solo o combinado (quimioterapia, tremelimumab,",
        "  olaparib, BCG) en pulmón, vías biliares, hígado,",
        "  endometrio, vejiga y estómago."],
        ilustracion("servier-t-lymphocyte.svg", x1 + w - 140, y1 + 20, 110, 112))
    c += tarjeta(x2, y1, w, h, ROJO, "Error frecuente", [
        "«Durvalumab es quimioterapia: ataca al tumor.»",
        "Falso: no es citotóxico ni induce CCDA; quita un",
        "freno al linfocito T. Por eso sus efectos adversos",
        "típicos son inflamatorios (inmunomediados), no los",
        "de la quimioterapia.",
        "",
        "Para pensar: ¿por qué se evitan los corticoides",
        "antes de empezar, pero se usan para tratar sus",
        "efectos adversos?"])
    c += tarjeta(x1, y2, w, h, AZUL, "Farmacocinética e interacciones", [
        "• Perfusión intravenosa de 1 hora; p. ej., 1 500 mg",
        "  cada 4 semanas o 10 mg/kg cada 2 semanas.",
        "• Vss 5,6 L; semivida ~18 días; estado estacionario",
        "  a las ~16 semanas.",
        "• Se elimina por catabolismo proteico y unión a su",
        "  diana, no por CYP: sin interacciones metabólicas.",
        "• Antes de iniciar, evitar corticoides sistémicos",
        "  (> 10 mg/día de prednisona) e inmunosupresores."], "")
    c += tarjeta(x2, y2, w, h, COLOR["enzima_borde"], "Efectos adversos", [
        "• ⚠ Inmunomediados, en cualquier órgano: neumonitis,",
        "  colitis, hepatitis, tiroides, suprarrenal, diabetes",
        "  tipo 1, nefritis, piel, miocarditis (puede ser mortal).",
        "• Más frecuentes en monoterapia: tos (18 %), diarrea",
        "  (15 %), erupción (15 %), hipotiroidismo (12 %).",
        "• Manejo: suspender y corticoides según el grado.",
        "• Embarazo: puede causar daño fetal; anticoncepción",
        "  hasta 3 meses tras la última dosis."], "")
    return lamina(4, "Aplicación clínica", "Del mecanismo al paciente",
                  "Qué significa quitar el freno PD-L1: eficacia, farmacocinética de un anticuerpo y efectos inmunomediados.",
                  c, " PMID 25943534.")


# --- Lámina 5 -----------------------------------------------------------------------

# Aprobaciones de la FDA (Drugs@FDA, BLA 761069; cartas de aprobación) y si constan en la ficha de CIMA 4.1.
# Tercer campo: True = consta en la UE; False = aún no; None = retirada.
HITOS = [
    ("05/2017", ["Urotelial avanzado", "tras platino (acelerada;", "retirada en 2021)"], None),
    ("02/2018", ["CPNM estadio III", "irresecable tras", "quimiorradioterapia"], True),
    ("03/2020", ["Microcítico extendido:", "1.ª línea con", "etopósido y platino"], True),
    ("09/2022", ["Vías biliares", "avanzado, con gem-", "citabina y cisplatino"], True),
    ("10/2022", ["Hepatocarcinoma", "irresecable, con", "tremelimumab"], True),
    ("11/2022", ["CPNM metastásico,", "con tremelimumab", "y quimioterapia"], True),
    ("06/2024", ["Endometrio dMMR", "avanzado, con carbo-", "platino y paclitaxel"], True),
    ("08/2024", ["CPNM resecable:", "antes (con QT) y", "después de la cirugía"], True),
    ("12/2024", ["Microcítico limitado", "tras quimio-", "rradioterapia"], True),
    ("03/2025", ["Vejiga músculo-", "invasivo: antes (con", "QT) y tras cistectomía"], True),
    ("11/2025", ["Gástrico o unión", "gastroesofágica", "resecable, con FLOT"], True),
    ("05/2026", ["Vejiga no músculo-", "invasivo de alto", "riesgo, con BCG"], False),
]


def lamina_5():
    x0, x1, y = 110, 1490, 400
    c = f'<line x1="{x0 - 50}" y1="{y}" x2="{x1 + 50}" y2="{y}" stroke="{COLOR["borde_panel"]}" stroke-width="6" ' \
        f'stroke-linecap="round"/>'
    c += texto(x0 - 50, 618, "← Al principio: enfermedad avanzada ya tratada", tam=14, color=SUAVE, cursiva=True)
    c += texto(x1 + 50, 618, "Ahora: primera línea y tratamiento alrededor de la cirugía →", tam=14, color=SUAVE,
               cursiva=True, anclaje="end")
    paso_x = (x1 - x0) / (len(HITOS) - 1)
    for i, (fecha, lineas, ue) in enumerate(HITOS):
        x = x0 + i * paso_x
        color = AZUL if ue else (NARANJA if ue is False else GRIS)
        arriba = i % 2 == 0
        y_txt = 200 if arriba else 476
        c += f'<line x1="{x:.0f}" y1="{y}" x2="{x:.0f}" y2="{(y_txt + 80) if arriba else (y_txt - 50)}" ' \
             f'stroke="{color}" stroke-width="1.6" stroke-dasharray="4 4"/>'
        c += f'<circle cx="{x:.0f}" cy="{y}" r="12" fill="#FFFFFF" stroke="{color}" stroke-width="4"/>'
        c += texto(x, y_txt, fecha, tam=17, peso="bold", anclaje="middle", color=color)
        c += texto(x, y_txt + 22, lineas, tam=13.5, anclaje="middle", interlineado=1.3)
        etiqueta = {True: "UE: sí", False: "UE: aún no", None: "UE: no"}[ue]
        c += (f'<rect x="{x - 44:.0f}" y="{(y_txt - 44)}" width="88" height="24" rx="12" fill="{color}" '
              f'fill-opacity="0.16"/>')
        c += texto(x, y_txt - 27, etiqueta, tam=12.5, peso="bold", anclaje="middle", color=color)
    c += tarjeta(40, 646, 740, 180, NARANJA, "Diferencias con la UE", [
        "Solo en la UE: hepatocarcinoma en monoterapia y endometrio",
        "pMMR con olaparib. CPNM estadio III: en la UE, solo si",
        "PD-L1 ≥ 1 %. Solo en la FDA (05/2026): vejiga no músculo-invasivo."])
    c += tarjeta(820, 646, 740, 180, AZUL, "Cómo leer esta lámina", [
        "La FDA y la EMA aprueban por separado y en fechas distintas.",
        "«UE: aún no» = no figura en la ficha de CIMA consultada.",
        "En Costa Rica rige el registro sanitario nacional."])
    return lamina(5, "Indicaciones", "Indicaciones aprobadas: de la enfermedad avanzada a la cirugía",
                  "Aprobaciones de la FDA (Drugs@FDA, BLA 761069) en orden cronológico y si constan en la ficha europea (CIMA 4.1).",
                  c, " Drugs@FDA.")


# --- Lámina 6 -----------------------------------------------------------------------

def ficha(x, y, w, titulo, lineas, fuente, color):
    """Hallazgo con título, texto y fuente (país y año) en una franja de color."""
    alto = 46 + 21 * len(lineas) + 24
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{alto}" rx="10" fill="#FFFFFF" stroke="{COLOR["borde_panel"]}"/>'
         f'<rect x="{x}" y="{y}" width="6" height="{alto}" rx="3" fill="{color}"/>')
    s += texto(x + 22, y + 28, titulo, tam=16, peso="bold", color=color)
    s += texto(x + 22, y + 52, lineas, tam=15, interlineado=1.4)
    s += texto(x + 22, y + alto - 12, fuente, tam=12.5, color=SUAVE, cursiva=True)
    return s, alto + 10


def lamina_6():
    c = texto(40, 160, "¿Vale lo que cuesta? · Farmacoeconomía", tam=21, peso="bold", color=VERDE)
    y = 178
    for titulo, lineas, fuente in [
        ("Chile: impacto presupuestario (CPNM estadio III)",
         ["Sistema público: de US$ 1,27 millones el primer año a US$ 8,5", "millones el quinto, con ahorros parciales en otros gastos."],
         "Modelo de supervivencia particionada · PMID 39058755, 2024"),
        ("Brasil y otros 3 países: ¿costo-efectivo?",
         ["Brasil: US$ 141 146 por AVAC frente a un umbral de US$ 22 251;", "no fue costo-efectivo a ese precio (tampoco en EE. UU.)."],
         "Modelo de Markov con datos de PACIFIC · PMID 38814640, 2024"),
        ("Reino Unido (NICE): CPNM estadio III",
         ["Recomendado si PD-L1 ≥ 1 %, con acuerdo comercial (descuento", "confidencial). Precio de lista: £2 466 por vial de 500 mg."],
         "NICE TA798, 2022"),
        ("Reino Unido (NICE): vías biliares, con quimioterapia",
         ["Costo-efectividad estimada entre £20 000 y £30 000 por AVAC", "(con ponderación por gravedad); recomendado con descuento."],
         "NICE TA944, 2024"),
    ]:
        f, alto = ficha(40, y, 740, titulo, lineas, fuente, VERDE)
        c += f
        y += alto
    c += f'<line x1="800" y1="140" x2="800" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    c += texto(830, 160, "¿Funciona igual fuera del ensayo? · Vida real", tam=21, peso="bold", color=AZUL)
    y = 178
    for titulo, lineas, fuente in [
        ("Brasil (LACOG 0120): 31 pacientes, CPNM estadio III",
         ["Supervivencia global mediana de 34,9 meses, similar a PACIFIC;", "supervivencia libre de progresión menor (9,9 meses)."],
         "Programa de acceso expandido, 7 centros · PMID 39813498, 2025"),
        ("Internacional (PACIFIC-R): 1 153 pacientes",
         ["A 5 años, el 49,2 % seguía vivo; supervivencia global mediana", "de 59 meses."],
         "Cohorte observacional retrospectiva · PMID 41643268, 2026"),
    ]:
        f, alto = ficha(830, y, 730, titulo, lineas, fuente, AZUL)
        c += f
        y += alto
    c += (f'<rect x="830" y="{y + 4}" width="730" height="160" rx="12" fill="#FFF4EE" stroke="{NARANJA}" '
          f'stroke-width="1.4"/>')
    c += texto(852, y + 34, "Cómo leer estos datos", tam=16, peso="bold", color=NARANJA)
    c += texto(852, y + 58, ["• Precio, umbral y comparador cambian con el país y el año.",
                             "• Los estudios observacionales muestran asociaciones, no causas:",
                             "  confirman o matizan los ensayos, no los sustituyen.",
                             "• AVAC: año de vida ajustado por calidad; la razón de costo-",
                             "  efectividad compara el costo extra con los AVAC ganados."], tam=15, interlineado=1.4)
    return lamina(6, "Valor y vida real", "Del ensayo a la práctica: valor y vida real",
                  "Qué dicen las evaluaciones económicas y los estudios en la práctica clínica, con prioridad para Latinoamérica.",
                  c)


LAMINAS = {1: lamina_1, 2: lamina_2, 3: lamina_3, 4: lamina_4, 5: lamina_5, 6: lamina_6}

if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or sorted(LAMINAS):
        salida = Path(__file__).with_name(f"lamina-{n}.svg")
        salida.write_text(LAMINAS[n](), encoding="utf-8")
        print(salida)
