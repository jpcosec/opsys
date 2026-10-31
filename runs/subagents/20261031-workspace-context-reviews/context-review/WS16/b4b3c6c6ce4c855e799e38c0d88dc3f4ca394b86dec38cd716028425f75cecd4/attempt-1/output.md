## REFORMULACION
Propósito: encargo de planificación para que una persona real valide el recorrido temprano de lectura/descubrimiento: UF01, UF03 lectura, UF07 diagnóstico, UF08 lectura entre desks y UF10 arranque/ausencia de desk. Resultado: acta y evidencia de aceptación en `graph_ui:runs/subagents/workspace-documental-acceptance/lectura/`, con tiempos y pruebas técnicas separados. Repo dueño: `graph_ui`. Límites: consumir el manifiesto de WS40 sin crear corpus propio; no implementar correcciones; no sustituir la aprobación humana; no habilitar mutaciones del baseline; guardados quedan para WS30; promoción no autorizada.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Lecturas previstas: `dag.yaml` (nodo WS16 y gates), `validacion-humana.md`, `cobertura.md`, `decisiones.md`, `alcance.md` y contratos de dependencias. Cambios previstos: ninguno durante la revisión; en ejecución futura, acta y registros de evidencia, sin corpus propio ni cambios de implementación. Dependencias: WS14, WS15, WS08, WS40 y WS41; `G_HUMAN_READ` pendiente. Validaciones futuras: recorrido humano real, al menos 20 aperturas y 10 búsquedas, registro de fallos y apertura de corrección por el repo dueño del nodo fallido. Sin ejecutar nada.

## FUTURO
WS40 produce y mantiene el corpus Taller y su manifiesto; WS41 habilita lectura entre desks; WS08 precisa los user-flows; WS14/WS15 entregan búsqueda y estados degradados. La persona decide la aprobación y firma el acta; los responsables de repos deciden y abren tareas de corrección ante fallos. La promoción exige TaskDoc, archivos/pills/átomos/evidencia y preflight, fuera de este nodo.
