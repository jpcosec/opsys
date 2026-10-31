# Reconciliación — observaciones y pendientes

Observado al iniciar ronda 2: graph_ui Board enruta tres tareas draft: workspace multiproyección, Changes y edición contextual. Las rutas actuales están en external_references de dag.yaml con hash de observación. No equivalen a trabajo implementado ni autorizado a duplicar.

| Línea existente | Nodos de este plan | Tratamiento propuesto |
|---|---|---|
| Workspace /workspace/node, Document/Graph/Code/Context | WS13–16, WS22–24 | Reutilizar capacidades existentes del shell/grafo; el lector/grafo/código/contexto del ticket workspace draft sigue siendo implementación pendiente; explorer/tabs/historia/búsqueda son deltas explícitos, no fingir equivalencia de productos. |
| Edición contextual campos/relaciones | WS19/21 | Reutilizar APIs/editores; fuente Markdown y política de campos son contratos adicionales WS12/20. |
| Changes actual sobre hashes/relaciones | WS15/29 | Separar errores inline de lectura y extensión Changes; no convertirlo en Merkle CST Kimun. |
| Scion RunDoc/cierre | WS32/33 | Descomponer candidato existente; WS34–36 agregan acciones/UI que no están cubiertas por un visor. |
| Contrato Opsys–Kimun en drawer | Referencia, fuera de baseline | No ejecutar ni contar M1/M2/C2 como dependencias de este plan. |

WS06 propone matriz; WS11/12 obtienen aceptación del alcance definido por responsables identificados en P01. WS04 debe comprobar Board/archivos/alcance/commits de nuevo y registrar cualquier plan adicional aportado al repo. La memoria privada de un agente o planes en su home no son autoridad compartida. Si un revisor los cita, transcribir la decisión relevante y obtener confirmación antes de incorporarla.

G_UI_READ/G_UI_WRITE siguen pendientes: el responsable de graph_ui debe aceptar cómo se integra cada delta en sus tareas existentes. Hasta entonces no se despacha código de UI de este DAG ni se modifica su Board. Esta restricción permite pulir el plan sin interferir con la sesión activa en graph_ui.

El alcance receptor se registra por gate y lista scope_nodes en dag.yaml. WS11 obtiene el acuerdo de lectura (incluye fixtures y multidesk); WS12 obtiene acuerdo de mutación graph_ui y, solo para source_mode editable, el de sldb. El actor receptor se identifica en WS07; si no hay designación, gate pendiente.
