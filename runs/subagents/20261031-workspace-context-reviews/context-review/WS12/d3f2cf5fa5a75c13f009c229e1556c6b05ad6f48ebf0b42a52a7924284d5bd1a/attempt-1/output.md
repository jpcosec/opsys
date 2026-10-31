## REFORMULACION
Propósito: cerrar el contrato técnico de operaciones y escritura antes de las implementaciones de mutación. Resultado: `contratos/operaciones.md` con whitelist por campo/modelo, capability exacta por operación (canal y efectos) y políticas de coordinador, Git, campos protegidos, CAS/locks, fallos parciales, permisos y closeout fuera del servidor UI. Repo dueño: `deskops`. Límites: no implementa UI ni APIs; usa canal público existente o registra hueco y dueño; no diseña sustituto; autoría/cierre quedan bloqueados por `G_CLOSEOUT`; delta sldb solo si `source_mode=editable`; no asume que el lock de UI protege escritores CLI.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Lecturas: guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo WS12 y gates. Sin ejecutar nada.

Cambios previstos: redactar `contratos/operaciones.md`; clasificar APIs como existentes/comprobadas o faltantes; registrar capabilities y políticas; recoger aceptación de delta en `graph_ui` y, si aplica, en `sldb`; no producir código.

Dependencias: WS11 (identidad/navegación), WS08 (user-flows), `G_WRITE_POLICY` de WS07; `G_CLOSEOUT`, `G_SOURCE`, `G_UI_WRITE` y `G_SLDB_WRITE` según `source_mode`; responsables de repo que fije P01.

Validaciones futuras: `G_WRITE_POLICY` aprobado por humano; aceptación de `graph_ui` y `sldb`; `source_mode` distinto de `pending`; capabilities con canal/efectos; operaciones sin contrato declaradas no disponibles; verificación de `G_WRITE_CONTRACT`.

## FUTURO
WS07/humano resuelve P01 y P03–P06, fija `source_mode` y emite `G_WRITE_POLICY`. WS11 entrega el contrato de navegación; WS08 los user-flows; WS20 produce la API fuente y `G_SOURCE`; los nodos consumidores usan la whitelist. `G_CLOSEOUT` es externo. Los responsables de `graph_ui` y `sldb` aceptan sus deltas; sin esa aceptación WS12 no cierra.
