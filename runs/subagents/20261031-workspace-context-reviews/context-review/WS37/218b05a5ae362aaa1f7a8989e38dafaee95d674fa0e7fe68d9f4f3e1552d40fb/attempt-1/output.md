REFORMULACION
Propósito: validar UF06 con Scion real y actor humano: pregunta, intervención, corrección, evidencia, decisión y cierre por el handoff de WS28. Resultado: acta versionada en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/` y dictamen del gate `G_HUMAN_DELEGATE`. Repo dueño: `graph_ui`; base: `graph_ui:repository_root/`. Límites: no autoriza ejecución (`promotion: not_authorized`), no sustituye integración por mocks, no confunde `completed` con aprobación y no bloquea WS31.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas previstas: input completo, guía, `dag.yaml#node:WS37`, gates, `validacion-humana.md`, `cobertura.md`, `user-flows.md`, `alcance.md`, `brief.md`, `decisiones.md` y contratos de WS36/WS30 como vecinos. Cambios previstos: redactar/actualizar el acta de WS37 en `graph_ui`, enlazar evidencia y soportes, y registrar la decisión humana del gate; no hay cambios de producto ni de código. Dependencias: WS36 y WS30; `G_EXEC` y `G_SCION`; WS28 llega transitivamente vía WS30. Validaciones futuras: ejecutar el guion UF06 con integración real, comprobar pregunta/intervención/corrección/evidencia/decisión/cierre, verificar que el acta está versionada y que el gate queda respaldado por actor humano, versión, guion y resultado.

FUTURO
El humano debe emitir la autorización explícita de `G_EXEC` y confirmar el participante de P08. WS44 debe producir el probe real de `G_SCION`; WS36 debe entregar la integración; WS30 debe acreditar la validación manual previa; WS28 aporta el handoff de cierre; WS38 publica el capítulo verificado y WS07 designa al operador Scion. Nada de esto se ejecuta ni se aprueba por inferencia en esta revisión.
