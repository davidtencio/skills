"""Diabetes tipo 2 en nueve láminas (plantilla: enfermedad metabólica con varios órganos).

1. Contexto: ocho defectos que elevan la glucosa.
2. Fisiología: cómo secreta insulina la célula β.
3. Fisiología: qué hace la insulina en músculo, tejido adiposo e hígado.
4. Fisiopatología: resistencia a la insulina.
5. Fisiopatología: la célula β no compensa y otros cuatro defectos.
6. Clínica: síntomas y complicaciones.
7. Diagnóstico: criterios y confirmación.
8. Tratamiento: dónde actúa cada grupo de fármacos.
9. Tratamiento: estrategia según el riesgo cardiorrenal.

Uso: python3 laminas.py [1 ... 9]
"""
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))
from componentes import COLOR, bloqueo, enzima, etiqueta_farmaco, flecha, mitocondria, paso, texto, vesicula  # noqa: E402
from recursos import ATRIBUCION, ilustracion  # noqa: E402
from piezas import (AZUL, LILA, NARANJA, ROJO, SUAVE, VERDE, Lamina, caja, leyenda_paso, membrana,  # noqa: E402
                    tarjeta)

INSULINA = "#CC79A7"
L = Lamina("DIABETES TIPO 2", "Fuentes: Normas de Atención de la ADA 2026 (Diabetes Care, supl. 1); DeFronzo 2009 (PMID 19336687); "
           f"Reactome R-HSA-422356, R-HSA-74752; UniProt; ADA y NIDDK (diagnóstico); OMS; FDA. {ATRIBUCION}.")


def lamina(n, etiqueta, titulo, subtitulo, contenido, extra=""):
    return L.dibujar(n, etiqueta, titulo, subtitulo, contenido, total=len(LAMINAS), extra=extra)


# --- Piezas propias --------------------------------------------------------------------

def glucosa(x, y, r=8):
    """Glucosa: hexágono naranja (ligando endógeno)."""
    return (f'<path d="M{x - r},{y} L{x - r / 2},{y - r * .87} L{x + r / 2},{y - r * .87} L{x + r},{y} '
            f'L{x + r / 2},{y + r * .87} L{x - r / 2},{y + r * .87} Z" fill="{COLOR["ligando"]}" '
            f'stroke="{NARANJA}" stroke-width="1.3"/>')


def insulina(x, y, r=6):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{INSULINA}" stroke="#8A3F7A" stroke-width="1.2"/>'


def transportador(x, y, etiqueta, color="#7FC8A9", borde=VERDE, abierto=True):
    """Transportador o canal en una membrana horizontal (y = centro de la membrana)."""
    s = (f'<rect x="{x - 14}" y="{y - 22}" width="12" height="44" rx="5" fill="{color}" stroke="{borde}" stroke-width="1.4"/>'
         f'<rect x="{x + 2}" y="{y - 22}" width="12" height="44" rx="5" fill="{color}" stroke="{borde}" stroke-width="1.4"/>')
    if not abierto:
        s += f'<rect x="{x - 3}" y="{y - 10}" width="6" height="20" fill="{borde}"/>'
    s += texto(x + 20, y + 44, etiqueta, tam=13, peso="bold", color=borde)
    return s


def receptor(x, y, etiqueta, color=VERDE):
    """Receptor de membrana con dominio extracelular hacia arriba."""
    return (f'<rect x="{x - 3}" y="{y - 24}" width="6" height="48" fill="{color}"/>'
            f'<path d="M{x - 16},{y - 24} C{x - 18},{y - 48} {x + 18},{y - 48} {x + 16},{y - 24} Z" fill="#BFE6D8" '
            f'stroke="{color}" stroke-width="1.5"/>'
            + texto(x, y + 40, etiqueta, tam=13, peso="bold", anclaje="middle", color=color))


