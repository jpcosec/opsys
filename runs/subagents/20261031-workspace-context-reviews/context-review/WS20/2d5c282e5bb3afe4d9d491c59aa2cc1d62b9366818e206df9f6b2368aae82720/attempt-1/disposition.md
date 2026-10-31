# Executor comparison — WS20, final per-effect contract input

State: accepted_current

## Reformulación examinada

## REFORMULACION
**Propósito:** comprobar si SLDB ya puede guardar de forma reversible un documento raw-source o completar solo lo que falte.
**Resultado:** API pública y pruebas de roundtrip, conflicto, recuperación tras fallo y campos protegidos; si la capacidad existente cumple todo, bastan esas pruebas y no se duplica código.
**Repo dueño:** `sldb`, con alcance en `src/sldb/api/documents/`, `src/sldb/cli/serve/` y `tests/`.
**Límites:** no sobrescribir Markdown desde browser; no crear un segundo productor; la promoción sigue `not_authorized`; el nodo solo aplica con `source_mode=editable`.

##

## Hallazgos/disposición contra intención

Comparación aceptada por contenido completo: propósito/resultado/repo/límites coinciden con contrato; dry-run identifica fuentes, cambios futuros, dependencias/transferencias y pruebas específicas, sin ejecutar. Gates técnicos se verifican por efecto propio, sin sustituirlos por permiso/UI o receipt vecino. Respeta estados reales/no disponibles, decisiones registradas y autorización futura separada. Ninguna ambigüedad real pendiente; no se acepta por token APTO.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
