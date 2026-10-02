"""Neumonía nosocomial en once láminas (plantilla: infecciosa, síndrome con varios agentes posibles).

1. Contexto: neumonía adquirida en el hospital y asociada a ventilación mecánica.
2. Fisiología: cómo se protege el pulmón sano.
3. Fisiopatología: cómo llegan las bacterias al pulmón (tubo endotraqueal).
4. Fisiopatología: colonización, agentes y riesgo de multirresistencia.
5. Clínica: cada signo tiene su mecanismo, y complicaciones.
6. Diagnóstico: sospecha clínica y pruebas.
7. Resistencia: cómo escapan las bacterias a los antibióticos.
8. Tratamiento: dónde actúa cada familia de antibióticos.
9. Tratamiento: estrategia empírica según la guía S3 2024.
10. Tratamiento: farmacocinética y farmacodinamia.
11. Prevención.

Uso: python3 laminas.py [1 ... 11]
"""
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))
from componentes import COLOR, adn, etiqueta_farmaco, flecha, ribosoma, texto  # noqa: E402
from recursos import ATRIBUCION, ilustracion  # noqa: E402
from piezas import (AZUL, NARANJA, ROJO, SUAVE, VERDE, Lamina, caja, curva_fcfd, leyenda_paso,  # noqa: E402
                    tarjeta)

PAT, PAT_B = COLOR["patogeno"], COLOR["patogeno_borde"]
L = Lamina("NEUMONÍA NOSOCOMIAL", "Fuentes: guía S3 alemana 2024 (AWMF 020-013); ERS/ESICM/ESCMID/ALAT 2017 (PMID 28890434); "
           f"Nat Commun 2024 (PMC11291905); SHEA/IDSA/APIC 2022 (PMC10903147); FDA. {ATRIBUCION}.")


def lamina(n, etiqueta, titulo, subtitulo, contenido, extra=""):
    return L.dibujar(n, etiqueta, titulo, subtitulo, contenido, total=len(LAMINAS), extra=extra)


def idea_clave(y, lineas, color=AZUL, fondo="#E3F0F8", titulo="Idea clave", alto=None):
    alto = alto or 46 + 26 * len(lineas)
    return (f'<rect x="40" y="{y}" width="1520" height="{alto}" rx="14" fill="{fondo}" stroke="{color}" stroke-width="1.5"/>'
            + texto(66, y + 34, titulo, tam=18, peso="bold", color=color)
            + texto(66, y + 62, lineas, tam=17, interlineado=1.5))


# --- Piezas propias: bacterias esquemáticas ------------------------------------------------

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


# --- Lámina 1 -------------------------------------------------------------------------------

def lamina_1():
    c = tarjeta(40, 140, 520, 250, AZUL, "Neumonía adquirida en el hospital", [
        "Aparece más de 48 h después del",
        "ingreso; no estaba en incubación.",
        "Puede o no requerir ventilación",
        "mecánica al diagnóstico."], tam=18)
    c += tarjeta(40, 410, 520, 250, AZUL, "Neumonía asociada a ventilación", [
        "Aparece en pacientes de la UCI con",
        "ventilación mecánica durante al",
        "menos 48 h.",
        "Precoz: ≤ 4 días; tardía: ≥ 5 días."], tam=18)
    c += ilustracion("servier-healthy-lung.svg", 600, 150, 400, 470)
    for x, y, a in [(735, 420, 20), (770, 470, -30), (860, 440, 60), (900, 500, 10), (700, 520, -50), (880, 360, 35)]:
        c += bacteria_pequena(x, y, a, 1.4)
    c += texto(800, 650, "Sin escala", tam=14, anclaje="middle", color=SUAVE, cursiva=True)
    c += tarjeta(1040, 140, 520, 520, PAT_B, "Agentes bacterianos", [
        "Sin factores de riesgo de MMR:",
        "• Enterobacterales (E. coli, Klebsiella,",
        "  Enterobacter)",
        "• H. influenzae, S. pneumoniae",
        "• S. aureus",
        "Además, con factores de riesgo:",
        "• Enterobacterales resistentes (BLEE)",
        "• P. aeruginosa",
        "• Menos frecuentes: SARM,",
        "  A. baumannii, S. maltophilia",
        "No son agentes de NN (flora",
        "orofaríngea): Candida, enterococos,",
        "estafilococos coagulasa negativos."], tam=17)
    c += idea_clave(684, ["Los agentes y su resistencia dependen de los factores de riesgo del paciente y de la ecología de cada unidad:",
                          "la guía S3 pide revisar el antibiograma de cada servicio cada 6–12 meses y usarlo para elegir el tratamiento."])
    return lamina(1, "Contexto", "Dos formas de neumonía nosocomial y los mismos protagonistas",
                  "Definiciones de la guía S3 2024 y de ERS/ESICM/ESCMID/ALAT 2017; agentes según la tabla 1 de la guía S3.", c)


