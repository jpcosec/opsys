**Reformulación**

- **Propósito:** revisar si el encargo permite cerrar un plan documental coherente con decisiones humanas ya registradas, sin implementar producto.
- **Resultado esperado:** plan reconciliado en `desk/drawer/plans/workspace-documental/`, `cierre.md`, evidencia de reviews baratos vigentes y validación independiente documental.
- **Repo/alcance:** `deskops`; solo plans/tasks de workspace-documental y `runs/subagents/20261031-finalizar-plan-workspace/`. Uso permitido del runner existente con evidencia nueva append-only. Prohibido tocar código de producto, repos hermanos, rituales/skills/Board y cambios dirty ajenos.
- **Límites:** no commit, no cierre, no Board por Executor; no autorización de producto; no suite global larga; no sustituir gates humanos ni revisiones por concilio experto.

**Ambigüedades del encargo**

1. “P01…P08 se actualizan según alcance literal confirmado” no enumera ediciones mínimas ni criterio de suficiencia.
2. `G_CLOSEOUT`: se pide “productor/artefacto verificable” si falta prueba, pero no se define el artefacto aceptable ni quién lo produce.
3. “Reviews vigentes” no fija matriz exacta de invalidación por cambio de inputs/gates.
4. “Tester independiente” no indica disponibilidad, perfil ni evidencia esperada.
5. “Fuente editable espera G_SOURCE real” menciona el gate, pero no su condición verificable ni productor.
6. “Candidatas aún no TaskDoc” no define formato o ubicación esperada.
7. “Plan legible sin chat” carece de criterio comprobable.
8. “Revisar todos nuevos” no aclara si incluye nodos hijos, aristas y cobertura derivada.

**Dry-run por roles, sin ejecutar**

- **Supervisor/coordinador:** leería TaskDoc, pills, ritual y `owner-decisions.json`; congelaría fuentes; lanzaría preflight TaskDoc-only y cold-bundle por nodo afectado en procesos nuevos; compararía reformulación, ambigüedades y dry-run con la intención; corregiría textos; re-revisaría solo afectados; regeneraría desde `dag.yaml`; verificaría `--check` y `status`; entregaría a Tester independiente. No commitearía ni cerraría.
- **Executor documental:** leería fuentes explícitas; actualizaría P01–P08, gates, deltas y `cierre.md`; mantendría ramales opcionales desacoplados; registraría productor/condición/evidencia por gate; ejecutaría solo checks locales documentales; dejaría handoff con hallazgos y limitaciones. No tocaría producto ni Board.
- **Revisor barato:** restituiría propósito, listaría ambigüedades y dry-run; no leería fuentes no suministradas ni ejecutaría comandos.
- **Tester independiente:** comprobaría hashes, aislamiento, cobertura y dry-runs; validaría referencias y trazabilidad; haría validación focalizada de `G_CLOSEOUT` si se propone satisfecho; no exigiría suite global.
- **Humano:** confirmaría decisiones ya dadas y aceptación de deltas; no se le atribuirían firmas técnicas ni autorización de implementación.

**Delegado vs. lagunas**

- **Delegado rutinario:** organizar evidencia, hashes, regeneración, lanzamiento de reviews nuevos, comparación de outputs y redacción de `cierre.md`.
- **Tarea futura asignada:** implementación de producto, designación de operador/permisos Scion y activación real de fuente editable quedan fuera.
- **Lagunas que deben resolverse en el texto:** criterio de suficiencia de P01–P08, artefacto/productor de `G_CLOSEOUT`, matriz de invalidación y disponibilidad del Tester independiente.
