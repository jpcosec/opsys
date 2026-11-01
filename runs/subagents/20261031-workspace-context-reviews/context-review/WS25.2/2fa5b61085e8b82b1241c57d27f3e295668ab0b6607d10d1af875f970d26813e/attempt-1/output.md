REFORMULACION

WS25.2 encarga en `graph_ui` una captura interna de UI con destino elegido explícitamente —candidato de drawer o protoátomo—, sin exigir tarea y usando solo operaciones permitidas por WS12. El resultado es una captura que persiste tras recargar, conserva un origen tipado —ruta o mensaje—, aplica permisos y controla colisiones; cada destino se prueba por separado. Límites: no crear API ni modelo por reflejo; si WS12 no define canal, representación o permiso, detenerse y registrar el hueco. `G_HUMAN_READ` solo habilita mutaciones en UI; el desarrollo y las pruebas aisladas de API pueden avanzar. No hay commits ni closeout.

AMBIGUEDADES

ninguna.

DRY-RUN

Hipotéticamente, un ejecutor leería `task_file`, el contrato WS12, el código y tests existentes de `capture/`, y el estado de los gates. Cambiaría solo `frontends/mindmap/views/workspace/capture/` y `tests/`: selector de destino, captura de origen ruta/mensaje, llamada al canal autorizado, visualización tras recarga y control de colisión; no tocaría API ni modelo. Consumiría WS12 para endpoints, permisos, representación de origen y colisión; `G_HUMAN_READ` antes de habilitar uso de mutaciones UI; `G_UI_WRITE` y `G_WRITE_CONTRACT` por delta. Si falta canal o whitelist, pararía y registraría el hueco. Validaría por destino: persistencia tras recarga, origen mostrado, ausencia de tarea implícita, permisos aplicados y colisión no silenciosa, con store temporal o corpus WS40. Errores esperados: endpoint no autorizado, origen no soportado, colisión y gate ausente.

FUTURO

WS12 comparará y fijará el canal de drawer/protoátomo, la representación del origen, permisos y control de colisión. WS16 producirá el acta de `G_HUMAN_READ`; P01 emitirá el recibo `G_UI_WRITE` por delta. WS25.1 aportará mensaje/ack y el agregado WS25 validará conjuntamente ambos hijos. WS40 aportará el corpus para validación humana; la promoción fijará archivos, pills y evidencia.
