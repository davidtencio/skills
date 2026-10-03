---
name: entrenamiento
description: Diseña planes personales de entrenamiento en gimnasio (fuerza, cardio, movilidad), recomendaciones nutricionales (calorías, proteína, distribución de comidas, suplementos con evidencia) y hábitos relacionados (sueño, pasos, seguimiento del progreso) para bajar de peso, ganar fuerza o masa muscular y mejorar la condición física. Se apoya en la evidencia científica más reciente (posicionamientos del ACSM, la OMS y la ISSN, metaanálisis actuales en PubMed) y cita cada recomendación. Úsala siempre que se pida una rutina, un plan de gimnasio, cuántas series o repeticiones hacer, cómo empezar a entrenar, cuántas calorías o cuánta proteína comer para adelgazar o ganar músculo, un menú o plan de alimentación para el gimnasio, si un suplemento sirve, cómo ajustar el plan cuando el peso se estanca, o cómo medir el progreso, aunque no se mencione la palabra «skill». No es para explicar una enfermedad (skill fisiopatologia) ni cómo actúa un medicamento (skill mecanismo-accion).
---

# Plan de entrenamiento y nutrición basado en evidencia

Produce un **plan personal** en PDF ilustrado (con su Markdown de origen) que una persona puede seguir desde el primer día en el gimnasio: rutina semana a semana con la ilustración de cada ejercicio y los músculos que trabaja, objetivo de calorías y proteína, ejemplo de un día de comidas, hábitos y una hoja de seguimiento. Cada recomendación sale de una fuente con nombre y año, y el plan se revisa cada 2–4 semanas con los datos reales.

## Principios

- **Seguridad primero.** Antes de planificar, se hace el cribado de `references/evaluacion-inicial.md`. Si aparece una señal de alarma o una enfermedad cardiovascular, metabólica o renal en una persona inactiva, el plan lo dice al principio y recomienda valoración médica antes del ejercicio intenso; mientras tanto, solo actividad de intensidad baja a moderada.
- **Evidencia actual, citada.** La base está en `references/evidencia.md` (con PMID y DOI). Antes de entregar, comprueba que no haya algo más reciente sobre los puntos clave (ver «Actualizar la evidencia»). Si una recomendación es una convención práctica y no un resultado de ensayos, se dice.
- **Lo que mueve la aguja, primero.** Para bajar de peso: déficit calórico sostenible, proteína suficiente, entrenamiento de fuerza para conservar músculo, actividad diaria (pasos) y sueño. Los detalles (horario de comidas, suplementos, «quemadores») van al final o no van.
- **Adherencia antes que perfección.** El mejor plan es el que la persona puede cumplir: se ajusta a sus días, horario, equipo, gustos, presupuesto y comida local. Se empieza por debajo de su capacidad y se progresa.
- **Estimaciones, no verdades.** Calorías, gasto y FC máxima son fórmulas con error de ±10 % o más. El plan las presenta como punto de partida y explica cómo corregirlas con el seguimiento.
- **Sin promesas ni culpas.** Nada de «pierde 10 kg en un mes». Ritmo objetivo: 0,5–1 % del peso por semana. Lenguaje neutro sobre el cuerpo y la comida.
- **En español**, con unidades métricas; si la persona es de Costa Rica o Latinoamérica, usa alimentos y porciones locales (gallo pinto, frijoles, plátano, tortilla, queso tierno, pollo, atún…).

## Flujo de trabajo

### 1. Recoger los datos
Pide lo que falte de `references/evaluacion-inicial.md` en una sola pregunta agrupada (no en diez mensajes). Lo imprescindible: edad, sexo, peso, talla, objetivo, días y minutos disponibles, experiencia, lesiones o enfermedades y medicamentos. Si la persona prefiere no dar un dato, sigue con supuestos conservadores y dilo.

### 2. Cribado de seguridad
Aplica el algoritmo de `references/evaluacion-inicial.md` (ACSM 2015, con PAR-Q+). Anota el resultado en la primera sección del plan.

### 3. Calcular el punto de partida
```bash
python3 scripts/calculos.py --sexo mujer --edad 32 --peso 78 --talla 162 --actividad ligera \
    --cintura 92 --objetivo perder --ritmo 0.75
```
Da IMC, índice cintura/talla, tasa metabólica basal (Mifflin-St Jeor), gasto total, calorías objetivo, proteína, grasa, carbohidratos, fibra, agua orientativa y rangos de frecuencia cardiaca. `--json` para usar los valores en el plan. Las reglas y sus fuentes están en `references/nutricion.md`.

