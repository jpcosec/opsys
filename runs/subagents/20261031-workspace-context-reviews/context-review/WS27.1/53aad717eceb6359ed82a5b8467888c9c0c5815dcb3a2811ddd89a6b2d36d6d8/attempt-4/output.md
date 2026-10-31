REFORMULACION
Propósito: mostrar junto a la TaskDoc un diff Git read-only acotado a repo y tarea, más historial. Resultado: vista en `frontends/mindmap/views/workspace/diff/` con rutas de lectura del contrato WS11 y tests. Repo dueño: `graph_ui`. Límites: no ejecutar ni revertir; no mostrar hallazgos de integridad del store (WS29); la asociación a intento llega en WS35. Depende de WS13, WS12 y G_UI_READ.

AMBIGUEDADES
1. «historial read-only junto a la TaskDoc»: el alcance promete historial, pero la aceptación solo exige «Diff real acotado al repo y tarea»; no define qué historial ni cómo comprobarlo. Obligaría a inventar alcance y prueba del historial.
2. «Base: commits de TaskDoc.references; sin ellos, working tree contra HEAD limitado a TaskDoc.files»: no se nombra quién produce ni con qué contrato se resuelven `TaskDoc.references`/`TaskDoc.files`. WS12 registra capabilities Git, no el modelo TaskDoc. Obligaría a inventar la fuente y el fallback.
3. «Diff real acotado al repo y tarea»: no se define qué repo cuando `TaskDoc.files` puede referenciar varios; `output_scope` solo declara `graph_ui`. Obligaría a inventar la selección de repos.

DRY-RUN
Lecturas: dag.yaml (WS27.1, WS27, WS13, WS12, gates), guía, brief, alcance, decisiones y cobertura. Cambios previstos: solo `frontends/mindmap/views/workspace/diff/` y `tests/` de `graph_ui`. Dependencias: WS13 (agregado), WS12 (contrato de operaciones), G_UI_READ pendiente, resuelto por WS11. Validaciones futuras: comprobar G_UI_READ y la capability Git de WS12; diff real acotado; ausencia de ejecución/reversión; no mostrar integridad de WS29. Nada ejecutado.

FUTURO
WS11 produce/acepta G_UI_READ; WS12 fija la capability Git; WS35 añade la asociación a intento; WS29 aporta integridad; WS27.2 cubre evidencia. La promoción sigue no autorizada y el TaskDoc fijará archivos y pruebas. Un humano designa responsables y acepta deltas.
