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

## Licencias

- Código: propio.
- Ilustraciones: Servier Medical Art (CC BY 3.0 y 4.0); detalle en `assets/ilustraciones/ATRIBUCION.md` de cada skill.
- Tipografías: Inter y Source Serif 4 (SIL Open Font License).
- Estructuras: RCSB PDB (CC0).
