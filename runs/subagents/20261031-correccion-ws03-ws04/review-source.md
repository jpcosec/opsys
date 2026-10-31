# Hallazgos de la revisión independiente, texto recibido

Fuente: mensaje de Codex `w3Y:p2` en el pane Claude `w3Y:p1`, 2026-10-31, durante la revisión del checkpoint WS02–WS04.

1. WS03 infraestructura.md §2.1 fila expected/409 (~línea49) promete 'payload actual extraído del archivo'. Puede ser runtime cache vieja: ../sldb/src/sldb/cli/serve/http_server.py:22–26 abre store una vez; save_routes.py:38–40 llama load_runtime_documents sin new_operation; runtime_cache.py:37–42 reusa hits; runtime_cache_signature.py:39–43,56–66,79–86 reutiliza stats/leaves hasta new_operation. Una edición externa que no altere índices puede preceder /save y no observarse en expected; no es solo carrera después del precheck. Deducción estática, no runtime reproducido. Corregir a payload obtenido por carga runtime sujeto a cache; extender límite de frescura en filas cache/expected y resumen. No anunciar cache fresca por defecto. Hay ausencia de CAS por hash, pero expected es comparación optimista por valor, no negar esa capability pública.

2. WS04 ui.md:165 atribuye al SPEC que +Add relation está fuera del plan. SPEC.md:79–82 se refiere a aristas semánticas sin archivo físico directo; editor connect-dialog modifica campos de referencia (connect-dialog.js:9–17). No equivalen. Corregir comparación: esa capability no cubierta/no comprobada como arista autónoma; no refutar SPEC por WS19.2 sin puente demostrado.

3. WS04 ui.md:42 trata task.txt active de runs/subagents/20261031-workspace-ui como incertidumbre de estado vigente. Es snapshot histórico; f16fcd1 elimina/cierra TaskDoc y HEAD134a665 actualiza Board. No hay contradicción actual. Corregir auditoría y handoff (preservando original ronda con nota de supersesión claramente fechada si es evidencia histórica).

4. WS03 ausencia de consultas guardadas: delimitar con capacidad vecina pron.ProjectionDoc persistida/evaluada: ../pron/src/pron/models/projection.py:14, world/projection_reader.py:22, world/lexicon.py:137. No equivale where guardado ni ViewDoc, pero grep saved_query no basta para negar toda selección persistida. Añadir distinción fuente verificada, sin inventar soporte.

Regla adicional: lo no probado queda como fuera de alcance/no ejecutado, con futuro test aislado explícito, sin ampliar la tarea a arreglar producto. No cambiar código SLDB/UI ni DAG. Testers de solo lectura son válidos para inventario estático si distinguen leído de no ejecutado.

## Hallazgo adicional, mensaje posterior de Codex `w3Y:p2`, 2026-10-31

Hallazgo ADICIONAL SUSTANTIVO de revisión propia root: el resumen global «ViewDoc solo modelo/sin evaluador» NO se sostiene en el ecosistema. En graph_ui TRACKED hay:
- frontends/mindmap/projection_views.py:107 evaluate_view: runtime_documents→selección _selected model/where(:52)→relation_edges relaciones/direction(:113), layout y notación resolve_documents. list_views/find_view :127+.
- frontends/mindmap/views_routes.py:1–7 y dispatch: GET /api/views, GET/POST /api/views/evaluate (ref guardada o payload), POST /api/views/save (guarda ViewDoc por sldb), save_view:58+.
- frontends/mindmap/serve.py:147–155 _api_views y dispatchGET:332/POST:382: conecta rutas, local mode; remote devuelve501.
- tests/test_projection_views.py sobre stores temporales reales; tests/e2e_review_workbench_views.py integra rutas. NO afirmo ejecutados.
- git ls-files confirma fuentes trackeadas; commits 0eb7dd7→b9ab83c→2a15356 (último 'Vistas (ViewDoc): ...resolve_documents...review-workbench la dibuja').

WS03 puede decir con precisión que no hay evaluador dentro de su universo sldb/pron/spec2viz, pero §6 no debe concluir que WS18 necesitará construirlo sin consultar consumidor. WS04 omitió por completo proyección/evaluación/guardado ViewDoc en su base reutilizable (rg ViewDoc/projection_views/views_routes en ui.md no da nada). Añadir esa base y enlazar WS18/WS24 donde corresponda; corregir handoff global y dictamen de ausencia: ya existe consumidor en graph_ui con límites local-only y pruebas existentes no ejecutadas. Mantener distinción modelo vs evaluador vs renderer y notación, sin anunciar aceptación del producto ampliado. No tocar código/repos hermanos. Incorporar a misma tarea de corrección del checkpoint antes WS06.
