# Comparación del Supervisor — completitud de WS08, aceptada para despacho

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01. Leí preflight y cold completos. Reproducen objetivo, lista cerrada y límites. Lo que marcan queda fijado aquí.

- Hueco nuevo de UF05: mismo formato que los demás de esa UF: `- hueco: <qué> (`cita`); dueño X, productor Y.`
- Son seis líneas Nodo: UF03, UF05, UF06, UF07, UF09, UF10. UF08 solo cambia en `cobertura.md`.
- Forma de la operación: `deskops list rituals`/`show ritual`, igual que en UF01.
- Matriz: una fila por ID tal como se cita. Un ID hijo citado lleva su fila y, si Nodo tiene el agregado, marca «cubierto por WSxx». La clase «fuera de alcance» no se usa: los IDs citados solo para excluirlos no llevan fila. WS22 en UF01 lleva fila, clase citación contextual.
- Productor necesario ausente no previsto: se anota en `result-summary.md` con evidencia y no se edita. Decide el Supervisor con root; no invalida por sí solo.
- `result-summary.md`: qué se aplicó, verificación de cada ítem de la lista, hallazgos, límites.
- Tester, commits, renovación y closeout: Supervisor.
- Tras el parche, `status` y `validate --check` quedan en rojo hasta renovar: `cobertura.md` entra en los 73 bundles. Es lo esperado. Se congela y va a root antes de renovar.