# --- Lámina 2 -------------------------------------------------------------------------------

def lamina_2():
    c = ilustracion("servier4-traquea-bronquios.svg", 40, 150, 440, 600)
    c += ilustracion("servier4-vias-intrapulmonares-1.svg", 900, 170, 300, 440)
    c += ilustracion("servier-macrophage.svg", 1210, 520, 110, 120)
    c += ilustracion("servier-neutrophil-granulocyte.svg", 1330, 556, 80, 84)
    c += flecha([(510, 196), (272, 214)]) + flecha([(510, 330), (290, 300)]) + flecha([(510, 470), (330, 470)])
    c += leyenda_paso(520, 200, 1, "Cierre de la glotis", ["Separa la vía aérea de la orofaringe."])
    c += leyenda_paso(520, 334, 2, "Tos y deglución", ["Expulsan o desvían las secreciones."])
    c += leyenda_paso(520, 474, 3, "Aclaramiento mucociliar", ["El moco y los cilios arrastran", "las secreciones hacia arriba."])
    c += flecha([(1180, 690), (1260, 640)])
    c += leyenda_paso(900, 700, 4, "Macrófagos y neutrófilos", ["Responden a los microorganismos", "que llegan al alvéolo."])
    c += tarjeta(1230, 160, 330, 300, ROJO, "Qué las anula", [
        "Tubo endotraqueal,",
        "sedación, parálisis y",
        "ventilación con",
        "presión positiva",
        "(lámina 3)."], tam=18)
    c += texto(800, 820, "Esquema simplificado y sin escala", tam=14, anclaje="middle", color=SUAVE, cursiva=True)
    return lamina(2, "Fisiología normal", "Cómo se protege el pulmón sano",
                  "Cuatro barreras impiden que la flora de la boca y la faringe llegue al alvéolo y se multiplique.", c)


# --- Lámina 3 -------------------------------------------------------------------------------

def tubo_endotraqueal():
    """Corte esquemático de la tráquea con el tubo endotraqueal, el balón y la microaspiración."""
    tx1, tx2, top, fondo = 520, 760, 150, 800          # paredes de la tráquea
    s = (f'<rect x="{tx1}" y="{top}" width="{tx2 - tx1}" height="{fondo - top}" fill="#FBE9E7"/>'
         f'<line x1="{tx1}" y1="{top}" x2="{tx1}" y2="{fondo}" stroke="#C48A86" stroke-width="8"/>'
         f'<line x1="{tx2}" y1="{top}" x2="{tx2}" y2="{fondo}" stroke="#C48A86" stroke-width="8"/>')
    for yy in range(top + 20, fondo, 46):                # anillos cartilaginosos
        s += (f'<rect x="{tx1 - 14}" y="{yy}" width="10" height="24" rx="4" fill="#DCE6EA" stroke="#9FB3BC"/>'
              f'<rect x="{tx2 + 4}" y="{yy}" width="10" height="24" rx="4" fill="#DCE6EA" stroke="#9FB3BC"/>')
    # Tubo endotraqueal
    s += (f'<rect x="600" y="{top - 20}" width="80" height="560" rx="6" fill="#F4F8FA" stroke="#6E8A96" stroke-width="3"/>'
          f'<rect x="608" y="{top - 20}" width="64" height="560" fill="#FFFFFF" opacity="0.6"/>')
    # Biopelícula en la cara interna
    for yy in range(top + 10, 690, 18):
        s += (f'<circle cx="611" cy="{yy}" r="4" fill="{PAT}" stroke="{PAT_B}" stroke-width="0.8"/>'
              f'<circle cx="669" cy="{yy + 9}" r="4" fill="{PAT}" stroke="{PAT_B}" stroke-width="0.8"/>')
    # Secreciones acumuladas sobre el balón
    s += (f'<path d="M{tx1 + 4},540 C560,520 590,530 600,536 L600,600 L{tx1 + 4},600 Z" fill="#E9E2A6" opacity="0.9"/>'
          f'<path d="M680,536 C700,526 730,522 {tx2 - 4},540 L{tx2 - 4},600 L680,600 Z" fill="#E9E2A6" opacity="0.9"/>')
    # Balón
    s += (f'<ellipse cx="560" cy="630" rx="38" ry="32" fill="#CFE3F0" stroke="#4F7A96" stroke-width="2.5"/>'
          f'<ellipse cx="720" cy="630" rx="38" ry="32" fill="#CFE3F0" stroke="#4F7A96" stroke-width="2.5"/>')
    # Fuga por un pliegue del balón
    s += (f'<path d="M{tx1 + 6},600 C{tx1 + 8},640 {tx1 + 4},680 {tx1 + 12},720" fill="none" stroke="#B9A94A" '
          f'stroke-width="5" stroke-linecap="round"/>')
    for yy, xx in [(664, tx1 + 14), (700, tx1 + 22), (742, tx1 + 30), (770, 560)]:
        s += bacteria_pequena(xx, yy, 70)
    s += flecha([(tx1 + 26, 730), (tx1 + 46, 790)], bloqueada=True)
    return s