### 4. Diseñar el entrenamiento
Sigue `references/entrenamiento.md`:
- elige la plantilla según días disponibles y experiencia (cuerpo completo 2–3 días, torso/pierna 4 días…);
- fija series, repeticiones, esfuerzo (repeticiones en reserva, RIR) y descanso;
- añade el trabajo aeróbico y los pasos diarios hasta llegar a la meta semanal de la OMS, de forma progresiva;
- escribe la regla de progresión (doble progresión) y la semana de descarga;
- incluye calentamiento, técnica y alternativas para cada ejercicio (máquina, mancuerna, peso corporal).

### 5. Diseñar la alimentación
Sigue `references/nutricion.md`: calorías y proteína del paso 3, reparto de proteína en 3–5 comidas, un día de ejemplo con alimentos y porciones caseras, lista de compras base, qué hacer al comer fuera, alcohol, y suplementos solo si aportan (creatina, cafeína, proteína en polvo por comodidad, vitamina D si hay déficit).

### 6. Hábitos y seguimiento
Sigue `references/habitos-y-seguimiento.md`: sueño, pasos, control semanal (peso medio, cintura, fotos, registro de cargas), reglas de ajuste cuando el peso se estanca, y cuándo consultar.

### 7. Escribir el plan y generar el PDF
Usa `assets/plantilla-plan.md` y guárdalo en `planes/<nombre-o-alias>/plan.md` (carpeta fuera de git; ver `CLAUDE.md`). Copia `assets/registro-semanal.csv` a la misma carpeta como hoja de seguimiento. Las citas van entre corchetes con el número de `references/evidencia.md` y al final una lista de referencias con PMID o DOI.

Cada ejercicio de la rutina va como tarjeta ilustrada, con una marca en su propia línea:

```
{{musculos: sentadilla-mancuernas, press-banca-mancuernas, remo-polea-baja | Sesión A}}
{{ejercicio: sentadilla-mancuernas | 3 × 8–12 · RIR 2–3}}
```

- `ejercicio`: las dos fases del movimiento ilustradas (con el equipo o la máquina), el mapa de músculos principales y secundarios, el equipo, la prescripción (lo que va tras «|») y tres claves de técnica.
- `musculos`: el mapa de todos los músculos que trabaja una sesión, al inicio de cada sesión.
- Las claves de los ejercicios están en `assets/ejercicios/catalogo.json` (`python3 scripts/plan_pdf.py --lista`). Elige ejercicios con ilustración siempre que sea posible; los pocos que no la tienen (plancha, hip thrust…) salen con el mapa y las claves. Si un ejercicio no está en el catálogo, usa la alternativa más cercana que sí esté o escríbelo como texto normal.

Luego genera el PDF y entrega solo el PDF:

```bash
python3 scripts/plan_pdf.py planes/<nombre>/plan.md
```

El PDF (A4) lleva paginación y, al final, los créditos de las ilustraciones (Everkinetic, CC BY-SA 4.0; ver `assets/ejercicios/ATRIBUCION.md`). Revisa las páginas antes de entregarlo (por ejemplo, convirtiéndolas a imagen con PyMuPDF). Hay un plan de ejemplo con datos ficticios en `ejemplos/principiante-3-dias/plan.md`.

### 8. Revisar el plan (siguientes conversaciones)
Cuando la persona vuelva con su registro: calcula la tendencia (peso medio de la semana frente a la anterior), compara con el ritmo objetivo y aplica las reglas de ajuste de `references/habitos-y-seguimiento.md`. Cambia una sola variable cada vez y explica por qué.

## Actualizar la evidencia

Antes de entregar un plan, busca si hay posicionamientos o metaanálisis más recientes que los de `references/evidencia.md` sobre lo que vas a recomendar:

```bash
python3 scripts/pubmed.py "resistance training prescription" --tipo guias --desde 2025
python3 scripts/pubmed.py "protein intake energy restriction lean mass" --tipo sintesis --desde 2024
```

También sirve la herramienta de PubMed (MCP) si está disponible. Si encuentras algo más reciente y de igual o mayor nivel (posicionamiento, revisión de revisiones, metaanálisis), lee el resumen, úsalo en el plan y propón añadirlo a `references/evidencia.md`. Si la red falla, usa la base local y dilo en una línea.

## Límites

- No sustituye la valoración médica, de nutrición clínica ni de fisioterapia. Embarazo, diabetes con insulina o sulfonilureas, enfermedad renal, cardiopatía, trastornos de la conducta alimentaria, IMC ≥ 40 o lesiones activas: el plan es conservador y recomienda supervisión profesional.
- Si la persona usa un fármaco para la obesidad (semaglutida, tirzepatida…), prioriza la proteína y el entrenamiento de fuerza para conservar masa muscular, y remite a su equipo tratante para el ajuste de calorías.
- No se recomiendan dietas por debajo de los mínimos de `references/nutricion.md`, ayunos prolongados, «quemadores de grasa», diuréticos ni sustancias prohibidas.
