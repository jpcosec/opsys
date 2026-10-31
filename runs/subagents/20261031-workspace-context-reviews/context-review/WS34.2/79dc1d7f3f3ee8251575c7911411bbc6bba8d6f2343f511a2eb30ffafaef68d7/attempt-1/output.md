## REFORMULACION

**Propósito:** revisar si WS34.2 está bien planteado como encargo de planificación para un adaptador público restringido de *reply* Scion, vinculado al intento, con timeout/errores y autoridad del coordinador.

**Resultado:** adaptador de respuesta y pruebas que demuestren vinculación al intento correcto y reporte de timeout como fallo sin confirmación.

**Repo dueño:** `deskops`; salidas en `runtime/`, `cli/commands/runtime.py` o API fijada por WS12, y `tests/`.

**Límites:** no ejecutar ni enviar mensajes durante planificación; no duplicar transporte; no inventar contrato ausente; promoción no autorizada.

## AMBIGUEDADES

Ninguna. El nodo nombra repo, resultado, aceptación comprobable, dependencias y gates. El umbral de timeout y la autoridad del coordinador se remiten al contrato de WS12; si faltara, aplican las reglas comunes de `alcance.md` (detenerse y registrar hueco), sin obligar a inventar.

## DRY-RUN

- **Lecturas previstas:** `dag.yaml#node:WS34.2`, guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y contratos vecinos como contexto, sin revisarlos como nodos.
- **Cambios previstos:** solo este informe de revisión; ningún archivo del repo ni del plan.
- **Dependencias:** WS33 aporta referencias mensaje/intento; WS12 aporta contrato de operaciones, autoridad y umbral; WS34.1 aporta dispatch previo. Gates G_EXEC, G_SCION y G_WRITE_CONTRACT son externos/pendientes.
- **Validaciones futuras:** comprobar gates; demostrar con agente real reply vinculado al intento correcto; verificar que timeout se reporta como fallo sin confirmación; confirmar ausencia de mensajes en planificación.

## FUTURO

- WS07 designa operador Scion y responsables; WS44 produce la sonda de G_SCION; WS12 produce contrato y G_WRITE_CONTRACT; un humano resuelve G_EXEC.
- La promoción exigirá TaskDoc, archivos/pills/átomos/evidencia y preflight específico, hoy `not_authorized`.
- Cualquier hueco contractual detectado al ejecutar se registra con repo dueño; no se sustituye aquí.
