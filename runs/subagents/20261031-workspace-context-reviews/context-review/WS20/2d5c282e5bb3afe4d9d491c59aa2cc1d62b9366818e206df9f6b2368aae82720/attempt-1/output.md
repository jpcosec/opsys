## REFORMULACION
**Propósito:** comprobar si SLDB ya puede guardar de forma reversible un documento raw-source o completar solo lo que falte.
**Resultado:** API pública y pruebas de roundtrip, conflicto, recuperación tras fallo y campos protegidos; si la capacidad existente cumple todo, bastan esas pruebas y no se duplica código.
**Repo dueño:** `sldb`, con alcance en `src/sldb/api/documents/`, `src/sldb/cli/serve/` y `tests/`.
**Límites:** no sobrescribir Markdown desde browser; no crear un segundo productor; la promoción sigue `not_authorized`; el nodo solo aplica con `source_mode=editable`.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas previstas:** fuentes suministradas; al ejecutar, contrato de WS12 y `desk/drawer/tasks/workspace-documental/task-ws20.md` para fijar archivos, escenarios y textos.
**Cambios previstos:** primero verificar capacidad en `sldb`; si existe y satisface la aceptación, añadir o confirmar pruebas; si es parcial, completar únicamente lo faltante y reprobar todo el contrato; si falta, implementar dentro de `output_scope` mediante la tarea receptora sldb.
**Dependencias:** WS12 como productor del contrato técnico; `G_WRITE_CONTRACT` por delta; `G_SLDB_WRITE` como recibo externo por delta; `source_mode=editable`.
**Validaciones futuras, sin ejecutar:** API pública; roundtrip guardar/extraer sin pérdida; conflicto con revisión; recuperación tras fallo; preservación de campos protegidos; repetición del contrato completo si la capacidad era parcial.

## FUTURO
WS12 produce y verifica `G_WRITE_CONTRACT` para el efecto concreto. El receptor P01 emite el acta externa de `G_SLDB_WRITE` en el repo sldb. La autorización de promoción corresponde al humano; sin ella no se ejecuta. WS20 produce `G_SOURCE`, cuya recepción habilita al consumidor WS21; la ausencia de otros deltas no bloquea este recibo.