def nodo(x, y, icono, titulo, efecto, color=ROJO, w=84, h=84):
    """Órgano del octeto: ilustración, nombre y defecto."""
    return (ilustracion(icono, x, y, w, h) + texto(x + w + 14, y + 34, titulo, tam=17, peso="bold")
            + texto(x + w + 14, y + 58, efecto, tam=15, color=color, peso="bold"))


OCTETO = [  # (icono, órgano, defecto, lado, fila)
    ("servier-langerhans-islet-pancreas.svg", "Célula β (islote)", "↓ secreción de insulina", 0, 0),
    ("servier4-higado.svg", "Hígado", "↑ producción de glucosa", 0, 1),
    ("servier-muscle-1.svg", "Músculo", "↓ captación de glucosa", 0, 2),
    ("servier-adipocyte-2.svg", "Tejido adiposo", "↑ lipólisis", 0, 3),
    ("servier-pancreas-2.svg", "Célula α (islote)", "↑ glucagón", 1, 0),
    ("servier4-intestino-delgado.svg", "Intestino", "↓ efecto incretina", 1, 1),
    ("servier-kidney-2.svg", "Riñón", "↑ reabsorción de glucosa", 1, 2),
    ("brain-2", "Cerebro", "resistencia a la insulina", 1, 3),
]


def posicion(lado, fila):
    return (60 if lado == 0 else 1110), 140 + fila * 145


# --- Lámina 1 ------------------------------------------------------------------------

def lamina_1():
    cx, cy = 800, 390
    c = ""
    for icono, organo, defecto, lado, fila in OCTETO:
        x, y = posicion(lado, fila)
        c += nodo(x, y, icono, organo, defecto)
        x0 = x + 330 if lado == 0 else x - 20
        c += flecha([(x0, y + 42), (cx - 120 if lado == 0 else cx + 120, cy + (fila - 1.5) * 40)])
    c += f'<circle cx="{cx}" cy="{cy}" r="110" fill="#FDEBD3" stroke="{NARANJA}" stroke-width="3"/>'
    c += texto(cx, cy - 8, "Hiperglucemia", tam=24, peso="bold", anclaje="middle", color=NARANJA)
    c += glucosa(cx - 30, cy + 34) + glucosa(cx, cy + 40) + glucosa(cx + 30, cy + 34)
    c += texto(cx, 168, "Triunvirato clásico: célula β, hígado, músculo", tam=14, anclaje="middle", color=SUAVE, cursiva=True)
    c += texto(cx, 190, "y cinco defectos más completan el octeto", tam=14, anclaje="middle", color=SUAVE, cursiva=True)
    c += (f'<rect x="40" y="716" width="1520" height="100" rx="14" fill="#E3F0F8" stroke="{AZUL}" stroke-width="1.5"/>')
    c += texto(66, 750, "Idea clave", tam=18, peso="bold", color=AZUL)
    c += texto(66, 780, "En el tercil superior de la intolerancia a la glucosa, la resistencia a la insulina ya es casi máxima y se ha perdido el 80–85 % "
                        "de la función de la célula β.", tam=17)
    c += texto(66, 804, "Varios defectos piden varios fármacos combinados.", tam=17)
    return lamina(1, "Contexto", "Ocho defectos que elevan la glucosa",
                  "La diabetes tipo 2 no es un solo fallo: ocho órganos contribuyen a la hiperglucemia (el «octeto»).", c)


# --- Lámina 2 ------------------------------------------------------------------------

