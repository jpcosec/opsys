## REFORMULACION
**Propósito:** validar UF06 real —pregunta, intervención, corrección, evidencia, decisión y cierre— con Scion real y actor humano.
**Resultado:** acta en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/` y satisfacción de `G_HUMAN_DELEGATE`; no se sustituye integración por mocks ni se equipara “completed” con aprobación.
**Repo dueño:** `graph_ui`, con `output_base: graph_ui:repository_root/` y `output_scope: runs/subagents/workspace-documental-acceptance/delegacion/`.
**Límites:** depende de WS36 y WS30; exige `G_EXEC` y `G_SCION`; el cierre usa el handoff de WS28, alcanzable transitivamente vía WS30; no bloquea WS31; promoción no autorizada.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas previstas:** `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `validacion-humana.md`, nodo WS37, contratos de WS36/WS30/WS38 y tabla de gates.
**Cambios previstos:** ninguno; esta revisión no ejecuta ni promueve.
**Dependencias:** WS36 aporta la integración del adaptador; WS30, la validación manual y el cierre por handoff; `G_EXEC` es externo; `G_SCION` lo produce WS44; WS37 produce `G_HUMAN_DELEGATE`.
**Validaciones futuras:** acta con actor humano, versión, guion y resultado; comprobación de `G_SCION`/`G_EXEC`; ausencia de mocks sustitutivos; distinción entre completado y aprobado; no bloqueo de WS31.

## FUTURO
WS07 debe designar al operador Scion y al participante humano; WS44 debe producir `G_SCION` mediante probe real; P08 debe confirmar participante y umbrales; WS38 publicará los capítulos verificados; WS31 no queda bloqueado por WS37.