def lamina_3():
    c = tubo_endotraqueal()
    # Reservorios
    for i, (titulo, sub) in enumerate([("Orofaringe", "flora de la boca"), ("Senos paranasales", "secreciones"),
                                       ("Estómago", "contenido gástrico")]):
        y = 160 + i * 112
        c += caja(40, y, 300, 80, titulo, sub, PAT_B, fondo="#FFFBE0")
        c += flecha([(342, y + 40), (510, 520)])
    c += tarjeta(40, 560, 440, 220, PAT_B, "Sin tubo (NAH)", [
        "En el paciente hospitalizado,",
        "la flora oral pasa a ser de",
        "bacilos gramnegativos que se",
        "aspiran (lámina 4)."], tam=18)
    c += texto(640, 820, "Esquema simplificado y sin escala", tam=14, anclaje="middle", color=SUAVE, cursiva=True)
    c += leyenda_paso(840, 190, 1, "El tubo impide cerrar la glotis", ["Comunica la faringe con el pulmón."])
    c += leyenda_paso(840, 310, 2, "Biopelícula en el tubo", ["Presente en el 95 % de los tubos;",
                                                             "se desprende al moverlo o aspirar."])
    c += leyenda_paso(840, 450, 3, "Secreciones sobre el balón", ["El balón evita la aspiración grande,",
                                                                 "no la microaspiración."])
    c += leyenda_paso(840, 590, 4, "Fugas: microaspiración silenciosa", ["Por pliegues, pérdida de presión",
                                                                         "o movimiento del tubo."])
    c += leyenda_paso(840, 730, 5, "Tos y aclaramiento debilitados", ["Sedación, parálisis, presión positiva."])
    return lamina(3, "Fisiopatología", "Cómo llegan las bacterias al pulmón ventilado",
                  "El tubo endotraqueal salta las defensas de la lámina 2 y deja pasar secreciones colonizadas.", c)


# --- Lámina 4 -------------------------------------------------------------------------------

def lamina_4():
    c = (f'<rect x="40" y="150" width="760" height="250" rx="16" fill="#FFFFFF" stroke="{COLOR["borde_panel"]}"/>'
         + texto(64, 188, "El tiempo cambia los agentes probables", tam=21, peso="bold"))
    c += f'<line x1="80" y1="256" x2="760" y2="256" stroke="{COLOR["linea"]}" stroke-width="3"/>'
    c += flecha([(700, 256), (770, 256)])
    for x, rot in [(80, "Ingreso"), (330, "Día 4"), (560, "Día 5 en adelante")]:
        c += f'<circle cx="{x}" cy="256" r="8" fill="{COLOR["linea"]}"/>' + texto(x, 234, rot, tam=16, anclaje="middle",
                                                                                     peso="bold")
    c += texto(70, 302, ["Precoz, sin factores de riesgo:", "S. pneumoniae, H. influenzae,", "S. aureus sensible a meticilina"],
               tam=18, interlineado=1.4, color=VERDE)
    c += texto(450, 302, ["Tardía: más riesgo de MMR", "P. aeruginosa, A. baumannii,", "SARM, otros bacilos gramnegativos"],
               tam=18, interlineado=1.4, color=ROJO)
    c += tarjeta(40, 420, 760, 270, PAT_B, "La flora del paciente cambia en el hospital", [
        "La flora oral pasa a estar dominada por bacilos",
        "gramnegativos aerobios, que pueden aspirarse.",
        "Vía exógena: equipos contaminados",
        "(p. ej., humidificadores)."], tam=19)
    c += tarjeta(830, 150, 730, 420, ROJO, "Factores de riesgo de MMR (guía S3)", [
        "• Antimicrobianos (> 24 h) en los últimos 30 días",
        "• Hospitalización ≥ 5 días antes del inicio",
        "• Colonización por gramnegativos MMR o SARM*",
        "• Shock séptico   • SDRA   • Hemodiálisis",
        "• Atención en los últimos 12 meses en un país con",
        "  alta prevalencia de gramnegativos MMR y SARM",
        "Además, para P. aeruginosa:",
        "• Enfermedad pulmonar estructural (EPOC avanzada,",
        "  bronquiectasias) o colonización conocida"], tam=17)
    c += texto(860, 556, "* La mayoría de los colonizados no tendrá una neumonía por esos agentes.", tam=14, color=SUAVE,
               cursiva=True)
    c += tarjeta(830, 590, 730, 100, NARANJA, "El momento no basta", [
        "Inmunosupresión, antibióticos u hospitalización previos también cuentan."], tam=17)
    c += idea_clave(712, ["Los factores de riesgo de MMR deciden el tratamiento empírico (lámina 9)."], alto=80)
    return lamina(4, "Fisiopatología", "Qué bacterias llegan: tiempo, exposición y riesgo de multirresistencia",
                  "ERS/ESICM/ESCMID/ALAT 2017 (precoz y tardía); tabla 3 de la guía S3 2024 (factores de riesgo).", c)


