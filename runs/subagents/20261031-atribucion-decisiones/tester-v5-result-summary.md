## Revisión v5

| Objeto | Evidencia real | Veredicto |
|---|---|---|
| WS01 disposición vigente | `...WS01/8746b4.../disposition.md`: sin mención de aprobación; justifica con `covered_work` | PASS |
| WS02/WS03/WS04 | Citan `runs/subagents/20261031-ws02-04-checkpoint/approval.md`; ese archivo dice «checkpoint WS02–WS04 aprobado como inventario documental» y «corrección WS03/WS04 aprobada documentalmente»; aclara que no es validación de runtime. Sostiene lo citado | PASS |
| WS06 | No invoca aprobación root: «cerrado en `ff28c68c`; no localicé un registro de aprobación root propio»; `tester-v5-facts.log` declara `ff28c68c desk: cierra WS06 correspondencia de alcance` | PASS |
| `owner-decisions.json` vs `decisiones.md` 0–2 | Preguntas y respuestas coinciden literalmente en los tres ítems (ítems 0, 1, 2), incluido `tool call call_387acc8d34de4f35bc4bafab9263bd58` | PASS |
| WS30 depende de WS26 | `dag.yaml:2056-2064`: `depends_on` de WS30 incluye `WS26` | PASS |
| Frase «sus aristas WS12/WS22/WS30» | WS12 y WS22 son `depends_on` de WS26 (`dag.yaml:1732-1734`); WS30 es dependiente (`dag.yaml:2063`), así que la arista existe. La frase es sostenible como aristas incidentes; «saliente» en el ledger es impreciso en dirección | PASS (imprecisión menor) |
| Adenda: WS02–WS04 citan `approval.md` | Confirmado en las tres disposiciones | PASS |
| Adenda: WS06 cita `ff28c68c` y declara no haber localizado aprobación root | Confirmado en la disposición WS06 | PASS |
| Adenda: cobertura da ruta completa de `owner-decisions.json` | `ws07-cobertura-efectiva.md:8` usa `runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json`, ruta legible | PASS |
| Adenda: «existe y está versionado» | `tester-v5-facts.log`: `git ls-files` lo lista versionado | PASS |
| Cobertura, líneas 1-22 iguales a `7b045a6f` | `decisiones-antes-7b045a6f.md` líneas 1-22 idénticas byte a byte | PASS |
| Cobertura, fila P07/P09: «Actor técnico registrado, **distinto de la autoría inicial**» | `decisiones.md` dice «cuya autoría inicial sigue sin localizar»; no hay fuente que acredite esa distinción. Afirma más de lo que la fuente sostiene | FAIL |
| Ledger: «dag.yaml solo cambia en evidencia» | `dag-diff.txt`: todos los hunks son `evidence`/`input_sha256` | PASS |
| Ledger: alcanzabilidad WS12→WS09, WS30→WS08 | WS12 `depends_on` WS11, WS08 (`dag.yaml:727-729`); WS11 ← WS09 (`dag.yaml:685-687`); WS30 ← WS17 ← WS11 ← WS08 | PASS |

No pude verificar:
- Afirmaciones sobre textos anteriores (que cuatro disposiciones decían «aprobado por root»; que la cobertura previa no daba la ruta): solo existe la versión vigente.
- `git diff 47b9e38b b2720ae2 -- dag.yaml` vacío: solo declarado en `tester-v5-facts.log`.
- Historial real de `decisiones.md` en `7b045a6f` y `35543965`.
- Los 73 recibos y el estado de la suite.

RESULTADO: FAIL
