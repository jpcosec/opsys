## REFORMULACION
**Propósito:** revisar WS13.3 como encargo de planificación: pestañas, divisiones, foco e historia sobre documentos.
**Resultado:** nodo con repo, dependencias y límites identificables; la aceptación no cubre todo el alcance y usa “foco/origen” de forma poco observable.
**Repo:** `graph_ui`; salida en `frontends/mindmap/views/workspace/layout/`, rutas de lectura según WS11 y `tests/`.
**Límites:** solo input explícito; no ejecutar; no revisar vecinos; Pxx pendientes no son aprobaciones.

## AMBIGUEDADES
1. **Cobertura de pestañas en la aceptación.** Cita: alcance “Pestañas, dos documentos lado a lado…” frente a aceptación “Abrir dos documentos en divisiones…”. Obliga a inventar si abrir/cambiar/cerrar pestañas es requisito verificable o si basta con dos divisiones; la aceptación no dice cómo comprobar la parte de pestañas.
2. **Significado operativo de “foco” y “origen”.** Cita: “alternar foco y volver conservando origen e historia” y “Foco es por documento; cambiar de pestaña cambia el documento activo, no el foco guardado…”. El glosario define foco como elemento seleccionado, pero aquí puede leerse como panel/documento activo. Obliga a inventar qué acción concreta demuestra “alternar foco” y qué estado observable prueba conservar el origen al volver.

## DRY-RUN
**Lecturas:** guía, brief, alcance, decisiones, cobertura, reconciliación y nodo WS13.3; contratos vecinos WS11/WS13.1 solo como dependencias.
**Cambios previstos:** ninguno; es revisión.
**Dependencias:** WS11 debe producir contrato/acta `G_UI_READ`; WS13.1 aporta lectura; `G_UI_READ` sigue pendiente; integración `delta_or_existing_ticket`.
**Validaciones futuras:** comprobar aceptación de pestañas/divisiones/foco/historia; acta receptora y no solapamiento; TaskDoc y preflight; promoción no autorizada.

## FUTURO
WS11 produce contrato y acta de aceptación; WS07 designa responsable; el TaskDoc de promoción fija archivos, textos y escenarios; un humano autoriza promoción y resuelve gates. Nada de esto se ejecuta aquí.
