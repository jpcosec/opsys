REFORMULACION
- Propósito: agrupar WS32.1/WS32.2 para refinar el candidato Scion: intento ≠ slug, dispatch `intent`/`confirmed` separado, manifiesto/RunDoc/cierre consistentes e idempotentes, sin segundo pipeline.
- Resultado: agregado no ejecutable; sus salidas son las de WS32.1 y WS32.2.
- Repo dueño: `deskops` (`deskops:repository_root/`).
- Límites: sin dispatch/reply de red, sin mocks ni eventos Hub inventados, sin tablas internas; los estados Hub reales se prueban en WS34/37 bajo G_EXEC. Depende de WS05, WS12, WS32.1/2; gates G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT.

AMBIGUEDADES
Ninguna. El nodo es `aggregate` y su aceptación es explícita: «se cumple cuando todos sus hijos cumplen su aceptación». El detalle ejecutable queda en WS32.1/2 y en los contratos de WS05/WS12.

DRY-RUN
- Lecturas: guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS32, gates y contratos de borde necesarios. Nada ejecutado.
- Cambios previstos: ninguno; es revisión.
- Dependencias: WS05 (inventario), WS12 (contrato), WS32.1/2 (hijos); gates citados.
- Validaciones futuras: cierre por aceptación de ambos hijos; comprobar ausencia de red/mocks y consistencia de contratos; G_SCION vía WS44; G_WRITE_CONTRACT por delta vía WS12.

FUTURO
WS05 entrega el inventario Scion; WS12 fija el contrato y ubicación del registro por intento; WS32.1/2 implementan y aceptan su parte local; WS34/37 prueban Hub real bajo G_EXEC; WS44 resuelve G_SCION. La promoción sigue `not_authorized` hasta decisión humana o WS06.
