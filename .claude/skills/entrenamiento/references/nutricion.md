# Nutrición

Los números entre corchetes remiten a `references/evidencia.md`. Los valores salen de `scripts/calculos.py`.

## Orden de prioridades

1. **Calorías** (déficit para perder grasa).
2. **Proteína** suficiente y repartida.
3. **Calidad**: verduras, frutas, legumbres, granos integrales, proteínas magras, grasas no saturadas; pocos ultraprocesados y bebidas azucaradas.
4. Reparto de carbohidratos y grasas según gusto y entrenamiento.
5. Horarios, suplementos y detalles: lo último.

## Calorías

- **Gasto:** Mifflin-St Jeor [18] × factor de actividad. Es una estimación (±10 % o más); el seguimiento manda.
- **Déficit para perder:** el que da 0,5–1 % del peso por semana (por defecto 0,75 %), sin pasar del 25 % del gasto ni bajar de 1200 kcal (mujeres) o 1500 kcal (hombres) sin supervisión [17]. Coincide con el déficit de 500–750 kcal/día de la guía AHA/ACC/TOS [17].
- **Primer objetivo realista:** 5–10 % del peso inicial en 3–6 meses; ya mejora presión, glucosa y lípidos [17].
- **Ganar músculo** (sin exceso de grasa): superávit ~5–10 %, ganancia ~0,25–0,5 % del peso al mes.
- **Fases de mantenimiento:** tras 12–16 semanas de déficit, o si la adherencia se rompe, 2–8 semanas en mantenimiento antes de seguir.

No hace falta contar calorías toda la vida. Opciones de menor a mayor precisión: método del plato → porciones con la mano → registro en una aplicación unas semanas para aprender. Elige con la persona.

## Proteína

- **Objetivo:** 1,6 g/kg/día como base (beneficio hasta ~1,6, con margen hasta ~2,2 [11]); en déficit, 1,8–2,2 g/kg/día para conservar masa magra [12][13]. `calculos.py` usa 2,0 g/kg al perder peso y 1,6 g/kg al mantener o ganar.
- **Con IMC ≥ 30** se calcula sobre el peso de un IMC de 25 (convención práctica).
- **Reparto:** 3–5 tomas de 20–40 g (≈ 0,25–0,4 g/kg por toma) cada 3–4 h [12].
- **Enfermedad renal:** no se sube la proteína sin su nefrólogo.

Equivalencias aproximadas de ~25 g de proteína: 100 g de pechuga de pollo cocida; 1 lata de atún (120–140 g escurrido); 4 claras + 1 huevo; 250 g de yogur griego natural; 150 g de queso cottage o tierno bajo en grasa; 1 taza y media de frijoles o lentejas cocidos + 1 vaso de leche; 1 medida de proteína en polvo.

## Grasa, carbohidratos y fibra

- **Grasa:** 20–35 % de las calorías (convención IOM); `calculos.py` usa 27 %. Prioriza aceite de oliva o canola, aguacate, frutos secos, pescado.
- **Carbohidratos:** el resto. Bajo en carbohidratos o bajo en grasa pierden lo mismo a 12 meses [16]: elige el patrón que la persona disfrute y mantenga. Antes de entrenar, una fuente de carbohidrato ayuda al rendimiento.
- **Fibra:** ≥ 14 g por 1000 kcal (≈ 25–38 g/día), con agua suficiente. Ayuda a la saciedad.

## Patrón de comidas

- **Método del plato** (cada comida principal): ½ verduras, ¼ proteína, ¼ almidón (arroz, papa, tortilla, plátano, pan integral) + una grasa + fruta o lácteo.
- **Número de comidas:** el que la persona prefiera (2–5); lo que importa es el total del día y repartir la proteína. El ayuno intermitente funciona si ayuda a comer menos, pero no supera al consejo dietético habitual en pérdida de peso [23]: se elige por preferencia.
- **Alrededor del entrenamiento:** una comida con proteína y carbohidrato 1–3 h antes y otra en las 2–3 h siguientes basta.
- **Alcohol:** aporta 7 kcal/g y empeora el sueño y la recuperación; limitarlo y contarlo.
- **Comer fuera:** proteína a la plancha + verduras + una porción de almidón; salsas y bebidas aparte.

### Ejemplo de día (~1900 kcal, ~150 g de proteína; adapta porciones al objetivo)

- **Desayuno:** gallo pinto (¾ taza) + 2 huevos + 2 claras + ½ plátano maduro asado + café sin azúcar.
- **Merienda:** yogur griego natural (200 g) + 1 fruta.
- **Almuerzo:** casado con 120 g de pollo o pescado, ½ taza de arroz, ½ taza de frijoles, ensalada abundante, ½ aguacate pequeño.
- **Merienda (pre-entreno):** 2 tortillas de maíz con 60 g de queso tierno bajo en grasa o atún.
- **Cena:** 120 g de carne magra o tofu salteado con verduras + 1 papa mediana.
- Agua a lo largo del día; orina de color claro como guía.

## Suplementos

| Suplemento | Evidencia | Uso |
|---|---|---|
| Creatina monohidrato | Fuerte: mejora fuerza y masa magra con el entrenamiento; segura en adultos sanos [14] | 3–5 g/día, cualquier hora, sin fase de carga. Puede subir 1–2 kg de agua al inicio (no es grasa). Con enfermedad renal: consultar. |
| Cafeína | Fuerte para rendimiento [15] | 3–6 mg/kg ~60 min antes (un café cargado ≈ 80–120 mg). Evitar en las 6–8 h previas a dormir. Hipertensión, arritmias, ansiedad o embarazo: consultar o no usar. |
| Proteína en polvo | Es comida, no imprescindible | Solo si cuesta llegar a la proteína con alimentos. |
| Vitamina D | Solo si hay déficit documentado o poca exposición al sol | Según su médico. |
| «Quemadores», detox, CLA, cetonas de frambuesa, BCAA (con proteína suficiente) | Sin beneficio relevante o con riesgos | No se recomiendan. |

Para cualquier suplemento: marcas con certificación de terceros (Informed Sport, NSF Certified for Sport). Revisa interacciones con los medicamentos de la persona.
