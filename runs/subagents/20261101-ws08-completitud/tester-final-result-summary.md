# Informe Tester final — WS08 completitud

## Tabla

| Objeto | Fuente | Evidencia | Veredicto |
|---|---|---|---|
| 10 nodos elegidos: WS07, WS08, WS10, WS12, WS13, WS22, WS23, WS29, WS42, WS45 | LECTURA PROPIA | dag.yaml:561, 602, 676, 792, 829, 1518, 1557, 2044, 2787, 2919 | PASS |
| `evidence` apunta al intento vigente de `final-attempts.json` (incl. attempt-2 en WS23/WS29/WS42) | LECTURA PROPIA | dag.yaml:1557, 2044, 2787 vs final-attempts.json:40,52,71 | PASS |
| `output.md` + `disposition.md` + `receipt.json` con `technical_failure: false` en los 10 | LECTURA PROPIA | p.ej. WS07/…/attempt-1/{output,disposition,receipt}.json; receipt.json:31 `technical_failure": false` en WS12, WS22, WS23, WS29, WS42, WS45 | PASS |
| `input_sha256` de la ruta = hash de carpeta | LECTURA PROPIA | receipt.json:29 y dag.yaml:562, 791, 2044, 2788 | PASS |
| `manifest.json` declara v2 | LECTURA PROPIA (parcial) | WS07 manifest.json:107 `v2-ejecucion-hipotetica` (leído entero); WS29/e57f…/attempt-2 y WS42/40bb…/attempt-2 vía grep | PASS con reserva (ver «no verificado») |
| Rechazo WS23: ruta de lectura fuera de `output_scope` | LECTURA PROPIA | attempt-1 output: «la ruta de lectura mínima»; dag.yaml:1530 `output_scope: …/procedure/; tests/`; attempt-2 sin esa frase | PASS (defecto real, desapareció) |
| Rechazo WS29: atribuía a WS06 promover el ticket Changes | LECTURA PROPIA | attempt-1 FUTURO: «WS06 promueve/ajusta el ticket Changes»; dag.yaml:517 «WS06 no firma ni registra recepción»; attempt-2: «el dueño del ticket Changes decide» | PASS |
| Rechazo WS42: «WS45 fija la precondición» | LECTURA PROPIA | attempt-1 FUTURO; gate G_PAYLOAD_PRECONDITION: evidencia «que fije el contrato WS12»; attempt-2: «WS12 produce whitelist/contrato» | PASS |
| Falsa aceptación en WS12, WS13.1, WS21, WS22, WS27.1, WS32.1, WS35, WS41, WS43, WS45 | LECTURA PROPIA | outputs+disposiciones+contrato de cada nodo | PASS con observaciones |
| Agregados WS13, WS15, WS19, WS25, WS26, WS27, WS32, WS33, WS34 | LECTURA PROPIA | dag.yaml:1019-1022, 1262-1265, 1620-1623, 1282, 1732-1736, 1856-1860, 2140-2144, 2280-2284, 2394-2398; 1813, 2236, 2358-2359, 2467-2470 | PASS |
| Productores de la decisión root en user-flows.md/cobertura.md | LECTURA PROPIA | user-flows.md:84, 129, 134, 158, 181, 218, 237; cobertura.md:7, 9, 10, 11, 13, 14 | PASS |
| WS29 no es gate ni prerrequisito | LECTURA PROPIA | user-flows.md:183 («no es gate humano»); cobertura.md:7 | PASS |
| WS22 fuera de Nodo en UF01 | LECTURA PROPIA | user-flows.md:22 (Operación, «base parcial WS22») vs user-flows.md:31 (Nodo sin WS22) | PASS |
| Conteos del ledger: 73, 70+3 intentos, 47 = 28+7+12 | LECTURA PROPIA / SUPERVISOR | final-attempts.json (73 entradas, 3 `attempt-2`); review-run.log:1-73 `ok`; review-run-retries.log (3) | PASS |
| Sin activación ni cambio de contrato/gate | LECTURA PROPIA | dag.yaml:10 `execution_authorized: false`; dag-diff.txt solo líneas `evidence`/`input_sha256` | PASS |
| `all reviews current`, build 0, 13 passed | DATO DEL SUPERVISOR (declarado en tester-final-facts.log y root-focal-approval.md) | tester-final-facts.log; root-focal-approval.md | No verificable por mí |

## Hallazgos

- **Integridad**: los 10 nodos seleccionados son coherentes; los tres reintentos son los únicos `attempt-2` vigentes y los únicos cambios de `evidence` respecto del estado previo (dag-diff.txt).
- **Menor (WS13.1)**: la tensión «seleccionar en Code actualiza el foco» vs «compartir foco solo donde WS11 lo defina» es real en el texto del contrato, no inventada; el ledger ya la señala como «la más discutible» y la clasifica `futuro asignado`.
- **Menor (WS41)**: el output propone «un humano debe corregir `depends_on`» si WS14/15 fueran prerrequisitos; no afirma la arista, pero roza cambio de contrato y no se escaló a root.
- **Menor (WS21)**: el FUTURO dice «WS12 produce `G_WRITE_CONTRACT`»; el gate se evalúa por IDs, WS12 produce el contrato. Impreciso, no material.
- **Menor (cobertura.md:10)**: la columna «Gate de aceptación» de UF06 añade «WS38 publicación»; WS38 no es gate. La instrucción root solo pedía incluir WS44.
- **Menor (ledger)**: `review-run-retries.log` ordena WS23, WS42, WS29; el ledger escribe WS23, WS29, WS42. Cosmético.
- Ninguna clase de los 10 nodos revisados oculta contradicción con arista, gate, productor, actor u `output_scope`; ningún dry-run contradice el contrato.

## No verificable

- `all reviews current`, `build --check`, `validate --check`, `13 passed`, hashes SHA de fuentes: solo DATO DEL SUPERVISOR.
- `manifest.json` v2 leído íntegro solo en WS07; en WS29 y WS42 por grep; en WS08, WS10, WS12, WS13, WS22, WS23, WS45 no lo abrí.
- Conteos por clase (28/7/12) por nodo: no sumé las 73 disposiciones; solo comprobé que 28+7+12=47 y que el total de intentos cuadra.

RESULTADO: PASS
