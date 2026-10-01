"""Genera la ficha técnica institucional de durvalumab 50 mg/mL, vial de 10 mL (500 mg), en Word.

Uso: python3 generar_ficha.py  →  crea durvalumab-500mg-10ml.docx junto a este script.
Datos verificados en la ficha técnica de la EMA/AEMPS (CIMA, n.º 1181322001), la ficha de la FDA
(DailyMed/openFDA, revisión 2026-08-31) y el índice ATC/DDD de la OMS, consultados el 2026-10-01.
"""
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

PENDIENTE = "[por completar]"
DENOMINACION = "Durvalumab 50 mg/mL, concentrado para solución para perfusión, vial de 10 mL (500 mg)"

GRIS = "D9E2F3"


def sombrear(celda, color=GRIS):
    tc = celda._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    tc.append(shd)


def texto(celda, contenido, negrita=False, tam=10):
    """Escribe en una celda. contenido: str o lista de str (una viñeta por elemento)."""
    celda.text = ""
    lineas = contenido if isinstance(contenido, list) else [contenido]
    for i, linea in enumerate(lineas):
        p = celda.paragraphs[0] if i == 0 else celda.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        if isinstance(contenido, list):
            linea = "• " + linea
        r = p.add_run(linea)
        r.bold = negrita
        r.font.size = Pt(tam)


def campo(parrafo, instruccion):
    """Inserta un campo automático de Word (PAGE, NUMPAGES)."""
    for tipo, valor in (("begin", None), ("instr", instruccion), ("separate", None), ("text", "1"), ("end", None)):
        run = parrafo.add_run()
        run.font.size = Pt(8)
        if tipo == "instr":
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = f" {valor} "
        elif tipo == "text":
            el = OxmlElement("w:t")
            el.text = "1"
        else:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), tipo)
        run._r.append(el)


def seccion(doc, titulo, filas):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(4)
    r = h.add_run(titulo)
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0x1F, 0x3A, 0x68)
    t = doc.add_table(rows=0, cols=2)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for nombre, valor in filas:
        c = t.add_row().cells
        c[0].width, c[1].width = Cm(4.6), Cm(12.4)
        texto(c[0], nombre, negrita=True)
        sombrear(c[0])
        texto(c[1], valor)
    t.autofit = False
    t.columns[0].width, t.columns[1].width = Cm(4.6), Cm(12.4)
    return t


def encabezado(doc):
    sec = doc.sections[0]
    t = sec.header.add_table(rows=3, cols=2, width=Cm(17))
    t.style = "Table Grid"
    datos = [
        ("FICHA TÉCNICA DE MEDICAMENTO", f"Código institucional: {PENDIENTE}"),
        (DENOMINACION, "Versión: 01   ·   Sustituye a: no aplica (emisión inicial)"),
        (f"Aprobada en sesión: {PENDIENTE}   ·   Fecha: {PENDIENTE}", f"Referencia: {PENDIENTE}"),
    ]
    for fila, (a, b) in zip(t.rows, datos):
        texto(fila.cells[0], a, negrita=fila is t.rows[0], tam=8)
        texto(fila.cells[1], b, tam=8)
    sombrear(t.rows[0].cells[0])
    sombrear(t.rows[0].cells[1])

    p = sec.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"{DENOMINACION} · Versión 01 · Página ")
    r.font.size = Pt(8)
    campo(p, "PAGE")
    r = p.add_run(" de ")
    r.font.size = Pt(8)
    campo(p, "NUMPAGES")