# --- Lámina 5 -------------------------------------------------------------------------------

def lamina_5():
    c = ilustracion("servier4-edema-pulmonar.svg", 50, 160, 380, 420)
    c += texto(240, 610, ["Alvéolos inflamados y ocupados", "por exudado (esquema)"], tam=15, anclaje="middle", color=SUAVE,
               cursiva=True, interlineado=1.35)
    c += tarjeta(460, 150, 540, 310, VERDE, "En el pulmón", [
        "Macrófagos y neutrófilos responden:",
        "el alvéolo se inflama y se llena.",
        "→ Infiltrado nuevo o progresivo",
        "→ Secreción purulenta",
        "→ Hipoxemia, taquipnea, crepitantes",
        "→ En ventilados: más presión",
        "    inspiratoria con volumen bajo"], tam=18)
    c += tarjeta(1020, 150, 540, 310, NARANJA, "En todo el organismo", [
        "Respuesta inflamatoria sistémica:",
        "→ Fiebre > 38,3 °C",
        "→ Leucocitos > 10 000/µl",
        "    o < 4000/µl",
        "→ Sepsis: evaluarla en todos",
        "    (qSOFA fuera de la UCI, SOFA",
        "    en la UCI; lactato)"], tam=18)
    c += tarjeta(460, 480, 1100, 150, ROJO, "Complicaciones: duración individual o más larga", [
        "• Shock séptico            • Empiema            • Absceso pulmonar",
        "• Bacteriemia por S. aureus: se trata como bacteriemia complicada (en general, 4 semanas o más)."], tam=18)
    c += idea_clave(650, ["Los criterios clínicos son sensibles pero poco específicos: atelectasia, edema pulmonar, embolia",
                          "pulmonar y traumatismo pulmonar pueden simular una NAV (ERS/ESICM/ESCMID/ALAT)."],
                    color=NARANJA, fondo="#FDF1E6", titulo="Error frecuente")
    return lamina(5, "Clínica", "Cada signo tiene su mecanismo",
                  "Signos locales por la inflamación del alvéolo y signos sistémicos por la respuesta del organismo.", c)


# --- Lámina 6 -------------------------------------------------------------------------------

