# Skill: mecanismo de acción

Generará imágenes didácticas del mecanismo de acción de medicamentos para estudiantes de farmacia, con tres paneles (fisiología normal → acción del fármaco → consecuencias) y material de apoyo.

Instrucciones de uso: `SKILL.md`. Referencias: `references/` (fuentes, plantillas, estilo, verificación, ficha del mecanismo).
Ejemplo de referencia: darolutamida (pendiente de revisión farmacológica).

- `scripts/componentes.py`: biblioteca visual propia (membranas, núcleo, ADN, flechas, bloqueos, pasos, etiquetas).
- `scripts/recursos.py`: inserta ilustraciones de Servier Medical Art (`assets/ilustraciones/`, CC BY 3.0; ver `ATRIBUCION.md`).
- `scripts/estructuras.py`: estructuras químicas 2D exactas con RDKit, verificadas por fórmula molecular.
- `scripts/fuentes.py`: consultas a PubChem, ChEMBL, RCSB PDB, AlphaFold, Bioicons y kits de Servier (con registro de licencias).
- `scripts/superficie.py`: superficie real de la diana (PDB/AlphaFold) cortada para mostrar el bolsillo de unión.
- `scripts/hoja_comparacion.py`: hoja para comparar candidatos visuales y elegir.
- `scripts/renderizar.py`: SVG → PNG con Chromium (Playwright).
- `ejemplos/darolutamida/laminas.py`: serie de 4 láminas (versión actual); `darolutamida.py`: versión anterior en una sola imagen.

Requisitos: Python 3, `pip install rdkit playwright python-pptx pymupdf`, Chromium y LibreOffice Impress (solo para extraer de los kits de Servier).
