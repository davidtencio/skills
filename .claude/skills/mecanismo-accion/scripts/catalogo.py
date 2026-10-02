"""Catálogo de la biblioteca local de ilustraciones (`assets/ilustraciones/`), con búsqueda en español e inglés.

Uso:
    python3 scripts/catalogo.py                       # todas, agrupadas por categoría
    python3 scripts/catalogo.py pulmón bacteria       # las que coinciden con algún término (sin tildes ni mayúsculas)
    python3 scripts/catalogo.py inmune --hoja hoja.png  # además, hoja de miniaturas para revisarla con Read

El nombre que se muestra es el que se pasa a `recursos.ilustracion(nombre, x, y, w, h)`. Busca antes aquí que en
las bibliotecas externas: lo que ya está en la biblioteca tiene la licencia comprobada y está registrado.
"""
import json
import sys
import unicodedata
from pathlib import Path

CARPETA = Path(__file__).resolve().parent.parent / "assets" / "ilustraciones"

# Términos en español (y categoría) de cada ilustración, por fragmento del nombre del archivo.
TERMINOS = {
    "adipocyte": ("célula", "adipocito tejido adiposo grasa"),
    "antibody": ("molécula", "anticuerpo inmunoglobulina IgG biológico"),
    "b-lymphocyte": ("inmunitaria", "linfocito B célula B"),
    "bacterium": ("microorganismo", "bacteria bacilo"),
    "brain": ("órgano", "cerebro encéfalo sistema nervioso"),
    "cancerous-cell": ("célula", "célula tumoral cáncer"),
    "corazon": ("órgano", "corazón heart cardiaco"),
    "dendritic-cell": ("inmunitaria", "célula dendrítica presentadora de antígeno"),
    "edema-pulmonar": ("órgano", "edema pulmonar pulmón lung alvéolo"),
    "emptycell": ("célula", "célula vacía membrana"),
    "endoplasmatic-reticulum": ("orgánulo", "retículo endoplasmático"),
    "enzyme": ("molécula", "enzima proteína"),
    "erythrocyte": ("célula", "eritrocito glóbulo rojo hematíe sangre"),
    "golgi": ("orgánulo", "aparato de Golgi"),
    "healthy-lung": ("órgano", "pulmón sano lung"),
    "hepatitis-virus": ("microorganismo", "virus de la hepatitis"),
    "herpes-simplex-virus": ("microorganismo", "virus herpes simple"),
    "higado": ("órgano", "hígado liver hepático"),
    "hipofisis": ("órgano", "hipófisis pituitaria pituitary"),
    "hiv-virus": ("microorganismo", "VIH virus de la inmunodeficiencia humana retrovirus"),
    "influenza-virus": ("microorganismo", "virus de la gripe influenza"),
    "intestino-delgado": ("órgano", "intestino delgado intestine"),
    "kidney": ("órgano", "riñón renal"),
    "langerhans-islet": ("órgano", "islote de Langerhans páncreas célula beta insulina"),
    "ldl": ("molécula", "LDL lipoproteína colesterol"),
    "lung": ("órgano", "pulmón"),
    "macrophage": ("inmunitaria", "macrófago fagocito"),
    "mitochondrium": ("orgánulo", "mitocondria"),
    "muscle": ("órgano", "músculo esquelético"),
    "mycobacterium-tuberculosis": ("microorganismo", "micobacteria tuberculosis bacilo"),
    "nervio": ("órgano", "nervio neurona nerve"),
    "neutrophil": ("inmunitaria", "neutrófilo granulocito polimorfonuclear"),
    "normal-cell": ("célula", "célula normal"),
    "nucleus": ("orgánulo", "núcleo"),
    "pancreas": ("órgano", "páncreas"),
    "pared-gramnegativa": ("microorganismo", "pared bacteriana gramnegativa membrana externa porina"),
    "pared-grampositiva": ("microorganismo", "pared bacteriana grampositiva peptidoglucano"),
    "pill": ("objeto", "comprimido pastilla fármaco oral"),
    "protein": ("molécula", "proteína receptor"),
    "pseudomonas-aeruginosa": ("microorganismo", "Pseudomonas bacilo gramnegativo bacteria"),
    "rinon-suprarrenal": ("órgano", "riñón glándula suprarrenal kidney adrenal"),
    "rna": ("molécula", "ARN ácido ribonucleico"),
    "sars-cov-2": ("microorganismo", "SARS-CoV-2 coronavirus COVID-19 virus"),
    "sporozoites": ("microorganismo", "esporozoíto Plasmodium malaria paludismo parásito"),
    "syringe": ("objeto", "jeringa inyección vía parenteral"),
    "t-lymphocyte": ("inmunitaria", "linfocito T célula T"),
    "testiculo": ("órgano", "testículo testis"),
    "traquea-bronquios": ("órgano", "tráquea bronquios vía aérea"),
    "trypanosoma": ("microorganismo", "tripanosoma Trypanosoma cruzi Chagas parásito"),
    "vejiga-prostata": ("órgano", "vejiga próstata bladder prostate"),
    "vias-intrapulmonares": ("órgano", "bronquiolos alvéolos vías intrapulmonares pulmón"),
}
# Sinónimos que valen para toda una categoría (se buscan además de los términos de cada ilustración).
SINONIMOS_CATEGORIA = {"inmunitaria": "inmune inmunidad defensa leucocito", "microorganismo": "patógeno infección",
                       "orgánulo": "organela célula", "órgano": "anatomía"}