def lamina_6():
    c = tarjeta(40, 140, 1520, 120, AZUL, "Sospecha clínica (guía S3 2024): basta para empezar a tratar", [
        "Infiltrado nuevo, persistente o progresivo en la radiografía  +  2 de 3: leucocitos > 10 000 o < 4000/µl · "
        "fiebre > 38,3 °C · secreción purulenta"], tam=19)
    filas = [("Prueba", "Qué aporta", "Cuándo"),
             ("Hemocultivos", "Bacteriemia y agente", "Siempre"),
             ("Cultivo semicuantitativo (aspirado o LBA)", "Agente y antibiograma; el recuento orienta", "Antes del antibiótico, sin retrasarlo"),
             ("Tinción de Gram de la muestra", "Valida la muestra; negativa sin antibiótico: alto VPN", "Con el cultivo"),
             ("PCR de SARS-CoV-2 e influenza", "Virus respiratorios", "Según la situación epidemiológica"),
             ("Galactomanano en LBA (≥ 1,0)", "Aspergillus", "Si hay factores de riesgo de aspergilosis"),
             ("Radiografía; ecografía o TC", "Infiltrado; complicaciones (empiema)", "Ecografía o TC si la radiografía no aclara")]
    xs = [40, 560, 1080]
    for i, fila in enumerate(filas):
        y = 280 + i * 58
        fondo = "#E3F0F8" if i == 0 else ("#FFFFFF" if i % 2 else "#F5F8F9")
        c += f'<rect x="40" y="{y}" width="1520" height="56" fill="{fondo}" stroke="{COLOR["borde_panel"]}"/>'
        for j, celda in enumerate(fila):
            c += texto(xs[j] + 18, y + 36, celda, tam=17 if i else 17, peso="bold" if (i == 0 or j == 0) else "normal",
                       color=AZUL if i == 0 else COLOR["texto"])
    c += tarjeta(40, 700, 740, 136, NARANJA, "No de rutina", [
        "PCR múltiple bacteriana. Biomarcadores (PCT, proteína C",
        "reactiva): para seguir la evolución, no para diagnosticar."], tam=16)
    c += tarjeta(820, 700, 740, 136, SUAVE, "Diagnóstico diferencial", [
        "Atelectasias, insuficiencia cardiaca o sobrecarga de líquidos,",
        "embolia pulmonar, hemorragia alveolar, neumonía organizada, SDRA."], tam=16)
    return lamina(6, "Diagnóstico", "Sospechar con criterios clínicos y confirmar el agente",
                  "Recomendaciones 2–11 de la guía S3 2024; la broncoscopia no es superior a la toma no broncoscópica en la NAV.", c)


# --- Lámina 7 -------------------------------------------------------------------------------

def lamina_7():
    x, y, w, h = 80, 200, 780, 320
    c = texto(x, y - 34, "Bacilo gramnegativo (p. ej., P. aeruginosa, Enterobacterales)", tam=17, peso="bold", color=PAT_B)
    c += bacilo_gramnegativo(x, y, w, h)
    c += porina(230, y + 2, cerrada=True) + porina(300, y + 2)
    c += bomba(700, y + 2)
    c += enzima_bl(420, y + h - 7)
    c += pbp(560, y + 42, color=ROJO, relleno="#F6D6C8", etiqueta="PBP alterada")
    for n, (tx, ty) in enumerate([(252, y - 14), (722, y - 14), (592, y + 34), (486, y + h + 30)], 1):
        c += f'<circle cx="{tx}" cy="{ty - 5}" r="11" fill="{ROJO}"/>' + texto(tx, ty, str(n), tam=13, peso="bold",
                                                                                color="#FFFFFF", anclaje="middle")
    c += texto(470, y + h + 64, "Esquema simplificado y sin escala", tam=14, anclaje="middle", color=SUAVE, cursiva=True)
    c += leyenda_paso(60, 640, 1, "Menos porinas", ["Entra menos antibiótico."])
    c += leyenda_paso(480, 640, 2, "Bombas de expulsión", ["Sacan el antibiótico."])
    c += leyenda_paso(60, 750, 3, "PBP con menos afinidad", ["La diana no lo une bien."])
    c += leyenda_paso(480, 750, 4, "Enzimas que lo destruyen", ["β-lactamasas, BLEE, carbapenemasas."])
    c += coco_grampositivo(1230, 320, 120)
    c += pbp(1230, 218, color=ROJO, relleno="#F6D6C8", etiqueta="PBP2a")
    c += texto(1230, 168, "S. aureus resistente a meticilina (SARM)", tam=17, peso="bold", anclaje="middle", color=PAT_B)
    c += tarjeta(920, 470, 640, 160, ROJO, "SARM: una PBP nueva", [
        "El gen mecA codifica PBP2a, de baja afinidad por los",
        "β-lactámicos: sigue fabricando la pared con el fármaco."], tam=17)
    c += tarjeta(920, 650, 640, 170, AZUL, "Qué cambia en el tratamiento (guía S3)", [
        "BLEE: carbapenémico. Carbapenemasas (KPC, OXA-48,",
        "MBL): β-lactámico de reserva según antibiograma",
        "y consulta con infectología."], tam=17)
    return lamina(7, "Fisiopatología", "Cómo escapan las bacterias a los antibióticos",
                  "Mecanismos de resistencia a carbapenémicos (ficha de meropenem, FDA 12.4) y base del SARM (PMID 37760659).", c)


# --- Lámina 8 -------------------------------------------------------------------------------

