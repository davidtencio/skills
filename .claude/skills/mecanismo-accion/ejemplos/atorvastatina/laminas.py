"""Atorvastatina en seis láminas para estudiantes de farmacia (plantilla: enzima).

1. De dónde viene el colesterol LDL y dónde actúa cada hipolipemiante.
2. Cómo regula el hepatocito su colesterol (fisiología normal).
3. Cómo actúa atorvastatina (estructuras reales PDB 1DQ9 y 1HWK; potencia en ChEMBL y BindingDB).
4. Farmacocinética: el hígado es a la vez el lugar de acción y el filtro (con farmacogenética de SLCO1B1).
5. Del mecanismo al paciente.
6. Del ensayo a la práctica: farmacoeconomía y vida real (prioridad Costa Rica y Latinoamérica).

Uso: python3 laminas.py [1 2 3 4 5 6]
"""
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))
sys.path.insert(0, str(RAIZ / "ejemplos" / "darolutamida"))
from componentes import COLOR, bloqueo, etiqueta_farmaco, farmaco, flecha, paso, svg, texto  # noqa: E402
from estructuras import estructura, formula, molecula  # noqa: E402
from fuentes import pdb_descargar  # noqa: E402
from recursos import ATRIBUCION, ilustracion  # noqa: E402
from superficie import alinear, como_imagen, superficie_corte  # noqa: E402
from laminas import halo, leyenda_paso, nombre, guia, tarjeta, nota_farmaco  # noqa: E402

ANCHO, ALTO = 1600, 900
SUAVE = COLOR["texto_suave"]

# SMILES de PubChem, verificados por fórmula.
ATORVASTATINA = molecula("CC(C)C1=C(C(=C(N1CC[C@H](C[C@H](CC(=O)O)O)O)C2=CC=C(C=C2)F)C3=CC=CC=C3)C(=O)NC4=CC=CC=C4",
                         "C33H35FN2O5")  # CID 60823
HMG_COA = molecula("C[C@](CC(=O)O)(CC(=O)SCCNC(=O)CCNC(=O)[C@@H](C(C)(C)COP(=O)(O)OP(=O)(O)OC[C@@H]1[C@H]"
                   "([C@H]([C@@H](O1)N2C=NC3=C(N=CN=C32)N)O)OP(=O)(O)O)O)O", "C27H44N7O20P3S")  # CID 445127
MEVALONATO = molecula("CC(CCO)(CC(=O)O)O", "C6H12O4")  # CID 449
COLESTEROL = molecula("C[C@H](CCCC(C)C)[C@H]1CC[C@@H]2[C@@]1(CC[C@H]3[C@H]2CC=C4[C@@]3(CC[C@@H](C4)O)C)C",
                      "C27H46O")  # CID 5997

FUENTES = ("Fuentes: fichas técnicas de atorvastatina (CIMA, FDA), UniProt P04035, Reactome R-HSA-1655829, PMID 20566875. "
           f"{ATRIBUCION}. Estructuras: RDKit/PubChem.")
VERDE, AZUL, NARANJA, ROJO = COLOR["receptor_borde"], COLOR["farmaco"], COLOR["ligando_borde"], COLOR["bloqueo"]


def lamina(numero, etiqueta, titulo, subtitulo, contenido, extra=""):
    c = (f'<rect x="0" y="0" width="{ANCHO}" height="6" fill="{AZUL}"/>'
         + texto(40, 38, f"ATORVASTATINA · LÁMINA {numero} DE {len(LAMINAS)} · {etiqueta.upper()}", tam=14, peso="bold", color=AZUL)
         + texto(40, 76, titulo, tam=32, peso="bold") + texto(40, 104, subtitulo, tam=17, color=SUAVE)
         + contenido + texto(40, ALTO - 34, FUENTES + extra, tam=12.5, color=SUAVE)
         + texto(40, ALTO - 14, "Esquema simplificado y sin escala · Prototipo pendiente de revisión farmacológica",
                 tam=12.5, color=ROJO, peso="bold"))
    return svg(ANCHO, ALTO, c, f"Atorvastatina, lámina {numero}: {titulo}", subtitulo)


def ldl(x, y, tam=34, opacidad=1.0):
    return ilustracion("servier4-ldl.svg", x - tam / 2, y - tam / 2, tam, tam, opacidad=opacidad)


