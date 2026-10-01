"""Trastuzumab deruxtecán en cinco láminas (plantilla: conjugado anticuerpo-fármaco).

1. HER2: la diana y los fármacos que actúan sobre ella.
2. Fisiología: señalización de HER2 y función de la topoisomerasa I.
3. Cómo actúa trastuzumab deruxtecán (estructuras reales PDB 1N8Z y 1K4T).
4. Del mecanismo al paciente.
5. Indicaciones aprobadas por la FDA: evolución y novedades, comparadas con la UE (CIMA).

Uso: python3 laminas.py [1 2 3 4 5]
"""
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))
sys.path.insert(0, str(RAIZ / "ejemplos" / "darolutamida"))
from componentes import COLOR, adn, bloqueo, etiqueta_farmaco, farmaco, flecha, paso, svg, texto, vesicula  # noqa: E402
from estructuras import estructura, formula, molecula  # noqa: E402
from fuentes import pdb_descargar  # noqa: E402
from recursos import ATRIBUCION, ilustracion  # noqa: E402
from superficie import como_imagen, superficie_complejo, superficie_corte  # noqa: E402
from laminas import guia, halo, leyenda_paso, nombre, nota_farmaco, tarjeta  # noqa: E402

ANCHO, ALTO = 1600, 900
SUAVE = COLOR["texto_suave"]
VERDE, AZUL, ROJO, NARANJA = COLOR["receptor_borde"], COLOR["farmaco"], COLOR["bloqueo"], COLOR["ligando_borde"]
LILA = COLOR["coactivador_borde"]

# SMILES de PubChem verificados por fórmula.
DXD = molecula("CC[C@@]1(C2=C(COC1=O)C(=O)N3CC4=C5[C@H](CCC6=C5C(=CC(=C6C)F)N=C4C3=C2)NC(=O)CO)O",
               "C26H24FN3O6")  # CID 117888634, carga útil liberada
TOPOTECAN = molecula("CC[C@@]1(C2=C(COC1=O)C(=O)N3CC4=CC5=C(C=CC(=C5CN(C)C)O)N=C4C3=C2)O", "C23H23N3O5")  # CID 60700

FUENTES = ("Fuentes: ficha técnica de Enhertu (CIMA-AEMPS); FDA (pertuzumab, T-DM1, lapatinib, tucatinib); UniProt "
           f"P04626, P11387; Reactome R-HSA-1227986; PMID 27166974. {ATRIBUCION}. Estructuras: RDKit/PubChem.")


def lamina(numero, etiqueta, titulo, subtitulo, contenido, extra=""):
    c = (f'<rect x="0" y="0" width="{ANCHO}" height="6" fill="{AZUL}"/>'
         + texto(40, 38, f"TRASTUZUMAB DERUXTECÁN · LÁMINA {numero} DE {len(LAMINAS)} · {etiqueta.upper()}", tam=14, peso="bold",
                 color=AZUL)
         + texto(40, 76, titulo, tam=32, peso="bold") + texto(40, 104, subtitulo, tam=17, color=SUAVE)
         + contenido + texto(40, ALTO - 34, FUENTES + extra, tam=12.5, color=SUAVE)
         + texto(40, ALTO - 14, "Esquema simplificado y sin escala · Prototipo pendiente de revisión farmacológica",
                 tam=12.5, color=ROJO, peso="bold"))
    return svg(ANCHO, ALTO, c, f"Trastuzumab deruxtecán, lámina {numero}: {titulo}", subtitulo)


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


