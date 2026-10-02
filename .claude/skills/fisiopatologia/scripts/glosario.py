"""Comprueba que el glosario del material explique todas las abreviaturas de las láminas y del material.

Uso: python3 scripts/glosario.py ejemplos/<farmaco>

Busca siglas y abreviaturas (p. ej., ARNm, PD-L1, CYP3A4, IgG1κ, mNIS+7) en el texto de `lamina-N.svg` y de
`material.md`, y las compara con los términos de la sección «## Glosario» del material, escritos como
`- **SIGLA:** desarrollo` (una sigla compuesta como CIMA-AEMPS vale si están sus partes). Muestra las que faltan, con un ejemplo de dónde aparecen. Termina con código 1
si falta alguna, para usarlo como verificación antes de generar el PDF.

No cuenta como abreviatura lo que no lo es: identificadores (PMID, códigos PDB, UniProt, ATC, NDA/BLA y
guías NICE con su número), números romanos, unidades y fórmulas químicas.
"""
import html
import re
import sys
from pathlib import Path

# Una sigla: al menos dos mayúsculas, o mayúscula + minúsculas + mayúscula (ARNm, IgG, mNIS), con dígitos,
# guiones, «+» o letras griegas pegados (PD-L1, CYP3A4, IgG1κ, mNIS+7, IFN-γ).
SIGLA = re.compile(r"(?<![\w-])(?=[\w-]*[A-Z][\w-]*[A-Z])[A-Za-z][\w]*(?:[-+][\wαβγδκζθ]+)*[αβγδκζθ]?(?![\w-])")
IGNORAR = {
    # Números romanos y estadios
    "II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII",
    # Unidades y símbolos
    "UI", "mL", "mg", "kDa", "nM", "pM", "mOsm",
    # Nombres propios de bases de datos y programas (no son siglas)
    "UniProt", "PubMed", "ChEMBL", "PubChem", "BindingDB", "LiverTox", "LactMed", "MedlinePlus", "openFDA",
    "RDKit", "AlphaFold", "Bioicons", "BioArt", "LibreOffice", "ClinicalTrials",
    # Licencias y partes de abreviaturas con punto (EE. UU., US$)
    "CC", "BY", "SA", "CC0", "EE", "UU", "US",
    # Palabras escritas en mayúsculas dentro de las láminas
    "CON", "SIN", "NATURAL", "SUSTRATO", "FÁRMACO",
}
IDENTIFICADOR = re.compile(
    r"^(?:\d\w{3}"                          # códigos PDB (4ZQK, 1ICT)
    r"|[OPQ]\d[A-Z\d]{3}\d|[A-NR-Z]\d[A-Z][A-Z\d]{2}\d"  # UniProt
    r"|[A-Z]\d{2}[A-Z]{2}\d{2}"             # ATC (L01FF03)
    r"|R-HSA-\d+|C\d{5,}|TA\d+|NG\d+|S-\d+|CHEMBL\d+|NCT\d+|PMC\d+"  # Reactome, NCI, NICE, FDA, ChEMBL, ClinicalTrials, PMC
    r"|C[\d₀-₉]+H[\d₀-₉]+\w*"               # fórmulas químicas (C26H24FN3O6, C₁₉H₃₀O₂)
    r"|(?:De|Mc|Mac|Van|Von|Di|Le)[A-Z][a-z]+"  # apellidos de autores (DeFronzo, McDonald)
    r")$")


def terminos_glosario(material):
    seccion = re.search(r"^## Glosario\s*$(.*?)(?=^## |\Z)", material, re.M | re.S)
    if not seccion:
        return None
    return {t.strip() for t in re.findall(r"^\s*-\s*\*\*(.+?):?\*\*", seccion.group(1), re.M)}


def textos(carpeta):
    """Texto de las láminas (tspan) y del material, sin la sección Glosario ni enlaces."""
    for svg in sorted(carpeta.glob("lamina-*.svg")):
        contenido = re.sub(r'<image[^>]*/>', "", svg.read_text(encoding="utf-8"))
        for t in re.findall(r"<tspan[^>]*>(.*?)</tspan>", contenido):
            t = html.unescape(t)
            if " · LÁMINA " in t:  # cabecera en mayúsculas: nombre del fármaco y tema
                continue
            yield svg.name, t
    material = (carpeta / "material.md").read_text(encoding="utf-8")
    material = re.sub(r"^## (?:Glosario|Fuentes)\s*$.*?(?=^## |\Z)", "", material, flags=re.M | re.S)
    material = re.sub(r"\]\([^)]*\)|https?://\S+", "", material)
    for linea in material.splitlines():
        yield "material.md", linea


def siglas(carpeta):
    nombres = set(carpeta.name.lower().split("-")) | {carpeta.name.lower()}  # el fármaco en mayúsculas
    encontradas = {}
    for origen, linea in textos(carpeta):
        for m in SIGLA.finditer(linea):
            s = re.sub(r"^[Aa]nti-|^[a-z]+-(?=[A-Z])", "", m.group(0).strip("-+"))  # anti-PD-1, orto-OH
            s = re.sub(r"(-[a-záéíóú]+)+$", "", s)  # HER2-bajo, HER2-positivo
            s = re.sub(r"[₀-₉₋]+$", "", s)  # subíndices: ABC₀₋₂₄
            if s in IGNORAR or IDENTIFICADOR.match(s) or s.isdigit() or s.lower() in nombres:
                continue
            encontradas.setdefault(s, (origen, linea.strip()[:90]))
    return encontradas


def cubierta(sigla, glosario):
    """Una sigla compuesta (CIMA-AEMPS) queda cubierta si el glosario explica cada parte."""
    return sigla in glosario or ("-" in sigla and all(p in glosario for p in sigla.split("-") if p))


def main():
    carpeta = Path(sys.argv[1])
    material = (carpeta / "material.md").read_text(encoding="utf-8")
    glosario = terminos_glosario(material)
    encontradas = siglas(carpeta)
    if glosario is None:
        print("El material no tiene sección «## Glosario». Siglas encontradas:")
        faltan = encontradas
    else:
        # Un término del glosario cubre también sus variantes con número o sufijo (CYP3A4 cubre CYP3A).
        faltan = {s: v for s, v in encontradas.items() if not cubierta(s, glosario)}
        print(f"Glosario: {len(glosario)} términos. Siglas en láminas y material: {len(encontradas)}.")
        if faltan:
            print("Faltan en el glosario:")
    for s, (origen, linea) in sorted(faltan.items(), key=lambda x: x[0].lower()):
        print(f"  {s:<14} {origen}: {linea}")
    if not faltan:
        print("Todas las siglas tienen su descripción.")
    sys.exit(1 if faltan else 0)


if __name__ == "__main__":
    main()
