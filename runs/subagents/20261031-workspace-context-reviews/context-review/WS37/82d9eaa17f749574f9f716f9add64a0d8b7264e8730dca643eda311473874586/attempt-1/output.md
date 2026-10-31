## REFORMULACION

**Propósito:** validar de punta a punta UF06 con un agente real y un actor humano: pregunta, intervención, corrección, evidencia, decisión y cierre por autoridad. Es un nodo de validación, no de implementación.

**Resultado:** acta y evidencia en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/`, que alimentan `G_HUMAN_DELEGATE`. `graph_ui` es el repo dueño; `deskops` solo contiene el plan.

**Límites:** no sustituir la integración por mocks; no confundir “completed” con aprobación; promoción no autorizada; no bloquea WS31; el gate `G_SCION` depende del probe de WS44 y `G_EXEC` de autorización humana externa.

## AMBIGUEDADES

1. **“cierre vía autoridad, con actor humano”**
   - Cita: *“cierre vía autoridad, con actor humano”*.
   - Qué obligaría a inventar: el canal concreto de cierre —CLI Deskops, coordinador, commit externo— y el artefacto que demuestra el cierre. Las fuentes remiten a handoff externo y a P05/P06, aún pendientes; el nodo no nombra operación ni evidencia específica. No se pide resolver P05/P06; se señala que el guion de WS37 debe decir qué se ejecutará y cómo se comprobará sin decidir la política.

## DRY-RUN

- **Lecturas previstas:** guía de revisión, nodo WS37, contratos vecinos WS36/WS30/WS38, gates, brief, alcance, decisiones, cobertura, validación humana y user-flows. Nada ejecutado.
- **Cambios previstos:** ninguno ahora. Al ejecutarse, produciría el acta en el `output_scope` de `graph_ui`, incluyendo versión, guion, resultados y soportes; el acta debe entrar en commit atómico del repo dueño.
- **Dependencias:** WS36 aporta despacho/respuesta autorizados; WS30 aporta el recorrido manual previo; `G_EXEC` requiere permiso humano explícito; `G_SCION` requiere probe real de WS44.
- **Validaciones futuras:** comprobar que cada mensaje/resultado corresponde al intento correcto, que la ausencia de API/permisos sea visible, que no haya autoaprobación y que el acta versionada permita resolver `G_HUMAN_DELEGATE`.

## FUTURO

WS44 produce `G_SCION`; un humano autoriza `G_EXEC`; P08 designa al participante; WS38 publica el capítulo verificado de delegación tras WS37 y WS31. La política exacta de cierre externo la fijan P05/P06 y el responsable humano, no este nodo.
