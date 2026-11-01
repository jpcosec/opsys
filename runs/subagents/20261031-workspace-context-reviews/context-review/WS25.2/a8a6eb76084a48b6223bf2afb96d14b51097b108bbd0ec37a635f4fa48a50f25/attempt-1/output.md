## REFORMULACION
**Propósito:** dotar a la UI de graph_ui de captura interna para que la persona elija explícitamente entre candidato de drawer o protoátomo, usando solo operaciones autorizadas por WS12 y sin exigir tarea.

**Resultado:** una captura persiste tras recargar en el destino elegido, conserva origen tipado y no crea tarea implícita; permisos y colisiones según contrato; cada destino se prueba por separado.

**Repo:** graph_ui; salida en `frontends/mindmap/views/workspace/capture/`, endpoints que autorice WS12 y `tests/`.

**Límites:** no crear API/modelo por reflejo; drawer y protoátomo deben estar en la whitelist WS12 o registrarse hueco/dueño; G_HUMAN_READ solo habilita uso de mutaciones en UI; promoción no autorizada.

## AMBIGUEDADES
1. «una captura persiste tras recargar en el destino elegido, con origen y sin tarea implícita» y «los orígenes ruta y mensaje se registran y se muestran tras recargar». La aceptación parece exigir origen para ambos destinos, pero el glosario define protoátomo solo por «título y contenido» y el scope liga «origen preservado» al candidato de drawer. El ejecutor tendría que inventar si protoátomo guarda y muestra origen, y si admite ambos tipos o solo el drawer.

## DRY-RUN
**Lecturas:** `dag.yaml` (WS25.2, WS12, gates), `contratos/operaciones.md` de WS12, `task-ws25-2.md`, código y tests existentes en graph_ui.

**Cambios previstos:** componentes de captura en `output_scope`, llamadas al canal autorizado para drawer y protoátomo, tests.

**Dependencias y gates:** entradas WS12 por operación; G_WRITE_CONTRACT por delta WS25.2 en `accepted_scope_nodes`; G_HUMAN_READ; G_UI_WRITE por acta delta. G_HUMAN_READ pendiente impide habilitar mutaciones en UI, no el desarrollo.

**Errores:** si WS12 no define canal, permisos o colisión para un destino, detenerse y registrar hueco con dueño; no sustituir API.

**Validación esperada:** store temporal real o corpus WS40; captura persiste tras recarga; origen ruta/mensaje visible; ninguna tarea creada; colisión de drawer no sobrescrita en silencio; ambos destinos probados por separado.

## FUTURO
WS12 publica contrato/whitelist y puede registrar hueco+dueño para protoátomo; WS16 produce acta G_HUMAN_READ; receptor P01 en graph_ui emite acta G_UI_WRITE por delta; TaskDoc fija archivos, textos y casos; WS25 cierra cuando WS25.1 y WS25.2 cumplan.
