## REFORMULACION

- **Propósito:** revisar PK08 como encargo de planificación del ramal Scion opcional, sin ejecutarlo.
- **Resultado sustantivo:** paquete integrado de delegación Scion posterior con intento/manifiesto/RunDoc/cierre idempotentes, mensajes/resultados/decisiones con procedencia y dedup, dispatch/reply autorizados, trazabilidad e intervención humanas, aceptación con agente real y capítulo de manual verificado.
- **Repo dueño:** `deskops`; hijos en `deskops` y `graph_ui`.
- **Límites:** agrupación sin ejecución propia; no autoriza tareas ni añade aristas; no duplica el pipeline Scion; ningún permiso de núcleo se convierte en dispatch; sin acceso real el ramal queda bloqueado; no se inventan permisos, actas ni estados.

## AMBIGUEDADES

ninguna.

## DRY-RUN

Sin ejecutar:

- **Lecturas previas:** alcance, brief, decisiones, gates, inventario WS05 y contratos/actas externas. WS05 y WS07 alimentan el paquete desde fuera.
- **Orden hipotético:** WS44 tras WS05/WS07, con operador/acceso registrados, produce `G_SCION` mediante probe read-only. Luego WS32 → WS33 → WS34 → WS35/WS36 → WS37 → WS38.
- **Entradas/salidas:** WS32 fija identidad, manifiesto y cierre; WS33 enlaza mensajes, resultados y decisiones; WS34 expone adaptador dispatch/reply bajo `G_EXEC`; WS35 muestra trazas; WS36 integra intervención; WS37 valida recorrido real; WS38 publica capítulo y átomos.
- **Integración/validación futura:** recorrido pregunta/intervención/corrección/evidencia/decisión/cierre por WS28, con acta humana WS37; pruebas locales de idempotencia y dedup; sin mocks en WS37; manual enlazado al acta. Si falta `G_SCION`, `G_EXEC` o contrato, detenerse y registrar hueco.

## FUTURO

WS05/WS07 aportan inventario y registro; el solicitante designa operador/acceso y autoriza `G_EXEC`; WS44 ejecuta el probe real; P01 verifica recibos por delta; WS37 produce acta humana; WS38 publica. Nada de esto equivale a aprobación ya emitida.
