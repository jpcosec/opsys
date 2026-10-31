REFORMULACION

Propósito: integrar en `graph_ui` las operaciones de conocimiento ya contratadas —split/merge de átomos y tipado de protoátomos— con confirmación de la persona usuaria en la UI, mostrando alcance y procedencia antes de ejecutar.

Resultado: operaciones invocables con persistencia, referencias y conflictos reales; materializaciones existentes solo inspeccionadas/validadas contra el modelo SLDB registrado en el store de la tarea, sin crear destinos; capabilities no soportadas declaradas no disponibles, bloqueando únicamente el escenario UF03 que las usa.

Repo: `graph_ui`. Ámbito: `frontends/mindmap/views/workspace/knowledge/`, endpoints limitados a la whitelist de WS12 y `tests/`.

Límites: no simular capabilities, no generar destinos arbitrarios, no exceder la whitelist. Gates: `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`. Validación final por WS30.

AMBIGUEDADES

ninguna.

La condición “cuando disponibles” queda resuelta por la aceptación: cada capability no soportada se declara no disponible y solo bloquea su escenario UF03. La ausencia de contrato la cubre la regla común de ejecución. Los detalles de pantalla, archivos y pruebas quedan para el TaskDoc de promoción.

DRY-RUN

Lecturas previstas: nodo WS42 y su `task_file`; contratos/operaciones.md producido por WS12; superficies de conocimiento y grafo de WS19/WS24; matriz UF03 de cobertura.md.

Cambios previstos: integrar en la vista knowledge las invocaciones de split/merge/tipado mediante el canal autorizado; añadir confirmación previa con alcance y procedencia; mostrar resultados, conflictos y materializaciones inválidas; declarar capabilities no disponibles; pruebas en `tests/`.

Dependencias: WS19 y WS24 aportan edición y vista de conocimiento/grafo; WS12 fija whitelist, canal y efectos. Gates pendientes: `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`.

Validaciones futuras: escenarios UF03 de dividir, reunir y tipar; persistencia, referencias y conflictos; inspección/validación de materializaciones existentes; verificación de que ninguna capability ausente se simula. Ejecución no autorizada en este nodo.

FUTURO

WS12 produce la whitelist y el contrato técnico. WS19 y WS24 entregan las superficies reutilizables. WS30 ejecuta la validación humana de UF03. Personas responsables resuelven los gates y autorizan la promoción. El TaskDoc fijará archivos exactos, pills, escenarios y textos de pantalla.
