#!/usr/bin/env python3
"""Búsqueda en PubMed de la evidencia más reciente (posicionamientos, guías, metaanálisis).

Uso:
    python3 pubmed.py "<consulta>" [--desde 2023] [--max 10] [--tipo sintesis|guias|todo]

Ejemplos:
    python3 pubmed.py "resistance training hypertrophy volume" --desde 2024
    python3 pubmed.py "protein intake energy restriction lean mass" --tipo sintesis
    python3 pubmed.py "position stand resistance training" --tipo guias

Devuelve PMID, año, revista, título y DOI, del más reciente al más antiguo. Solo usa E-utilities del NCBI
(sin clave). Si la red falla, se dice y se recurre a references/evidencia.md.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

FILTROS = {
    "sintesis": '(meta-analysis[pt] OR systematic review[pt] OR "umbrella review"[tiab] OR "overview of reviews"[tiab])',
    "guias": '(guideline[pt] OR practice guideline[pt] OR consensus[tiab] OR "position stand"[tiab] '
             'OR "position statement"[tiab])',
    "todo": "",
}


def _json(servicio, **params):
    params.update(db="pubmed", retmode="json")
    url = EUTILS + servicio + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def construir_consulta(consulta, tipo="sintesis", desde=None):
    partes = [f"({consulta})"]
    if FILTROS[tipo]:
        partes.append(FILTROS[tipo])
    if desde:
        partes.append(f'("{desde}"[dp] : "3000"[dp])')
    return " AND ".join(partes)


def resumir(documento):
    doi = next((i["value"] for i in documento.get("articleids", []) if i.get("idtype") == "doi"), "")
    return {"pmid": documento["uid"], "anio": documento.get("pubdate", "")[:4],
            "revista": documento.get("source", ""), "titulo": documento.get("title", ""), "doi": doi}


def buscar(consulta, tipo="sintesis", desde=None, maximo=10):
    termino = construir_consulta(consulta, tipo, desde)
    ids = _json("esearch.fcgi", term=termino, retmax=maximo, sort="pub_date")["esearchresult"]["idlist"]
    if not ids:
        return []
    resumen = _json("esummary.fcgi", id=",".join(ids))["result"]
    return [resumir(resumen[i]) for i in ids if i in resumen]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("consulta")
    p.add_argument("--desde", type=int, help="año de publicación mínimo")
    p.add_argument("--max", type=int, default=10)
    p.add_argument("--tipo", choices=list(FILTROS), default="sintesis")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    try:
        resultados = buscar(a.consulta, a.tipo, a.desde, a.max)
    except OSError as e:
        print(f"No se pudo consultar PubMed ({e}). Usa references/evidencia.md.", file=sys.stderr)
        return 1
    if a.json:
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
    else:
        for r in resultados:
            print(f"{r['pmid']} · {r['anio']} · {r['revista']} · {r['titulo']}" + (f" · doi:{r['doi']}" if r["doi"] else ""))
        if not resultados:
            print("Sin resultados: amplía la consulta o quita --desde.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
