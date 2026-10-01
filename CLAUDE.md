# Instrucciones para Claude

## Material de medicamentos: solo el PDF

Cuando se pida el material de un medicamento (láminas, mecanismo de acción, ficha del mecanismo), genera el material con la skill `mecanismo-accion` y entrega solo el PDF. Puedes construirlo en `ejemplos/<farmaco>/`, como indica la skill, pero no hagas commit, push ni PR con esa carpeta: queda sin seguimiento en git.

La única excepción es cuando la persona usuaria pide expresamente guardar el medicamento en el repositorio, por ejemplo como nuevo ejemplo de la skill.

## Mejoras a la skill: rama y PR

Los cambios en cómo funciona la skill (scripts, `SKILL.md`, referencias, plantillas, estilo, ilustraciones de la biblioteca) se hacen en una rama y se proponen con un PR para que la persona usuaria lo revise. Si al hacer una mejora hay que regenerar los PDF de `ejemplos/` para que sigan siendo coherentes con la skill, inclúyelos en ese mismo PR.
