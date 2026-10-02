# Instrucciones para Claude

## Material de medicamentos y enfermedades: solo el PDF

Cuando se pida material sobre un medicamento o una enfermedad, genéralo con la skill que corresponda y entrega solo el PDF:

- **Medicamento** (láminas, mecanismo de acción, ficha del mecanismo): skill `mecanismo-accion`.
- **Enfermedad** (fisiopatología, clínica y diagnóstico, tratamiento): skill `fisiopatologia`.

Puedes construirlo en `ejemplos/<nombre>/`, como indica cada skill, pero no hagas commit, push ni PR con esa carpeta: queda sin seguimiento en git.

La única excepción es cuando la persona usuaria pide expresamente guardar el material en el repositorio, por ejemplo como nuevo ejemplo de la skill.

## Mejoras a las skills: rama y PR

Los cambios en cómo funciona una skill (scripts, `SKILL.md`, referencias, plantillas, estilo, ilustraciones de la biblioteca) se hacen en una rama y se proponen con un PR para que la persona usuaria lo revise. Si una mejora cambia el PDF de los ejemplos, regenera en ese mismo PR la huella de cada uno (`python3 scripts/pdf.py ejemplos/<nombre> --huella`, que escribe `huella-pdf.json`) y versiona el PDF solo de los dos ejemplos que lo guardan (neumonía nosocomial y durvalumab); los demás PDF de ejemplo no se versionan. Los módulos comunes a las dos skills deben coincidir (lo vigila `tests/test_paridad.py`): si cambias uno, copia el cambio a la otra skill. Antes de proponer el PR, ejecuta los tests (`python -m pytest`, ver el README); si fallan porque el cambio altera un ejemplo a propósito, regenera sus láminas y su PDF.
