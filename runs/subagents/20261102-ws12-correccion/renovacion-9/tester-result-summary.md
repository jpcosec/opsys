## DATO DEL SUPERVISOR

De `runs/subagents/20261102-ws12-correccion/tester-g-facts.log`:
- HEAD deskops: `d5bc7d96`
- sha256 `operaciones.md`: `754546d6…ce9f39`
- sha256 `dag.yaml`: `fd09f584…b64cf9`

## LECTURA PROPIA

| Objeto | Evidencia real | Veredicto |
|---|---|---|
| Alcance del diff | `patch-6-dag.diff:1-19`: solo 2 hunks sobre `dag.yaml`; reemplazo en WS47 y en WS48, sin otros archivos | PASS |
| WS48: quién fija formato/ubicación/vigencia | `dag.yaml:3085` («su formato, ubicación y vigencia los fija este nodo en su TaskDoc, no WS12»); `operaciones.md:375` (§5.8: formato y ubicación los fija WS48) y `operaciones.md:387` (§5.9: producto de WS48 incluye formato y punto de carga) | PASS |
| «Como mínimo … piso de detección» vs §6.7 | `dag.yaml:3047`; `operaciones.md:450` («No se inventa otro criterio»; las tres comprobaciones no son exhaustivas) | PASS |
| vs punto 7 de `review-source-2.md` | `review-source-2.md:21`; `dag.yaml:3047` mantiene archivo previo y efecto de reescribir | PASS |
| vs decisión 5 de `review-source-3.md` | `review-source-3.md:17`; `dag.yaml:3047` usa «como mínimo», no afirma exhaustividad | PASS |
| ¿Promete merge o editar todo? | `dag.yaml:3054` («Sin merge ni restauración, y sin prometer editar todo documento con ruido»); `operaciones.md:452` | PASS |
| Coherencia gramatical de WS47 | `dag.yaml:3047`: «…y de `refuse_structural_noise` y `refuse_undeclared_frontmatter` **leído** en fuente, **sin inventar otro**». Al eliminar «criterio», «leído» queda sin antecedente singular concordante y «otro» queda sin núcleo explícito | FAIL |
| `context_review` / dependencias | Hunks en `dag.yaml:3044-3047` y `3082-3085`; WS47 `context_review` en `3063`, WS48 en `3109`, `depends_on` en `3024-3025` y `3072-3073`, fuera de los hunks | PASS |

Nota: los derivados `task-ws47.md:31` y `task-ws48.md:27` ya contienen el texto nuevo, pero no forman parte de `patch-6-dag.diff`.

RESULTADO: FAIL
