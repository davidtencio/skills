# skills

Skills de Claude de David Tencio. Están pensadas para la docencia en farmacia y la formación de profesionales de salud. Cada skill vive en `.claude/skills/<nombre>/`, de modo que se carga sola en cualquier sesión de Claude Code abierta con este repositorio.

| Skill | Qué hace |
|---|---|
| [`mecanismo-accion`](.claude/skills/mecanismo-accion/SKILL.md) | Láminas ilustradas y PDF profesional del mecanismo de acción de un medicamento para estudiantes de farmacia, con datos verificados y una cita por dato. Incluye farmacocinética, farmacogenética, indicaciones de la FDA, farmacoeconomía y estudios de vida real, con prioridad para Costa Rica y Latinoamérica. |
| [`fisiopatologia`](.claude/skills/fisiopatologia/SKILL.md) | Láminas ilustradas y PDF profesional de una enfermedad para profesionales de salud: fisiopatología, clínica y diagnóstico, y tratamiento farmacológico según la guía vigente, con datos verificados y una cita por dato. |

## Uso

- **Claude Code (web o terminal):** abre una sesión con este repositorio y pide, por ejemplo, «Haz las láminas del mecanismo de acción de metformina» o «Haz el material de fisiopatología de la insuficiencia cardiaca».
- **Chat de claude.ai:** ejecuta `./empaquetar.sh` y sube el `.zip` de `dist/` en Configuración → Capacidades → Skills.

## Requisitos

Python 3 con `rdkit playwright python-pptx pymupdf markdown` (`fisiopatologia` no necesita `rdkit` ni `python-pptx`), y Chromium. Para extraer nuevos dibujos de los kits de Servier también hace falta LibreOffice Impress. Ver el `SKILL.md` de cada skill.

## Tests y monitor de fuentes

- **Tests** (`tests/`, sin red): comprueban que las láminas de cada ejemplo se regeneran idénticas, que el glosario no tiene siglas pendientes, que cada ilustración está en `registro.json` con una licencia reutilizable, que cada `SKILL.md` es válido y que lo que cita existe. Los de PDF (marcador `pdf`) regeneran cada PDF y comparan páginas e índice. Se ejecutan en GitHub Actions en cada PR y en cada push a `main`.

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
- Ilustraciones: Servier Medical Art (CC BY 3.0 y 4.0); detalle en `assets/ilustraciones/ATRIBUCION.md` de cada skill.
- Tipografías: Inter y Source Serif 4 (SIL Open Font License).
- Estructuras: RCSB PDB (CC0).