def lamina_2():
    y_m = 250
    c = texto(1010, 214, "sangre", tam=14, cursiva=True, color=SUAVE, anclaje="end")
    c += (f'<rect x="60" y="{y_m}" width="940" height="580" rx="0" fill="url(#g_citoplasma)" stroke="none"/>')
    c += membrana(60, 1000, y_m)
    c += texto(1000, 300, "célula β", tam=15, peso="bold", anclaje="end", color=LILA)
    # Glucosa entra por GLUT2
    c += glucosa(150, 190) + glucosa(180, 210) + flecha([(170, 222), (170, 300)])
    c += transportador(170, y_m, "GLUT2")
    c += glucosa(170, 320)
    c += enzima(170, 400, "Glucocinasa", r=26)
    c += flecha([(198, 404), (268, 430)])
    c += mitocondria(320, 450, largo=90, ancho=40, angulo=-10)
    c += texto(320, 500, "↑ ATP", tam=17, peso="bold", anclaje="middle", color=VERDE)
    # K-ATP se cierra
    c += flecha([(360, 430), (470, 300)])
    c += transportador(480, y_m, "K-ATP", color="#F6D6C8", borde=ROJO, abierto=False)
    c += bloqueo(480, 196, r=12)
    c += texto(480, 172, "se cierra", tam=13, anclaje="middle", color=ROJO, peso="bold")
    c += texto(560, 390, ["despolarización", "de la membrana"], tam=15, anclaje="middle", color=SUAVE, cursiva=True)
    c += flecha([(520, 360), (650, 300)])
    # Canal de calcio se abre
    c += transportador(670, y_m, "Ca²⁺ (voltaje)", color="#DCD3F0", borde=LILA)
    c += flecha([(670, 180), (670, 300)])
    c += texto(700, 196, "Ca²⁺", tam=15, peso="bold", color=LILA)
    # Exocitosis
    c += vesicula(800, 420, 22, carga=5) + vesicula(860, 470, 22, carga=5)
    c += flecha([(820, 400), (860, 290)])
    c += insulina(870, 220) + insulina(890, 200) + insulina(905, 225)
    c += texto(905, 180, "insulina", tam=15, peso="bold", color="#8A3F7A")
    # Incretinas
    c += receptor(320, y_m, "GLP-1R / GIPR", color=AZUL)
    c += f'<circle cx="320" cy="198" r="7" fill="{COLOR["ligando"]}" stroke="{NARANJA}"/>'
    c += texto(320, 160, "GLP-1, GIP", tam=13, peso="bold", anclaje="middle", color=NARANJA)
    c += texto(300, 600, "AMPc amplifica la exocitosis", tam=15, peso="bold", color=AZUL)
    c += flecha([(340, 590), (780, 470)], discontinua=True)
    # Pasos
    c += f'<line x1="1060" y1="140" x2="1060" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    for i, (t, d) in enumerate([("La glucosa entra por GLUT2", ["y la glucocinasa la fosforila:", "es el sensor de glucosa."]),
                                ("Su metabolismo eleva el ATP", ["en la mitocondria."]),
                                ("El ATP cierra el canal K-ATP", ["y la membrana se despolariza."]),
                                ("Se abren canales de Ca²⁺", ["dependientes de voltaje."]),
                                ("El Ca²⁺ libera insulina", ["en dos fases."]),
                                ("GLP-1 y GIP la amplifican", ["vía AMPc, solo si hay glucosa."])], 1):
        c += leyenda_paso(1080, 130 + i * 112, i, t, d)
    return lamina(2, "Fisiología normal", "Cómo secreta insulina la célula β",
                  "La glucosa es a la vez el estímulo y la señal: su metabolismo cierra un canal de potasio y abre uno de calcio.", c)


# --- Lámina 3 ------------------------------------------------------------------------

