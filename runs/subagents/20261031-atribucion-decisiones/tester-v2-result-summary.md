## 1. Filas P01–P09 (parte «Humana») frente a ítems 0–2

| Fila | Dictamen | Palabra/omisión relevante |
|---|---|---|
| P01 | PASS | «Extender Mindmap» omitido «lectura y operación manual primero» (omisión, no añade); «Scion se designa cuando abordemos ese ramal» = ítem 2 literal; «responsable producto/aceptación de deltas» = ítem 2 + «Sí, yo» |
| P02 | PASS | «Kimun fuera de esta línea base» parafrasea «sin migrar a Kimun»; root ya indicó que P02 no requiere reescritura |
| P03 | PASS | Texto idéntico a la pregunta ítem 1; es premisa, no respuesta, pero la respuesta la acepta («En ambos casos») sin contradecirla |
| P04 | PASS | «Markdown editable tras probar API reversible, conflictos y campos protegidos» literal; «source_mode=editable» exento por encargo de root |
| P05 | PASS | Omite «promoción» (queda en P06); «Guardar no hace commit» y «cierre respeta el workflow Deskops» = pregunta ítem 1 |
| P06 | PASS | «Promoción y cierre respetan workflow Deskops» + «con otro coordinador escribiendo… lectura/handoff» recuperados; sin añadido |
| P07 | N/A | Fila rotulada Técnica conservadora, sin parte Humana |
| P08 | PASS | «Taller temporal; solicitante participa» y las tres cifras = pregunta ítem 2 + «acepto Taller y esos objetivos iniciales» |
| P09 | N/A | Fila rotulada Técnica conservadora, sin parte Humana |

No encontré ninguna fila Humana que afirme más de lo aceptado.

## 2. Condiciones perdidas
- No hay pérdida que amplíe la afirmación. La única omisión sensible es «lectura y operación manual primero» en P01 y «promoción» en P05; ambas quedan cubiertas (ítem 0 en P02/nodos, promoción en P06) o no añaden contenido.

## 3. Precisiones técnicas y su fila T-Pxx
- P01 «operador» / «recepción técnica pendiente por delta» → T-P01, ambas nombradas. PASS
- P03 «canal público… probado; lock solo UI no basta» → T-P03, nombrada. PASS
- P04 «con revisión» y «recuperación» → T-P04 («revisión esperada y recuperación»). PASS
- P05 «CLI/coordinador» y «refresco verificable» → T-P05 dice «refresco que verifica el resultado»; misma precisión con otra frase, no se pierde. PASS (observación de redacción)
- P06 «preparar» y «canal completo comprobado» → T-P06, ambas nombradas. PASS

## 4. Adendas frente al archivo actual
- Adenda 1 (T-P01 161-167/225-233; T-P05 1984-1987/1991-1994; T-P07 con 945-946): coincide con el texto actual de `decisiones.md`.
- Adenda 2 (P01 sin «Operador», P03 con el texto de la pregunta, P04 «Markdown editable», P06 con la condición recuperada, T-P06 conservada): coincide con el archivo actual.
- Sin discrepancias detectadas adenda ↔ archivo. Las afirmaciones sobre versiones anteriores («la fila decía…», «era falso que…») no las pude verificar sin git.

## 5. `dag.yaml` 515 y 543 y `preflight-input-v2.md` 36
- 515: sostiene «operador Scion posterior solo para ramal E». PASS
- 543: solo contiene «…es del solicitante; operador y permisos»; la frase continúa en 544 («Scion se designan al abordar E»). Sostiene la regla, pero la cita de una sola línea es parcial. PASS con reserva
- `preflight-input-v2.md` 36: «Operador/permisos Scion se designan al abordar ramal y no bloquean L/M». PASS
- En conjunto, T-P01 queda respaldada; la cita «543» debería abarcar 543-544.

## No verificado
- No abrí `dag.yaml` 161-167, 225-233, 693-695, 945-946, 1188-1196, 2804-2830, ni `preflight-input-v2.md` 107-110/124-126/127-128/131-133.
- No verifiqué historial git (35543965, cc8d83da, HEAD 7b045a6f) ni las versiones previas que citan las adendas.
- No ejecuté nada ni toqué archivos.

RESULTADO: PASS
