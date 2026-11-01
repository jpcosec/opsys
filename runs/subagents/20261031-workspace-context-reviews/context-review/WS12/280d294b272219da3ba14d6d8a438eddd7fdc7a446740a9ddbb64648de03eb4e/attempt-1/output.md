## REFORMULACION
**Propósito:** cerrar el contrato de operaciones y escritura de WS12, no implementar ni habilitar mutaciones.
**Resultado:** `contratos/operaciones.md` con whitelist por operación/campo/canal/actor/revisión/Git/efectos, matriz de capacidades y huecos asignados.
**Repo:** `deskops` (solo contrato y enlaces).
**Límites:** no ejecutar mutaciones, no crear actas interrepo, no inventar APIs/modelos, no aprobar Scion ni cambiar P03; si falta canal/API, registrar hueco con dueño.

## AMBIGUEDADES
1. «compara API SLDB existente (`sldb.api.create_document`, DrawerService), composición y eventual wrapper Deskops»
   «composición» está definida en el glosario como representación que reúne contenido de varios documentos, pero aquí parece significar composición de llamadas API. Obligaría a inventar si debe evaluarse una capacidad de producto o una secuencia de APIs, y condiciona si el contrato de captura puede cerrarse.

2. «Solo si falta conducta de workflow se registra un productor Deskops explícito antes de WS25.2»
   No nombra nodo/ID de productor ni criterio para decidir cuándo «falta conducta de workflow». Obligaría a inventar un productor y un umbral de suficiencia, aunque la regla común permite registrar el hueco con repo dueño.

## DRY-RUN
- **Lecturas:** `dag.yaml` (WS12, gates), guía, brief, alcance, decisiones, cobertura; contrastar inventarios WS02–04 y WS11 citando path/símbolo/commit.
- **Cambios previstos:** redactar `contratos/operaciones.md`; enlazar contratos/gates; documentar huecos y productores; sin tocar código ni mutar stores.
- **Dependencias:** WS11 y WS08; `G_WRITE_POLICY` satisfecho; WS20/WS45 como productores futuros; recibos P01 por delta.
- **Validaciones futuras:** `G_WRITE_CONTRACT` por delta/efecto, `G_UI_WRITE`, `G_SLDB_WRITE`, `G_PAYLOAD_PRECONDITION` y `G_SOURCE`; no ejecutar.

## FUTURO
WS45 verificará/completará la precondición de payload; WS20 producirá raw-source; el receptor P01 registrará actas por delta; WS25.2 consumirá el contrato de captura. Un humano decide si la comparación de APIs basta o si procede registrar un productor.