def her2(x, y, color="#5DB58F", borde="#2E7D5B", activo=False, etiqueta=True):
    """HER2: cuatro subdominios extracelulares, segmento transmembrana y dominio cinasa."""
    s = ""
    for i, (dy, rx) in enumerate(((-86, 15), (-64, 12), (-44, 15), (-24, 11))):
        s += (f'<ellipse cx="{x}" cy="{y + dy}" rx="{rx}" ry="10" fill="{color}" stroke="{borde}" stroke-width="1.4"/>')
    s += f'<rect x="{x - 3}" y="{y - 14}" width="6" height="28" fill="{borde}"/>'
    s += f'<rect x="{x - 14}" y="{y + 14}" width="28" height="34" rx="9" fill="{color}" stroke="{borde}" stroke-width="1.4"/>'
    if activo:
        s += "".join(f'<circle cx="{x + dx}" cy="{y + 52}" r="5" fill="#F2B84B" stroke="#9A6A00"/>'
                     f'<text x="{x + dx}" y="{y + 55}" font-size="7" text-anchor="middle" fill="#5A3E00" '
                     f'font-family="Arial" font-weight="bold">P</text>' for dx in (-8, 8))
    if etiqueta:
        s += texto(x, y - 104, "HER2", tam=12, peso="bold", anclaje="middle", color=borde)
    return s


def anticuerpo(x, y, w=60, invertido=False, opacidad=1.0, girar=0):
    """Anticuerpo IgG (Servier). invertido=True: brazos (Fab) hacia abajo, como al unirse a un receptor."""
    h = w * 82 / 66.935
    return ilustracion("servier-antibody-3-recortado.svg", x - w / 2, y - h / 2, w, h, opacidad=opacidad,
                       girar=180 + girar if invertido else girar)