def lamina_8():
    x, y, w, h = 70, 230, 820, 320
    c = texto(x, y - 50, "Bacilo gramnegativo", tam=17, peso="bold", color=PAT_B)
    c += bacilo_gramnegativo(x, y, w, h)
    c += porina(260, y + 2) + pbp(520, y + 42) + enzima_bl(330, y + h - 7, etiqueta=None)
    ax, ay = round(x + w * 0.45), round(y + h * 0.55)       # ADN
    rx, ry = round(x + w * 0.76), round(y + h * 0.66)       # ribosoma
    c += etiqueta_farmaco(400, y - 34, "β-lactámicos → PBP: síntesis de pared", ancho=330)
    c += flecha([(520, y - 8), (520, y + 22)])
    c += etiqueta_farmaco(750, y - 34, "Colistina → membrana", ancho=210)
    c += flecha([(850, y - 8), (860, y + 34)])
    c += etiqueta_farmaco(70, y + h + 24, "Tazobactam → β-lactamasa", ancho=240)
    c += flecha([(200, y + h + 24), (318, y + h - 2)])
    c += etiqueta_farmaco(330, y + h + 24, "Fluoroquinolonas → ADN girasa, topoisomerasa IV", ancho=390)
    c += flecha([(470, y + h + 24), (ax, ay + 24)])
    c += etiqueta_farmaco(740, y + h + 24, "Aminoglucósidos → ribosoma", ancho=270)
    c += flecha([(820, y + h + 24), (rx, ry + 14)])
    c += coco_grampositivo(1250, 310, 110)
    c += texto(1250, 176, "Coco grampositivo (S. aureus, SARM)", tam=17, peso="bold", anclaje="middle", color=PAT_B)
    c += etiqueta_farmaco(1040, 450, "Vancomicina → síntesis de pared", ancho=290)
    c += flecha([(1180, 450), (1180, 400)])
    c += etiqueta_farmaco(1340, 450, "Linezolid → ARNr 23S (50S)", ancho=220)
    c += flecha([(1420, 450), (1294, 290)])
    c += tarjeta(1040, 520, 520, 290, AZUL, "Cómo leer el mapa", [
        "• Vancomicina no es activa frente a",
        "  bacilos gramnegativos.",
        "• Tazobactam casi no tiene actividad",
        "  propia: inhibe β-lactamasas y",
        "  protege a la piperacilina.",
        "• β-lactámicos y aminoglucósidos son",
        "  bactericidas; linezolid es",
        "  bacteriostático en estafilococos."], tam=17)
    c += texto(70, 650, ["Fichas de la FDA, sección 12.4 (Microbiology): piperacilina/tazobactam, cefepime, meropenem,",
                         "vancomicina, linezolid, amikacina, tobramicina, levofloxacino y colistimetato."],
               tam=15, color=SUAVE, interlineado=1.4)
    c += texto(70, 720, "Esquema simplificado y sin escala", tam=14, color=SUAVE, cursiva=True)
    return lamina(8, "Tratamiento", "Dónde actúa cada familia de antibióticos",
                  "Cada familia golpea una estructura distinta de la bacteria; por eso se combinan en el paciente grave.", c)


# --- Lámina 9 -------------------------------------------------------------------------------

def decision(cx, cy, w, h, lineas):
    return (f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="12" fill="#FFFFFF" '
            f'stroke="{COLOR["texto"]}" stroke-width="1.6"/>'
            + texto(cx, cy - (len(lineas) - 1) * 11 + 6, lineas, tam=17, peso="bold", anclaje="middle", interlineado=1.3))