def lamina_3():
    y_m = 260
    c = texto(40, 160, "En el músculo y el tejido adiposo", tam=21, peso="bold")
    c += membrana(40, 900, y_m)
    c += insulina(170, 196) + receptor(170, y_m, "", color=VERDE)
    c += texto(200, 214, "Receptor de insulina", tam=14, peso="bold", color=VERDE)
    c += (f'<circle cx="184" cy="292" r="9" fill="#F2B84B" stroke="#9A6A00"/>'
          + texto(184, 296, "P", tam=11, peso="bold", anclaje="middle"))
    c += flecha([(170, 320), (170, 370)])
    c += caja(100, 376, 140, 52, "IRS", "", VERDE)
    c += flecha([(240, 402), (300, 402)])
    c += caja(300, 376, 140, 52, "PI3K → AKT", "", VERDE)
    c += flecha([(440, 402), (520, 402)])
    c += vesicula(570, 440, 26) + vesicula(630, 470, 26)
    c += texto(600, 520, "vesículas con GLUT4", tam=14, anclaje="middle", color=SUAVE, cursiva=True)
    c += flecha([(600, 410), (640, 300)])
    c += transportador(660, y_m, "GLUT4")
    c += glucosa(640, 190) + glucosa(680, 205) + flecha([(660, 218), (660, 330)])
    c += glucosa(660, 350)
    c += texto(720, 380, ["la glucosa", "entra a la célula"], tam=15, peso="bold", color=VERDE)
    c += leyenda_paso(60, 600, 1, "La insulina activa su receptor", ["tirosina cinasa que fosforila IRS."])
    c += leyenda_paso(60, 690, 2, "IRS activa PI3K y AKT", ["cascada de señalización intracelular."])
    c += leyenda_paso(480, 600, 3, "GLUT4 va a la membrana", ["desde vesículas internas."])
    c += leyenda_paso(480, 690, 4, "Entra la glucosa", ["y baja la glucemia posprandial."])
    c += f'<line x1="930" y1="140" x2="930" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    c += tarjeta(960, 150, 600, 300, VERDE, "En el hígado", [
        "• Inhibe la producción hepática", "  de glucosa.",
        "• En la diabetes tipo 2 este freno", "  falla (lámina 4)."],
        ilustracion("servier4-higado.svg", 1440, 170, 100, 90))
    c += tarjeta(960, 480, 600, 300, VERDE, "En el tejido adiposo", [
        "• Inhibe la lipólisis: bajan los ácidos", "  grasos libres en sangre.",
        "• También aumenta la captación de", "  glucosa por GLUT4."],
        ilustracion("servier-adipocyte-2.svg", 1450, 500, 90, 80))
    return lamina(3, "Fisiología normal", "Qué hace la insulina en el músculo, el tejido adiposo y el hígado",
                  "Tres tejidos responden a la insulina: dos captan glucosa y el hígado deja de producirla.", c)


# --- Lámina 4 ------------------------------------------------------------------------

def lamina_4():
    w, h = 490, 360
    c = ""
    for i, (icono, titulo, lineas) in enumerate([
        ("servier4-higado.svg", "Hígado", ["Produce glucosa en ayunas", "pese a la hiperinsulinemia", "y no frena esa producción",
                                          "después de comer.", "", "→ glucemia en ayunas alta"]),
        ("servier-muscle-1.svg", "Músculo", ["Capta menos glucosa tras", "una comida con hidratos", "de carbono.", "", "",
                                             "→ glucemia posprandial alta"]),
        ("servier-adipocyte-2.svg", "Tejido adiposo", ["Lipólisis acelerada: más", "ácidos grasos libres, que",
                                                       "empeoran la resistencia", "en hígado y músculo y dañan",
                                                       "la célula β (lipotoxicidad).", "→ círculo vicioso"])]):
        x = 40 + i * (w + 25)
        c += tarjeta(x, 150, w, h, ROJO, titulo, lineas, ilustracion(icono, x + w - 120, 168, 96, 86), tam=20)
    c += (f'<rect x="40" y="545" width="1520" height="250" rx="14" fill="#FDF0EA" stroke="{ROJO}" stroke-width="1.5"/>')
    c += texto(70, 590, "Qué significa «resistencia a la insulina»", tam=21, peso="bold", color=ROJO)
    c += insulina(96, 670, 9) + insulina(124, 684, 9) + insulina(150, 664, 9) + insulina(178, 686, 9) + insulina(204, 670, 9)
    c += flecha([(230, 676), (330, 676)], discontinua=True)
    c += receptor(370, 700, "", color=ROJO)
    c += texto(430, 640, ["Hay insulina (al principio, incluso más de lo normal), pero la señal a través de su receptor",
                          "es débil: la misma insulina consigue menos captación de glucosa en el músculo y menos",
                          "freno de la producción de glucosa en el hígado.",
                          "La célula β compensa secretando más insulina, mientras puede (lámina 5)."],
               tam=18, interlineado=1.45)
    return lamina(4, "Fisiopatología", "Resistencia a la insulina: tres tejidos que no responden",
                  "Hígado, músculo y tejido adiposo necesitan más insulina para conseguir el mismo efecto.", c)


