## Informe de verificación

| Objeto | Evidencia leída | Resultado |
|---|---|---|
| Cláusula WS12 condicionada | `dag.yaml:771-772`; `task-ws12.md:31` | PASS |
| Sin forma incondicional en proyecciones | `task-ws21.md:11-14` y `:49`; `dag.diagram.yaml:1300-1303` | PASS |
| WS21 base y variantes coherentes | `dag.yaml:1436-1471`; `task-ws21.md:44-56` | PASS |
| Timeout asumido por WS12 | `dag.yaml:779-783`; `task-ws12.md:31` | PASS |
| WS34.1 solo avanza con política verificada | `dag.yaml:2447-2448` | PASS |
| WS34.2 solo avanza con política verificada | `dag.yaml:2481-2484` | PASS |
| Disposición WS34.2 sin futuro no asumido | `WS34.2/.../disposition.md:9` | PASS |
| WS19.1 final describe campos, precondición, protegidos, buffer/conflicto y validación | `WS19.1/731a.../attempt-1/output.md` (DRY-RUN); `disposition.md:9` | PASS |
| Intento previo WS19.1 conservado y sin crédito | `WS19.1/c342b4d.../attempt-1/disposition.md:3,9`; disposición nueva | PASS |
| Receipt/argv WS19.1 | `WS19.1/731a.../attempt-1/receipt.json:1`; `manifest.json:4` | PASS |
| Receipt/argv WS37 y WS12 attempt-2 | `WS37/3c32.../attempt-2/receipt.json:18`; `WS12/bb6a.../attempt-2/receipt.json:18` | PASS con hallazgo |
| Ledger con 73 filas | `comparison-ledger.md:31-103` | PASS |
| Supersesión de la frase falsa y culpa | `comparison-ledger.md:5-11` | PASS |
| Disposiciones viejas no editadas | muestras `WS19.1/c342b4d...:3`, `WS37/.../attempt-1:9`, `WS34.1/442.../disposition.md:9` | PASS |
| Muestra de 12 disposiciones contra output | WS03, WS13.1, WS15.2, WS20, WS22, WS24, WS26.2, WS28, WS30, WS35, WS41, WS44 | PASS con hallazgos |
| 10+ outputs delivery no citados como defectuosos | mismos 12 nodos, secciones DRY-RUN | PASS |
| WS42 cubre validación de materializaciones | `dag.yaml:2762-2775`; `WS42/.../output.md` | PASS |
| WS12 cubre protoátomo | `dag.yaml:760-761`; `WS12/bb6a.../output.md` | PASS |
| Nota de corrección WS42 | `runs/subagents/20261031-ajuste-canonico-ws06/result-summary.md` (nota final) | PASS |
| promotion-notes marca resuelto timeout | `runs/subagents/20261031-ajuste-canonico-ws06/promotion-notes.md:15` | PASS |
| P04, validadores y código intactos | `tester-facts.log` (dato del Supervisor) | NO VERIFICADO |
| Hashes de las 73 filas | no puedo recomputarlos en solo lectura; spot-check WS19.1 coincide con `receipt.json` | NO VERIFICADO |

## Hallazgos

- **Metadatos de intentos fuera del runner:** los manifiestos de `WS12/.../attempt-2` y `WS37/.../attempt-2` registran `"attempt": 1` y apuntan su argv a `attempt-1/input.md` (`manifest.json:4` y `:307`/`:114`). El hash de input es idéntico y el `receipt.json` registra proceso fresco; no hay discrepancia de bytes, pero el metadato de intento es inconsistente con la fila del ledger.
- **WS22, disposición no sustentada:** afirma que «comunes» significa «no modificar el lector» y que WS13 abre cualquier documento (`WS22/.../disposition.md:9-11`), mientras el output deja abierto el conflicto entre aceptación y `output_scope` board/ y el renderer de pills/átomos. No puedo demostrar que sea falsa, pero oculta un hueco no cerrado por el contrato.
- **WS13.1, cita desplazada:** la disposición califica de «no es ambigüedad» la ruta de apertura sin ID y atribuye a la aceptación «rutas de lectura contrato WS11», que está en `output_scope`, no en aceptación (`WS13.1/.../disposition.md:9-10`). Hueco residual de selección inicial, no falsedad demostrable.
- **Cobertura de la comparación:** la muestra de 12 disposiciones y 12 outputs no reproduce una falsedad demostrable en las filas clave; la afirmación global de haber comparado los 73 nodos queda NO VERIFICADA.

RESULTADO: PASS
