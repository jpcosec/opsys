REFORMULACION
Propósito: agregar la integración de edición de campos y relaciones con revisión/conflicto, como delta sobre el ticket draft de edición. Resultado: nodo agregado no ejecutable; se cumple cuando WS19.1 y WS19.2 cumplen su aceptación, y sus dependientes siguen dependiendo de WS19. Repo dueño: `graph_ui` (`output_base: graph_ui:repository_root/`), consumiendo el contrato WS12 sin cambiarlo. Límites: no crear semántica de relaciones en el componente; campos workflow-protected no editables por este canal; usar API real y before-image; gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT; promoción no autorizada.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: bloque WS19, vecinos WS12/WS16, hijos WS19.1/WS19.2 y fuentes de alcance/decisiones/reconciliación; sin ejecutar nada.
Cambios previstos: ninguno; esta revisión no modifica archivos.
Dependencias: WS12 aporta whitelist/capabilities y G_WRITE_CONTRACT/G_UI_WRITE; WS16 aporta G_HUMAN_READ; ambos hijos cubren campos y relaciones. La dependencia del agregado respecto de sus hijos es coherente con “no ejecutable”.
Validaciones futuras: actas de gates, contrato WS12, aceptación de ambos hijos, guardar/recargar, conflicto con texto local conservado, alta/baja de relaciones y rechazo por revisión obsoleta.

FUTURO
WS12 produce el contrato técnico y la aceptación del delta de escritura; WS16 produce el acta humana de lectura; WS07/WS12 resuelven P03–P06 y G_WRITE_POLICY; WS19.1/WS19.2 implementan y evidencian; WS30 verificará edición; WS04 comprueba Board y ticket receptor antes de promover. La decisión de promover o aprobar gates corresponde a un humano.