# --- Lámina 5 ------------------------------------------------------------------------

def lamina_5():
    c = texto(40, 160, "La célula β se agota", tam=21, peso="bold")
    x0, y0, w, h = 90, 200, 620, 330
    c += f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 + h}" stroke="{COLOR["linea"]}" stroke-width="2"/>'
    c += f'<line x1="{x0}" y1="{y0 + h}" x2="{x0 + w}" y2="{y0 + h}" stroke="{COLOR["linea"]}" stroke-width="2"/>'
    c += texto(x0 + w, y0 + h + 28, "tiempo →", tam=14, anclaje="end", color=SUAVE)
    c += texto(x0 + 10, y0 + h + 28, "normal", tam=13, color=SUAVE)
    c += texto(x0 + 300, y0 + h + 28, "intolerancia", tam=13, anclaje="middle", color=SUAVE)
    c += texto(x0 + 520, y0 + h + 28, "diabetes", tam=13, anclaje="middle", color=SUAVE)
    c += (f'<path d="M{x0 + 10},{y0 + 280} C{x0 + 200},{y0 + 270} {x0 + 260},{y0 + 60} {x0 + 610},{y0 + 50}" fill="none" '
          f'stroke="{ROJO}" stroke-width="3.4"/>')
    c += texto(x0 + 380, y0 + 40, "resistencia a la insulina", tam=14, peso="bold", color=ROJO)
    c += (f'<path d="M{x0 + 10},{y0 + 60} C{x0 + 150},{y0 + 70} {x0 + 260},{y0 + 250} {x0 + 610},{y0 + 300}" fill="none" '
          f'stroke="{INSULINA}" stroke-width="3.4"/>')
    c += texto(x0 + 20, y0 + 40, "función de la célula β", tam=14, peso="bold", color="#8A3F7A")
    c += f'<line x1="{x0 + 300}" y1="{y0}" x2="{x0 + 300}" y2="{y0 + h}" stroke="{SUAVE}" stroke-dasharray="5 5"/>'
    c += texto(40, 600, ["En el tercil superior de la intolerancia a la glucosa ya se ha",
                         "perdido el 80–85 % de la función de la célula β (DeFronzo 2009).",
                         "La diabetes aparece cuando la secreción de insulina",
                         "deja de compensar la resistencia."], tam=16, interlineado=1.4)
    c += texto(40, 715, "Esquema cualitativo: curvas sin escala.", tam=13, color=SUAVE, cursiva=True)
    c += f'<line x1="800" y1="140" x2="800" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    c += texto(830, 160, "Los otros cuatro defectos", tam=21, peso="bold")
    for i, (icono, titulo, lineas) in enumerate([
        ("servier4-intestino-delgado.svg", "Intestino: efecto incretina", ["Deficiencia o resistencia a", "GLP-1 y GIP."]),
        ("servier-pancreas-2.svg", "Célula α: hiperglucagonemia", ["Más glucagón: el hígado", "produce más glucosa."]),
        ("servier-kidney-2.svg", "Riñón: más reabsorción", ["Reabsorbe más glucosa", "filtrada (SGLT2)."]),
        ("brain-2", "Cerebro: resistencia", ["Resistencia a la insulina", "en el sistema nervioso central."])]):
        y = 185 + i * 160
        c += (f'<rect x="830" y="{y}" width="730" height="140" rx="12" fill="#FFFFFF" stroke="{COLOR["borde_panel"]}"/>'
              f'<rect x="830" y="{y}" width="6" height="140" rx="3" fill="{ROJO}"/>')
        c += ilustracion(icono, 850, y + 20, 100, 100)
        c += texto(970, y + 46, titulo, tam=18, peso="bold", color=ROJO)
        c += texto(970, y + 76, lineas, tam=16, interlineado=1.35)
    return lamina(5, "Fisiopatología", "La célula β no compensa, y otros cuatro defectos",
                  "Mientras la célula β compensa, la glucemia se mantiene; cuando falla, aparece la diabetes.", c)