def lamina_9():
    c = decision(800, 170, 300, 50, ["¿Shock séptico?"])
    c += flecha([(650, 170), (420, 170), (420, 214)]) + texto(520, 160, "No", tam=16, peso="bold", color=SUAVE)
    c += flecha([(950, 170), (1180, 170), (1180, 214)]) + texto(1060, 160, "Sí", tam=16, peso="bold", color=ROJO)
    c += decision(420, 246, 400, 60, ["¿Factores de riesgo de MMR?"])
    c += decision(1180, 246, 440, 60, ["¿Otro factor de riesgo de MMR?"])
    for x0, xs, etq in [(420, (230, 610), ("No", "Sí")), (1180, (990, 1370), ("No", "Sí"))]:
        c += flecha([(x0 - 60, 278), (xs[0], 316)]) + flecha([(x0 + 60, 278), (xs[1], 316)])
        c += texto((x0 - 60 + xs[0]) / 2 - 14, 296, etq[0], tam=15, peso="bold", color=SUAVE, anclaje="end")
        c += texto((x0 + 60 + xs[1]) / 2 + 14, 296, etq[1], tam=15, peso="bold", color=ROJO)
    cajas = [
        (40, VERDE, "Monoterapia", ["Aminopenicilina con", "inhibidor de β-lactamasa", "(ampicilina/sulbactam)", "o cefalosporina 3a",
                                    "(cefotaxima, ceftriaxona)", "o fluoroquinolona", "(levofloxacino, moxifloxacino)"]),
        (420, NARANJA, "Monoterapia", ["β-lactámico", "antipseudomónico:", "piperacilina/tazobactam", "o cefepime",
                                       "o meropenem", "Combinación si la", "resistencia local es alta"]),
        (800, NARANJA, "Monoterapia", ["Carbapenémico:", "meropenem", "", "(shock sin otro factor", "de riesgo de MMR)"]),
        (1180, ROJO, "Combinación", ["β-lactámico antipseudomónico", "más fluoroquinolona", "antipseudomónica", "(ciprofloxacino,",
                                     "levofloxacino)", "o aminoglucósido", "(tobramicina) o fosfomicina"]),
    ]
    for x, color, titulo, lineas in cajas:
        c += (f'<rect x="{x}" y="320" width="370" height="270" rx="14" fill="#FFFFFF" stroke="{color}" stroke-width="2"/>'
              f'<rect x="{x}" y="320" width="370" height="8" rx="4" fill="{color}"/>')
        c += texto(x + 185, 360, titulo, tam=19, peso="bold", anclaje="middle", color=color)
        c += texto(x + 185, 394, lineas, tam=17, anclaje="middle", interlineado=1.35)
    c += caja(40, 606, 1520, 46, "Si se sospecha SARM: añadir vancomicina o linezolid", "", AZUL, fondo="#E3F0F8")
    c += tarjeta(40, 670, 1520, 160, VERDE, "Después: reevaluar a las 48–72 h", [
        "Si no se confirma la neumonía, suspender. Si el paciente se estabiliza, desescalar aun sin agente identificado;",
        "si hay agente, dirigir el tratamiento. Duración: 7–8 días si la respuesta es buena. En shock séptico: antibiótico en la 1.ª hora."],
        tam=17)
    return lamina(9, "Tratamiento", "Tratamiento empírico: shock séptico y riesgo de multirresistencia",
                  "Diagrama de flujo y recomendaciones 12–21 de la guía S3 2024 (en alemán; traducción propia).", c)


# --- Lámina 10 ------------------------------------------------------------------------------

def lamina_10():
    c = curva_fcfd(60, 190, 700, 420, titulo="Tres formas de medir la exposición")
    filas = [(["Grupo"], ["Familias"], ["Consecuencia"]),
             (["Tiempo-dependientes", "(fT > CMI)"], ["Penicilinas, cefalos-", "porinas, carbapenémicos"],
              ["Infusión prolongada (3–4 h)", "tras dosis de carga"]),
             (["Concentración-", "dependientes (Cmáx/CMI)"], ["Aminoglucósidos"],
              ["Dosis única diaria", "(tobramicina 6 mg/kg)"]),
             (["Concentración y", "tiempo (ABC/CMI)"], ["Fluoroquinolonas,", "vancomicina, linezolid"],
              ["Vancomicina: dosis según", "concentraciones (MDT)"])]
    xs = [816, 1050, 1300]
    y = 160
    for i, fila in enumerate(filas):
        alto = 48 if i == 0 else 92
        fondo = "#E3F0F8" if i == 0 else ("#FFFFFF" if i % 2 else "#F5F8F9")
        c += f'<rect x="800" y="{y}" width="760" height="{alto}" fill="{fondo}" stroke="{COLOR["borde_panel"]}"/>'
        for j, celda in enumerate(fila):
            c += texto(xs[j], y + 31, celda, tam=17, peso="bold" if (i == 0 or j == 0) else "normal",
                       color=AZUL if i == 0 else COLOR["texto"], interlineado=1.35)
        y += alto
    c += tarjeta(800, 500, 760, 120, AZUL, "Objetivos de fT > CMI (guía S3)", [
        "Penicilinas ≥ 50 %, cefalosporinas 60–70 %, carbapenémicos ≥ 40 % del intervalo."], tam=17)
    c += tarjeta(40, 640, 500, 196, NARANJA, "El riñón cambia la exposición", [
        "FG ≥ 130 ml/min/m²: riesgo de dosis",
        "insuficiente aun con infusión larga.",
        "Insuficiencia renal o TRR: la infusión",
        "prolongada probablemente aporta poco."], tam=16)
    c += tarjeta(560, 640, 500, 196, AZUL, "Monitorizar concentraciones", [
        "Infusión continua de β-lactámicos",
        "solo con MDT (resultado ≤ 24 h).",
        "Tobramicina: valle < 1 mg/l si se usa",
        "más de 3 días."], tam=16)
    c += tarjeta(1080, 640, 480, 196, VERDE, "Antibióticos inhalados", [
        "No de rutina. Considerarlos solo si",
        "el gramnegativo MMR es sensible",
        "únicamente a colistina o a",
        "aminoglucósidos."], tam=16)
    return lamina(10, "Tratamiento", "Farmacocinética y farmacodinamia: por qué se dosifica así",
                  "Guía S3 2024 (versión larga, apartado 7.1.1.1, en alemán); índices FC/FD del documento de posición de 2020 (PMC7223855).", c)


