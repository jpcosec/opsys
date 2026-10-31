REFORMULACION
Propósito: evaluar WS30 como encargo de planificación para validación humana de autoría/revisión manual completas (UF01–UF05 según protocolo), no como implementación. Resultado: acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/manual/acta.md` y resolución de `G_HUMAN_MANUAL`; un fallo bloquea el gate. Repo dueño: `graph_ui`; `output_scope: runs/subagents/workspace-documental-acceptance/manual/`; `kind: validation`; `promotion: not_authorized`. Límites: no ejecutar, no revisar vecinos ni implementar; no aprobar Pxx; no declarar ready por tests.

AMBIGUEDADES
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md». WS08 no está en `depends_on` ni se aporta su guion. Obligaría a inventar la lista de escenarios, el criterio de conflicto/teclado y sus condiciones de paso, o suponer que `validacion-humana.md` los define, aunque solo menciona conflicto y gates.
2. «el responsable del repo dueño abre tarea en el nodo que lo causó». No aclara si el responsable es `graph_ui` (dueño de WS30) o el `owner_repo` del nodo causante, ni cómo atribuir fallos de corpus/entorno (WS17/WS40). Obligaría a inventar actor y criterio de atribución.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, validacion-humana, user-flows y nodo/gate WS30; `task_file` no suministrado. Cambios previstos: producir acta y evidencia en `manual/`, registrar resultado y estado del gate; sin código. Dependencias: WS17, WS21, WS22, WS23, WS24, WS25, WS26, WS28, WS42; WS25/26 son agregados; WS17 depende de WS40; P04 pendiente condiciona WS21. Validaciones futuras: recorrido humano UF01–UF05, errores/conflicto/teclado, `source_mode` elegido, acta versionada por el repo dueño, `G_HUMAN_MANUAL`; fallo abre tarea en nodo causante.

FUTURO
El humano/WS07 decide P04 y P08 designa participante; WS21, WS25, WS26, WS28 y WS42 producen contratos/implementaciones; WS31 publica manual tras WS30; WS43 publica en deskops. Nada de esto se ejecuta aquí.
