REFORMULACION
Propósito: cerrar el contrato técnico de operaciones y escritura del workspace documental, fijando whitelist de lectura/mutación por campo/modelo, canal público por operación y políticas de coordinador, Git, campos protegidos, CAS/locks, fallos parciales, permisos y closeout fuera del servidor UI. Resultado: `contratos/operaciones.md` con capabilities exactas (operación, canal, efectos) para los nodos consumidores; APIs clasificadas como existentes/comprobadas o faltantes; huecos con repo dueño; actas/deltas de G_UI_WRITE y G_SLDB_WRITE cuando corresponda; operaciones sin contrato no disponibles. Repo: deskops. Límites: no diseña adapters ni implementa WS20; no asume lock UI; no convierte Pxx en decisiones; closeout Git fuera del servidor UI; con read_only no activa G_SLDB_WRITE.

AMBIGUEDADES
Ninguna. Las aparentes faltas —actor graph_ui/sldb, `source_mode`, G_CLOSEOUT/G_SOURCE— están cubiertas por gates, WS07 o las reglas comunes; no obligan al ejecutor de WS12 a inventar resultado, aceptación, repo o límite.

DRY-RUN
Lecturas: nodo WS12 y gates en dag.yaml; brief, alcance, decisiones, cobertura y guía; salidas de WS11 (`contratos/navegacion.md`, actas G_UI_READ/G_SPEC_VIEW), WS08 (`borradores/user-flows.md`) y WS07 (P01–P06, `source_mode`, responsables); auditorías vía WS06/07. Cambios previstos: redactar `contratos/operaciones.md`; clasificar APIs; registrar huecos; obtener aceptación de delta en graph_ui y, si editable, en sldb; no tocar implementación. Dependencias: G_WRITE_POLICY (WS07) y, transitivamente, G_PRODUCT; G_CLOSEOUT externo bloquea autoría/cierre; G_SOURCE pertenece a WS20. Validaciones futuras: G_WRITE_CONTRACT, G_UI_WRITE, G_SLDB_WRITE; revisión por responsables; consumo por WS19/20/21/25/26/27/28/32/34/36/39/42.

FUTURO
WS07 humano: resolver P03–P06 y P01/P04; designar responsables graph_ui/sldb/spec2viz y operador Scion. WS11/WS08 entregan contratos previos. WS20 produce G_SOURCE y la capacidad raw-source si editable. G_CLOSEOUT permanece externo. Los responsables de graph_ui/sldb aceptan y firman actas; sin recepción, WS12 no cierra. WS12 no decide Pxx ni promueve.
