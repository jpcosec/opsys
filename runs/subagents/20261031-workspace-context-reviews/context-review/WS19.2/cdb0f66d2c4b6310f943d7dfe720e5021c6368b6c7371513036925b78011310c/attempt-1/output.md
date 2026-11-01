## REFORMULACION

**Propósito:** implementar en `graph_ui` el alta y baja de relaciones permitidas por el contrato WS12, dentro del workspace integrado, sin definir semántica de relaciones en el componente.

**Resultado:** relaciones persistidas y confirmadas tras recargar; rechazo visible de una relación no permitida o de una revisión obsoleta; pruebas en `graph_ui`.

**Repo dueño:** `graph_ui` (`frontends/mindmap/views/workspace/relations/`, endpoints autorizados por WS12, `tests/`). Promoción no autorizada.

**Límites:** no crear semántica de relaciones; no duplicar en paralelo el ticket de edición; G_HUMAN_READ solo habilita uso de mutaciones en UI, no desarrollo ni pruebas aisladas de API; la precondición de escritura la fija WS12.

## AMBIGUEDADES

Ninguna.

Los huecos aparentes tienen productor nombrado y regla de falta: WS12 publica whitelist, canal y representación de la precondición; WS45 resuelve `G_PAYLOAD_PRECONDITION`; WS16, `G_HUMAN_READ`; el receptor P01, `G_UI_WRITE` por delta. `alcance.md` ordena detenerse y registrar el hueco si falta contrato, API o permiso. Archivos exactos, escenarios de prueba y textos de pantalla quedan al TaskDoc de promoción. La posible coincidencia con el ticket de edición está cubierta por `overlap_with` e `integration_mode`.

## DRY-RUN

Sin ejecutar.

- **Lecturas previstas:** nodo WS19.2 y gates; contrato WS12 cuando exista; ticket de edición (`sha256 ea6b71f2…`); `reconciliacion.md`; `alcance.md` y `decisiones.md`.
- **Cambios previstos:** UI de relaciones y pruebas bajo `graph_ui`; consumo de la API real existente o del canal que fije WS12; sin cambios en `deskops`.
- **Dependencias:** WS12 (whitelist, operaciones y precondición), `G_PAYLOAD_PRECONDITION` (WS45), `G_HUMAN_READ` (WS16), `G_UI_WRITE` y `G_WRITE_CONTRACT` por delta; base reutilizable a1b2b22/f16fcd1/134a665.
- **Validaciones futuras:** alta y baja persisten tras recarga; relación no permitida rechazada con error visible; revisión obsoleta rechazada con error visible; ausencia de duplicación o solapamiento con el ticket de edición.

## FUTURO

WS12 entrega el contrato de operaciones y la representación de la precondición; WS45 verifica esa precondición en sldb; WS16 produce el acta humana de lectura; el receptor P01 registra el acta por delta en `graph_ui`; la promoción fija TaskDoc, archivos y pruebas. Nada de esto se ejecuta aquí.