def adc(x, y, w=70, n=4, opacidad=1.0, invertido=False):
    """Trastuzumab deruxtecán: anticuerpo con moléculas de DXd (rombos azules) en los brazos."""
    s = anticuerpo(x, y, w, invertido, opacidad)
    signo = -1 if invertido else 1
    for i in range(n):
        lado = -1 if i % 2 == 0 else 1
        s += farmaco(x + lado * w * (0.24 + 0.1 * (i // 2)), y - signo * w * (0.12 + 0.16 * (i // 2)), "", s=6)
    return s


def cola_flecha(x1, y1, x2, y2, etiqueta=None):
    s = flecha([(x1, y1), (x2, y2)])
    if etiqueta:
        s += texto((x1 + x2) / 2 + 8, (y1 + y2) / 2, etiqueta, tam=13, color=SUAVE)
    return s


# --- Lámina 1 ------------------------------------------------------------------------

def lamina_1():
    c = texto(40, 168, "Exterior de la célula", tam=15, color=SUAVE, cursiva=True)
    c += membrana(40, 1560, 380)
    c += texto(1560, 560, "Citoplasma de la célula tumoral", tam=15, color=SUAVE, cursiva=True, anclaje="end")
    xs = (230, 330, 560, 780, 1000, 1240)
    for x in xs:
        c += her2(x, 380, etiqueta=False)
    c += texto(330, 250, "HER2 sobreexpresado", tam=15, peso="bold", anclaje="middle", color=VERDE)
    c += texto(330, 270, "(amplificación del gen ERBB2)", tam=13, anclaje="middle", color=SUAVE)
    # Fármacos sobre HER2
    c += anticuerpo(560, 252, 46, invertido=True)
    c += etiqueta_farmaco(450, 190, "Trastuzumab: subdominio IV")
    c += anticuerpo(800, 286, 46, invertido=True, girar=-35)
    c += etiqueta_farmaco(640, 140, "Pertuzumab: subdominio II (dimerización)")
    c += adc(1000, 252, 46, invertido=True)
    c += etiqueta_farmaco(900, 190, "T-DM1: ADC con DM1 (microtúbulos)")
    c += adc(1240, 252, 46, invertido=True)
    c += etiqueta_farmaco(1150, 140, "Trastuzumab deruxtecán: ADC con DXd", destacado=True)
    c += farmaco(780, 470, "", s=10) + farmaco(1000, 470, "", s=10)
    c += etiqueta_farmaco(650, 500, "Lapatinib, tucatinib: inhiben la cinasa (intracelular)")
    # Señalización
    c += flecha([(230, 440), (230, 560)]) + flecha([(330, 440), (330, 560)])
    c += (f'<rect x="150" y="566" width="260" height="70" rx="12" fill="#FFFFFF" stroke="{VERDE}" stroke-width="1.5"/>')
    c += texto(280, 594, "Vías MAPK y PI3K/AKT", tam=16, peso="bold", anclaje="middle", color=VERDE)
    c += texto(280, 618, "proliferación y supervivencia", tam=14, anclaje="middle", color=SUAVE)
    c += (f'<rect x="40" y="716" width="1520" height="96" rx="14" fill="#E3F0F8" stroke="{AZUL}" stroke-width="1.5"/>')
    c += texto(66, 754, "Idea clave", tam=18, peso="bold", color=AZUL)
    c += texto(66, 784, "Trastuzumab deruxtecán usa HER2 como «dirección de entrega»: el anticuerpo lleva un citotóxico "
                        "(DXd) al interior de la célula que expresa HER2.", tam=18)
    return lamina(1, "Contexto", "HER2: la diana y los fármacos que actúan sobre ella",
                  "HER2 es un receptor tirosina cinasa de membrana; en algunos tumores está aumentado y estimula su crecimiento.", c)


# --- Lámina 2 ------------------------------------------------------------------------

def lamina_2():
    c = texto(40, 160, "A · HER2 en la membrana", tam=21, peso="bold")
    c += membrana(40, 760, 330)
    c += her2(300, 330, activo=True) + her2(370, 330, color="#9CB8D9", borde="#4A6A9A", activo=True, etiqueta=False)
    c += texto(370, 226, "HER3", tam=12, peso="bold", anclaje="middle", color="#4A6A9A")
    c += f'<circle cx="398" cy="248" r="9" fill="{COLOR["ligando"]}" stroke="{NARANJA}"/>'
    c += texto(412, 244, "ligando (neurregulina)", tam=12, color=NARANJA)
    c += flecha([(335, 410), (335, 470)])
    c += (f'<rect x="200" y="474" width="270" height="62" rx="12" fill="#FFFFFF" stroke="{VERDE}" stroke-width="1.5"/>')
    c += texto(335, 500, "MAPK y PI3K/AKT", tam=16, peso="bold", anclaje="middle", color=VERDE)
    c += texto(335, 522, "↑ proliferación y supervivencia", tam=14, anclaje="middle", color=SUAVE)
    c += leyenda_paso(60, 610, 1, "HER2 no tiene ligando propio", ["Actúa formando dímeros con otros receptores",
                                                                   "HER (EGFR, HER3, HER4) que sí lo tienen."])
    c += leyenda_paso(60, 700, 2, "El dímero se fosforila", ["y activa las vías MAPK y PI3K/AKT."])
    c += f'<line x1="800" y1="140" x2="800" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    c += texto(830, 160, "B · Topoisomerasa I en el núcleo", tam=21, peso="bold")
    c += ilustracion("nucleus", 830, 180, 720, 420, ajustar="none")
    c += adn(900, 1480, 410, region=(1140, 1240), etiqueta_region="")
    c += ilustracion("protein-12", 1140, 300, 100, 80)
    c += texto(1260, 300, "Topoisomerasa I", tam=14, peso="bold", anclaje="start", color="#1F5F8B")
    c += leyenda_paso(840, 650, 1, "Corta una hebra del ADN", ["y queda unida a ella de forma transitoria."])
    c += leyenda_paso(840, 720, 2, "La hebra gira y libera la tensión", ["que generan la replicación y la transcripción."])
    c += leyenda_paso(840, 790, 3, "Vuelve a unir la hebra", ["El ADN queda íntegro."])
    return lamina(2, "Fisiología normal", "Señalización de HER2 y función de la topoisomerasa I",
                  "Las dos proteínas que usa el fármaco: HER2 para entrar en la célula y la topoisomerasa I como blanco.", c)


# --- Lámina 3 ------------------------------------------------------------------------

_HER2 = superficie_complejo(pdb_descargar("1N8Z"), [("C", "#7FC8A9"), ("AB", "#E9A6C0")])
_TOP1 = superficie_corte(pdb_descargar("1K4T"), "ABCD", "TTC", cadena_ligando="D", color_ligando="#0072B2",
                         colores_cadena={"A": "#9CB8D9", "B": "#C9B3DD", "C": "#C9B3DD", "D": "#C9B3DD"},
                         radio_vista=18)[0]


def lamina_3():
    c = texto(40, 160, "El conjugado anticuerpo-fármaco", tam=21, peso="bold")
    c += adc(130, 300, 110, n=6)
    c += texto(230, 216, ["Anticuerpo IgG1 anti-HER2", "(misma secuencia que trastuzumab)"], tam=14, color="#B0476E")
    c += texto(230, 268, ["Enlazador tetrapeptídico", "escindible"], tam=14, color=SUAVE)
    c += texto(230, 318, ["~8 moléculas de DXd por", "anticuerpo (inhibidor de la", "topoisomerasa I)"], tam=14,
               color=AZUL, peso="bold")
    c += halo(36, 390, 230, 120, AZUL) + estructura(DXD, 40, 394, 222, 96)
    c += texto(151, 506, f"DXd · {formula(DXD)}", tam=13, anclaje="middle", color=AZUL, peso="bold")
    c += como_imagen(_HER2, 290, 380, 230, 150)
    c += texto(405, 546, ["HER2 (verde) + Fab de", "trastuzumab (rosa) · PDB 1N8Z"], tam=12.5, anclaje="middle",
               color=SUAVE, cursiva=True)
    c += como_imagen(_TOP1, 560, 380, 200, 150)
    c += texto(660, 546, ["Topoisomerasa I + ADN +", "topotecán · PDB 1K4T"], tam=12.5, anclaje="middle",
               color=SUAVE, cursiva=True)
    c += halo(560, 600, 200, 104, AZUL) + estructura(TOPOTECAN, 564, 604, 192, 80)
    c += texto(660, 720, "Topotecán: misma familia que DXd", tam=12.5, anclaje="middle", color=AZUL, peso="bold")
    c += texto(40, 620, ["No hay estructura publicada de la", "topoisomerasa I con DXd: se muestra", "topotecán, otro derivado de la",
                         "camptotecina, en el mismo sitio."], tam=14, color=SUAVE)
    c += f'<line x1="800" y1="140" x2="800" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    # Recorrido en la célula
    c += texto(830, 160, "En la célula tumoral", tam=21, peso="bold")
    c += ilustracion("emptycell-3d-1", 826, 176, 580, 520, ajustar="none")
    c += her2(1000, 318, etiqueta=False) + adc(1000, 196, 40, invertido=True)
    c += paso(1050, 196, 1, radio=12, tam=13)
    c += vesicula(1040, 410, 22) + adc(1040, 410, 22, n=2, invertido=True)
    c += cola_flecha(1006, 370, 1024, 392) + paso(1080, 396, 2, radio=12, tam=13)
    c += (f'<circle cx="1150" cy="480" r="28" fill="#F7D9E6" stroke="#B0476E" stroke-width="2"/>')
    c += texto(1150, 522, "lisosoma", tam=12, anclaje="middle", color="#B0476E", cursiva=True)
    c += farmaco(1142, 474, "", s=6) + farmaco(1160, 486, "", s=6)
    c += cola_flecha(1058, 428, 1124, 466) + paso(1194, 462, 3, radio=12, tam=13)
    c += ilustracion("nucleus", 1120, 540, 240, 140, ajustar="none")
    c += farmaco(1225, 610, "", s=7) + bloqueo(1255, 610, r=10)
    c += cola_flecha(1170, 506, 1210, 580) + paso(1290, 590, 4, radio=12, tam=13)
    # Efecto espectador
    c += ilustracion("cancerous-cell-3", 1410, 380, 150, 150)
    c += farmaco(1380, 360, "", s=7) + flecha([(1300, 400), (1400, 420)], discontinua=True)
    c += paso(1350, 386, 5, radio=12, tam=13)
    c += texto(1485, 556, "célula vecina sin HER2", tam=12, anclaje="middle", color=SUAVE, cursiva=True)
    c += leyenda_paso(830, 734, 1, "Se une a HER2", ["y se internaliza (2)"])
    c += leyenda_paso(1060, 734, 3, "En el lisosoma", ["las enzimas cortan el", "enlazador: sale DXd"])
    c += leyenda_paso(1300, 734, 4, "DXd daña el ADN", ["→ apoptosis. (5) Efecto", "espectador en vecinas"])
    return lamina(3, "Mecanismo de acción", "Cómo actúa trastuzumab deruxtecán",
                  "Conjugado anticuerpo-fármaco: el anticuerpo anti-HER2 entrega DXd, un inhibidor de la topoisomerasa I.",
                  c, " PDB 1N8Z, 1K4T.")


# --- Lámina 4 ------------------------------------------------------------------------

def lamina_4():
    w, h = 752, 336
    x1, x2, y1, y2 = 40, 808, 136, 488
    c = tarjeta(x1, y1, w, h, VERDE, "Efecto terapéutico", [
        "• Muerte de la célula tumoral por apoptosis tras el",
        "  daño del ADN; además, citotoxicidad mediada por",
        "  anticuerpos e inhibición de la vía PI3K.",
        "• Indicado (monoterapia) en cáncer de mama HER2+,",
        "  HER2-bajo y HER2-muy bajo; CPNM con mutación de",
        "  HER2; cáncer gástrico; tumores sólidos HER2 3+."],
        ilustracion("cancerous-cell-1", x1 + w - 150, y1 + 20, 120, 118))
    c += tarjeta(x2, y1, w, h, ROJO, "Error frecuente", [
        "«Es lo mismo que trastuzumab.»",
        "Falso: comparte el anticuerpo, pero lleva ~8",
        "moléculas de un citotóxico. No son intercambiables:",
        "la ficha pide comprobar el vial para no confundirlo",
        "con trastuzumab ni con trastuzumab emtansina.",
        "",
        "Para pensar: ¿por qué puede actuar en tumores con",
        "poca expresión de HER2?"],
        adc(x2 + w - 80, y1 + 90, 64))
    c += tarjeta(x1, y2, w, h, AZUL, "Farmacocinética e interacciones", [
        "• Perfusión intravenosa; semivida de ~7 días",
        "  (conjugado y DXd liberado).",
        "• El anticuerpo se degrada como una IgG; DXd se",
        "  metaboliza sobre todo por CYP3A4.",
        "• Ritonavir o itraconazol aumentan la exposición solo",
        "  un 10–20 %: no se ajusta la dosis.",
        "• DXd se une a proteínas plasmáticas en ~97 %."], "")
    c += tarjeta(x2, y2, w, h, COLOR["enzima_borde"], "Efectos adversos", [
        "• ⚠ Enfermedad pulmonar intersticial / neumonitis,",
        "  con casos mortales: consultar ante tos, disnea o",
        "  fiebre.",
        "• Más frecuentes: náuseas (70 %), fatiga (57 %),",
        "  vómitos, neutropenia, anemia, alopecia.",
        "• Embarazo: verificar antes de iniciar y usar",
        "  anticoncepción eficaz."], "")
    return lamina(4, "Aplicación clínica", "Del mecanismo al paciente",
                  "Qué significa entregar un inhibidor de la topoisomerasa I a las células con HER2.", c)


# --- Lámina 5 -----------------------------------------------------------------------

# Aprobaciones de la FDA (Drugs@FDA, BLA 761139; cartas de aprobación) y si constan en la ficha de CIMA 4.1.
HITOS = [
    ("12/2019", ["Mama HER2+ metastásico", "tras ≥ 2 pautas anti-HER2", "(aprobación acelerada)"], True),
    ("01/2021", ["Gástrico o de la unión", "gastroesofágica HER2+", "tras trastuzumab"], True),
    ("05/2022", ["Mama HER2+ metastásico", "tras 1 pauta anti-HER2", "(aprobación regular)"], True),
    ("08/2022", ["Mama HER2-bajo tras", "quimioterapia; pulmón", "con mutación de HER2"], True),
    ("04/2024", ["Tumores sólidos HER2", "IHC 3+ sin otras", "opciones (acelerada)"], True),
    ("01/2025", ["Mama RH+, HER2-bajo", "o HER2-ultrabajo tras", "terapia endocrina"], True),
    ("12/2025", ["Mama HER2+ metastásico:", "primera línea con", "pertuzumab"], False),
    ("05/2026", ["Mama HER2+ temprana:", "neoadyuvante (antes de", "THP) y adyuvante"], False),
]


def lamina_5():
    x0, x1, y = 110, 1490, 400
    c = f'<line x1="{x0 - 50}" y1="{y}" x2="{x1 + 50}" y2="{y}" stroke="{COLOR["borde_panel"]}" stroke-width="6" ' \
        f'stroke-linecap="round"/>'
    c += texto(x0 - 50, 600, "← Al principio: enfermedad metastásica ya tratada", tam=14, color=SUAVE, cursiva=True)
    c += texto(x1 + 50, 600, "Ahora: primera línea y enfermedad temprana →", tam=14, color=SUAVE, cursiva=True,
               anclaje="end")
    paso_x = (x1 - x0) / (len(HITOS) - 1)
    for i, (fecha, lineas, ue) in enumerate(HITOS):
        x = x0 + i * paso_x
        color = AZUL if ue else NARANJA
        arriba = i % 2 == 0
        y_txt = 196 if arriba else 470
        c += f'<line x1="{x:.0f}" y1="{y}" x2="{x:.0f}" y2="{(y_txt + 92) if arriba else (y_txt - 50)}" ' \
             f'stroke="{color}" stroke-width="1.6" stroke-dasharray="4 4"/>'
        c += f'<circle cx="{x:.0f}" cy="{y}" r="13" fill="#FFFFFF" stroke="{color}" stroke-width="4"/>'
        c += texto(x, y_txt, fecha, tam=18, peso="bold", anclaje="middle", color=color)
        c += texto(x, y_txt + 24, lineas, tam=14, anclaje="middle", interlineado=1.3)
        etiqueta = "UE: sí" if ue else "UE: aún no"
        c += (f'<rect x="{x - 44:.0f}" y="{(y_txt - 46)}" width="88" height="24" rx="12" fill="{color}" '
              f'fill-opacity="{0.14 if ue else 0.18}"/>')
        c += texto(x, y_txt - 29, etiqueta, tam=12.5, peso="bold", anclaje="middle", color=color)
    c += tarjeta(40, 640, 740, 186, NARANJA, "Lo último (FDA)", [
        "12/2025: con pertuzumab en primera línea del cáncer de mama",
        "HER2+ metastásico. 05/2026: neoadyuvante y adyuvante (con",
        "enfermedad residual) en cáncer de mama HER2+ temprano."])
    c += tarjeta(820, 640, 740, 186, AZUL, "Cómo leer esta lámina", [
        "La FDA y la EMA aprueban por separado y en fechas distintas.",
        "«UE: aún no» = no figura en la ficha de CIMA consultada.",
        "En Costa Rica rige el registro sanitario nacional."])
    return lamina(5, "Indicaciones", "Indicaciones aprobadas: de la enfermedad avanzada a la temprana",
                  "Aprobaciones de la FDA (Drugs@FDA, BLA 761139) en orden cronológico y si ya constan en la ficha europea (CIMA 4.1).",
                  c, " Drugs@FDA.")


LAMINAS = {1: lamina_1, 2: lamina_2, 3: lamina_3, 4: lamina_4, 5: lamina_5}

if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or sorted(LAMINAS):
        salida = Path(__file__).with_name(f"lamina-{n}.svg")
        salida.write_text(LAMINAS[n](), encoding="utf-8")
        print(salida)
