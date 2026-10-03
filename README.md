# skills

Skills de Claude de David Tencio. Las dos primeras están pensadas para la docencia en farmacia y la formación de profesionales de salud; `entrenamiento` es de uso personal. Cada skill vive en `.claude/skills/<nombre>/`, de modo que se carga sola en cualquier sesión de Claude Code abierta con este repositorio.

| Skill | Qué hace |
|---|---|
| [`mecanismo-accion`](.claude/skills/mecanismo-accion/SKILL.md) | Láminas ilustradas y PDF profesional del mecanismo de acción de un medicamento para estudiantes de farmacia, con datos verificados y una cita por dato. Incluye farmacocinética, farmacogenética, indicaciones de la FDA, farmacoeconomía y estudios de vida real, con prioridad para Costa Rica y Latinoamérica. |
| [`fisiopatologia`](.claude/skills/fisiopatologia/SKILL.md) | Láminas ilustradas y PDF profesional de una enfermedad para profesionales de salud: fisiopatología, clínica y diagnóstico, y tratamiento farmacológico según la guía vigente, con datos verificados y una cita por dato. |
| [`entrenamiento`](.claude/skills/entrenamiento/SKILL.md) | PDF ilustrado con el plan personal de gimnasio y nutrición para bajar de peso, ganar fuerza o músculo y mejorar la condición física: cribado de seguridad, rutina con progresión y una tarjeta por ejercicio (ilustración del movimiento y del equipo de Everkinetic, CC BY-SA 4.0, y mapa de músculos principales y secundarios), calorías y proteína calculadas, día de comidas con alimentos locales, hábitos y reglas de ajuste. Cada recomendación cita su fuente (ACSM 2026, OMS, ISSN, metaanálisis recientes) y la skill busca en PubMed si hay algo más nuevo. |

## Uso

- **Claude Code (web o terminal):** abre una sesión con este repositorio y pide, por ejemplo, «Haz las láminas del mecanismo de acción de metformina», «Haz el material de fisiopatología de la insuficiencia cardiaca» o «Hazme un plan de gimnasio para bajar de peso».
- **Chat de claude.ai:** ejecuta `./empaquetar.sh` y sube el `.zip` de `dist/` en Configuración → Capacidades → Skills.

## Requisitos

Python 3 con `rdkit playwright python-pptx pymupdf markdown` (`fisiopatologia` no necesita `rdkit` ni `python-pptx`), y Chromium. `entrenamiento` necesita `playwright pymupdf markdown` y Chromium para el PDF (y red para consultar PubMed). Para extraer nuevos dibujos de los kits de Servier también hace falta LibreOffice Impress. Ver el `SKILL.md` de cada skill.

## Tests y monitor de fuentes

- **Tests** (`tests/`, sin red). Comprueban que:
  - las láminas de cada ejemplo se regeneran idénticas y ningún texto se pisa ni se sale de su recuadro (`revisar_lamina.py`, marcador `chromium`);
  - el glosario no tiene siglas pendientes y, en los ejemplos con `evidencias.json`, cada cifra de las láminas está registrada con la frase de su fuente;
  - cada ilustración está en `registro.json` con una licencia reutilizable y tiene términos en `catalogo.py`;
  - cada `SKILL.md` es válido y lo que cita existe;
  - el código común de las dos skills es idéntico (`test_paridad.py`): si cambias un módulo compartido, copia el cambio a la otra skill;
  - los analizadores de `fuentes.py` interpretan bien respuestas reales grabadas (`tests/datos/fuentes/`).
  - la bibliografía estructurada (`bibliografia.py`) numera, formatea y comprueba las citas `[@clave]`, y el PDF las enlaza con su referencia (`test_bibliografia.py`).

  Los de PDF (marcador `pdf`) regeneran cada PDF y lo comparan con la huella del ejemplo (`huella-pdf.json`: páginas, índice y texto de cada página). Solo se versiona un PDF de ejemplo por skill, para verlo: `neumonia-nosocomial.pdf` y `durvalumab.pdf`. Se ejecutan en GitHub Actions en cada PR y en cada push a `main`.

  ```bash
  pip install -r requirements-test.txt && python -m playwright install chromium
  python -m pytest -m "not pdf"   # rápidos
  python -m pytest -m pdf         # PDF (lentos)
  ```

- **Monitor de fuentes** (`monitor/salud_fuentes.py`, con red): hace una consulta mínima a cada fuente externa (PubMed, PMC, openFDA, CIMA, UniProt, TogoTV, Commons…) y verifica un campo clave. Repite una vez lo que falla y termina con código 1 si alguna fuente sigue sin responder como se espera. Una rutina semanal lo ejecuta y abre un *issue* si algo falla.

  ```bash
  python3 monitor/salud_fuentes.py --informe informe.md
  ```

## Licencias

- Código: propio.
- Ilustraciones: Servier Medical Art (CC BY 3.0 y 4.0); detalle en `assets/ilustraciones/ATRIBUCION.md` de cada skill de láminas. Ejercicios de `entrenamiento`: Everkinetic (CC BY-SA 4.0), detalle en `assets/ejercicios/ATRIBUCION.md`.
- Tipografías: Inter y Source Serif 4 (SIL Open Font License).
- Estructuras: RCSB PDB (CC0).