def main():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.59), Cm(27.94)
    sec.left_margin = sec.right_margin = Cm(2.2)
    sec.top_margin, sec.bottom_margin = Cm(3.2), Cm(2)
    doc.styles["Normal"].font.name = "Arial"
    doc.styles["Normal"].font.size = Pt(10)
    encabezado(doc)

    titulo = doc.add_paragraph()
    titulo.paragraph_format.space_before = Pt(6)
    titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = titulo.add_run("FICHA TÉCNICA\n" + DENOMINACION.upper())
    r.bold = True
    r.font.size = Pt(13)

    seccion(doc, "1. DESCRIPCIÓN GENERAL", [
        ("Principio activo", "Durvalumab. Anticuerpo monoclonal humano IgG1κ dirigido contra el ligando 1 de muerte "
                             "programada (PD-L1), producido en células de ovario de hámster chino (CHO) mediante "
                             "tecnología de ADN recombinante."),
        ("Código ATC", "L01FF03 (Agentes antineoplásicos › Anticuerpos monoclonales y conjugados anticuerpo-fármaco › "
                       "Inhibidores de PD-1/PD-L1 › durvalumab)."),
        ("Concentración", "50 mg/mL. Cada vial contiene 500 mg de durvalumab en 10 mL de concentrado."),
        ("Forma farmacéutica", "Concentrado para solución para perfusión (solución inyectable concentrada, estéril, "
                               "sin conservantes). Se acepta la denominación «solución inyectable» o «solución "
                               "concentrada para infusión» cuando así conste en el registro sanitario."),
        ("Vía de administración", "Intravenosa (perfusión), previa dilución."),
    ])

    seccion(doc, "2. ESPECIFICACIONES TÉCNICAS", [
        ("Especificaciones de calidad y metodología analítica", [
            "Producto biológico sin monografía farmacopeica: debe cumplir las especificaciones de producto terminado "
            "del fabricante aprobadas en el registro sanitario vigente ante el Ministerio de Salud de Costa Rica.",
            "Metodología analítica validada, conforme a los principios de ICH Q6B (identidad, pureza e impurezas, "
            "potencia, cantidad de proteína) y a los ensayos farmacopeicos generales aplicables a inyectables: "
            "esterilidad, endotoxinas bacterianas, partículas visibles y subvisibles, pH, osmolalidad y volumen "
            "extraíble.",
        ]),
        ("Atributos de calidad", [
            "Solución de transparente a opalescente, de incolora a ligeramente amarilla, sin partículas visibles.",
            "pH aproximado de 6,0 y osmolalidad aproximada de 400 mOsm/kg (producto de referencia).",
            "Vial de dosis única, sin conservantes.",
        ]),
        ("Condiciones de transporte", [
            "Cadena de frío entre 2 °C y 8 °C en todo el trayecto hasta la entrega. No congelar.",
            "Protegido de la luz y de golpes; evitar la agitación del producto.",
            "Embalaje de transporte calificado para mantener el intervalo de temperatura, con registrador continuo "
            "de temperatura (data logger) o indicador equivalente.",
        ]),
        ("Condiciones de almacenamiento", "Conservar en refrigeración entre 2 °C y 8 °C. No congelar. No agitar. "
                                          "Conservar el vial en su empaque secundario para protegerlo de la luz."),
        ("Vida útil", [
            "La aprobada en el registro sanitario (referencia: 36 meses para el vial sin abrir).",
            f"Vida útil remanente mínima al momento de la entrega: {PENDIENTE} (según la política institucional "
            "vigente).",
        ]),
    ])

    seccion(doc, "3. REQUISITOS DE EMPAQUE PRIMARIO", [
        ("Presentación", "Vial (frasco ampolla) de vidrio tipo I, con tapón de elastómero y precinto de aluminio con "
                         "tapa de apertura fácil (flip-off)."),
        ("Contenido", "10 mL de concentrado, equivalentes a 500 mg de durvalumab (50 mg/mL). Un vial de dosis única."),
        ("Aditamentos de dosificación", "No aplica."),
        ("Rotulación", [
            "Conforme al RTCA 11.01.02:04 «Productos farmacéuticos. Etiquetado de productos farmacéuticos para uso "
            "humano» y sus reformas vigentes.",
            "Como mínimo: nombre del producto, denominación común internacional (durvalumab), concentración "
            "(50 mg/mL) y contenido total (500 mg/10 mL), vía de administración (intravenosa), número de lote, fecha "
            "de vencimiento y nombre del fabricante o titular.",
            "Etiqueta legible e indeleble, que resista la refrigeración y la condensación sin desprenderse.",
        ]),
    ])

    seccion(doc, "4. REQUISITOS DE EMPAQUE SECUNDARIO", [
        ("Presentación", "Caja de cartón individual que proteja el vial de la luz."),
        ("Cantidad de unidades", "Un (1) vial de 10 mL (500 mg) por caja."),
        ("Sistema de fijación", "Inserto, separador o bandeja que inmovilice el vial y lo proteja de quebraduras y "
                                "derrames."),
        ("Rotulación", [
            "Conforme al RTCA 11.01.02:04 y sus reformas vigentes, incluidas las leyendas especiales del Anexo 1 que "
            "correspondan según la composición del producto ofertado.",
            "Como mínimo: nombre del producto, denominación común internacional, concentración y contenido total, "
            "forma farmacéutica, vía de administración, composición cuali-cuantitativa del principio activo por mL, "
            "número de lote, fecha de vencimiento, número de registro sanitario, nombre y país del fabricante.",
            "Condiciones de almacenamiento: «Conservar en refrigeración entre 2 °C y 8 °C. No congelar. No agitar. "
            "Proteger de la luz».",
            "Leyendas de venta bajo prescripción médica y de uso exclusivo institucional, según la disposición "
            "vigente de la institución.",
        ]),
    ])

    seccion(doc, "5. REQUISITOS TÉCNICOS DOCUMENTALES A PRESENTAR EN LA OFERTA", [
        ("Documentos", [
            "Registro sanitario vigente emitido por el Ministerio de Salud de Costa Rica para la presentación "
            "ofertada (50 mg/mL, vial de 10 mL).",
            "Certificado de Buenas Prácticas de Manufactura vigente del fabricante del producto terminado.",
            "Monografía o inserto aprobado en español.",
            "Especificaciones del producto terminado y certificado de análisis de un lote comercial.",
            "Declaración de la vida útil aprobada y de las condiciones de almacenamiento.",
            "Artes o muestras de los empaques primario y secundario.",
            "Descripción del sistema de distribución en cadena de frío (embalaje calificado y monitoreo de "
            "temperatura).",
        ]),
    ])

    seccion(doc, "6. REQUISITOS TÉCNICOS POR PRESENTAR EN CADA ENTREGA", [
        ("Documentos", [
            "Certificado de análisis de cada lote entregado, emitido por el fabricante.",
            "Registro de temperatura del transporte, desde la salida del almacén del proveedor hasta la recepción, "
            "que demuestre el cumplimiento del intervalo de 2 °C a 8 °C.",
            "El producto entregado debe corresponder al registro sanitario y a la presentación adjudicados, y cumplir "
            "la vida útil remanente indicada en el apartado 2.",
        ]),
    ])

    seccion(doc, "7. CONTROL DE CAMBIOS GENERAL DE LA FICHA TÉCNICA", [
        ("Versión 01", f"Emisión inicial. Sesión: {PENDIENTE}. Fecha: {PENDIENTE}."),
    ])

    seccion(doc, "FUENTES DE REFERENCIA (consultadas el 1 de octubre de 2026)", [
        ("Ficha técnica UE", "IMFINZI 50 mg/ml concentrado para solución para perfusión, AEMPS/CIMA n.º 1181322001 "
                             "(EU/1/18/1322/001, vial de 500 mg), secciones 2, 3, 6.1, 6.3, 6.4, 6.5 y 6.6. "
                             "https://cima.aemps.es/cima/dochtml/ft/1181322001/FT_1181322001.html"),
        ("Ficha técnica FDA", "IMFINZI (durvalumab) injection, sección 16 «How Supplied/Storage and Handling», "
                              "revisión del 31-08-2026 (openFDA/DailyMed)."),
        ("Código ATC", "WHO Collaborating Centre for Drug Statistics Methodology, índice ATC/DDD: L01FF03 "
                       "(DDD 53,6 mg, parenteral). https://atcddd.fhi.no/atc_ddd_index/?code=L01FF03"),
        ("Rotulación", "RTCA 11.01.02:04 Productos farmacéuticos. Etiquetado de productos farmacéuticos para uso "
                       "humano, y sus reformas."),
    ])

    salida = Path(__file__).with_name("durvalumab-500mg-10ml.docx")
    doc.save(salida)
    print(salida)


if __name__ == "__main__":
    main()
