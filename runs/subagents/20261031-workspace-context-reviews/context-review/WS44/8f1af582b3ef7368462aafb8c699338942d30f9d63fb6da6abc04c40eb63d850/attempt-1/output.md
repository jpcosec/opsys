REFORMULACION
- **Propósito:** comprobar mediante probe read-only que la API pública de Scion responde y que identidad, Hub y capabilities mínimas —las que WS05 marque para WS32/WS33— están disponibles.
- **Resultado:** `auditoria/scion-probe.md` en `deskops` y recibo de G_SCION; si falta API o acceso, WS44 queda bloqueada sin cierre ni avance a WS32.
- **Repo:** `deskops`, con `output_scope: auditoria/scion-probe.md`.
- **Límites:** no crear agentes, enviar mensajes, cambiar configuración ni mostrar secretos. Requiere registro previo del solicitante en `autorizaciones/scion.md`; sin él no se ejecuta el probe.

AMBIGUEDADES
ninguna.

DRY-RUN
- **Lecturas previstas:** `auditoria/scion.md` de WS05; `autorizaciones/scion.md`; configuración Scion existente sin secretos; referencias de WS32/WS33 para capabilities mínimas.
- **Cambios previstos:** escribir únicamente `auditoria/scion-probe.md` con respuesta pública real, actor del probe, Hub, fecha y capabilities. No mutar Scion.
- **Dependencias:** WS05 y WS07; G_PRODUCT satisfecho; operador designado y permiso read-only registrado por el solicitante. Si WS05 no mapea capabilities por nodo, detenerse y registrar el hueco antes del probe.
- **Validaciones futuras:** G_SCION solo se satisface con el probe real; tras cambio de Hub/API/credencial debe repetirse e invalidarse el recibo previo. WS32 no avanza sin G_SCION.

FUTURO
El solicitante designa al operador y registra su acceso read-only; WS05 produce el inventario y el mapeo de capabilities; WS32/WS33 consumen el recibo; una persona decide la designación y la revalidación. Nada de esto es ambigüedad del nodo.
