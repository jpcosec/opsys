## Separación de fuentes

- **LECTURA PROPIA:** leí `patch-8-dag.diff`, `dag.yaml` (nodo WS47 completo), `operaciones.md` §6.7, `task-ws47.md`, `review-source-2.md` y `review-source-3.md`. No ejecuté nada.
- **DATO DEL SUPERVISOR (no verificado por mí):** `tester-i-facts.log` → HEAD `75737add`, sha256 `dag.yaml` `d7089964…c693ece5`.
- `sha256 dag.yaml` del fact log no se corresponde con el estado del archivo que leo (el diff aplica a `c93c9b3f..3adac8c1`); lo trato como dato recibido, no comprobado.

## Verificación

| Objeto | Evidencia real archivo:línea | Veredicto |
|---|---|---|
| 1) Cambia una sola frase | `patch-8-dag.diff:7` un solo hunk; sustitución contigua `sin inventar otro criterio;` → `que no se rebaja … inventario lo justifica;` dentro de la misma oración. Aplicado en `dag.yaml:3047` | PASS |
| 2) Resuelve la contradicción «reutiliza antes de crear otro» vs aceptación | `dag.yaml:3040-3041` mantiene «reutiliza ese criterio antes de crear otro»; `dag.yaml:3047` admite piso que «solo se amplía si el inventario lo justifica»; `operaciones.md:450` conserva «**No se inventa otro criterio.**» | PASS |
| 3a) No contradice punto 7 de review-source-2 | `review-source-2.md:21`; requisitos intactos: `dag.yaml:3046-3054` (archivo previo+efecto, update seguro se aplica, documento limpio, 409, sin merge/ruido) y `operaciones.md:452` (propiedades 1-3) | PASS |
| 3b) No contradice decisión 5 de review-source-3 | `review-source-3.md:17`; `dag.yaml:3048-3054` conserva declaración de pérdida/no detectado/deshabilitado, residuo que no aprueba pérdida y «sin merge … sin prometer editar todo»; `operaciones.md:450` no afirma exhaustividad | PASS |
| 4) La ficha coincide | `task-ws47.md:31` reproduce literal la misma frase que `dag.yaml:3047` | PASS |

Nota: la frase eliminada «sin inventar otro criterio» sigue vigente en el contrato (`operaciones.md:450`), por lo que no se pierde esa restricción.

RESULTADO: PASS
