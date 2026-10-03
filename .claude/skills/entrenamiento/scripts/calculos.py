#!/usr/bin/env python3
"""Cálculos de partida para un plan de entrenamiento y nutrición.

Uso:
    python3 calculos.py --sexo hombre --edad 35 --peso 92 --talla 175 --actividad ligera \
        [--cintura 104] [--objetivo perder|mantener|ganar] [--ritmo 0.75]

Devuelve un informe en texto (o JSON con --json). Las fórmulas y sus fuentes están en
references/evidencia.md; todas son estimaciones de partida que se ajustan con el seguimiento real
(peso medio semanal, cintura, rendimiento), nunca valores exactos.
"""
import argparse
import json
import sys

# Factores de actividad clásicos para multiplicar la tasa metabólica basal (aproximados).
FACTORES_ACTIVIDAD = {
    "sedentaria": 1.2,    # trabajo sentado, sin ejercicio
    "ligera": 1.375,      # ejercicio 1-3 días/semana o trabajo con algo de movimiento
    "moderada": 1.55,     # ejercicio 3-5 días/semana
    "alta": 1.725,        # ejercicio intenso 6-7 días/semana
    "muy-alta": 1.9,      # trabajo físico pesado más entrenamiento
}

KCAL_POR_KG = 7700  # aproximación clásica de la energía de 1 kg de tejido perdido; sobrestima la pérdida a largo plazo

# Mínimos orientativos de las dietas para perder peso (AHA/ACC/TOS 2013): 1200-1500 kcal mujeres, 1500-1800 hombres.
MINIMO_KCAL = {"mujer": 1200, "hombre": 1500}


def imc(peso, talla_cm):
    return peso / (talla_cm / 100) ** 2


def categoria_imc(valor):
    if valor < 18.5:
        return "bajo peso"
    if valor < 25:
        return "normal"
    if valor < 30:
        return "sobrepeso"
    if valor < 35:
        return "obesidad grado 1"
    if valor < 40:
        return "obesidad grado 2"
    return "obesidad grado 3"


def tmb_mifflin(sexo, edad, peso, talla_cm):
    """Tasa metabólica basal (kcal/día) de Mifflin-St Jeor."""
    base = 10 * peso + 6.25 * talla_cm - 5 * edad
    return base + 5 if sexo == "hombre" else base - 161


def peso_para_proteina(peso, talla_cm):
    """Peso sobre el que se calcula la proteína.

    Con IMC ≥ 30 se usa el peso correspondiente a un IMC de 25 para esa talla, para no inflar la cifra con masa
    grasa. Es una convención práctica, no un valor derivado de ensayos; se dice así en el plan.
    """
    if imc(peso, talla_cm) >= 30:
        return round(25 * (talla_cm / 100) ** 2, 1), True
    return peso, False


def objetivo_calorico(sexo, get, peso, objetivo, ritmo):
    """Calorías diarias según el objetivo.

    perder: déficit para perder `ritmo` % del peso por semana (0,5-1 %), sin pasar del 25 % del gasto ni bajar del
    mínimo orientativo. ganar: superávit pequeño (~10 %). mantener: el gasto estimado.
    """
    if objetivo == "mantener":
        return round(get), 0
    if objetivo == "ganar":
        return round(get * 1.10), round(get * 0.10)
    deficit = peso * ritmo / 100 * KCAL_POR_KG / 7
    deficit = min(deficit, 0.25 * get)
    kcal = max(get - deficit, MINIMO_KCAL[sexo])
    return round(kcal), round(get - kcal)


def macronutrientes(kcal, peso_proteina, objetivo):
    """Gramos de proteína, grasa, carbohidratos y fibra para unas calorías dadas."""
    g_kg = 2.0 if objetivo == "perder" else 1.6  # 1,6 g/kg: meseta de Morton 2018; en déficit, más alto (ISSN 2017)
    proteina = round(peso_proteina * g_kg)
    grasa = round(kcal * 0.27 / 9)  # dentro del 20-35 % (IOM); el resto, carbohidratos
    carbohidratos = max(round((kcal - proteina * 4 - grasa * 9) / 4), 0)
    fibra = round(kcal / 1000 * 14)  # 14 g por cada 1000 kcal (Guías Alimentarias de EE. UU.)
    return {"proteina_g": proteina, "proteina_g_kg": g_kg, "grasa_g": grasa,
            "carbohidratos_g": carbohidratos, "fibra_g": fibra}


def zonas_fc(edad):
    """FC máxima estimada (Tanaka: 208 − 0,7 × edad) y rangos de intensidad moderada y vigorosa (ACSM)."""
    fcmax = round(208 - 0.7 * edad)
    return {"fc_max": fcmax,
            "moderada": (round(fcmax * 0.64), round(fcmax * 0.76)),
            "vigorosa": (round(fcmax * 0.77), round(fcmax * 0.95))}


