"""Cálculos de la skill entrenamiento y referencias de su base de evidencia (sin red)."""
import json
import re

import pytest

from conftest import SKILLS_DIR, ejecutar

SKILL = SKILLS_DIR / "entrenamiento"
CALCULOS = SKILL / "scripts" / "calculos.py"


def calcular(*args):
    r = ejecutar(CALCULOS, *args, "--json")
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout)


def test_mifflin_y_gasto():
    # Mifflin-St Jeor, hombre 35 años, 95 kg, 175 cm: 950 + 1093,75 − 175 + 5 = 1873,75
    r = calcular("--sexo", "hombre", "--edad", "35", "--peso", "95", "--talla", "175", "--actividad", "ligera")
    assert r["tmb_kcal"] == 1874
    assert r["gasto_total_kcal"] == round(1873.75 * 1.375)
    assert r["imc"] == 31.0 and r["categoria_imc"] == "obesidad grado 1"


def test_deficit_limitado_y_proteina_sobre_peso_de_referencia():
    r = calcular("--sexo", "hombre", "--edad", "35", "--peso", "95", "--talla", "175", "--actividad", "ligera",
                 "--ritmo", "1")
    assert r["deficit_kcal"] <= 0.25 * r["gasto_total_kcal"] + 1  # tope del 25 % del gasto
    assert r["proteina_sobre_peso_ajustado"] and r["peso_para_proteina"] == round(25 * 1.75 ** 2, 1)
    assert r["macros"]["proteina_g"] == round(r["peso_para_proteina"] * 2.0)


def test_no_baja_del_minimo():
    r = calcular("--sexo", "mujer", "--edad", "60", "--peso", "55", "--talla", "150", "--actividad", "sedentaria",
                 "--ritmo", "1")
    assert r["kcal_objetivo"] >= 1200


def test_macros_cuadran_con_las_calorias():
    r = calcular("--sexo", "mujer", "--edad", "28", "--peso", "70", "--talla", "165", "--actividad", "moderada",
                 "--objetivo", "mantener")
    m = r["macros"]
    kcal = m["proteina_g"] * 4 + m["grasa_g"] * 9 + m["carbohidratos_g"] * 4
    assert abs(kcal - r["kcal_objetivo"]) <= 10
    assert m["proteina_g_kg"] == 1.6 and not r["proteina_sobre_peso_ajustado"]


def test_frecuencia_cardiaca_tanaka():
    r = calcular("--sexo", "mujer", "--edad", "40", "--peso", "70", "--talla", "165", "--actividad", "ligera")
    assert r["fc"]["fc_max"] == 180  # 208 − 0,7 × 40


def test_cintura_talla():
    r = calcular("--sexo", "hombre", "--edad", "35", "--peso", "95", "--talla", "175", "--actividad", "ligera",
                 "--cintura", "105")
    assert r["indice_cintura_talla"] == 0.6 and r["riesgo_cintura_talla"] == "alto"


@pytest.mark.parametrize("args", [["--ritmo", "2"], ["--actividad", "extrema"]])
def test_rechaza_valores_fuera_de_rango(args):
    base = {"--sexo": "hombre", "--edad": "30", "--peso": "80", "--talla": "180", "--actividad": "ligera"}
    base.update(dict(zip(args[::2], args[1::2])))
    r = ejecutar(CALCULOS, *[x for par in base.items() for x in par])
    assert r.returncode != 0


def test_citas_de_las_referencias_existen_en_la_base():
    """Cada [n] citado en SKILL.md y references/ está en la tabla de evidencia.md, y cada fila tiene PMID o DOI."""
    evidencia = (SKILL / "references" / "evidencia.md").read_text(encoding="utf-8")
    filas = dict(re.findall(r"^\| (\d+) \|.*\| ([^|]+) \|$", evidencia, re.M))
    assert filas and all(re.search(r"\d{6,}|10\.\d{4,}/", v) for v in filas.values())
    numeros = sorted(map(int, filas))
    assert numeros == list(range(1, len(numeros) + 1)), "La numeración de evidencia.md debe ser continua"
    citados = set()
    for doc in [SKILL / "SKILL.md", *(SKILL / "references").glob("*.md")]:
        citados |= {n for grupo in re.findall(r"\[(\d+(?:\]\[\d+)*)\]", doc.read_text(encoding="utf-8"))
                    for n in grupo.split("][")}
    assert not sorted(citados - set(filas), key=int), "Citas sin entrada en evidencia.md"


