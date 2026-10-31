## REFORMULACION
**Propósito:** definir el encargo de implementación de autoría explícita desde un candidato del drawer, con evidencia declarada, dependencias y binding de contexto/pills.
**Resultado:** UI en `graph_ui` que permite autorar esos datos y verlos persistir tras recargar, sin avanzar estados manualmente.
**Repo:** `graph_ui`, con salidas en `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados por WS12 y `tests/`.
**Límites:** no editar `status` para avanzar; si una operación Git carece de contrato o dueño, queda en handoff y se declara no disponible. Las mutaciones en UI requieren `G_HUMAN_READ`; desarrollo y pruebas aisladas de API pueden avanzar con contratos/gates técnicos.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas previstas:** guía de revisión, brief, alcance, decisiones, cobertura, nodo WS26.1, contratos vecinos WS12/WS22/WS26/WS26.2 y gates.
**Cambios previstos:** implementación de autoría en `graph_ui`, pruebas y consumo de endpoints del contrato WS12; sin ejecución ahora.
**Dependencias:** WS12 (contrato de operaciones y escritura) y WS22 (Board navegable). Gates: `G_CLOSEOUT` satisfecho; `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT` pendientes, evaluados por delta.
**Validaciones futuras:** UF04 sobre TaskDoc real; candidato autorado con evidencia, dependencias y pills visibles tras recarga; comprobar que no se edita `status`; verificar handoff explícito cuando falte contrato/dueño Git; pruebas API aisladas permitidas sin acta de lectura.

## FUTURO
WS12 debe producir la whitelist y el contrato técnico por operación; WS22, la representación del Board. La persona designada acepta deltas concretos de `G_UI_WRITE`/`G_WRITE_CONTRACT`; WS16 resuelve `G_HUMAN_READ`. El TaskDoc de promoción fijará archivos, pills/átomos, evidencia, escenarios y textos de pantalla dentro de esta aceptación. La promoción sigue no autorizada.
