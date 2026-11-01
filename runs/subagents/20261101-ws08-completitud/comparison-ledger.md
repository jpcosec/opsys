# Ledger de comparación, tanda sobre 023a05e3

Fecha: 2026-11-01. Rol: Supervisor. Actor: Claude Opus 5.5, pane `w3Y:p1`. Revisores: `pi`, deepseek-flash, thinking low, por `context_review.py`, instrucción `v2-ejecucion-hipotetica`. Vigente. Sustituye como evidencia a la renovación de WS08/WS10 y a la tanda sobre `b2720ae2`, que quedan como historia; tampoco se tocó WS10 ni `manual.md`.

Fuente aprobada de forma focal por root, por bytes: `root-focal-approval.md`. Esa aprobación no cubre estos outputs ni el cierre de fase.

## Qué se corrió

- `run --stale --jobs 6`: 73 `ok`, `review-run.log`. `cobertura.md` entra en los 73 bundles.
- Reintentos con `--new-attempt --reason`: WS23, WS29, WS42, `review-run-retries.log`.
- Vigentes: 70 `attempt-1` y 3 `attempt-2`, los 73 con recibo completo, sin fallo técnico, manifest v2 e `input_sha256` igual al bundle. Lista: `final-attempts.json`.

## Qué leí exactamente

`output.md` completo de los 73 y de los tres reintentos, cada uno junto a title, scope, acceptance, depends_on, requires, output_scope y children del nodo, en esta pasada. No leí bundles completos, `reconciliation` salvo WS29, `promotion`, ni TaskDocs generados. No hubo agente preparatorio.

Por programa: cuatro secciones en cada output, una clase por ambigüedad numerada, recibos y hashes. El script solo cuenta: las clases son juicio mío.

## Regla de rechazo

Intento nuevo si el output afirma algo contrario al contrato sobre arista, gate, productor, actor u output_scope. Sin cota de intentos: ninguna cantidad autoriza aceptar una contradicción material, según la corrección root. Una paráfrasis equivalente se acepta leída en contexto, con motivo en su disposición.

| Nodo | Defecto del attempt-1 |
|---|---|
| WS23 | Preveía una ruta de lectura fuera de output_scope |
| WS29 | Atribuía a WS06 promover el ticket Changes |
| WS42 | Decía que WS45 fija la precondición; la fija WS12 |

## Resultado

| Dato | Valor |
|---|---|
| Comparadas | 73 |
| Aceptadas como comprensión | 73 |
| Ambigüedades en intentos vigentes | 47 |
| `detalle de promoción` | 28 |
| `no es ambigüedad` | 7 |
| `futuro asignado` | 12 |
| Ambigüedades reales | 0 |

## Límites

- **WS12** volvió a señalar que su aceptación no enumera la definición de «modo manual exclusivo» y que la sección de timeout se difiere. Queda en T-P03.1, la decisión root y `promotion-notes.md`, sin cambio de contrato. Su TaskDoc debe citarlo.
- **WS13.1** señaló tensión entre aceptación incondicional y scope condicionado sobre foco en Code. La clasifico `futuro asignado` a WS11; es la más discutible de esta tanda.
- **WS09** señaló que «futura implementación» no identifica nodo: su TaskDoc debe resolverlo como WS08.
- **WS08** señaló el universo de «listas completas»; lo fijó la decisión root, no el contrato del nodo.
- Las clases son juicio del Supervisor.

## Para la promoción

Vigente la lista de `runs/subagents/20261031-ajuste-canonico-ws06/promotion-notes.md`. Añadir: WS09 productor por tipo; WS13.1 foco en Code; WS27.1 canal Git; WS39 documento sin Schema.