def calcular(sexo, edad, peso, talla, actividad, objetivo="perder", ritmo=0.75, cintura=None):
    if sexo not in MINIMO_KCAL:
        raise ValueError("sexo debe ser «hombre» o «mujer» (determina la fórmula de Mifflin-St Jeor)")
    if actividad not in FACTORES_ACTIVIDAD:
        raise ValueError(f"actividad debe ser una de {sorted(FACTORES_ACTIVIDAD)}")
    if objetivo not in ("perder", "mantener", "ganar"):
        raise ValueError("objetivo debe ser perder, mantener o ganar")
    if not 0.25 <= ritmo <= 1.0:
        raise ValueError("ritmo debe estar entre 0,25 y 1 % del peso por semana")

    valor_imc = imc(peso, talla)
    tmb = tmb_mifflin(sexo, edad, peso, talla)
    get = tmb * FACTORES_ACTIVIDAD[actividad]
    kcal, diferencia = objetivo_calorico(sexo, get, peso, objetivo, ritmo)
    p_prot, ajustado = peso_para_proteina(peso, talla)
    resultado = {
        "imc": round(valor_imc, 1),
        "categoria_imc": categoria_imc(valor_imc),
        "tmb_kcal": round(tmb),
        "gasto_total_kcal": round(get),
        "objetivo": objetivo,
        "kcal_objetivo": kcal,
        "deficit_kcal" if objetivo == "perder" else "diferencia_kcal": diferencia,
        "perdida_semanal_estimada_kg": round(diferencia * 7 / KCAL_POR_KG, 2) if objetivo == "perder" else None,
        "peso_para_proteina": p_prot,
        "proteina_sobre_peso_ajustado": ajustado,
        "macros": macronutrientes(kcal, p_prot, objetivo),
        "fc": zonas_fc(edad),
        "agua_ml_orientativa": round(peso * 35 / 50) * 50,  # ~30-35 ml/kg; se ajusta a sed, clima y sudor
    }
    if cintura:
        ict = cintura / talla
        resultado["indice_cintura_talla"] = round(ict, 2)
        resultado["riesgo_cintura_talla"] = ("bajo" if ict < 0.5 else "aumentado" if ict < 0.6 else "alto")
    return resultado


def informe(r):
    m, fc = r["macros"], r["fc"]
    lineas = [
        f"IMC: {r['imc']} ({r['categoria_imc']})",
    ]
    if "indice_cintura_talla" in r:
        lineas.append(f"Índice cintura/talla: {r['indice_cintura_talla']} (riesgo {r['riesgo_cintura_talla']})")
    lineas += [
        f"Tasa metabólica basal (Mifflin-St Jeor): {r['tmb_kcal']} kcal/día",
        f"Gasto total estimado: {r['gasto_total_kcal']} kcal/día",
        f"Calorías objetivo ({r['objetivo']}): {r['kcal_objetivo']} kcal/día",
    ]
    if r["objetivo"] == "perder":
        lineas.append(f"Déficit: {r['deficit_kcal']} kcal/día → ~{r['perdida_semanal_estimada_kg']} kg/semana al inicio")
    nota = " (peso de referencia por IMC ≥ 30)" if r["proteina_sobre_peso_ajustado"] else ""
    lineas += [
        f"Proteína: {m['proteina_g']} g/día ({m['proteina_g_kg']} g/kg sobre {r['peso_para_proteina']} kg{nota})",
        f"Grasa: {m['grasa_g']} g/día · Carbohidratos: {m['carbohidratos_g']} g/día · Fibra: ≥ {m['fibra_g']} g/día",
        f"Agua orientativa: ~{r['agua_ml_orientativa']} ml/día",
        f"FC máx. estimada: {fc['fc_max']} lpm · moderada {fc['moderada'][0]}-{fc['moderada'][1]} · "
        f"vigorosa {fc['vigorosa'][0]}-{fc['vigorosa'][1]} lpm",
    ]
    return "\n".join(lineas)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--sexo", required=True, choices=sorted(MINIMO_KCAL))
    p.add_argument("--edad", required=True, type=int)
    p.add_argument("--peso", required=True, type=float, help="kg")
    p.add_argument("--talla", required=True, type=float, help="cm")
    p.add_argument("--actividad", required=True, choices=list(FACTORES_ACTIVIDAD))
    p.add_argument("--cintura", type=float, help="cm, a la altura del ombligo")
    p.add_argument("--objetivo", default="perder", choices=["perder", "mantener", "ganar"])
    p.add_argument("--ritmo", type=float, default=0.75, help="%% del peso por semana al perder (0,25-1)")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    try:
        r = calcular(a.sexo, a.edad, a.peso, a.talla, a.actividad, a.objetivo, a.ritmo, a.cintura)
    except ValueError as e:
        p.error(str(e))
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else informe(r))


if __name__ == "__main__":
    sys.exit(main())