# --- Lámina 11 ------------------------------------------------------------------------------

def lamina_11():
    medidas = [
        ("Evitar intubación y reintubación", "Oxígeno de alto flujo o VNI si es seguro.", "Alta", "1"),
        ("Minimizar la sedación", "Estrategias sin benzodiacepinas.", "Alta", "5"),
        ("Protocolo de retirada del ventilador", "Valorar la extubación cada día.", "Alta", "1"),
        ("Movilización temprana", "Ejercicio y movilización precoces.", "Moderada", "5"),
        ("Cabecera a 30–45°", "Menos NAV; sin cambio en mortalidad.", "Baja", "3–4"),
        ("Cepillado dental diario", "Sin clorhexidina.", "Moderada", "3"),
        ("Nutrición enteral temprana", "Mejor que la parenteral temprana.", "Alta", "—"),
        ("Circuito del ventilador", "Cambiarlo solo si está sucio o falla.", "Alta", "—"),
    ]
    c = (f'<rect x="40" y="150" width="1080" height="44" fill="#E3F0F8" stroke="{COLOR["borde_panel"]}"/>'
         + texto(60, 179, "Prácticas esenciales (SHEA/IDSA/APIC 2022)", tam=17, peso="bold", color=AZUL)
         + texto(840, 179, "Evidencia", tam=17, peso="bold", color=AZUL)
         + texto(960, 179, "Paso (lám. 3)", tam=17, peso="bold", color=AZUL))
    for i, (titulo, detalle, evidencia, paso_) in enumerate(medidas):
        y = 194 + i * 72
        c += (f'<rect x="40" y="{y}" width="1080" height="72" fill="{"#FFFFFF" if i % 2 == 0 else "#F5F8F9"}" '
              f'stroke="{COLOR["borde_panel"]}"/>')
        c += texto(60, y + 30, titulo, tam=18, peso="bold") + texto(60, y + 56, detalle, tam=15, color=SUAVE)
        c += texto(840, y + 42, evidencia, tam=17, color=VERDE if evidencia == "Alta" else NARANJA)
        c += texto(1010, y + 42, f"paso {paso_}" if paso_ != "—" else "—", tam=17, color=SUAVE)
    c += tarjeta(1150, 150, 410, 290, NARANJA, "Medidas adicionales", [
        "Si no se controla con las",
        "esenciales: tubo con drenaje",
        "subglótico, traqueostomía",
        "temprana; descontaminación",
        "selectiva solo en UCI con",
        "poca resistencia."], tam=17)
    c += tarjeta(1150, 460, 410, 310, ROJO, "No recomendado", [
        "• Clorhexidina oral",
        "• Probióticos",
        "• Balones ultrafinos o",
        "  cónicos",
        "• Control automático de",
        "  la presión del balón"], tam=17)
    c += (f'<rect x="40" y="786" width="1520" height="50" rx="12" fill="#EAF6F1" stroke="{VERDE}" stroke-width="1.5"/>'
          + texto(64, 818, "También cuenta:", tam=17, peso="bold", color=VERDE)
          + texto(210, 818, "programas de uso racional de antibióticos en cada hospital (guía S3, recomendación 26).", tam=17))
    return lamina(11, "Prevención", "Prevención: menos tubo, menos sedación, cabecera elevada",
                  "Guía SHEA/IDSA/APIC 2022 para prevenir la NAV en adultos; la guía S3 remite la prevención a la KRINKO.", c)


LAMINAS = {1: lamina_1, 2: lamina_2, 3: lamina_3, 4: lamina_4, 5: lamina_5, 6: lamina_6, 7: lamina_7, 8: lamina_8,
           9: lamina_9, 10: lamina_10, 11: lamina_11}

if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or sorted(LAMINAS):
        salida = Path(__file__).with_name(f"lamina-{n}.svg")
        salida.write_text(LAMINAS[n](), encoding="utf-8")
        print(salida)
