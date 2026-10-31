**Reformulación**

- **Propósito:** finalizar un plan documental de workspace, no implementar ni auditar producto. Debe quedar coherente con decisiones humanas registradas, estado real del repo, deltas, gates y reviews baratos vigentes.
- **Resultado:** paquete final legible sin chat —DAG, brief, alcance, decisiones, reconciliación, cobertura, validación humana, guía de context-review, borradores y `cierre.md`— con `execution_authorized=false`, pendientes con productor/evidencia y candidatas no convertidas aún en TaskDoc.
- **Repo/límites:** trabajar en `/home/jp/proyectos/SLDB_1/deskops`, solo `desk/drawer/plans/workspace-documental/`, `desk/drawer/tasks/workspace-documental/` y evidencia en `runs/subagents/20261031-finalizar-plan-workspace/`. Lectura externa permitida; no modificar producto, rituales/skills/Board de repos hermanos, cambios dirty ajenos ni recrear tasks borradas. Executor no commitea, no cierra ni cambia Board. No debilitar validación ni afirmar producto/gates disponibles.

**Ambigüedades del encargo**

- “Tres respuestas humanas exactas”: no están transcritas literalmente ni se fija formato actor/fecha/origen.
- P01–P09 no se listan; falta matriz decisión→nodo y criterio de “alcance literal confirmado”.
- Deltas graph_ui/sldb/spec2viz, WS13…WS44 y “workspace base real” requieren mapa de correspondencia no incluido.
- G_CLOSEOUT: “prueba de autoridad/identidad requerida” no define productor/artefacto aceptable si falta.
- `source_mode=editable`: “guardas reales” no enumeradas.
- “canal seguro”, “UI read-only/handoff”, “coordinador escritor”, “Taller”, “primera capa preparable” y “aceptación receptora/whitelist por delta” no tienen criterio verificable explícito.
- “Reviews afectados”: no se fija umbral de cambio que invalida.
- “Concilio final separado” y “Tester independiente”: no se define quién, insumo y veredicto.
- “Regenerar desde dag.yaml”: no se aclara si `cierre.md` se genera o se redacta aparte.

**Dry-run por roles, sin ejecutar**

- **Revisor barato/preflight:** solo lee este texto; entrega reformulación, ambigüedades y plan de verificación. No abre fuentes ni lanza procesos.
- **Supervisor:** ordena TaskDoc, fija `owner-decisions`, decide qué ambigüedad se resuelve por decisión y cuál queda como pendiente; administra Board/cierre; al final convoca concilio y tester.
- **Executor:** lee TaskDoc, pills, ritual, fuentes y estado git; mapea decisiones→P/WS/deltas; corrige fuentes y `cierre.md`; ejecuta build/validate/status; congela fuentes; lanza context_review solo afectados con proceso nuevo y flags indicados; compara salidas, dispone hallazgos, corrige y re-revisa; entrega handoff sin commit/Board.
- **Tester independiente:** verifica hashes, integridad, aislamiento, cobertura, dry-runs, refs y decisiones; validación focalizada de G_CLOSEOUT; no suite global salvo justificación; reporta sin arreglar.
- **Revisor de outputs:** coteja intención vs salida, cita evidencia y declara que “APTO” no basta.

**Distinción**

- **Tareas futuras asignadas:** actualizar P01–P06/P08; reconciliar WS/deltas; redactar `cierre.md`; regenerar; revisar afectados; concilio/tester; validación G_CLOSEOUT.
- **Rutinarios delegados:** leer git/commits, calcular hashes, usar flags de proceso, recibos append-only, pytest focalizado.
- **Lagunas:** mapa P/WS/delta, texto exacto de respuestas, guardas de `source_mode`, criterio de autoridad G_CLOSEOUT, roles de concilio/tester y definiciones de Taller/canal seguro/primera capa.
