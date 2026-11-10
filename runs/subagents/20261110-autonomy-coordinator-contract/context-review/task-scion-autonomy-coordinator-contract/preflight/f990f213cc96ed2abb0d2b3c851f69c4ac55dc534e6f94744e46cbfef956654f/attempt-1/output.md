## REFORMULACION
Propósito: eliminar contradicciones entre rol fuente y modos Scion para que el coordinador progrese trabajo autorizado sin intervención. Resultado: contrato fuente coherente en el repo deskops (RoleDoc, `deskops/runtime/scion.py`, CLI runtime, tests, docs, CHANGELOG) que recupera contexto configurado, selecciona una hoja ready/reviewed sin dueño y despacha ejecutor y tester independiente, conciliando closeout. Repo: deskops, raíz que contiene `deskops/` y `desk/`. Límites: sin motor de ciclo de vida nuevo, sin decisiones automáticas de política, sin pi-subagents ni tareas CC ajenas; cambios de estado/historial no alteran identidad; sin secretos en contexto; se preserva el comportamiento sin `--context-file`.

## AMBIGUEDADES
1. "requires the declared setup runtime task" — no nombra cuál; obligaría a inventar el identificador de esa tarea de setup (¿`task-scion-autonomy-review-status`?).
2. "obtained using existing sldb.store.hashing.hash_fields_with_map(TaskDoc, markdown)" — no define qué `markdown` (crudo o canónico) ni el mapa; obligaría a inventar la canonicalización.
3. "generated Scion modes/prompts" — no indica archivo ni plantilla de modos en `files`; obligaría a inventar dónde se generan.
4. "auto-detect tester RoleDoc" — se acota después a nombre/id terminado en `-tester`, pero no el criterio si coincide con supervisor/coordinator; obligaría a inventar prioridad.
5. "affected CLI help/output goldens" — no fija golden concreto salvo la ruta `template.txt`; obligaría a inventar expectativas.

## DRY-RUN
Un ejecutor futuro leería RoleDoc, atom, `scion.py`, CLI registry/runtime, tests, manual y golden. Cambios previstos: `--context-file` con validación de cinco claves; variables de entorno y `PYTHONPATH`; modo `tester` y autodetección; nombres/labels deterministas; instrucciones de reintentos y ejemplos CLI; actualizar goldens, docs y CHANGELOG. Dependencia declarada: `task-scion-autonomy-review-status` y la tarea runtime de setup. Validaciones futuras: `pytest tests/test_scion_runtime.py`, goldens de help y experimento live coordinador→ejecutor→tester→closeout. Sin ejecutar.

## FUTURO
La tarea runtime de setup aporta hooks/bootstrap e integración unattended; el owner resuelve conflictos de propiedad y credenciales; la aceptación live y el cierre los decide quien valide la evidencia. Una revisión aceptada no se repite con input sin cambios.
