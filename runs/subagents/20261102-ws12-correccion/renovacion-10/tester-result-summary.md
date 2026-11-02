## DATO DEL SUPERVISOR

- HEAD deskops `2fcc22da`; sha256 `dag.yaml` `a8d39a19…b2191b5e` (`tester-h-facts.log:1-2`).

## LECTURA PROPIA

| Objeto | Evidencia real | Veredicto |
|---|---|---|
| Alcance: solo una frase | `patch-7-dag.diff:1-11`: un único hunk sobre `dag.yaml`; sustituye una sola frase de `acceptance` (líneas 8-9 → 10-11). Sin otros archivos | PASS |
| Derivados incluidos/regenerados | El diff no incluye derivados; `task-ws47.md:31` conserva el texto anterior («como mínimo… leído en fuente, sin inventar otro») con los mismos antecedentes rotos | FAIL |
| Coherencia interna del nodo en DAG | `dag.yaml:3047`: «leídas» concuerda con «las comprobaciones» y «otro criterio» tiene núcleo explícito; ya no queda «leído»/«otro» sin antecedente | PASS |
| ¿Contradice §6.7? | `operaciones.md:450`: criterio = guarda de `deskops edit` leída en fuente, «No se inventa otro criterio»; el nuevo texto mantiene archivo previo + efecto de reescribir y reutiliza `refuse_*` «donde apliquen» | PASS |
| ¿Contradice punto 7 de review-source-2? | `review-source-2.md:21`: exige archivo previo y efecto de reescribir, no solo render; `dag.yaml:3047` lo conserva | PASS |
| ¿Contradice decisión 5 de review-source-3? | `review-source-3.md:17`: no afirmar exhaustividad ni residuo como aprobación; `dag.yaml:3047` usa «piso de detección» y conserva la declaración de pérdidas/no detectados/deshabilitados en `dag.yaml:3047-3049` | PASS |
| WS48 conservado | `dag.yaml:3084-3085` y `task-ws48.md:27` intactos respecto de la ronda anterior | PASS |
| Resto de WS47 conservado | `dag.yaml:3049-3053`: update seguro se aplica, expected obsoleto 409, «Sin merge ni restauración» | PASS |

Conclusión: el arreglo gramatical del DAG es correcto, pero el derivado `task-ws47.md:31` no fue regenerado y mantiene exactamente el defecto anterior, por lo que DAG y derivado divergen.

RESULTADO: FAIL
