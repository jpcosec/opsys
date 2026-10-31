## REFORMULACION
Propósito: que la vista del workspace alterne fuente y render sobre un solo origen, con revisión y buffer sucio, guardando fuente por canal autorizado y haciendo que una composición escriba solo en el documento dueño. Resultado: nodo de implementación en graph_ui. Repo: `owner_repo: graph_ui`, `output_base: graph_ui:repository_root/`, `output_scope: frontends/mindmap/views/workspace/; tests/`. Límites: depende de WS19; gates G_UI_WRITE y G_WRITE_CONTRACT; ejecuta solo la variante que fije P04; `pending` bloquea; si WS12 no soporta composición, queda read-only y se declara; `promotion: not_authorized`; nunca duplicar ticket.

## AMBIGUEDADES
1. «pending bloquea preparación»: no define si el bloqueo abarca todo el nodo o solo preflight/promoción, ni qué parte read-only podría prepararse; el ejecutor inventaría el alcance del bloqueo. Además, «Cumplir la aceptación específica de la variante P04» carece de rama para `pending`.
2. «Alternar fuente/render con mismo origen, revisión y dirty buffer»: no fija qué ocurre al alternar con cambios sin guardar en modo editable (conservar, descartar, bloquear); solo read_only dice «Conservar buffer/foco». Se inventaría política y prueba.
3. Título «Integrar fuente y renderizado editables» contradice la variante read_only («Fuente explícitamente read-only»); no se sabe cómo nombrar/documentar la entrega en ese modo.

## DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, reconciliación, nodos WS19/WS20/WS30, gates y parameters. Cambios previstos (hipotéticos, sin ejecutar): vista en `frontends/mindmap/views/workspace/` y `tests/` de graph_ui. Dependencias: WS19; G_UI_WRITE y G_WRITE_CONTRACT (WS12); en editable, WS20 y G_SOURCE. Validaciones futuras: WS30 (manual humano), WS16 (lectura), aceptación de G_UI_WRITE.

## FUTURO
P04 la resuelve un humano/WS07 fijando `source_mode`; WS12 produce G_UI_WRITE y G_WRITE_CONTRACT y define si existe composición; WS20 produce G_SOURCE; WS06/WS12 confirman integración sin duplicado; WS30 valida el manual; la promoción sigue sin autorizar.
