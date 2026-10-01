# skills

Skills de Claude de David Tencio. La primera está pensada para la docencia en farmacia. Cada skill vive en `.claude/skills/<nombre>/`, de modo que se carga sola en cualquier sesión de Claude Code abierta con este repositorio.

| Skill | Qué hace |
|---|---|
| [`mecanismo-accion`](.claude/skills/mecanismo-accion/SKILL.md) | Láminas ilustradas y PDF profesional del mecanismo de acción de un medicamento para estudiantes de farmacia, con datos verificados y una cita por dato. Incluye farmacocinética, farmacogenética, indicaciones de la FDA, farmacoeconomía y estudios de vida real, con prioridad para Costa Rica y Latinoamérica. |

## Uso

- **Claude Code (web o terminal):** abre una sesión con este repositorio y pide, por ejemplo, «Haz las láminas del mecanismo de acción de metformina».
- **Chat de claude.ai:** ejecuta `./empaquetar.sh` y sube el `.zip` de `dist/` en Configuración → Capacidades → Skills.

## Requisitos

Python 3 con `rdkit playwright python-pptx pymupdf markdown`, y Chromium. Para extraer nuevos dibujos de los kits de Servier también hace falta LibreOffice Impress. Ver `SKILL.md`.

## Licencias

- Código: propio.
- Ilustraciones: Servier Medical Art (CC BY 3.0 y 4.0); detalle en `assets/ilustraciones/ATRIBUCION.md`.
- Tipografías: Inter y Source Serif 4 (SIL Open Font License).
- Estructuras: RCSB PDB (CC0).

## Fichas técnicas

`fichas-tecnicas/<medicamento>/` guarda fichas técnicas institucionales de medicamentos en Word, junto con el script que las genera (`python3 generar_ficha.py`, requiere `python-docx`).
