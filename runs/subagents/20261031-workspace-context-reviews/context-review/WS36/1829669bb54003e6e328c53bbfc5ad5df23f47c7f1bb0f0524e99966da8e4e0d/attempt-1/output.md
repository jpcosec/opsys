## REFORMULACION

**Propósito:** integrar en el workspace la delegación y la intervención humanas sobre ejecuciones Scion, usando exclusivamente el adaptador público de WS34 para dispatch/reply y registrando decisiones con WS33.2.

**Resultado:** una vista de ejecución en `graph_ui` donde la respuesta queda vinculada al intento, la operación se confirma y la revisión muestra actor humano y evidencia enlazada de WS33.1/WS33.2, con tests que cubren también el error visible por falta de API o permisos.

**Repo dueño:** `graph_ui`, con salidas en `frontends/mindmap/views/workspace/execution/`, ruta fina al adaptador autorizada por contrato WS12 y `tests/`.

**Límites:** solo el adaptador WS34; nada de autoaprobación ni simulación. Los gates `G_EXEC`, `G_SCION`, `G_UI_WRITE` y `G_WRITE_CONTRACT` están pendientes por diseño y no habilitan ejecución.

## AMBIGUEDADES

Ninguna.

Las referencias a WS34, WS33.1, WS33.2 y al contrato WS12 tienen productor nombrado y heredan la regla común de detenerse y registrar el hueco si faltan. La ruta exacta, los textos de pantalla y los escenarios concretos quedan delegados al TaskDoc de promoción dentro de la aceptación. Los gates pendientes son intencionales según la guía.

## DRY-RUN

- **Lecturas previstas:** contrato del adaptador WS34; contratos/evidencia de WS33.1 y WS33.2; contrato de escritura y autorización de WS12; estados de gates en `dag.yaml`; salida de lectura de WS35.
- **Cambios previstos:** componentes de vista de intervención en `frontends/mindmap/views/workspace/execution/`, llamada al adaptador WS34, presentación de actor/evidencia y tests asociados.
- **Dependencias:** WS34 y WS35 como prerrequisitos directos; WS33 vía WS34; WS12 para contrato de escritura.
- **Validaciones futuras:** test de respuesta vinculada al intento y operación confirmada; test de error visible por ausencia de API/permisos; comprobación de ausencia de autoaprobación/simulación; validación humana posterior en WS37.

## FUTURO

WS12 debe producir `G_WRITE_CONTRACT` y `G_UI_WRITE`; WS07 designa responsables y operador Scion; WS44 produce `G_SCION`; el solicitante o su designado resuelve `G_EXEC`; WS37 valida con agente real. Nada de esto se ejecuta ni se aprueba en esta revisión.
