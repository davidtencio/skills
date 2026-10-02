"""Comprueba que cada cifra de las láminas está registrada en `evidencias.json`, con la frase de la fuente que la
respalda.

Uso:
    python3 scripts/verificar_evidencias.py ejemplos/<tema>              # sin red: registro completo y coherente
    python3 scripts/verificar_evidencias.py ejemplos/<tema> --en-linea   # además, vuelve a leer cada fuente
    python3 scripts/verificar_evidencias.py ejemplos/<tema> --pendientes # plantilla con las cifras sin registrar

Una «cifra» es un número con unidad (48 h, 7–8 días, 38,3 °C, 6 mg/kg, 95 %) o precedido de un comparador
(≥ 1,0, < 4000/µl). No cuentan la cabecera ni el pie de la lámina, los números de paso, ni las referencias
(lámina 3, recomendación 26, PMID…). Formato de `evidencias.json`:

    {"evidencias": [
       {"cifras": ["48 h"], "laminas": [1], "afirmacion": "La NAH aparece más de 48 h después del ingreso.",
        "fuente": "ERS/ESICM/ESCMID/ALAT 2017 (PMC6018155)", "ref": "ers-2017-resumen", "idioma": "en",
        "frase": "HAP, which develops in hospitalised patients after 48 h of admission",
        "fuerza": "recomendación fuerte, consenso de expertos",
        "verificar": {"tipo": "pmc", "id": "PMC6018155", "patron": "48 h"}}],
     "ignorar": ["cifras que no son datos, p. ej. 30 días si forma parte de un nombre propio"]}

«laminas» dice en qué láminas está la cifra (sin el campo, en todas; con [], solo en el material).
«ref» es la clave de la fuente en bibliografia.json (obligatoria si el ejemplo tiene bibliografía estructurada);
«fuerza», la fuerza de la recomendación cuando la guía la da (fuerte o débil, grado, consenso de expertos).

Sin red se comprueba: que cada cifra de las láminas está en alguna evidencia de esa lámina; que cada evidencia
tiene fuente y frase (y «ref», con bibliografía); y que el número de cada cifra aparece en su frase (38,3 → 38.3;
las cifras traducidas conservan el número). Con --en-linea, cada evidencia con «verificar» se vuelve a leer en la
fuente (tipos: pmc, texto —PMC y, si no, acceso abierto—, pdf, pagina, pubmed) y la frase registrada tiene que
estar en lo que devuelve.
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

NS = "{http://www.w3.org/2000/svg}"
NUMERO = r"\d{1,3}(?:[  ]\d{3})+|\d+(?:[.,]\d+)?"
UNIDAD = (r"%|°C|°|h\b|horas?\b|min\b|días?\b|semanas?\b|meses\b|años\b|mg/kg(?:/d[ií]a)?|mg/l|mg/dl|mmol/l|"
          r"ml/min(?:/1,73 m²|/m²)?|ml/kg|mmHg|µg/ml|g/dl|g\b|mg\b|UI\b|/µl|/mm³|kg/m²|mEq/l")
CIFRA = re.compile(rf"(?:(?:[<>≤≥]|más de|menos de)\s*)?(?:{NUMERO})(?:\s*[–-]\s*(?:{NUMERO}))?\s*(?:{UNIDAD})"
                   rf"|(?:[<>≤≥])\s*(?:{NUMERO})")
REFERENCIA = re.compile(r"(lámina|lám\.|paso|recomendaci[oó]n(es)?|tabla|apartado|PMID|PMC|AWMF)\s*\d", re.I)


def _norm(texto):
    return re.sub(r"\s+", " ", texto.replace(" ", " ").replace(" ", " ")).strip()


PALABRAS = {  # números escritos con letras en la fuente («vier Wochen», «four days», «cuatro semanas»)
    "1": "uno una one ein eine", "2": "dos two zwei", "3": "tres three drei", "4": "cuatro four vier",
    "5": "cinco five fünf", "6": "seis six sechs", "7": "siete seven sieben", "8": "ocho eight acht",
    "9": "nueve nine neun", "10": "diez ten zehn", "12": "doce twelve zwölf"}


def _frase_normalizada(frase):
    """Frase de la fuente preparada para buscar números: coma decimal como punto, sin espacios de miles y con los
    números escritos con letras pasados a cifras."""
    texto = _norm(frase).replace(",", ".")
    for cifra, palabras in PALABRAS.items():
        texto = re.sub(rf"\b({'|'.join(palabras.split())})\b", cifra, texto, flags=re.I)
    return texto.replace(" ", "")


def _numeros(cifra):
    """Números de una cifra, normalizados para buscarlos en la frase de la fuente (38,3 → 38.3; 10 000 → 10000)."""
    return [n.replace(",", ".").replace(" ", "").replace(" ", "").replace(" ", "")
            for n in re.findall(NUMERO, cifra)]


def lineas_lamina(svg):
    """Líneas de texto de una lámina, sin la cabecera («… LÁMINA N DE M …») ni el pie (fuentes y aviso)."""
    raiz = ET.parse(svg).getroot()
    lineas = []
    for t in raiz.iter(NS + "text"):
        partes = [ts.text or "" for ts in t.iter(NS + "tspan")] or [t.text or ""]
        for linea in map(_norm, partes):
            if not linea or re.search(r"LÁMINA \d+ DE \d+|^Fuentes:|Ilustraciones:|Prototipo pendiente", linea):
                continue
            if re.fullmatch(r"\d{1,2}", linea):  # número de un paso
                continue
            lineas.append(linea)
    return lineas


def cifras_lamina(svg):
    cifras = []
    for linea in lineas_lamina(svg):
        sin_refs = REFERENCIA.sub("", linea)
        cifras += [_norm(m.group(0)) for m in CIFRA.finditer(sin_refs)]
    return list(dict.fromkeys(cifras))


def _laminas(carpeta):
    return sorted(((int(m.group(1)), p) for p in carpeta.glob("lamina-*.svg")
                   if (m := re.fullmatch(r"lamina-(\d+)", p.stem))))


def revisar(carpeta):
    """Devuelve (errores, pendientes): errores del registro y cifras de las láminas sin registrar, por lámina."""
    carpeta = Path(carpeta)
    ruta = carpeta / "evidencias.json"
    registro = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {"evidencias": []}
    evidencias, ignorar = registro.get("evidencias", []), {_norm(c) for c in registro.get("ignorar", [])}
    errores, pendientes = [], {}
    con_bibliografia = (carpeta / "bibliografia.json").exists()
    for k, e in enumerate(evidencias, 1):
        nombre = f"evidencia {k} ({', '.join(e.get('cifras', [])) or 'sin cifras'})"
        for campo in ("cifras", "fuente", "frase") + (("ref",) if con_bibliografia else ()):
            if not e.get(campo):
                errores.append(f"{nombre}: falta «{campo}»")
        if "fuerza" in e and not (isinstance(e["fuerza"], str) and e["fuerza"].strip()):
            errores.append(f"{nombre}: «fuerza» vacía (quítala si la guía no la da)")
        frase = _frase_normalizada(e.get("frase", ""))
        for cifra in e.get("cifras", []):
            faltan = [n for n in _numeros(cifra) if n not in frase]
            if e.get("frase") and faltan:
                errores.append(f"{nombre}: {', '.join(faltan)} no aparece en la frase de la fuente")
    for n, svg in _laminas(carpeta):
        registradas = {_norm(c) for e in evidencias if "laminas" not in e or n in e["laminas"]
                       for c in e.get("cifras", [])}
        faltan = [c for c in cifras_lamina(svg) if c not in registradas and c not in ignorar]
        if faltan:
            pendientes[n] = faltan
    return errores, pendientes


def verificar_en_linea(carpeta):
    """Vuelve a leer cada fuente con fuentes.py y comprueba que la frase registrada sigue ahí."""
    sys.path.insert(0, str(Path(__file__).parent))
    import fuentes
    errores = []
    registro = json.loads((Path(carpeta) / "evidencias.json").read_text(encoding="utf-8"))
    for k, e in enumerate(registro.get("evidencias", []), 1):
        v = e.get("verificar")
        if not v:
            continue
        try:
            if v["tipo"] in ("pmc", "texto"):
                r = (fuentes.pmc_texto(v["id"], (v["patron"],), contexto=600) if v["tipo"] == "pmc" else
                     fuentes.texto_completo(v["id"], (v["patron"],)))
                textos = [x["texto"] if isinstance(x, dict) else x
                          for x in r.get("fragmentos", {}).get(v["patron"], [])]
            elif v["tipo"] == "pdf":
                textos = [f["texto"] for f in fuentes.pdf_texto(v["url"], (v["patron"],), contexto=3, maximo=40)
                          ["fragmentos"][v["patron"]]]
            elif v["tipo"] == "pagina":
                textos = fuentes.pagina(v["url"], (v["patron"],), contexto=600)["fragmentos"][v["patron"]]
            elif v["tipo"] == "pubmed":
                textos = [f for a in fuentes.pubmed(f"{v['id']}[pmid]", v["patron"], completo=True)
                          for f in a["frases"]]
            else:
                errores.append(f"evidencia {k}: tipo de verificación desconocido «{v['tipo']}»")
                continue
        except Exception as ex:  # noqa: BLE001
            errores.append(f"evidencia {k}: no se pudo consultar la fuente ({ex})")
            continue
        frase = _norm(e["frase"]).replace("…", "")
        trozos = [t for t in re.split(r"\s*\.\.\.\s*|\s*\[…\]\s*", frase) if t]
        # cada trozo de una frase con «...» basta que esté en algún fragmento (PubMed devuelve frase a frase)
        if not all(any(_norm(t) in _norm(texto) for texto in textos) for t in trozos):
            errores.append(f"evidencia {k} ({', '.join(e['cifras'])}): la frase ya no aparece en {e['fuente']}")
    return errores


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    carpeta = Path(sys.argv[1])
    errores, pendientes = revisar(carpeta)
    if "--pendientes" in sys.argv:
        plantilla = [{"cifras": [c], "laminas": [n], "afirmacion": "", "fuente": "", "idioma": "", "frase": "",
                      "verificar": {"tipo": "", "patron": ""}} for n, cs in pendientes.items() for c in cs]
        print(json.dumps(plantilla, indent=2, ensure_ascii=False))
        return
    if "--en-linea" in sys.argv:
        errores += verificar_en_linea(carpeta)
    for e in errores:
        print(f"ERROR  {e}")
    for n, cifras in pendientes.items():
        print(f"lámina {n}: sin registrar {', '.join(cifras)}")
    total = sum(map(len, pendientes.values()))
    print(f"{len(errores)} errores; {total} cifras sin registrar." if errores or total else
          "Todas las cifras de las láminas están registradas con su fuente.")
    sys.exit(1 if errores or total else 0)


if __name__ == "__main__":
    main()
