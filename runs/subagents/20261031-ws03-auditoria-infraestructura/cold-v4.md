## REFORMULACION

**Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md`, auditoría de solo lectura, verificable fila por fila, sobre persistencia de fuente/payload, conflictos/concurrencia, referencias documentales, búsquedas/índices y notaciones/renderers de spec2viz con alcance real de ViewDoc.

**Alcance:** una sección por capacidad; filas por repo y mecanismo con columnas capacidad, repo, ubicación, operación expuesta, estado (comprobado/ausente/hueco), evidencia. Encabezado con fecha ISO, HEAD completo y líneas de `git status --short` por repo leído, SHA-256 de evidencia sucia.

**Repo:** deskops (entregable y validaciones); lectura en `../sldb`, `../pron`, `../spec2viz`. Kimun fuera de universo, no se lee.

**Límites:** Executor escribe solo entregable y `runs/subagents/20261031-ws03-auditoria-infraestructura/`; sin commits, closeout ni cambios en otros repos, `dag.yaml`, Board ajeno. Supervisor valida/commitea; Tester verifica. Mecanismos nombrados son hipótesis, no hechos.

## AMBIGUEDADES

1. **Autorización de ejecución.** «`dag.yaml` mantiene `execution_authorized=false`» frente a «Activada por runs/subagents/20261031-ws02-04-checkpoint/activation.md», archivo no incluido. Obligaría a inventar si la tarea está activa o solo preparable.
2. **Ejecutar CLIs.** «Auditoría de solo lectura» frente a «hallado por esa búsqueda y por la ayuda de cada CLI». Obligaría a decidir si se permite invocar `--help` (y solo eso) en repos ajenos.
3. **Ubicación de lo ausente.** «ubicación (archivo:línea o símbolo)» con estado «ausente». Obligaría a inventar qué poner en ubicación/evidencia cuando no existe archivo.
4. **ViewDoc contradictorio.** Brief: «Proyección de grafo ViewDoc: contrato existente de spec2viz»; tarea: hipótesis y, si no aparece, «se registra ausente». Obligaría a elegir qué autoridad manda y qué cuenta como «en su lugar».
5. **Filas por repo ausente.** «una fila por repo y mecanismo» y «filas también para los mecanismos nombrados… que resulten ausentes». No queda claro si cada mecanismo ausente genera fila por cada repo o una sola.
6. **Alcance de «documento».** «cualquier forma implementada de que un documento apunte a otro». Obligaría a inventar si «documento» es archivo Markdown o cualquier entidad persistida.
7. **Evidencia por comando.** «salida de comando» frente a `commands.log` como registro. Obligaría a decidir si la salida se transcribe en la fila o se referencia.
8. **Validaciones.** «el Supervisor corre las validaciones de plan» frente a `## Validation` listada en la tarea sin asignar quién la ejecuta antes del handoff.

Formato restante queda delegado al Executor («lo decide el Executor y lo anota en result-summary.md»).

## DRY-RUN

**Fuentes a leer:** task-ws03, `cierre.md`, `brief.md`, `dag.yaml` (referenciado, ausente del bundle), `activation.md` (referenciado, ausente), rituales execution/testing/closeout, cuatro pills, y los tres repos.

**Entregable:** `infraestructura.md` + `commands.log` + `result-summary.md`; luego `tester-result-summary.md` por Tester.

**Comandos previstos (no ejecutados):** `git -C <repo> rev-parse HEAD`, `git -C <repo> status --short`, `grep -rIn ViewDoc` y `-i` excluyendo `.venv`/`node_modules`, `--help` de cada CLI si se autoriza, `sha256sum` de evidencia sucia, y las cuatro validaciones de `## Validation`.

**Resultado esperado:** secciones por capacidad con filas comprobado/ausente/hueco; ViewDoc declarado ausente con el comando usado si no aparece.

**Futuras, no lagunas:** WS05 Scion, WS06/08–12, contratos nuevos, implementación y deltas WS13+.
