## REFORMULACION

**Propósito:** cerrar el contrato de operaciones y escritura del workspace documental, fijando qué lectura/mutación existe, por qué canal y con qué efectos.

**Resultado:** `contratos/operaciones.md` en `deskops`, con whitelist por operación/campo/canal/actor/revisión/Git/efectos, matriz de capacidades y huecos con productor asignado.

**Repo dueño:** `deskops`.

**Límites:** no ejecutar mutaciones, no crear actas interrepo, no diseñar adapters ausentes, no inventar una whitelist universal. Solo contrato y enlaces; el cierre no requiere habilitar ninguna mutación.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** `dag.yaml` (WS12, vecinos y gates), guía, brief, alcance, decisiones, cobertura; auditorías WS02–04 y contrato WS11 por dependencia transitiva; evidencia de G_WRITE_POLICY y G_CLOSEOUT.

**Cambios previstos:** publicar `contratos/operaciones.md` con whitelist, matriz de capacidades/efectos, estado comprobado/faltante y enlaces de recepción por delta. Sin tocar actas ni ejecutar operaciones.

**Dependencias:** WS11 y WS08 como prerrequisitos; G_WRITE_POLICY y G_CLOSEOUT ya satisfechos. G_SOURCE pendiente de WS20; G_SLDB_WRITE, G_UI_WRITE y G_WRITE_CONTRACT se evalúan por delta. G_EXEC/G_SCION no habilitan nada en WS12.

**Validaciones futuras:** citar path/símbolo/commit para lo comprobado; clasificar lo demás como faltante con dueño; mapear recibo/prueba por delta; verificar que el contrato no autoriza mutaciones ni sustituye APIs inexistentes; contrastar inventarios WS02–04 y WS11.

## FUTURO

El receptor P01 emite actas por delta en el repo dueño. WS20 produce G_SOURCE y desbloquea el consumidor WS21. La aceptación de G_WRITE_CONTRACT y G_UI_WRITE corresponde por IDs/efecto a cada delta, no a una aceptación conjunta. La promoción fijará archivos, pills y TaskDoc. WS34/WS37 y los gates G_EXEC/G_SCION quedan fuera de este nodo.
