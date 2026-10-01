# Plantillas por tipo de enfermedad

Todas las series siguen el mismo arco; cambia qué se dibuja en cada tramo. El número de láminas no es fijo: cada lámina explica una sola idea.

1. **Contexto:** qué falla y dónde, en una imagen (órganos implicados, defecto principal).
2. **Fisiología normal:** cómo funciona el sistema sano, paso a paso (una o dos láminas).
3. **Fisiopatología:** qué se altera, en qué orden y por qué (una a tres láminas).
4. **Clínica:** síntomas explicados por el mecanismo, y complicaciones.
5. **Diagnóstico:** criterios con sus puntos de corte, en tabla, y cómo se confirma.
6. **Tratamiento:** mapa de dónde actúa cada grupo de fármacos sobre los defectos de la lámina 3, y estrategia según la guía vigente.

## Metabólica con varios órganos (ej.: diabetes tipo 2, dislipidemia, obesidad)

- **Contexto:** los órganos alrededor del defecto central (p. ej., el octeto alrededor de la hiperglucemia).
- **Fisiología:**
  - Secreción de la hormona (célula, canales, vesículas).
  - Acción de la hormona en sus tejidos diana (receptor → cascada → transportador).
- **Fisiopatología:**
  - Tarjetas por tejido con el defecto y su consecuencia.
  - Una curva cualitativa de la evolución temporal.
- **Tratamiento:** mapa fármaco–órgano (`etiqueta_farmaco` junto a cada órgano) y algoritmo de la guía (diagrama de decisión con tarjetas).
- **Ejemplo:** `ejemplos/diabetes-tipo-2/`.

## Cardiovascular (ej.: insuficiencia cardiaca, hipertensión)

- **Fisiología:** el ciclo o la regulación (precarga, poscarga, contractilidad; sistema renina-angiotensina-aldosterona, sistema simpático).
- **Fisiopatología:** la compensación que se vuelve dañina (activación neurohormonal, remodelado).
- **Clínica:** congestión frente a bajo gasto; clasificación funcional en tabla.
- **Tratamiento:** cada grupo sobre el eje neurohormonal que bloquea.

## Inflamatoria o autoinmune (ej.: artritis reumatoide, asma, EPOC)

- **Fisiología:** la respuesta inmunitaria o inflamatoria normal (células y citocinas).
- **Fisiopatología:** pérdida de tolerancia o inflamación crónica, y el daño del tejido.
- **Diagnóstico:** criterios de clasificación y pruebas (anticuerpos, espirometría).
- **Tratamiento:** escalones; los biológicos sobre la citocina o la célula que bloquean.

## Infecciosa (ej.: VIH, tuberculosis, hepatitis C)

- **Fisiología:** el ciclo del microorganismo en la célula huésped.
- **Fisiopatología:** cómo daña al huésped y cómo responde el sistema inmunitario.
- **Diagnóstico:** pruebas de cribado y de confirmación, y su ventana.
- **Tratamiento:** cada familia de fármacos sobre el paso del ciclo que bloquea; resistencia.

## Oncológica (ej.: cáncer de mama, leucemia mieloide crónica)

- **Fisiología:** la vía de proliferación o de reparación normal.
- **Fisiopatología:** la mutación o la alteración que activa la vía; invasión y metástasis.
- **Diagnóstico:** estadificación y biomarcadores (tabla).
- **Tratamiento:** terapia dirigida según el biomarcador; para el mecanismo de un fármaco concreto, remitir a la skill `mecanismo-accion`.

## Neurológica o psiquiátrica (ej.: Parkinson, epilepsia, depresión)

- **Fisiología:** el circuito o el neurotransmisor (síntesis, liberación, receptor, recaptación).
- **Fisiopatología:** qué neuronas se pierden o qué circuito se desequilibra.
- **Tratamiento:** cada grupo sobre el punto de la sinapsis que modifica.
