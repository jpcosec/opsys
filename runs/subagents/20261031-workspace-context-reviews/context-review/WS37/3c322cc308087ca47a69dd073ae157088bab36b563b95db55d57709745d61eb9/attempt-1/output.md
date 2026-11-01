## REFORMULACION

- **Propósito**: validar UF06 con un agente Scion real e intervención humana: pregunta, respuesta/decisión, corrección, evidencia y cierre mediante el handoff de WS28, con actor humano.
- **Resultado**: acta de aceptación en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/acta.md` conforme al protocolo de `validacion-humana.md`.
- **Repo dueño**: `graph_ui`, con `output_base: graph_ui:repository_root/` y `output_scope` en `runs/subagents/workspace-documental-acceptance/delegacion/`.
- **Límites**: no sustituir la integración por mocks ni equiparar “completed” con aprobación; no bloquea WS31; requiere WS36, WS30, G_EXEC y G_SCION.

## AMBIGUEDADES

**ninguna**.

El guion detallado no aparece en el nodo, pero la guía excluye como ambigüedad los casos de prueba que fija el TaskDoc de promoción y `cobertura.md` atribuye a WS08 su refinamiento; el protocolo y los gates están en fuentes suministradas.

## DRY-RUN

- **Lecturas previstas**: guía de revisión; `brief.md`; `alcance.md`; `decisiones.md`; `cobertura.md` (UF06); `validacion-humana.md` (WS37); `borradores/user-flows.md` (UF06); `dag.yaml` (WS37, WS36, WS30, gates).
- **Cambios previstos**: ninguno; esta revisión no modifica el nodo ni ejecuta validaciones.
- **Dependencias**: WS36 aporta la integración sobre el adaptador WS34; WS30 aporta la validación manual y, transitivamente, WS28 (handoff de cierre) y WS12. Gates: G_EXEC (resolver externo) y G_SCION (WS44/operador). El nodo produce la evidencia de G_HUMAN_DELEGATE.
- **Validaciones futuras**: comprobar que el acta existe, está versionada en `graph_ui` con commit/blob verificable, cubre el guion UF06 sin mocks y registra decisión humana; verificar G_EXEC/G_SCION antes de ejecutar.

## FUTURO

- WS38 publicará los capítulos de delegación a partir del acta de WS37.
- WS44 o el operador designado producirá G_SCION; el solicitante firmará la autorización de G_EXEC en `deskops`.
- El TaskDoc de promoción fijará guion, casos y textos; el responsable humano aceptará el delta.
- WS31 permanece independiente; no se autoriza ejecución por esta revisión.