def receptor_ldl(x, y, con_ldl=True, opacidad=1.0):
    """Receptor de LDL anclado a la membrana (proteína Servier) con su partícula de LDL."""
    s = ilustracion("protein-12", x - 16, y - 10, 32, 34, girar=180, opacidad=opacidad)
    if con_ldl:
        s += ldl(x, y - 24, 30, opacidad)
    return s


def chip(x, y, contenido, color, ancho=None):
    """Metabolito sin estructura dibujada: etiqueta redondeada."""
    w = ancho or len(contenido) * 8.6 + 26
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="30" rx="15" fill="#FFFFFF" stroke="{color}" '
            f'stroke-width="1.8"/>' + texto(x + w / 2, y + 20, contenido, tam=15, peso="bold", anclaje="middle",
                                            color=color))


# --- Lámina 1 -----------------------------------------------------------------------

def lamina_1():
    c = ilustracion("servier4-intestino-delgado.svg", 70, 176, 170, 176)
    c += nombre(155, 380, "Intestino") + texto(155, 402, "colesterol de la dieta", tam=15, anclaje="middle", color=SUAVE)
    c += flecha([(250, 264), (352, 264)])
    c += ilustracion("servier4-higado.svg", 360, 170, 250, 186)
    c += nombre(485, 380, "Hígado") + texto(485, 402, "sintetiza colesterol y capta LDL", tam=15, anclaje="middle",
                                            color=SUAVE)
    c += flecha([(616, 240), (716, 240)]) + texto(666, 228, "libera", tam=14, anclaje="middle", color=SUAVE)
    c += flecha([(716, 300), (616, 300)]) + texto(666, 324, "capta LDL", tam=14, anclaje="middle", color=SUAVE)
    c += f'<rect x="720" y="196" width="300" height="136" rx="68" fill="#FBE4E1" stroke="#B4534B" stroke-width="3"/>'
    for ex, ey, g in ((750, 216, 10), (930, 280, -20), (980, 212, 30)):
        c += ilustracion("erythrocyte", ex, ey, 38, 32, girar=g)
    for lx, ly in ((800, 240), (860, 290), (900, 230), (780, 300), (960, 260)):
        c += ldl(lx, ly, 40)
    c += nombre(870, 380, "Sangre") + texto(870, 402, "colesterol LDL («malo»)", tam=15, anclaje="middle", color=SUAVE)
    c += flecha([(1026, 264), (1090, 264)])
    c += (f'<rect x="1096" y="196" width="440" height="136" rx="16" fill="#FFF4EE" stroke="{ROJO}" stroke-width="1.6"/>')
    c += texto(1120, 234, "LDL elevada en sangre", tam=19, peso="bold", color=ROJO)
    c += texto(1120, 264, ["→ se deposita en la pared arterial", "→ aterosclerosis: infarto e ictus"], tam=16)
    # Dónde actúa cada fármaco
    c += guia([(155, 414), (155, 470)]) + etiqueta_farmaco(40, 470, "Ezetimiba: inhibe NPC1L1")
    c += nota_farmaco(52, 520, ["↓ absorción intestinal", "de colesterol"])
    c += guia([(440, 414), (440, 470)]) + etiqueta_farmaco(330, 470, "Estatinas: inhiben la HMG-CoA reductasa",
                                                           destacado=True)
    c += nota_farmaco(342, 520, ["↓ síntesis de colesterol en el hígado", "→ ↑ receptores de LDL"])
    c += guia([(540, 414), (540, 440), (720, 440), (720, 590)]) + etiqueta_farmaco(610, 590,
                                                                                  "Anti-PCSK9: evolocumab, inclisirán")
    c += nota_farmaco(622, 640, ["evitan la degradación del receptor", "de LDL → ↑ captación de LDL"])
    c += guia([(200, 560), (200, 590)]) + etiqueta_farmaco(40, 590, "Colesevelam: secuestra ácidos biliares")
    c += nota_farmaco(52, 640, ["el hígado usa más colesterol", "para fabricar ácidos biliares"])
    c += (f'<rect x="40" y="716" width="1520" height="96" rx="14" fill="#E3F0F8" stroke="{AZUL}" stroke-width="1.5"/>')
    c += texto(66, 754, "Idea clave", tam=18, peso="bold", color=AZUL)
    c += texto(66, 784, "Las estatinas no «sacan» el colesterol de la sangre: el hígado fabrica menos colesterol y, para "
                        "compensar, capta más LDL de la sangre.", tam=18)
    return lamina(1, "Contexto", "¿De dónde viene el colesterol LDL y dónde actúa cada fármaco?",
                  "El hígado fabrica colesterol y retira la LDL de la sangre mediante sus receptores de LDL.", c)