def test_consulta_pubmed_con_filtros():
    codigo = ("import sys; sys.path.insert(0, sys.argv[1]); import pubmed; "
              "print(pubmed.construir_consulta('creatine', 'guias', 2024))")
    r = ejecutar("-c", codigo, SKILL / "scripts")
    assert r.returncode == 0, r.stderr[-2000:]
    consulta = r.stdout.strip()
    assert consulta.startswith("(creatine) AND (guideline[pt]") and '"2024"[dp]' in consulta


# --- Catálogo ilustrado, mapas musculares y PDF -------------------------------------------------------------

EJERCICIOS = SKILL / "assets" / "ejercicios"


def _importar(codigo, *args):
    r = ejecutar("-c", "import json, sys; sys.path.insert(0, sys.argv[1]); " + codigo, SKILL / "scripts", *args)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


def test_catalogo_coherente_y_licencias():
    catalogo = json.loads((EJERCICIOS / "catalogo.json").read_text(encoding="utf-8"))
    registro = json.loads((EJERCICIOS / "img" / "registro.json").read_text(encoding="utf-8"))
    validos = set(_importar("import musculos; print(json.dumps(sorted(musculos.NOMBRES)))"))
    claves = [e["id"] for e in catalogo]
    assert len(claves) == len(set(claves)), "Claves repetidas en el catálogo"
    usadas = set()
    for e in catalogo:
        assert e["principales"] and set(e["principales"] + e["secundarios"]) <= validos, e["id"]
        assert not set(e["principales"]) & set(e["secundarios"]), e["id"]
        assert len(e["claves"]) >= 2 and e["nombre"] and e["equipo"], e["id"]
        assert len(e["imagenes"]) in (0, 2), e["id"]
        for ruta in e["imagenes"]:
            assert (EJERCICIOS / ruta).exists(), ruta
            usadas.add(ruta.split("/")[-1])
    archivos = {p.name for p in (EJERCICIOS / "img").glob("*.svg")}
    assert archivos == usadas == set(registro), "Imágenes sin usar, sin registrar o que faltan"
    for nombre, datos in registro.items():
        assert datos["licencia"] == "CC BY-SA 4.0" and datos["origen"].startswith("https://"), nombre


def test_mapa_resalta_principales_y_secundarios():
    svg = _importar("import musculos; print(json.dumps(musculos.mapa(['pecho'], ['triceps', 'pecho'])))")
    assert 'class="m-pecho principal"' in svg and 'class="m-triceps secundario"' in svg
    assert "m-pecho secundario" not in svg and svg.count("<svg") == 1


def test_mapa_rechaza_musculos_desconocidos():
    r = ejecutar(SKILL / "scripts" / "musculos.py", "pecho,bicepz")
    assert r.returncode != 0 and "bicepz" in r.stderr


def test_marcas_del_plan_se_convierten_en_tarjetas():
    plan = ("# Plan\n\n{{musculos: press-banca-mancuernas, plancha | Sesión A}}\n\n"
            "{{ejercicio: press-banca-mancuernas | 3 × 8–12}}\n\n{{ejercicio: plancha | 3 × 30 s}}\n\n| a | b |\n|---|---|\n| 1 | 2 |\n")
    html = _importar("import plan_pdf; print(json.dumps(plan_pdf.a_html(sys.argv[2])))", plan)
    assert html.count('class="ejercicio"') == 2 and html.count('class="sesion"') == 1
    assert "press-banca-mancuernas-1.svg" in html and "Sin ilustración" in html and "3 × 8–12" in html
    assert "<table>" in html and "{{" not in html
    assert "Créditos de las imágenes" in html and "Everkinetic" in html


def test_marca_con_clave_desconocida_falla():
    r = ejecutar("-c", "import sys; sys.path.insert(0, sys.argv[1]); import plan_pdf; plan_pdf.a_html('{{ejercicio: inventado}}')",
                 SKILL / "scripts")
    assert r.returncode != 0 and "inventado" in r.stderr


@pytest.mark.chromium
def test_pdf_del_ejemplo(tmp_path):
    import shutil
    plan = tmp_path / "plan.md"
    shutil.copyfile(SKILL / "ejemplos" / "principiante-3-dias" / "plan.md", plan)
    r = ejecutar(SKILL / "scripts" / "plan_pdf.py", plan)
    assert r.returncode == 0, r.stderr[-2000:]
    import pymupdf
    doc = pymupdf.open(tmp_path / "plan.pdf")
    texto = "".join(p.get_text() for p in doc)
    assert doc.page_count >= 4 and "Créditos de las imágenes" in texto and "Sentadilla con mancuernas" in texto
    assert sum(len(p.get_images()) + len(p.get_drawings()) for p in doc) > 100  # ilustraciones vectoriales
