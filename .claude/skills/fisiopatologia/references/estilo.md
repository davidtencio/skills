# Reglas de estilo

- **Formato:** 1600 × 900 (16:9). Margen lateral de 40 px. Pie con fuentes y atribuciones (12,5 px) y la marca «Prototipo pendiente de revisión clínica» hasta que haya revisión.
- **Cabecera:** etiqueta «ENFERMEDAD · LÁMINA N DE TOTAL · TEMA» (TOTAL = número real de láminas de la serie) (14 px, azul), título (32 px), subtítulo de una línea (17 px).
- **Texto:** mínimo 14 px en el cuerpo; pasos con título de 17 px en negrita y detalle de 15 px. Explicaciones largas al material de apoyo, no a la lámina.
- **Pasos numerados** (`leyenda_paso`) sobre fondo blanco semitransparente cuando quedan sobre una ilustración.
- **Colores con significado** (paleta Okabe-Ito, apta para daltonismo): verde = fisiología normal y efecto terapéutico; bermellón = defecto, daño o complicación; naranja = sustrato o ligando endógeno (p. ej., glucosa); azul = fármacos y diagnóstico; morado = hormonas propias de la enfermedad (p. ej., insulina). Los colores propios de las ilustraciones de Servier se respetan.
- **Fármacos:** en el mapa de tratamiento se usan las etiquetas de `etiqueta_farmaco` (rombo lleno = efecto principal, rombo vacío = efecto adicional), sobre el órgano o el defecto que corrigen.
- **Marco común:** `piezas.Lamina` dibuja cabecera, título, pie y aviso; no se añaden fuentes extra al pie si no caben en una línea (van dentro de la lámina, en un recuadro, o al material).
- **Una familia de ilustraciones por escena.** Si la célula es de Servier, sus organelos también. Las piezas propias se usan para flechas, rótulos y lo que no exista.
- **Rótulos de honestidad:** «Esquema simplificado y sin escala», «Esquema cualitativo: curvas sin escala» en las gráficas sin datos, y la guía o consenso del que sale cada algoritmo de tratamiento con su año.
- **Densidad:** cada lámina explica una idea. Si una lámina necesita más de ~6 pasos o más de ~120 palabras, divídela en dos: el número de láminas no está limitado.