# --- Lámina 6 ------------------------------------------------------------------------

def lamina_6():
    c = texto(40, 160, "Síntomas: por qué aparecen", tam=21, peso="bold")
    pasos = [("Hiperglucemia", NARANJA), ("Glucosa en orina", NARANJA), ("Diuresis osmótica", ROJO),
             ("Poliuria → sed", ROJO)]
    for i, (t, col) in enumerate(pasos):
        y = 190 + i * 90
        c += caja(60, y, 320, 42, t, "", col)
        if i < len(pasos) - 1:
            c += flecha([(220, y + 44), (220, y + 88)])
    c += texto(420, 220, ["Otros síntomas (OMS):", "• visión borrosa", "• cansancio", "• pérdida de peso", "  no intencional"],
               tam=18, interlineado=1.45)
    c += (f'<rect x="40" y="580" width="720" height="190" rx="14" fill="#FDF0EA" stroke="{ROJO}" stroke-width="1.5"/>')
    c += texto(62, 620, "Para el profesional", tam=20, peso="bold", color=ROJO)
    c += texto(62, 656, ["Los síntomas aparecen despacio, a lo largo de años, y",
                         "pueden ser tan leves que no se notan; muchas personas",
                         "no tienen ninguno. Por eso se piden pruebas a quien",
                         "tiene factores de riesgo, aunque no tenga síntomas."], tam=18, interlineado=1.4)
    c += f'<line x1="800" y1="140" x2="800" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    c += texto(830, 160, "Complicaciones: daño de los vasos", tam=21, peso="bold")
    c += tarjeta(830, 180, 730, 290, ROJO, "Microvasculares", [
        "• Ojos: pérdida permanente de visión.",
        "• Riñones: insuficiencia renal.",
        "• Nervios: neuropatía; con mala circulación,",
        "  úlceras del pie y amputación."], tam=20, icono=ilustracion("servier-kidney-2.svg", 1470, 196, 70, 80))
    c += tarjeta(830, 490, 730, 290, ROJO, "Macrovasculares", [
        "• Infarto de miocardio.",
        "• Accidente cerebrovascular.",
        "• Alrededor del 11 % de las muertes",
        "  cardiovasculares se deben a la glucosa alta."], tam=20, icono=ilustracion("servier4-corazon.svg", 1470, 500, 70, 90) if (RAIZ / "assets/ilustraciones/servier4-corazon.svg").exists() else "")
    return lamina(6, "Clínica", "Síntomas y complicaciones",
                  "Los síntomas vienen de la glucosuria; las complicaciones, del daño de los vasos pequeños y grandes.", c)


# --- Lámina 7 ------------------------------------------------------------------------

