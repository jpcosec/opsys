| Objeto | Evidencia real (archivo:línea leído) | Resultado |
|---|---|---|
| P01–P09, todas las columnas | `decisiones-antes-7b045a6f.md:25-33` vs `decisiones.md:25-33`; precisiones en `decisiones.md:43-50` | PASS |
| Secciones fuera de tabla | `decisiones-antes-7b045a6f.md:5,19`; `decisiones.md:5,19,37-50` | PASS |
| P07/P09: actor, autoría inicial | `decisiones.md:31,33,39,49-50`; `attribution-map.md:68-74` | PASS |
| T-P03.1 contra `dag.yaml` 735 y 1327 | `dag.yaml:734-743,1327`; `decisiones.md:45` | PASS |
| Guía: secuencia entre hermanos sin arista | `context-review-guide.md:15`; `dag.yaml:2980,3024,3062,3100,3139,3177,3228,3261,3294` | PASS |
| Guía: requisito de producto / agregados | `context-review-guide.md:3,15`; scopes agregados leídos en `dag.yaml:2977-2983,3021-3027,3059-3065,3097-3102,3136-3142,3174-3180,3225-3230,3258-3263,3291-3297` | PASS |
| Guía: P01–P06/P08 y precisiones técnicas | `context-review-guide.md:17`; `decisiones.md:25-33,43-50` | PASS |
| Adendas contra archivos | `attribution-map.md:46-74`; `decisiones.md:25-50`; `dag.yaml:161-167,225-233,945-946,1984-1994,734-743,1327` | PASS |

**Hallazgos**
- P01 perdió «Operador Scion se designa después» en la fila; reaparece en T-P01 con fuente (`decisiones.md:43`).
- P03 perdió «canal público… lock solo UI no basta»; reaparece en T-P03 (`decisiones.md:44`).
- P04 perdió «revisión/recuperación/probados» de la fila; T-P04 conserva revisión y recuperación (`decisiones.md:46`). «probados» aplicado a campos no reaparece literal.
- P05 perdió «CLI/coordinador» y «refresco verificable»; T-P05 los recoge como «CLI/coordinador» y «refresco que verifica el resultado» (`decisiones.md:47`).
- P06 perdió «preparar/handoff hasta canal completo comprobado»; reaparece en T-P06 (`decisiones.md:48`).
- P03/P05/P06 cambiaron «pregunta y respuesta ítem 1» por «pregunta ítem 1». La respuesta literal sigue íntegra y el contenido citado está en la pregunta; no se perdió actor ni condición.
- P07/P09: «Executor por encargo TaskDoc v2» está en la fila actual y se distingue de la autoría inicial; se afirma que esta «sigue sin localizar» (`decisiones.md:31,33,39,49-50`).
- T-P03.1 no atribuye a humano ni al ítem 1, no crea API/gate/mecanismo y rechaza exclusividad por ausencia de señal (`decisiones.md:45`).
- La guía nueva evita serialización ficticia y separa núcleo humano de derivaciones técnicas (`context-review-guide.md:15,17`).
- Los scopes agregados condicionan la descripción a «orden/aristas»; no leí un agregado que exija transferencia entre hermanos sin arista.

**No verificable**
- La versión intermedia donde se borró el actor P07/P09: el archivo «antes» ya lo contiene (`decisiones-antes-7b045a6f.md:31,33`); la restitución solo consta por la adenda (`attribution-map.md:72`).
- El literal de la «tabla inicial línea 9» en el commit 35543965.
- Que todas las parejas de hermanos citadas en cada agregado carezcan o tengan arista; solo abrí los scopes agregados, no todas sus aristas.

RESULTADO: PASS
