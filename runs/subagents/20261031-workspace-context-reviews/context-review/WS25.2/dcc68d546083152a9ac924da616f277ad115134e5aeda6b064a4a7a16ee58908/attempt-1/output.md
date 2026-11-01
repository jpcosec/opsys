## REFORMULACION

**Propósito:** revisar WS25.2 como encargo de planificación: captura interna con destino explícito —candidato de drawer o protoátomo— usando solo operaciones autorizadas por WS12.  
**Resultado:** una captura persiste tras recargar en el destino elegido, con origen tipado —ruta o mensaje—, sin tarea implícita, permisos aplicados y colisión de candidato no sobrescrita en silencio.  
**Repo:** `graph_ui`; salida en `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`.  
**Límites:** no crear API ni modelo por reflejo; el canal de drawer está pendiente de WS12; G_HUMAN_READ habilita mutaciones en UI, no bloquea desarrollo ni pruebas aisladas de API.

## AMBIGUEDADES

Ninguna.

El contrato que falta —operaciones, canal de drawer y representación del origen— tiene productor nombrado, WS12, y el procedimiento ante ausencia está resuelto por las reglas comunes: detenerse y registrar el hueco. Los textos exactos, archivos y escenarios detallados quedan delegados al TaskDoc de promoción.

## DRY-RUN

**Lecturas previstas, sin ejecutar:** nodo WS25.2, contrato vecino WS12, gates G_HUMAN_READ/G_UI_WRITE/G_WRITE_CONTRACT, brief, alcance, decisiones y cobertura.  
**Cambios previstos:** implementar captura y pruebas solo dentro de `output_scope`; no definir endpoints ni modelos nuevos.  
**Dependencias:** contrato WS12 y sus operaciones por destino; G_HUMAN_READ para habilitar uso de mutaciones en UI; G_UI_WRITE por delta; G_WRITE_CONTRACT.  
**Validaciones futuras:** persistencia tras recarga por cada destino; origen ruta/mensaje registrado y mostrado; ausencia de tarea implícita; permisos del contrato; colisión no silenciosa; verificar que WS12 cubra también protoátomo.

## FUTURO

WS12 produce el contrato de operaciones y decide el canal permitido para drawer/protoátomo. WS16 produce el acta de G_HUMAN_READ. El receptor P01 produce el acta por delta de G_UI_WRITE. La promoción fija archivos, pills, evidencia y preflight. Cualquier contrato faltante se detiene y se registra con repo dueño; no se sustituye.