def lamina_7():
    filas = [("Prueba", "Normal", "Prediabetes", "Diabetes"),
             ("HbA1c", "< 5,7 %", "5,7–6,4 %", "≥ 6,5 %"),
             ("Glucosa en ayunas (≥ 8 h)", "< 100 mg/dl", "100–125 mg/dl", "≥ 126 mg/dl"),
             ("PTOG: glucosa a las 2 h", "< 140 mg/dl", "140–199 mg/dl", "≥ 200 mg/dl"),
             ("Glucosa al azar con síntomas", "—", "—", "≥ 200 mg/dl")]
    xs, anchos = [40, 520, 860, 1200], [480, 340, 340, 360]
    c = ""
    for i, fila in enumerate(filas):
        y = 150 + i * 78
        fondo = "#E3F0F8" if i == 0 else ("#FFFFFF" if i % 2 else "#F5F8F9")
        c += f'<rect x="40" y="{y}" width="1520" height="74" fill="{fondo}" stroke="{COLOR["borde_panel"]}"/>'
        for j, celda in enumerate(fila):
            color = AZUL if i == 0 else (ROJO if j == 3 else (NARANJA if j == 2 else COLOR["texto"]))
            c += texto(xs[j] + 20, y + 46, celda, tam=20 if i else 18, peso="bold" if (i == 0 or j == 3) else "normal",
                       color=color)
    c += tarjeta(40, 560, 740, 230, AZUL, "Confirmación", [
        "Salvo hiperglucemia inequívoca, hacen falta dos",
        "resultados alterados: dos pruebas distintas a la vez",
        "(p. ej., HbA1c y glucosa en ayunas) o la misma",
        "prueba en dos momentos."], tam=20)
    c += tarjeta(820, 560, 740, 230, AZUL, "Qué mide cada prueba", [
        "HbA1c: glucemia media de 2 a 3 meses, sin ayuno.",
        "Ayunas: tras al menos 8 horas sin comer.",
        "PTOG: glucosa 2 h después de una bebida azucarada."], tam=20)
    return lamina(7, "Diagnóstico", "Criterios diagnósticos y confirmación",
                  "Cuatro pruebas con los puntos de corte de las Normas de la ADA 2026; salvo hiperglucemia inequívoca, se confirma.", c)


# --- Lámina 8 ------------------------------------------------------------------------

FARMACOS = {  # por órgano del octeto: etiquetas de fármacos
    "Célula β (islote)": ["Sulfonilureas: ↑ insulina", "AR GLP-1, tirzepatida, iDPP-4"],
    "Hígado": ["Metformina: ↓ producción", "Pioglitazona (PPARγ)"],
    "Músculo": ["Pioglitazona: ↓ resistencia", "Insulina: sustitución"],
    "Tejido adiposo": ["Pioglitazona (PPARγ)"],
    "Célula α (islote)": ["AR GLP-1, tirzepatida, iDPP-4: ↓ glucagón"],
    "Intestino": ["iDPP-4: ↑ GLP-1 y GIP propios", "AR GLP-1: imitan GLP-1"],
    "Riñón": ["iSGLT2: ↑ glucosa en orina"],
    "Cerebro": ["AR GLP-1: ↓ apetito (semaglutida)"],
}


def lamina_8():
    c = ""
    for icono, organo, defecto, lado, fila in OCTETO:
        x, y = posicion(lado, fila)
        c += ilustracion(icono, x, y, 70, 70)
        c += texto(x + 84, y + 26, organo, tam=16, peso="bold") + texto(x + 84, y + 48, defecto, tam=13, color=ROJO)
        for k, f in enumerate(FARMACOS[organo]):
            c += etiqueta_farmaco(x + 84, y + 60 + k * 30, f, destacado=(k == 0), ancho=360)
    c += (f'<rect x="540" y="200" width="520" height="520" rx="14" fill="#E3F0F8" stroke="{AZUL}" stroke-width="1.5"/>')
    c += texto(564, 236, "Cómo leer el mapa", tam=18, peso="bold", color=AZUL)
    c += texto(564, 266, ["• AR GLP-1 e iDPP-4 aumentan la insulina",
                          "  solo cuando la glucosa está alta.",
                          "• Metformina e iSGLT2 no estimulan la",
                          "  secreción de insulina.",
                          "  → solos, rara vez causan hipoglucemia.",
                          "• Las sulfonilureas liberan insulina",
                          "  aunque la glucosa sea baja:",
                          "  más hipoglucemia.",
                          "• La pioglitazona necesita insulina",
                          "  para actuar: no es secretagogo.",
                          "• Ninguno corrige los ocho defectos:",
                          "  de ahí las combinaciones."], tam=16, interlineado=1.38)
    c += etiqueta_farmaco(564, 600, "efecto principal", destacado=True, ancho=200)
    c += etiqueta_farmaco(780, 600, "efecto adicional", ancho=200)
    c += texto(564, 664, ["Fichas FDA (12.1): metformina, glipizida,", "pioglitazona, sitagliptina, semaglutida,",
                          "tirzepatida, empagliflozina, insulina glargina."], tam=13, color=SUAVE, interlineado=1.35)
    return lamina(8, "Tratamiento", "Dónde actúa cada grupo de fármacos",
                  "Mapa del tratamiento sobre los ocho defectos, según el mecanismo de las fichas de la FDA (sección 12.1).", c)


