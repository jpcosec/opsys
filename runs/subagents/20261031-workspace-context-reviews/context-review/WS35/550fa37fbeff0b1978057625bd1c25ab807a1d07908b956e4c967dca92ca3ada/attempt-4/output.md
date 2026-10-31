REFORMULACION
- Propósito: nodo de implementación en `graph_ui` para una vista de solo lectura de ejecución y trazabilidad.
- Resultado: mostrar mensajes y resultados bajo su intento, enlazar cada uno a su fuente y abrir la evidencia en el lector; `completed` no equivale a aprobado/cerrado.
- Repo: `graph_ui`; salida en `frontends/mindmap/views/workspace/execution/; tests/`.
- Límites: lectura; depende de WS33 y WS27; exige `G_SCION` y `G_UI_READ`; promoción no autorizada.

AMBIGUEDADES
1. «Cada mensaje y resultado se muestra bajo su intento» junto con «mensajes de Scion por su API»: no se define qué es un «resultado» ni qué dependencia lo produce con contrato propio. WS33 se titula «Vincular mensajes, resultados y decisiones», pero el alcance de WS35 solo nombra mensajes de Scion, tarea, intento y decisión. El ejecutor tendría que inventar si «resultado» es un payload de mensaje Scion, una salida del intento o un registro de WS33, y cómo se enlaza «a su fuente».

DRY-RUN
- Lecturas: `dag.yaml` (nodo WS35 y aristas WS33/WS27 como contratos de vecinos, sin revisarlas), guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`.
- Cambios previstos: ninguno; es revisión de encargo, no ejecución.
- Dependencias: WS33 y WS27; gates `G_SCION` (resuelve WS44) y `G_UI_READ` (resuelve WS11).
- Validaciones futuras: comprobar agrupación bajo intento, enlace a fuente, apertura de evidencia en lector y ausencia de traducción de `completed` a aprobado/cerrado; el TaskDoc fijará archivos y pruebas dentro de la aceptación.

FUTURO
- WS44 produce la probe de `G_SCION`; WS11 acepta el delta de `G_UI_READ`; el humano autoriza la promoción. El TaskDoc precisará archivos, textos y casos de prueba.
