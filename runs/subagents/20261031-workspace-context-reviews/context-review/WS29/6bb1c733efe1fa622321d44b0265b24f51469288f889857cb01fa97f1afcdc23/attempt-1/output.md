## REFORMULACION
Propósito: definir WS29 como delta de implementación en `graph_ui` que integra Changes y hace comprobable el impacto del store actual. Resultado: extensión sobre la tarea Changes existente (check/doctor/drift, relaciones comprobadas), con errores y alcance visibles, sin reparación automática ni supuestos CST/Kimun. Repo dueño: `graph_ui`; superficies: `frontends/mindmap/views/workspace/changes/`, rutas de integridad y `tests/`. Límites: depende de WS15 y WS24, exige G_UI_READ, no se ejecuta en paralelo ni duplica ticket, no bloquea lector/manual básico y su promoción no está autorizada.

## AMBIGUEDADES
1. «Mutaciones reales muestran soporte/alcance/errores». «Soporte» y «alcance» no se definen: el ejecutor debería inventar qué evidencia visual/datos demuestra cada uno y qué mutaciones se prueban.
2. «Reparar no es automático: acción documentada o tarea explícita». No se dice quién documenta, dónde ni con qué formato; obligaría a inventar el entregable de reparación.
3. «stores check/doctor/drift y relaciones comprobadas». No se identifican los stores, comandos ni quién produce ese inventario; el ejecutor tendría que suponer API/superficie existente.
4. «integration_mode: delta_or_existing_ticket_only_after_WS06» y `overlap_with: changes`, pero WS06 no figura en `depends_on`. Obliga a decidir si WS06 es prerrequisito real o solo condición de promoción.
5. «output_scope: ... rutas integridad» no nombra rutas ni criterio de pertenencia; aunque los archivos exactos se delegan a promoción, aquí no hay base para saber qué rutas quedan dentro.

## DRY-RUN
Lecturas previstas: `task-ws29.md`, contratos de WS15/WS24, tarea Changes existente en `graph_ui`, matriz/resultado de WS06 y acuerdos de WS11/WS12. Cambios previstos: delta en `changes/`, rutas de integridad y tests, sin reparación automática. Dependencias: WS15/WS24 entregados, G_UI_READ aceptado y designación del responsable. Validaciones futuras: demostrar mutaciones con soporte/alcance/errores, verificar que reparar exige acción documentada o tarea, y confirmar que el lector/manual básico no queda bloqueado. No se ejecuta nada.

## FUTURO
WS06 produce la matriz/ticket receptor y el no solapamiento; WS11 resuelve G_UI_READ; WS12/WS20 definen canales de mutación y política de campos; WS15/WS24 entregan sus contratos. La promoción y creación de `task-ws29.md` requieren autorización humana y preflight task-only.