# --- Lámina 9 ------------------------------------------------------------------------

def lamina_9():
    c = caja(40, 150, 1520, 42, "Base para todos: hábitos saludables, educación (DSMES) y determinantes sociales de la salud", "",
             VERDE, fondo="#EAF6F1")
    c += flecha([(800, 194), (800, 250)])
    c += (f'<rect x="560" y="252" width="480" height="76" rx="12" fill="#FFFFFF" stroke="{COLOR["texto"]}" '
          f'stroke-width="1.5"/>')
    c += texto(800, 283, ["¿Enfermedad CV o alto riesgo CV,", "insuficiencia cardiaca o ERC?"], tam=17,
               peso="bold", anclaje="middle", interlineado=1.3)
    c += flecha([(560, 290), (420, 290), (420, 350)]) + texto(470, 280, "Sí", tam=16, peso="bold", color=VERDE)
    c += flecha([(1040, 290), (1180, 290), (1180, 350)]) + texto(1110, 280, "No", tam=16, peso="bold", color=SUAVE)
    c += tarjeta(40, 354, 760, 330, VERDE, "Protección cardiorrenal", [
        "Con beneficio demostrado, sea cual sea la HbA1c:",
        "• Enfermedad CV o alto riesgo CV: AR GLP-1 y/o iSGLT2.",
        "• Insuficiencia cardiaca: iSGLT2; con obesidad e",
        "  ICFEp sintomática, también tirzepatida o AR GLP-1.",
        "• ERC (TFGe 20–60 y/o albuminuria): iSGLT2",
        "  o AR GLP-1. Si la TFGe es < 30: mejor AR GLP-1."], tam=18)
    c += tarjeta(820, 354, 740, 330, AZUL, "Control glucémico y peso", [
        "• Objetivo para muchos adultos: HbA1c < 7 %, sin",
        "  hipoglucemia grave; individualizar.",
        "• Metformina: eficacia alta, sin hipoglucemia;",
        "  reducir la dosis con TFGe < 45 y suspender con < 30.",
        "• Elegir según peso, comorbilidades y riesgo de",
        "  hipoglucemia; combinar pronto si hace falta."], tam=18)
    c += tarjeta(40, 700, 1520, 120, NARANJA, "Si hace falta insulina",
                 "Antes, un tratamiento basado en GLP-1. Insulina si hay síntomas, HbA1c > 10 % o glucosa ≥ 300 mg/dl: basal de "
                 "0,1–0,2 U/kg/día, combinada con un AR GLP-1 o tirzepatida, sin retirar los demás fármacos.", tam=18)
    return lamina(9, "Tratamiento", "Estrategia: primero el riesgo cardiorrenal, luego la glucosa",
                  "Resumen de las Normas de Atención de la ADA 2026 (secciones 6 y 9).", c)


LAMINAS = {1: lamina_1, 2: lamina_2, 3: lamina_3, 4: lamina_4, 5: lamina_5, 6: lamina_6, 7: lamina_7, 8: lamina_8,
           9: lamina_9}

if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or sorted(LAMINAS):
        salida = Path(__file__).with_name(f"lamina-{n}.svg")
        salida.write_text(LAMINAS[n](), encoding="utf-8")
        print(salida)