# --- Lámina 2 -----------------------------------------------------------------------

def lamina_2():
    c = ilustracion("emptycell-3d-1", 200, 112, 1375, 728, ajustar="none")
    c += texto(560, 272, "Hepatocito", tam=15, color=SUAVE, cursiva=True)
    c += ilustracion("mitochondrium-1", 300, 640, 112, 60, girar=18)
    # 1-3. Síntesis de colesterol
    c += chip(330, 300, "Acetil-CoA", SUAVE)
    c += flecha([(452, 315), (500, 315)])
    c += chip(504, 300, "HMG-CoA", NARANJA)
    c += ilustracion("endoplasmatic-reticulum-rough-3d", 470, 380, 280, 100)
    c += ilustracion("enzyme-pink-3d", 584, 330, 52, 76, girar=-90)
    c += texto(610, 500, "HMG-CoA reductasa (en el RE)", tam=14, peso="bold", anclaje="middle", color=COLOR["enzima_borde"])
    c += flecha([(612, 316), (700, 316)])
    c += halo(704, 274, 118, 86, NARANJA) + estructura(MEVALONATO, 708, 278, 110, 66)
    c += texto(763, 376, "Mevalonato", tam=14, peso="bold", anclaje="middle", color=NARANJA)
    c += flecha([(826, 316), (880, 316)]) + texto(853, 304, "varios", tam=12, anclaje="middle", color=SUAVE)
    c += texto(853, 340, "pasos", tam=12, anclaje="middle", color=SUAVE)
    c += halo(884, 268, 196, 100, NARANJA) + estructura(COLESTEROL, 888, 272, 188, 86)
    c += texto(982, 386, "Colesterol", tam=14, peso="bold", anclaje="middle", color=NARANJA)
    c += leyenda_paso(240, 560, 1, "Síntesis de colesterol", ["La HMG-CoA reductasa cataliza el",
                                                              "paso limitante: HMG-CoA → mevalonato"])
    # 4. SREBP-2 retenido en el RE
    c += ilustracion("protein-2", 1120, 300, 30, 60) + ilustracion("protein-20", 1150, 310, 56, 44)
    c += texto(1166, 382, "SREBP-2 + SCAP", tam=14, peso="bold", anclaje="middle", color=COLOR["coactivador_borde"])
    c += texto(1166, 402, "retenido en el RE", tam=14, anclaje="middle", color=SUAVE)
    c += flecha([(1080, 320), (1112, 320)])
    c += leyenda_paso(1040, 450, 2, "Hay colesterol suficiente", ["SREBP-2 queda retenido", "en el retículo"])
    # Núcleo con genes poco activos
    c += ilustracion("nucleus", 700, 560, 420, 250, ajustar="none")
    c += texto(910, 640, "Núcleo", tam=15, anclaje="middle", color=COLOR["borde_nucleo"], cursiva=True)
    c += chip(760, 680, "gen LDLR", SUAVE) + chip(900, 680, "gen HMGCR", SUAVE)
    c += texto(910, 740, "transcripción basal", tam=14, anclaje="middle", color=SUAVE)
    # 5. Receptores de LDL en la membrana
    c += receptor_ldl(1420, 300) + receptor_ldl(1490, 420)
    c += leyenda_paso(1220, 560, 3, "Pocos receptores de LDL", ["captan LDL de la sangre", "por endocitosis"])
    c += texto(1500, 212, "Sangre", tam=14, color=SUAVE, cursiva=True)
    return lamina(2, "Fisiología normal", "Cómo regula el hepatocito su colesterol",
                  "Sin fármaco: la célula fabrica colesterol y, si tiene suficiente, mantiene pocos receptores de LDL.", c)


# --- Lámina 3 -----------------------------------------------------------------------

