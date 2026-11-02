**REFORMULACION**
WS32 es un **agregado no ejecutable** del repo `deskops`: unificar identidad de intento y cierre Scion refinando el candidato de drawer citado, sin segundo pipeline. Su resultado son las salidas de WS32.1 y WS32.2: identidad/registro local de intento y manifiesto/RunDoc/cierre idempotentes. Depende de WS05 y WS12 y de sus hijos; requiere `G_CLOSEOUT`, `G_SCION` y `G_WRITE_CONTRACT`. Límites: sin dispatch/reply de red, sin mocks ni eventos Hub inventados; los estados Hub reales se prueban en WS34/37 bajo `G_EXEC`; el candidato no es ticket del Board; no autoriza promoción ni duplica pipeline. Aceptación: se cumple cuando ambos hijos cumplen la suya.

**AMBIGUEDADES**
Ninguna. Las menciones a WS05/WS12, WS34/37 y WS44/`G_SCION` nombran productores o pruebas futuras; los gates pendientes son intencionales y la aceptación del agregado está definida por sus hijos, sin obligar a inventar resultado, repo o criterio.

**DRY-RUN**
Nodo no ejecutable: no habría cambios ni pruebas propias de WS32. Un ejecutor futuro leería `dag.yaml`, contratos WS05/WS12 y salidas hijas. Orden: WS05 y WS12 como prerrequisitos; WS32.1 (consume contrato WS12; produce IDs de intento y registro intent/no confirmado) y WS32.2 (consume registro y contrato; produce manifiesto/RunDoc/cierre idempotentes con mismo id, hash de sesión y evidencia); WS32.2 depende además de WS32.1. WS32 cierra solo con aceptación de ambos. Validación conjunta: IDs distintos antes de dispatch, no etiquetar no confirmado como éxito/fallo Hub, idempotencia sin registros nuevos y coincidencia de id/hash/evidencia. Sin red, mocks ni eventos fingidos. Errores/gates: `G_SCION` o `G_WRITE_CONTRACT` no satisfechos, contrato WS12 ausente, artefacto/hash no declarado o divergencia → alto y hueco con dueño; no sustituto. `G_CLOSEOUT` ya satisfecho; no se finge.

**FUTURO**
WS05 inventaría identidad/API Scion; WS12 fija registro por intento, hash de sesión, actor y operaciones; WS44 produce `G_SCION`; un humano designa operador Scion al abordar el ramal E; WS34/37 prueban Hub real bajo `G_EXEC`. Un humano decide la autorización de promoción; WS32 no la otorga.
