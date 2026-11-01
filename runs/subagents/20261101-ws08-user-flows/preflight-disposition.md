# Comparación del Supervisor — WS08, aceptada para despacho

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01. Leí preflight y cold completos. Reproducen objetivo, archivos y límites. Lo que marcan queda fijado aquí; prevalece sobre la TaskDoc donde la precisa.

- Auditorías: WS02 = `auditoria/deskops.md`, WS03 = `auditoria/infraestructura.md`, WS04 = `auditoria/ui.md`, según `output_scope` en `dag.yaml`.
- «Repo dueño» = `owner_repo` del nodo. «Productor» = ID de nodo del DAG que lo producirá. Si ningún nodo lo produce, escribir «sin productor en el DAG» y el repo dueño, sin inventar uno.
- Nodo: lista desde `cobertura.md`, `validacion-humana.md` y `dag.yaml`. Si una operación no tiene nodo, es hueco.
- UF07 cubre diagnóstico, cambios (WS29) y modo degradado: una misma UF, con listas.
- ack local: operación «pendiente de contrato WS12», marcada hueco con productor WS12. No se da por disponible.
- Gate humano: solo WS16, WS30, WS37, WS39 o «ninguno adicional», como dice la aceptación. WS43 va en Nodo como publicación, no como gate humano de esta columna.
- «Revisiones afectadas renovadas» es tarea del Supervisor, no del Executor: WS08, WS16, WS30, WS37, WS44.
