## REFORMULACION

**Objetivo:** crear `desk/drawer/plans/workspace-documental/contratos/navegacion.md` con las 13 secciones obligatorias en orden (alcance/estado; identidad y origen; resolución repo/store; fuente propia vs Code referenciado; navegación/enlaces/historia; foco y correspondencias; errores de lectura y red; lectura multidesk read-only; ViewDoc solo grafo; authored/derivado/preferencia local; huecos clasificados; mapa de deltas graph_ui con recepción; trazabilidad a WS09).

**Alcance:** solo documentación y lectura. Toda API se cita como `path:línea` o símbolo verificado en graph_ui `134a665` y sldb `77bd6d00`. Huecos clasificados instancia/vínculo/consulta/API/renderer con dueño y productor; escritura remitida a WS12; sin tablas internas, endpoints ni pruebas supuestas.

**Repo:** `/home/jp/proyectos/SLDB_1/deskops`; hermanos `../UIs/graph_ui` y `../sldb` en solo lectura.

**Límites:** Executor escribe únicamente el contrato y `runs/subagents/20261101-ws11-navegacion/result-summary.md`; sin commits ni revisiones; sin tocar `dag.yaml`, helper, validadores, UI ni Wi12; sin preguntar al solicitante; `execution_authorized` global sigue false; el contrato básico cierra sin actas receptoras y sin Changes/Scion/ViewDoc opcional.

## AMBIGUEDADES

1. «Si WS13.1 o el catálogo lo comprometen y falta mapeo, se registra hueco con productor o cambio de alcance explícito» — no dice quién autoriza el cambio de alcance, y «Sin preguntar al solicitante» lo impide. Obligaría a inventar un gate o a elegir por cuenta del Executor.
2. «G_SPEC_VIEW opcional aparte» y «G_SPEC_VIEW se obtiene separadamente al preparar WS18» — no se define qué gate o artefacto es. Obligaría a inventar su contenido, productor o formato.
3. «Leer auditorías… y los nodos consumidores» y «Trece nodos dependen» — no los enumera. Obligaría a inventar la lista, aunque pueda derivarse por `grep` en `dag.yaml`.
4. Validación lista `build_plan.py --check`, `validate_plan.py --check` y `status`, mientras Roles dice «Sin commits ni revisiones» y el ritual de closeout los atribuye al cierre. No queda claro si el Executor los ejecuta o solo el Tester/root.

## DRY-RUN

1. Leer completas las auditorías `deskops.md`, `infraestructura.md`, `ui.md`, más `vistas.md`, `user-flows.md`, `decisiones.md`, `reconciliacion.md` y `dag.yaml:681-711`.
2. Abrir en solo lectura `../UIs/graph_ui` y `../sldb` en los commits citados; anotar símbolo y línea de cada API que el contrato invoque.
3. Escribir `contratos/navegacion.md` con las 13 secciones en orden, tablas de foco, huecos y deltas; marcar cada delta «sin acta registrada».
4. Escribir `result-summary.md` con lo leído, lo no leído, huecos y trazabilidad.
5. Errores esperables: `build_plan.py --check` o `status` marcan revisiones obsoletas al cambiar inputs; APIs citadas en auditorías que no aparezcan en el commit; `contratos/` inexistente como directorio.
6. Resultado esperado: contrato no vacío con APIs verificadas, huecos clasificados con productor o «sin productor en el DAG», y checks en verde salvo revisiones que el helper exija renovar; Tester independiente deja `tester-result-summary.md`.
