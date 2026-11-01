REFORMULACION
Propósito: validar con una persona el recorrido completo de autoría y revisión manual (UF02, UF03 edición, UF04, UF05, más UF01 con entradas WS17 materializadas por WS40). Resultado: acta humana bajo protocolo en `graph_ui:runs/subagents/workspace-documental-acceptance/manual/acta.md`, con plantillas/entradas, paths/hashes, recorridos y fallos. Repo dueño: `graph_ui`. Límites: no ejecutar, no implementar, no declarar ready por tests, no atribuir causalidad ni corregir otros repos; `G_HUMAN_MANUAL` solo se resuelve con aceptación humana.

AMBIGUEDADES
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08». WS08 no aparece en `depends_on` de WS30 y `validacion-humana.md` no detalla el guion ni la navegación por teclado. El ejecutor tendría que inventar esos escenarios o asumir un prerrequisito no declarado.
2. «que supervisor receptor autorice diagnóstico antes de atribuir nodo». No se define quién es el supervisor receptor ni cómo se registra su autorización; obligaría a inventar actor y evidencia.
3. «paths/hashes y recorridos». No queda claro si son hashes de plantillas WS17 o de su materialización WS40; WS17 distingue fuente versionada y destino temporal, y el acta debe servir a WS43.

DRY-RUN
Lecturas: guion WS08 (no dependencia formal), `validacion-humana.md`, WS17/WS40, P04/P08, contratos WS12, DAG y gate. Cambios previstos: solo acta en `graph_ui:.../manual/`; sin código. Registrar entradas, paths/hashes, recorridos, fallos/observaciones. Dependencias: WS17, WS21–WS26, WS28, WS42; WS40 vía WS17; `G_HUMAN_MANUAL`. Validaciones futuras: acta versionada en commit, evidencia del gate, trazabilidad para WS43 y WS31; fallo abre tarea en nodo causante o incidente.

FUTURO
WS08 debe entregar el guion; la persona participante ejecuta la sesión y decide; WS43 consume el acta para publicación real; WS31 la cita; un supervisor autoriza diagnóstico si el fallo no está aislado. Nada de esto autoriza ejecución.
