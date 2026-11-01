REFORMULACION

Propósito: cerrar el contrato técnico de operaciones y escritura del workspace (WS12). Resultado: `contratos/operaciones.md` en deskops con whitelist por operación/campo/canal/actor/revisión/Git/efectos y estado comprobado/faltante, elección justificada de representación de precondición de payload, comparación del canal de captura a drawer, captura a protoátomo, matriz de capacidades/efectos y huecos asignados. Límites: solo escribe contrato y enlaces en deskops; no ejecuta mutaciones ni crea actas interrepo, APIs, modelos o wrappers; no aprueba implementación ni dispatch Scion; P03 y `source_mode` no cambian.

AMBIGUEDADES

1. «esa sección del contrato WS12 la fija al preparar esos deltas, no WS34» / «su ausencia no impide cerrar el contrato núcleo». ¿WS12 debe incluir ya la sección de política/umbral de timeout o dejarla para una reapertura al preparar WS34.1/34.2? El actor que la fija tampoco se nombra; obliga a inventar momento y productor.

2. «La captura a protoátomo entra en la whitelist con su canal o con su hueco y dueño» y «si no existe, se registra hueco y dueño». No se nombra repo/actor dueño del hueco; obliga a inventarlo si el canal falta.

DRY-RUN

Nodo `planning`, no agregado; el ejecutor leería `dag.yaml` (WS12, gates, vecinos), `decisiones.md` P03–P06, `alcance.md`, brief/glosario, `contratos/navegacion.md` (WS11), `borradores/user-flows.md` (WS08) y auditorías WS02–04 citadas transitivamente. Cambios previstos: crear/editar `contratos/operaciones.md` con matriz whitelist, decisión de precondición, comparación drawer, protoátomo, huecos y matriz de efectos. Consumiría G_WRITE_POLICY ya `satisfied` (sin re-firmar); G_WRITE_CONTRACT queda `pending` `per_delta`, producido por WS12 y aceptado por receptor por delta; no trata G_UI_WRITE/G_SLDB_WRITE como aceptación conjunta. Errores: API/inventario ausente → registrar hueco con dueño, no sustituir; contrato WS11 ausente → detenerse. Validación esperada: revisión del documento contra `acceptance`, sin mutaciones ni actas.

FUTURO

Los recibos G_WRITE_CONTRACT/G_UI_WRITE/G_SLDB_WRITE por delta los produce el receptor P01 en el repo dueño al preparar cada delta. WS45 verifica la precondición; WS20 conserva raw-source; WS34.1/34.2 fijan su timeout al prepararse. Consumidores WS19.x, WS25.x, WS26.x, WS28, WS32.x, WS33.x, WS34.x, WS36, WS39, WS42, WS43, WS45 usan solo su recibo. La aceptación por delta la decide P01.
