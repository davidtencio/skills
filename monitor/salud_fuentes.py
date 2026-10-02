"""Monitor de las fuentes externas de las skills: comprueba que cada fuente responde y devuelve lo esperado.

Uso:
    python3 monitor/salud_fuentes.py                 # todas las skills; informe en Markdown por la salida
    python3 monitor/salud_fuentes.py --informe x.md  # además, guarda el informe
    python3 monitor/salud_fuentes.py --skill fisiopatologia --json   # una skill, resultado en JSON

Cada comprobación hace una consulta mínima con las mismas funciones que usan las skills (fuentes.py, valor.py)
y verifica un campo clave, no solo el estado HTTP: así detecta también cambios de formato (p. ej., que openFDA
deje de devolver el campo «microbiology»). Nunca llama a funciones que descargan a assets/ (…_descargar,
servier_extraer). Termina con código 1 si alguna fuente falla.
"""
import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SKILLS_DIR = RAIZ / ".claude" / "skills"
ESPERA_REINTENTO = 30  # segundos antes de repetir las comprobaciones que fallaron


def _no_vacio(r):
    return bool(r)


# (nombre, dominio, expresión con los módulos f = fuentes y v = valor, validación del resultado)
COMPROBACIONES = {
    "fisiopatologia": [
        ("PubMed (búsqueda)", "eutils.ncbi.nlm.nih.gov", "f.pubmed('metformin', maximo=2)",
         lambda r: r and r[0].get("pmid")),
        ("PMC (texto completo)", "eutils.ncbi.nlm.nih.gov", "f.pmc_texto('PMC6018155', ('48 h',))",
         lambda r: r.get("texto_completo") and r["fragmentos"]["48 h"]),
        ("Guías en PubMed con PMCID", "eutils.ncbi.nlm.nih.gov", "f.guias('type 2 diabetes', maximo=3)", _no_vacio),
        ("MeSH", "eutils.ncbi.nlm.nih.gov", "f.mesh('Diabetes Mellitus, Type 2')",
         lambda r: r and r[0].get("definicion")),
        ("MONDO (OLS)", "www.ebi.ac.uk", "f.mondo('type 2 diabetes mellitus')", _no_vacio),
        ("Europe PMC", "www.ebi.ac.uk", "f.europepmc('metformin mechanism of action', citas_minimas=0)", _no_vacio),
        ("openFDA, 12.4 Microbiology", "api.fda.gov", "f.openfda('dolutegravir')", lambda r: r.get("microbiology")),
        ("DailyMed", "dailymed.nlm.nih.gov", "f.dailymed('meropenem')", lambda r: r.get("fuente")),
        ("CIMA (AEMPS)", "cima.aemps.es", "f.cima('metformina')", lambda r: r.get("fuente")),
        ("Reactome", "reactome.org", "f.reactome('insulin secretion')", _no_vacio),
        ("UniProt", "rest.uniprot.org", "f.uniprot('INSR')", lambda r: r and r[0].get("uniprot") == "P06213"),
        ("MedlinePlus", "connect.medlineplus.gov", "f.medlineplus('metformin')", _no_vacio),
        ("TogoTV (búsqueda en japonés)", "togotv-api.dbcls.jp", "f.togopic('結核')",
         lambda r: any("tuberculosis" in (x.get("nombre") or "") for x in r)),
        ("Wikimedia Commons", "commons.wikimedia.org", "f.commons('Pharmakokinetik', maximo=3)", _no_vacio),
        ("Bioicons (GitHub)", "raw.githubusercontent.com",
         "f._get('https://raw.githubusercontent.com/duerrsimon/bioicons/main/static/icons/cc-by-3.0/"
         "Human_physiology/Servier/lung.svg')", lambda r: b"<svg" in r[:2000]),
        ("Kits de Servier", "smart.servier.com", "f.servier_kits()", _no_vacio),
        ("OMS (nota descriptiva)", "www.who.int",
         "f.pagina('https://www.who.int/news-room/fact-sheets/detail/diabetes', ('insulin',))",
         lambda r: r["caracteres"] > 2000 and r["fragmentos"]["insulin"]),
        ("EUCAST (documentos)", "www.eucast.org",
         "f.pagina('https://www.eucast.org/publications-and-documents/rd', ('Rationale',))",
         lambda r: r["fragmentos"]["Rationale"]),
        ("Käypä hoito (finés)", "www.kaypahoito.fi",
         "f.pagina('https://www.kaypahoito.fi/hoi50056', ('diabe',))", lambda r: r["fragmentos"]["diabe"]),
    ],
    "mecanismo-accion": [
        ("PubChem", "pubchem.ncbi.nlm.nih.gov", "f.pubchem('metformin')", lambda r: r.get("cid") == 4091),
        ("ChEMBL", "www.ebi.ac.uk", "f.chembl('metformin')", _no_vacio),
        ("RCSB PDB (búsqueda)", "search.rcsb.org", "f.pdb_buscar('durvalumab PD-L1', 3)", _no_vacio),
        ("AlphaFold DB (API)", "alphafold.ebi.ac.uk",
         "json.loads(f._get('https://alphafold.ebi.ac.uk/api/prediction/P06213'))",
         lambda r: r and r[0].get("pdbUrl")),
        ("NCI Thesaurus", "api-evsrest.nci.nih.gov", "f.nci_tesauro('metformin')", _no_vacio),
        ("CPIC", "api.cpicpgx.org", "f.cpic('clopidogrel')", _no_vacio),
        ("FDA, aprobaciones (Drugs@FDA)", "api.fda.gov", "f.fda_indicaciones('durvalumab', cartas=False)",
         lambda r: r.get("solicitud")),
        ("LiverTox (NCBI Bookshelf)", "eutils.ncbi.nlm.nih.gov", "f.livertox('metformin')", _no_vacio),
        ("Lista de medicamentos esenciales (OMS)", "list.essentialmeds.org", "v.eml('metformin')", _no_vacio),
        ("NADAC (Medicaid)", "data.medicaid.gov", "v.nadac('metformin')", _no_vacio),
        ("NICE", "www.nice.org.uk", "v.nice('dapagliflozin')", _no_vacio),
        ("ClinicalTrials.gov (observacionales)", "clinicaltrials.gov", "v.observacionales('metformin', 'global')",
         _no_vacio),
    ],
}


