## REFORMULACION
**Propósito:** cerrar el contrato técnico de operaciones y escritura: whitelist lectura/mutación por campo/modelo, canal CLI/API, política de coordinador, Git, campos protegidos, CAS/locks, fallos parciales, permisos y closeout fuera de la UI.

**Resultado:** `contratos/operaciones.md` y `G_WRITE_CONTRACT`, con capability exacta por acción; aceptación del delta en `graph_ui`; aceptación condicional en `sldb` si `source_mode=editable`. Toda operación sin contrato queda no disponible.

**Repo dueño:** `deskops`.

**Límites:** no implementa UI ni WS20; no asume que el lock de UI protege escritores CLI; no anuncia closeout; con `read_only`, `G_SLDB_WRITE` no es prerrequisito ni se presenta como aprobado.

## AMBIGUEDADES
1. «registrar capability exacta para cada acción». No se enumera el universo de «acciones» ni su granularidad: ¿campo, relación, endpoint, comando o flujo? El ejecutor tendría que inventar el catálogo y el nivel de detalle, con riesgo de omitir operaciones de WS19/25/26/28/32/34/39/42 o exceder el contrato.
2. «adapter CLI/API público». No se identifica si es un adaptador ya existente de `deskops`, una API pública verificada de otro repo o un componente nuevo. El ejecutor tendría que inventar si WS12 documenta canales existentes o diseña nombres/endpoints nuevos, y de quién es la autoridad del adapter.

## DRY-RUN
- **Lecturas:** WS12 en `dag.yaml`, guía, brief, alcance, decisiones, cobertura y gates; contrastar consumidores del contrato.
- **Cambios previstos:** redactar/actualizar `contratos/operaciones.md`; registrar `G_WRITE_CONTRACT`; acta `G_UI_WRITE`; `G_SLDB_WRITE` solo si `editable`.
- **Dependencias:** WS08 y WS11 cerrados; `G_WRITE_POLICY` aprobado por humano; `source_mode` ya no `pending`; responsables `graph_ui`/`sldb` designados.
- **Validaciones futuras:** whitelist contra cada consumidor; clasificar APIs existentes/comprobadas o faltantes; verificar permisos y CAS/locks; confirmar que autoría/cierre quedan bloqueados por `G_CLOSEOUT`; no exigir WS20 para cerrar WS12.

## FUTURO
WS07 resuelve P01–P06 y designa responsables; WS20 produce `G_SOURCE` si falta capacidad; los repos receptores aceptan deltas; el humano aprueba los gates. WS12 no implementa ni promueve nada.
