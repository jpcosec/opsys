**Reformulación de intención**
Cerrar el plan documental `workspace-documental` coherente con las tres respuestas humanas registradas (P01–P09), los deltas reales de `graph_ui`/`sldb`/`spec2viz`, gates con productor/condición/evidencia/scope, ramales opcionales desacoplados y reviews baratos vigentes. Entregable documental; no producto.

**Resultado esperado**
`dag.yaml` regenerado, `decisiones.md` trazada, `cierre.md` authored, candidatas `status=candidate` y `execution_authorized=false`, evidencia de reviews nuevos, G_CLOSEOUT con WS45 si falta prueba real, `context_review.py status` sin stale.

**Límites**
Solo `plans/` y `tasks/workspace-documental/` y el run indicado; no commit, Board, TaskDoc, producto, rituales ajenos ni cambios dirty. No suite global ni formato editorial exacto. No atribuir firma humana no dada.

**Ambigüedades reales que podrían forzar invención**
1. Los commits citados no se mapean explícitamente a WS/nodos; el Executor debe decidir la correspondencia. Resoluble con auditoría read-only, pero conviene tabla de trazabilidad.
2. "editing y Changes siguen drafts con hashes actuales": no se especifica qué hashes ni de qué archivos; riesgo de inventar estado.
3. WS45 aparece como condicional ("si todavía falta prueba"), pero no se fija el criterio objetivo de suficiencia ni quién lo declara.
4. "P07/P09 defaults técnicos revisables": no se indica artefacto donde conste que no son decisión humana.
5. "Matriz invalidación exactamente la que implementa `context_review.py`": falta versión/hash del script; el revisor no puede verificarlo sin leerlo.
6. "Primera capa preparable" no está operacionalizada (qué significa "dependencias probadas").
7. `cierre.md` pide contenido amplio sin plantilla ni longitud; puede interpretarse de forma divergente.

Ninguna exige cambiar el encargo; sí requieren que el Executor documente su criterio.

**Dry-run por roles, sin ejecutar**
- **Executor:** leerá TaskDoc, pills 001/005/007, ritual, `owner-decisions.json`, fuentes listadas, commits y `tests/test_closeout_declared_evidence.py`/`test_lifecycle_end_to_end.py`; corregirá fuentes primero; regenerará con `build_plan.py --check`; validará con `validate_plan.py --check` y `context_review.py status`; lanzará solo reviews stale con Pi deepseek-flash low, proceso nuevo, stdin DEVNULL, sin contexto/herramientas; guardará reformulación/ambigüedades/dry-run. No ejecutará WS20 ni suite global.
- **Supervisor:** comparará outputs con intención, dispondrá hallazgos con cita, congelará plan, lanzará Tester independiente y concilio final.
- **Tester:** PASS/FAIL con muestras de todos los reviews nuevos y limitaciones; pytest focalizado de G_CLOSEOUT si se propone `satisfied`.
- **Dependencias:** cambios en guide/brief/alcance/decisiones invalidan todos; cada nodo nuevo requiere review propio.

**Validaciones esperadas:** cero stale, hashes/aislamiento correctos, decisiones trazadas, sin gate humano falso ni autorización de producto, referencias actuales.

No he auditado las fuentes; su lectura corresponde al Executor.
