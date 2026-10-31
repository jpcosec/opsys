REFORMULACION
Propósito: revisar WS21 como encargo de planificación, no como producto ni ejecución. Resultado esperado: un nodo que integra fuente/renderizado según `source_mode`, conserva buffer sucio, usa guardado autorizado y limita composición al origen dueño. Repo dueño: `graph_ui`; salidas en `frontends/mindmap/views/workspace/; tests/`. Límites: revisar solo WS21 sin ejecutar ni revisar contratos edge vecinos; con `pending` no se prepara ni promueve; la variante `editable` añade WS20 y G_SOURCE; `read_only` no exige G_SOURCE.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas previstas: nodo WS21, guía, `decisiones.md` (P04), gates G_UI_WRITE/G_WRITE_CONTRACT, contrato WS19 y variantes. Cambios previstos: ninguno; es revisión. Dependencias: WS19; gates G_UI_WRITE y G_WRITE_CONTRACT; en `editable`, WS20 y G_SOURCE. Validaciones futuras: que P04 haya elegido `source_mode`; en `editable`, edición/conflicto/roundtrip con G_SOURCE y G_WRITE_CONTRACT; en `read_only`, fuente legible no editable y campos editables; conservación de buffer y confirmación explícita al alternar; composición solo sobre documento dueño o declaración de solo lectura. WS30 verificará después el manual en el modo elegido.

FUTURO
El humano o WS07 resuelve P04 y fija `source_mode`; WS12 produce G_UI_WRITE, G_WRITE_CONTRACT y el contrato de operaciones; WS20 produce la API reversible y G_SOURCE cuando el modo sea editable; WS19.1/WS19.2 completan la edición de campos; WS30 valida manualmente y ajusta sus afirmaciones. Nada de esto se inventa en WS21.
