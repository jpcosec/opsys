## REFORMULACION

**Propósito:** cerrar el contrato de operaciones y escritura del workspace documental, para que los deltas posteriores sepan qué lectura/mutación se permite, por qué canal y actor, con qué precondición, efectos y errores.

**Resultado:** `contratos/operaciones.md` con whitelist por operación/campo/canal/actor/revisión/Git/efectos, estado existente comprobado/faltante, mapa de recibos o pruebas por delta, matriz de capacidades/efectos y huecos con dueño; elección razonada de la precondición de payload; comparación documentada del canal de captura directa a drawer.

**Repo:** `deskops`; lecturas de contraste en `sldb`, `graph_ui` y `spec2viz`.

**Límites:** no ejecutar mutaciones, no crear actas interrepo, no aprobar API/modelo nuevo ni permisos Scion, no habilitar mutaciones, no cambiar P03 ni forzar CAS o un algoritmo de hash.

## AMBIGUEDADES

Ninguna. Las pendientes (`G_PAYLOAD_PRECONDITION`, `G_SOURCE`, recibos P01) tienen productor o resolución nombrados, y el comportamiento ante contrato ausente está fijado.

## DRY-RUN

- **Lecturas:** brief, alcance, decisiones, `dag.yaml`, auditorías WS02–04, contrato WS11, API sldb (`create_document`, `DrawerService`, guardado/`expected`/`version`) e inventarios de graph_ui/spec2viz.
- **Cambios previstos:** redactar `contratos/operaciones.md` y enlaces en `deskops`; no tocar código ni actas interrepo; no se espera modificar `dag.yaml`.
- **Dependencias:** WS11, WS08 y `G_WRITE_POLICY` (satisfecho); WS45 y WS20 como productores futuros.
- **Validaciones futuras:** evidencia path/símbolo/commit; prueba real del canal de captura; WS45 para `G_PAYLOAD_PRECONDITION`; WS20 para `G_SOURCE`; actas P01 por delta; pruebas de los consumidores.

## FUTURO

WS45 inventaría/prueba la precondición de payload; WS20 produce `G_SOURCE`; P01 emite actas por delta en repos receptores; WS25.2 implementa captura solo si el contrato la admite; WS19/21/26/28/42 consumen la whitelist; un humano decide promoción e implementación. Si falta conducta de workflow, se registra un productor Deskops explícito antes de WS25.2. WS16/WS30 realizan validaciones humanas.
