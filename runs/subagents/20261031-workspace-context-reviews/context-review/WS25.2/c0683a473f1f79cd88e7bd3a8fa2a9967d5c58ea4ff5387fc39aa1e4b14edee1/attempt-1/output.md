## REFORMULACION
**Propósito:** encargo de implementación para captura interna con destino elegido explícitamente —candidato de drawer o protoátomo— usando solo operaciones permitidas por el contrato WS12, sin exigir tarea. **Resultado:** una captura persiste tras recargar en el destino elegido, con origen (ruta o mensaje), sin tarea implícita; permisos aplicados y colisión no sobrescrita en silencio. **Repo:** graph_ui, en `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`. **Límites:** no crear API o modelo por reflejo; no se asume wrapper Deskops ni composición; cada destino se prueba por separado; gates pendientes son intencionales; G_HUMAN_READ solo condiciona uso de mutaciones en UI, no desarrollo/pruebas aisladas de API.

## AMBIGUEDADES
1. «mediante operaciones permitidas por el contrato WS12» y «cada destino se prueba por separado». El contrato WS12 describe el canal de captura directa a drawer, pero no nombra operación, almacenamiento ni permisos para protoátomo. Obligaría a inventar ese canal para cumplir la persistencia del segundo destino.
2. «los orígenes ruta y mensaje se registran y se muestran tras recargar». WS25.1 integra mensaje/ack, pero WS25.2 no depende de él ni define de dónde obtiene la referencia del mensaje. Obligaría a inventar el suministro e identidad del mensaje o a duplicar intake.

## DRY-RUN
**Lecturas:** nodo WS25.2 y aristas WS12/WS25 en dag.yaml; guía; brief; alcance; decisiones; cobertura. **Cambios previstos:** módulo de captura en el output_scope, llamadas a endpoints autorizados por WS12 y pruebas por destino. **Dependencias:** contrato WS12 (canal drawer, permisos, colisión, origen); gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT por delta. **Validaciones futuras:** persistencia tras recarga para drawer y protoátomo; origen ruta/mensaje visible; no tarea implícita; permisos; colisión controlada; recibos per_delta de WS25.2; acta humana de lectura antes de habilitar mutaciones UI.

## FUTURO
WS12 publica la matriz de operaciones/canales y decide la composición para drawer; si el protoátomo no queda cubierto, debe registrar productor explícito antes de WS25.2. La promoción fija archivos, escenarios y textos; el receptor P01 emite el acta per_delta de G_UI_WRITE, WS12 la evidencia de G_WRITE_CONTRACT y WS16 produce G_HUMAN_READ. La aceptación del delta corresponde al humano.