_A, _B = pdb_descargar("1DQ9"), pdb_descargar("1HWK")
SUP_SUSTRATO = superficie_corte(_A, "AB", "HMG", cadena_ligando="A", color_cadena2="#9CB8D9", radio_vista=16)
SUP_FARMACO = superficie_corte(_B, "AB", "117", cadena_ligando="A", marco=SUP_SUSTRATO[2],
                               transformar=alinear(_B, _A, "AB"), color_cadena2="#9CB8D9",
                               color_ligando="#0072B2", radio_vista=16)


def lamina_3():
    c = texto(40, 160, "En el sitio activo de la HMG-CoA reductasa", tam=21, peso="bold")
    c += texto(40, 196, "SUSTRATO NATURAL", tam=14, peso="bold", color=NARANJA)
    c += halo(36, 212, 250, 150, NARANJA) + estructura(HMG_COA, 40, 216, 242, 120)
    c += texto(161, 352, f"HMG-CoA · {formula(HMG_COA)}", tam=13, anclaje="middle", color=NARANJA, peso="bold")
    c += flecha([(292, 286), (318, 286)])
    c += como_imagen(SUP_SUSTRATO[0], 322, 196, 200, 180)
    c += texto(422, 392, "Estructura real: PDB 1DQ9", tam=12.5, anclaje="middle", color=SUAVE, cursiva=True)
    c += texto(548, 256, ["El HMG-CoA entra al", "sitio activo y se", "convierte en mevalonato"], tam=17)
    c += texto(40, 436, "CON ATORVASTATINA", tam=14, peso="bold", color=AZUL)
    c += halo(36, 452, 250, 150, AZUL) + estructura(ATORVASTATINA, 40, 456, 242, 120)
    c += texto(161, 592, f"Atorvastatina · {formula(ATORVASTATINA)}", tam=13, anclaje="middle", color=AZUL, peso="bold")
    c += flecha([(292, 526), (318, 526)])
    c += como_imagen(SUP_FARMACO[0], 322, 436, 200, 180)
    c += texto(422, 632, "Estructura real: PDB 1HWK", tam=12.5, anclaje="middle", color=SUAVE, cursiva=True)
    c += texto(548, 486, ["Ocupa el mismo sitio:", "inhibidor selectivo y", "competitivo"], tam=17)
    c += texto(548, 556, "no se forma mevalonato", tam=17, peso="bold", color=ROJO)
    c += (f'<rect x="40" y="676" width="740" height="150" rx="14" fill="#FFFFFF" stroke="{COLOR["borde_panel"]}"/>')
    c += texto(62, 708, "Para observar", tam=16, peso="bold", color=AZUL)
    c += texto(62, 732, ["Ocupa parte del sitio del HMG-CoA y bloquea su acceso (PMID 11349148).",
                         "El sitio activo se forma entre dos subunidades (verde y azul)."], tam=15, color=SUAVE)
    c += texto(62, 784, "Potencia: IC50 ≈ 6–13 nM", tam=15, peso="bold", color=AZUL)
    c += texto(254, 784, "(ChEMBL, BindingDB). Para inhibir OATP1B1 o CYP3A4", tam=15, color=SUAVE)
    c += texto(62, 806, "hacen falta concentraciones unas 100 a 600 veces mayores: es selectiva.", tam=15,
               color=SUAVE)
    c += f'<line x1="800" y1="140" x2="800" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    # Panel derecho: la respuesta del hepatocito
    c += texto(830, 160, "En el hepatocito: la respuesta que baja la LDL", tam=21, peso="bold")
    c += ilustracion("emptycell-3d-1", 826, 176, 740, 520, ajustar="none")
    c += ilustracion("endoplasmatic-reticulum-rough-3d", 900, 330, 170, 64)
    c += ilustracion("enzyme-pink-3d", 960, 290, 40, 58, girar=-90) + farmaco(1004, 314, "A", s=12)
    c += bloqueo(1040, 300, r=11) + paso(1040, 272, 1, radio=12, tam=13)
    c += texto(985, 420, "↓ colesterol", tam=15, peso="bold", anclaje="middle", color=ROJO)
    c += texto(985, 440, "intracelular", tam=14, anclaje="middle", color=SUAVE)
    c += ilustracion("golgi-3d-1", 1100, 250, 120, 76)
    c += flecha([(1070, 340), (1110, 310)]) + paso(1090, 296, 2, radio=12, tam=13)
    c += texto(1160, 344, "SREBP-2 se activa", tam=13, anclaje="middle", color=COLOR["coactivador_borde"], peso="bold")
    c += ilustracion("nucleus", 1040, 470, 330, 196, ajustar="none")
    c += flecha([(1170, 352), (1180, 500)]) + paso(1200, 470, 3, radio=12, tam=13)
    c += chip(1080, 560, "↑ gen LDLR", VERDE) + chip(1210, 560, "↑ gen HMGCR", SUAVE)
    c += flecha([(1290, 520), (1420, 420)]) + paso(1360, 440, 4, radio=12, tam=13)
    for rx, ry in ((1430, 300), (1480, 360), (1505, 430), (1500, 510), (1460, 580)):
        c += receptor_ldl(rx, ry)
    c += leyenda_paso(834, 734, 1, "Inhibe la enzima", ["↓ síntesis de colesterol", "en el hígado"])
    c += leyenda_paso(1066, 734, 2, "Activa SREBP-2", ["la célula detecta", "el déficit"])
    c += leyenda_paso(1290, 734, 3, "↑ Receptores de LDL", ["más captación de LDL", "de la sangre (4)"])
    c += texto(830, 838, "Resultado: ↓ colesterol LDL en sangre", tam=17, peso="bold", color=VERDE)
    return lamina(3, "Mecanismo de acción", "Cómo actúa atorvastatina",
                  "Inhibidor selectivo y competitivo de la HMG-CoA reductasa, la enzima limitante de la síntesis de colesterol.",
                  c, " PDB 1DQ9, 1HWK; PMID 11349148; ChEMBL; BindingDB.")