def comprobar_skill(skill):
    """Ejecuta las comprobaciones de una skill con sus propios módulos (llamar en un proceso aparte)."""
    import importlib
    import socket
    socket.setdefaulttimeout(90)
    sys.path.insert(0, str(SKILLS_DIR / skill / "scripts"))
    entorno = {"json": json, "f": importlib.import_module("fuentes")}
    if (SKILLS_DIR / skill / "scripts" / "valor.py").exists():
        entorno["v"] = importlib.import_module("valor")

    def una(nombre, dominio, expresion, valida):
        inicio = time.monotonic()
        try:
            ok = bool(valida(eval(expresion, entorno)))  # noqa: S307 (expresiones fijas de este archivo)
            detalle = "" if ok else "respondió, pero sin el contenido esperado"
        except Exception as e:  # noqa: BLE001
            ok, detalle = False, f"{type(e).__name__}: {e}"[:300]
        return {"skill": skill, "fuente": nombre, "dominio": dominio, "ok": ok, "detalle": detalle,
                "segundos": round(time.monotonic() - inicio, 1)}

    resultados = [una(*c) for c in COMPROBACIONES[skill]]
    if not all(r["ok"] for r in resultados):  # segunda oportunidad: los cortes de red suelen ser pasajeros
        time.sleep(ESPERA_REINTENTO)
        for k, c in enumerate(COMPROBACIONES[skill]):
            if not resultados[k]["ok"]:
                primero, resultados[k] = resultados[k]["detalle"], una(*c)
                if resultados[k]["ok"]:
                    resultados[k]["detalle"] = f"intermitente: el primer intento falló ({primero[:150]})"
    return resultados


def informe(resultados):
    fallos = [r for r in resultados if not r["ok"]]
    fecha = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lineas = [f"# Estado de las fuentes externas ({fecha})", "",
              f"**{len(resultados) - len(fallos)} de {len(resultados)} fuentes responden como se espera.**", ""]
    if fallos:
        lineas += ["## Fallan", "", "| Skill | Fuente | Dominio | Detalle |", "|---|---|---|---|"]
        lineas += [f"| {r['skill']} | {r['fuente']} | `{r['dominio']}` | {r['detalle'].replace('|', '/')} |"
                   for r in fallos]
        lineas += [""]
    intermitentes = [r for r in resultados if r["ok"] and r["detalle"]]
    if intermitentes:
        lineas += ["## Intermitentes (respondieron al segundo intento)", ""]
        lineas += [f"- {r['skill']}, {r['fuente']} (`{r['dominio']}`): {r['detalle']}" for r in intermitentes]
        lineas += [""]
    lineas += ["## Todas", "", "| Estado | Skill | Fuente | Dominio | s |", "|---|---|---|---|---|"]
    lineas += [f"| {'✅' if r['ok'] else '❌'} | {r['skill']} | {r['fuente']} | `{r['dominio']}` | {r['segundos']} |"
               for r in resultados]
    return "\n".join(lineas) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--skill", choices=sorted(COMPROBACIONES))
    ap.add_argument("--json", action="store_true", help="resultado en JSON en lugar del informe")
    ap.add_argument("--informe", help="ruta donde guardar también el informe en Markdown")
    a = ap.parse_args()
    if a.skill:
        resultados = comprobar_skill(a.skill)
    else:
        resultados = []
        for skill in COMPROBACIONES:  # un proceso por skill: sus módulos tienen los mismos nombres
            r = subprocess.run([sys.executable, __file__, "--skill", skill, "--json"], capture_output=True,
                               text=True, timeout=3600)
            try:
                resultados += json.loads(r.stdout)
            except json.JSONDecodeError:
                resultados.append({"skill": skill, "fuente": "(todas)", "dominio": "—", "ok": False, "segundos": 0,
                                   "detalle": f"el proceso falló: {r.stderr.strip()[-300:]}"})
    if a.json:
        print(json.dumps(resultados, ensure_ascii=False))
    else:
        texto = informe(resultados)
        print(texto)
        if a.informe:
            Path(a.informe).write_text(texto, encoding="utf-8")
    sys.exit(0 if all(r["ok"] for r in resultados) else 1)


if __name__ == "__main__":
    main()
