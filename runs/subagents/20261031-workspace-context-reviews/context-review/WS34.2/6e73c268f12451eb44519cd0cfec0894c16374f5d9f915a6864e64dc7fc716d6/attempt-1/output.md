## REFORMULACION
**Propósito:** revisar WS34.2 como encargo de planificación, no como producto ni ejecución.
**Resultado:** adaptador público restringido para reply vinculado al intento, con timeout/errores y autoridad del coordinador; aceptación mediante agente real y timeout reportado como fallo sin confirmación.
**Repo:** `deskops`; salidas en `runtime/`, `cli/commands/runtime.py` o API definida, y `tests/`.
**Límites:** no enviar mensajes en planificación; no implementar aquí; `promotion: not_authorized`; dependencias y gates son prerrequisitos, no permisos concedidos.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas previstas:** nodo WS34.2, guía, brief, alcance, decisiones y referencias del DAG a WS33, WS12, WS34.1 y gates. También el TaskDoc de promoción cuando exista.
**Cambios previstos:** ninguno en esta revisión. En ejecución futura, adaptador de reply y pruebas en `deskops`; no se modifica el plan.
**Dependencias:** WS33, WS12 y WS34.1; requieren G_EXEC, G_SCION y G_WRITE_CONTRACT.
**Validaciones futuras:** agente real demuestra respuesta vinculada al intento correcto; timeout se reporta como fallo sin confirmación; umbral según contrato WS12. No se ejecuta nada.

## FUTURO
- WS12 produce el contrato técnico por operación, incluidos umbral/errores y política de autoridad del coordinador.
- WS44 y el operador designado producen G_SCION; el solicitante/designee produce G_EXEC.
- WS33 y WS34.1 aportan referencias de mensaje/intento y dispatch previo.
- La promoción fija archivos exactos, pills, evidencias y preflight; el agregado WS34 termina cuando terminan sus hijos.