# --- Lámina 4 -----------------------------------------------------------------------

def lamina_4():
    # Intestino: absorción
    c = ilustracion("servier4-intestino-delgado.svg", 40, 170, 150, 156)
    c += ilustracion("cc0-pill_blue.svg", 60, 140, 70, 36, girar=-20)
    c += nombre(115, 350, "Intestino") + texto(115, 370, "absorción rápida", tam=14, anclaje="middle", color=SUAVE)
    c += texto(115, 388, "(Cmax en 1–2 h)", tam=14, anclaje="middle", color=SUAVE)
    c += flecha([(196, 250), (300, 250)]) + texto(248, 238, "vena porta", tam=13, anclaje="middle", color=SUAVE)
    c += paso(220, 274, 1, radio=12, tam=13)
    # Hepatocito ampliado
    c += ilustracion("emptycell-3d-1", 296, 140, 760, 440, ajustar="none")
    c += texto(560, 476, "Hepatocito", tam=15, color=SUAVE, cursiva=True, anclaje="middle")
    c += ilustracion("protein-2", 302, 220, 30, 62)
    c += texto(250, 318, "OATP1B1", tam=14, peso="bold", anclaje="middle", color=VERDE)
    c += texto(250, 336, "(gen SLCO1B1)", tam=12.5, anclaje="middle", color=SUAVE)
    c += farmaco(390, 252, "A", s=12) + flecha([(406, 252), (470, 252)]) + paso(438, 226, 2, radio=12, tam=13)
    # Lugar de acción
    c += ilustracion("endoplasmatic-reticulum-rough-3d", 470, 270, 210, 76)
    c += ilustracion("enzyme-pink-3d", 548, 232, 44, 62, girar=-90) + farmaco(600, 258, "A", s=12)
    c += bloqueo(634, 246, r=11)
    c += texto(575, 372, "HMG-CoA reductasa", tam=14, peso="bold", anclaje="middle", color=COLOR["enzima_borde"])
    c += texto(575, 390, "lugar de acción", tam=13, anclaje="middle", color=SUAVE)
    # Metabolismo por CYP3A4
    c += ilustracion("enzyme-green-3d", 710, 400, 46, 64, girar=-90)
    c += texto(734, 490, "CYP3A4", tam=14, peso="bold", anclaje="middle", color=VERDE)
    c += farmaco(668, 432, "A", s=12) + flecha([(684, 432), (712, 432)]) + paso(696, 406, 3, radio=12, tam=13)
    c += flecha([(760, 432), (800, 432)])
    c += chip(806, 400, "orto-OH", AZUL) + chip(806, 440, "para-OH", AZUL)
    c += texto(860, 494, ["metabolitos activos:", "~70 % de la actividad"], tam=13, anclaje="middle", color=AZUL)
    # Bilis
    c += ilustracion("protein-20", 900, 214, 46, 36)
    c += texto(896, 276, "BCRP, P-gp", tam=13, peso="bold", anclaje="middle", color=COLOR["coactivador_borde"])
    c += flecha([(924, 210), (924, 162)]) + paso(950, 186, 4, radio=12, tam=13)
    c += texto(940, 156, "a la bilis", tam=14, peso="bold", color=COLOR["coactivador_borde"])
    # Circulación sistémica
    c += flecha([(1060, 330), (1110, 330)])
    c += (f'<rect x="1114" y="150" width="446" height="262" rx="18" fill="#FBE4E1" fill-opacity="0.5" '
          f'stroke="#B4534B" stroke-width="2"/>')
    c += ilustracion("erythrocyte", 1490, 160, 52, 44, girar=20)
    c += texto(1136, 186, "Circulación sistémica", tam=18, peso="bold", color="#8E3B34")
    c += paso(1136, 222, 5, radio=12, tam=13)
    c += texto(1156, 228, "Llega poco fármaco a la sangre", tam=15, peso="bold")
    c += texto(1136, 258, ["• Biodisponibilidad ~12–14 %; actividad", "  inhibitoria sistémica ~30 %.",
                           "• Unión a proteínas ≥ 98 %.",
                           "• Vida media ~14 h; la actividad dura",
                           "  20–30 h por los metabolitos.",
                           "• Eliminación sobre todo biliar;",
                           "  < 2 % en la orina."], tam=15, interlineado=1.32)
    # Tarjetas inferiores
    c += tarjeta(40, 600, 494, 226, NARANJA, "Interacciones", [
        "• Inhibidores de CYP3A4 (claritromicina,",
        "  itraconazol) u OATP1B1 (ciclosporina):",
        "  ↑ concentración y riesgo de miopatía.",
        "• Rifampicina induce CYP3A4 e inhibe",
        "  OATP1B1: dar ambos a la vez."])
    c += tarjeta(553, 600, 494, 226, VERDE, "Farmacogenética: SLCO1B1", [
        "CPIC, nivel A. Con OATP1B1 de función",
        "disminuida entra menos fármaco al hígado:",
        "↑ exposición en sangre y riesgo de miopatía.",
        "• Función disminuida: iniciar con ≤ 40 mg.",
        "• Función pobre: ≤ 20 mg o rosuvastatina."])
    c += tarjeta(1066, 600, 494, 226, AZUL, "Dato clave", [
        "El hígado es el lugar de acción: la dosis",
        "predice mejor la bajada de LDL que la",
        "concentración en sangre. El primer paso",
        "hepático no es una pérdida: lleva el",
        "fármaco a donde actúa."])
    return lamina(4, "Farmacocinética", "Farmacocinética: el hígado es diana y filtro",
                  "Atorvastatina entra al hepatocito por OATP1B1, actúa allí, se metaboliza por CYP3A4 y sale por la bilis.",
                  c, " CPIC (PMID 35152405); NCBI Gene SLCO1B1.")


