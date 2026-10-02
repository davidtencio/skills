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

## Infecciosa

En una infección hay dos protagonistas, el microorganismo y el huésped, y el arco se adapta:

- **Contexto:** agente, vía de transmisión y órgano diana. La transmisión y la prevención (vacunas, profilaxis) se incluyen por defecto, porque explican quién enferma y cómo se evita; las cifras de incidencia y prevalencia, solo si se piden.
- **Fisiología normal:** la defensa del huésped que el microorganismo supera (barreras, inmunidad innata y adaptativa) o el tejido sano que va a dañar.
- **Fisiopatología:** cómo entra, se multiplica y daña (ciclo del microorganismo, toxinas, respuesta inflamatoria del huésped), y qué parte del daño se debe al propio huésped.
- **Clínica:** síntomas explicados por el mecanismo; fases (aguda, latente, crónica) y complicaciones.
- **Diagnóstico:** tabla de pruebas con qué detectan (microorganismo, antígeno, ácido nucleico, anticuerpo), cuándo se positivizan, la muestra y cómo se interpreta el resultado; si hay cribado y confirmación, el algoritmo de la guía.
- **Tratamiento:** cada familia de fármacos sobre el paso o la estructura del microorganismo que bloquea; mecanismos de resistencia; y la estrategia de la guía (empírico o dirigido, duración, control del foco, cuándo cambiar a la vía oral). Si la guía condiciona el tratamiento a la resistencia local, dilo y cita los datos locales disponibles (ver «Infecciones» en `fuentes.md`).

Cada tipo de agente cambia lo que se dibuja:

| Tipo | Ejemplos | Fisiopatología | Tratamiento |
|---|---|---|---|
| **Virus** | VIH, hepatitis B y C, herpes, gripe | Ciclo en la célula huésped (unión, entrada, replicación, ensamblaje, salida) y efecto en el tejido; latencia o cronicidad | Cada familia sobre el paso del ciclo que bloquea (entrada, polimerasa, integrasa, proteasa, salida); barrera genética y resistencia |
| **Bacteria** | Tuberculosis, neumonía neumocócica, infección por *S. aureus* | Adhesión, invasión, factores de virulencia (cápsula, toxinas) y respuesta inflamatoria; intracelular o extracelular | Cada familia sobre su diana bacteriana (pared, ribosoma, ADN girasa, folato, membrana); mecanismos de resistencia (β-lactamasas, bombas de expulsión, cambio de diana) |
| **Hongo** | Candidiasis invasora, criptococosis, aspergilosis | Factor del huésped que permite la infección (inmunosupresión, catéter) e invasión del tejido | Cada familia sobre la membrana (ergosterol) o la pared (β-glucano) |
| **Parásito** | Malaria, enfermedad de Chagas, toxoplasmosis | Ciclo con sus huéspedes y vectores; qué fase causa la enfermedad y cuál se transmite | Fármacos por fase del ciclo (esquizonticida, gametocida, hipnozoiticida); resistencia regional |
| **Toxina** | Tétanos, botulismo, cólera | La toxina y su diana en el huésped; el microorganismo puede no invadir | Antitoxina, soporte y antimicrobiano si procede; vacunación |
| **Síndrome** (varios agentes posibles) | Sepsis, neumonía adquirida en la comunidad, infección urinaria, meningitis | Respuesta del huésped común a todos los agentes; tabla de agentes según la edad, el lugar de adquisición y los factores de riesgo | Tratamiento empírico de la guía según la gravedad y los factores de riesgo, desescalada con el cultivo y duración |

**Recordatorios:**

- El microorganismo se dibuja con la ilustración de Servier de la biblioteca (`servier-hiv-virus`, `servier-bacterium`, `servier-sporozoites`…) o con el color `patogeno` de `componentes.py` si es un esquema propio (ver `estilo.md`).
- Para el mecanismo de un antimicrobiano concreto, con su estructura y su diana a escala molecular, remite a la skill `mecanismo-accion`.

## Oncológica (ej.: cáncer de mama, leucemia mieloide crónica)

- **Fisiología:** la vía de proliferación o de reparación normal.
- **Fisiopatología:** la mutación o la alteración que activa la vía; invasión y metástasis.
- **Diagnóstico:** estadificación y biomarcadores (tabla).
- **Tratamiento:** terapia dirigida según el biomarcador; para el mecanismo de un fármaco concreto, remitir a la skill `mecanismo-accion`.

## Neurológica o psiquiátrica (ej.: Parkinson, epilepsia, depresión)

- **Fisiología:** el circuito o el neurotransmisor (síntesis, liberación, receptor, recaptación).
- **Fisiopatología:** qué neuronas se pierden o qué circuito se desequilibra.
- **Tratamiento:** cada grupo sobre el punto de la sinapsis que modifica.