ORDEN = ["órgano", "célula", "inmunitaria", "orgánulo", "microorganismo", "molécula", "objeto", "sin clasificar"]


def _plano(texto):
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return sin_tildes.lower()


def catalogo():
    """Lista de ilustraciones con nombre, categoría, términos, licencia y origen (del registro)."""
    registro = json.loads((CARPETA / "registro.json").read_text(encoding="utf-8"))
    salida = []
    for archivo in sorted(registro):
        clave = next((k for k in sorted(TERMINOS, key=len, reverse=True) if k in archivo), None)
        categoria, terminos = TERMINOS.get(clave, ("sin clasificar", ""))
        datos = registro[archivo]
        salida.append({"nombre": archivo, "categoria": categoria, "terminos": terminos,
                       "licencia": datos.get("licencia", ""), "origen": datos.get("origen", ""),
                       "notas": datos.get("notas", "")})
    return salida


def buscar(*terminos):
    """Ilustraciones que coinciden con alguno de los términos (en el nombre, los términos, el origen o las notas)."""
    buscados = [_plano(t) for t in terminos]
    return [i for i in catalogo()
            if any(b in _plano(" ".join((i["nombre"], i["categoria"], SINONIMOS_CATEGORIA.get(i["categoria"], ""),
                                         i["terminos"], i["origen"], i["notas"])))
                   for b in buscados)]


def main():
    args = sys.argv[1:]
    hoja_png = None
    if "--hoja" in args:
        k = args.index("--hoja")
        hoja_png = args[k + 1]
        del args[k:k + 2]
    elementos = buscar(*args) if args else catalogo()
    if not elementos:
        sys.exit("Nada en la biblioteca local: busca en Bioicons, los kits de Servier, TogoTV o Commons (fuentes.py).")
    for categoria in ORDEN:
        grupo = [i for i in elementos if i["categoria"] == categoria]
        if grupo:
            print(f"\n## {categoria.capitalize()} ({len(grupo)})")
            for i in grupo:
                print(f"- {i['nombre']}: {i['terminos'] or '—'} · {i['licencia']}")
    if hoja_png:
        sys.path.insert(0, str(Path(__file__).parent))
        from hoja_comparacion import hoja
        hoja(hoja_png, [CARPETA / i["nombre"] for i in elementos])
        print(f"\nHoja de miniaturas: {hoja_png}")


if __name__ == "__main__":
    main()