# --- Lámina 5 -----------------------------------------------------------------------

def lamina_5():
    w, h = 752, 336
    x1, x2, y1, y2 = 40, 808, 136, 488
    c = tarjeta(x1, y1, w, h, VERDE, "Efecto terapéutico", [
        "• ↓ colesterol LDL entre 41 % y 61 % según la dosis;",
        "  también ↓ colesterol total, apo B y triglicéridos.",
        "• Prevención de eventos cardiovasculares en",
        "  pacientes de alto riesgo.",
        "• Siempre junto con dieta y cambios de estilo de vida."],
        ilustracion("servier4-higado.svg", x1 + w - 170, y1 + 24, 140, 104))
    c += tarjeta(x2, y1, w, h, ROJO, "Error frecuente", [
        "«La estatina saca el colesterol de la sangre.»",
        "Falso: inhibe su síntesis en el hígado. La LDL baja",
        "porque el hepatocito, con menos colesterol,",
        "fabrica más receptores de LDL y la capta.",
        "",
        "Para pensar: ¿por qué funciona peor en quien no",
        "tiene receptores de LDL funcionales?"],
        ldl(x2 + w - 80, y1 + 70, 80))
    c += tarjeta(x1, y2, w, h, AZUL, "Hígado, embarazo y lactancia", [
        "• Transaminasas: elevaciones leves, asintomáticas y",
        "  pasajeras; la lesión hepática clínica es rara",
        "  (LiverTox). Control de la función hepática.",
        "• Contraindicada en el embarazo y la lactancia",
        "  (ficha técnica). LactMed coincide: preferir otra",
        "  opción, sobre todo con recién nacidos o prematuros."],
        ilustracion("cc0-pill_blue.svg", x1 + w - 150, y2 + 26, 120, 60, girar=-20))
    c += tarjeta(x2, y2, w, h, COLOR["enzima_borde"], "Efectos adversos", [
        "• Frecuentes: nasofaringitis, cefalea, molestias",
        "  digestivas, mialgia, hiperglucemia.",
        "• Miopatía y, rara vez, rabdomiólisis: consultar",
        "  ante dolor o debilidad muscular inexplicable.",
        "• Más riesgo de miopatía con inhibidores de CYP3A4",
        "  u OATP1B1 y con SLCO1B1 de función disminuida",
        "  (lámina 4)."], "")
    return lamina(5, "Aplicación clínica", "Del mecanismo al paciente",
                  "Qué significa inhibir la HMG-CoA reductasa para el tratamiento y la seguridad.", c,
                  " LiverTox PMID 31643561; LactMed PMID 30000420.")


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
        ("Medicamento esencial (OMS) y compra conjunta (OPS)",
         ["En la Lista de la OMS como equivalente de simvastatina y en", "polipíldoras; el Fondo Estratégico de la OPS incluye 40 y 80 mg."],
         "OMS, Lista Modelo (eEML) · OPS, precios de referencia 2026"),
        ("Brasil (SUS): ¿qué intensidad conviene?",
         ["Intensidad intermedia (p. ej., atorvastatina 10 mg): < Int$ 10 000", "por AVAC; alta frente a intermedia: > Int$ 27 000 por AVAC."],
         "Umbral: PIB per cápita (~Int$ 11 770) · PMID 25409878, 2015"),
        ("Brasil y Colombia: atorvastatina frente a rosuvastatina",
         ["En Colombia, pasar a rosuvastatina costaría > 200 000 $ por AVAC", "ganado: resultados parecidos, precio mucho mayor."],
         "Precios reales de cada país · PMID 29702787, 2014"),
        ("Reino Unido (NICE) y precio de referencia",
         ["Estatinas de alta intensidad: coste-efectivas; atorvastatina 20 mg", "en prevención primaria. Genérico en EE. UU.: US$ 0,02–0,07/comp."],
         "NICE NG238, 2023 · NADAC (Medicaid), septiembre de 2026"),
    ]:
        f, alto = ficha(40, y, 740, titulo, lineas, fuente, VERDE)
        c += f
        y += alto
    c += f'<line x1="800" y1="140" x2="800" y2="830" stroke="{COLOR["borde_panel"]}" stroke-width="1.5"/>'
    c += texto(830, 160, "¿Funciona igual fuera del ensayo? · Vida real", tam=21, peso="bold", color=AZUL)
    y = 178
    for titulo, lineas, fuente in [
        ("Costa Rica (CRELES): la brecha de control",
         ["En adultos mayores con diabetes, el 78 % tenía LDL ≥ 100 mg/dl:", "la eficacia del ensayo no garantiza el control en la población."],
         "Muestra nacional de ≥ 60 años, n = 542 · PMID 18447930, 2008"),
        ("Brasil: prescripción en un hospital público",
         ["9 594 pacientes con estatina: 18 % sin LDL reciente y 2,4 %", "con LDL ≥ 190 mg/dl. Solo simvastatina (77,6 %) y atorvastatina."],
         "Estudio retrospectivo · PMID 33886720, 2021"),
        ("Brasil (ELSA-Brasil MSK): ¿dolor muscular?",
         ["En 2 156 personas, el uso de estatinas no se asoció con dolor", "ni debilidad muscular en el análisis principal."],
         "Estudio transversal de una cohorte · PMID 37261675, 2024"),
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
                  c, " Lámina 6: fuentes en cada ficha.")


LAMINAS = {1: lamina_1, 2: lamina_2, 3: lamina_3, 4: lamina_4, 5: lamina_5, 6: lamina_6}

if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or sorted(LAMINAS):
        salida = Path(__file__).with_name(f"lamina-{n}.svg")
        salida.write_text(LAMINAS[n](), encoding="utf-8")
        print(salida)
