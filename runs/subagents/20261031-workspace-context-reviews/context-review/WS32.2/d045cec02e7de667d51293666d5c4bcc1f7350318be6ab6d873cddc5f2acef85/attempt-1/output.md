## REFORMULACION
Propósito: hacer idempotentes manifiesto, RunDoc y cierre sobre el intento correcto. Resultado: una finalización repetida conserva identidad y evidencia sin duplicar. Repo: `deskops` (`runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`). Límites: nodo `implementation`; depende de WS05, WS12 y WS32.1, y de los gates G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT; promoción no autorizada; sin segundo pipeline; integración solo por delta o ticket existente tras WS06.

## AMBIGUEDADES
1. «acceptance: G_CLOSEOUT pasa» — G_CLOSEOUT figura a la vez en `requires` y en la aceptación, con `state: blocked` y `resolver: external`. Si debe estar satisfecho para ejecutar, no puede ser criterio de salida del nodo; si el nodo debe hacerlo pasar, contradice al resolver externo. Obliga a inventar si el ejecutor consume o produce evidencia de ese gate.
2. «Manifiesto, RunDoc y cierre consistentes e idempotentes» — «manifiesto» no aparece definido en brief.md, alcance.md, decisiones.md ni en el alcance de WS05. Obliga a inventar qué artefacto es, su contrato y su ubicación.
3. «sobre el intento correcto» y «sin duplicar» — no se define qué identifica el intento correcto para el cierre ni qué constituye duplicación de evidencia. WS32.1 solo exige identidades distintas entre intentos, no una regla de selección. Obliga a inventar la clave de identidad y el criterio de no duplicación.

## DRY-RUN
Lecturas previstas: nodo WS32.2, guía, brief, alcance, decisiones, reconciliación, contratos-vecinos WS05/WS12/WS32.1 y gates. Cambios previstos: solo los archivos de `output_scope`. Dependencias: WS32.1 aporta separación intento/dispatch; WS12, contrato de escritura; WS05, inventario; gates pendientes condicionan ejecución. Validaciones futuras: prueba de finalización repetida, conservación de identidad/evidencia, ausencia de duplicados y evidencia de gates. Sin ejecutar.

## FUTURO
WS07 designa operador Scion; WS44 produce G_SCION mediante probe; el resolver externo define la evidencia de G_CLOSEOUT; WS12 produce G_WRITE_CONTRACT; un humano autoriza promoción/preflight; WS32 cierra cuando cumplen sus hijos.
