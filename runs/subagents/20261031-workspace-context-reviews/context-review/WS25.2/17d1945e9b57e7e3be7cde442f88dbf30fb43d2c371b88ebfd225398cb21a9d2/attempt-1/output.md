REFORMULACION
Propósito: implementar en graph_ui la captura interna cuyo destino elige explícitamente la persona —candidato de drawer o protoátomo—, usando solo operaciones permitidas por WS12 y sin crear tarea.
Resultado: capturas persistidas tras recargar, con origen tipado (ruta o mensaje), permisos del contrato aplicados y sin tarea implícita; cada destino se prueba por separado.
Repo: graph_ui. Límites: `frontends/mindmap/views/workspace/capture/` y `tests/`; endpoints solo los autorizados por WS12; no promoción ni ejecución; depende de WS12/WS16 y de G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.

AMBIGUEDADES
1. «ambos tipos se registran y se muestran tras recargar». No queda claro si “ambos tipos” son los destinos —drawer/protoátomo— o los orígenes —ruta/mensaje—. Obligaría a inventar qué matriz debe registrarse y mostrarse, aunque el alcance exige probar cada destino por separado.

DRY-RUN
Lecturas: nodo WS25.2, guía, brief, alcance, decisiones, cobertura; contratos vecinos WS12, WS16 y agregado WS25 solo como contexto. Cambios previstos: módulo de captura y pruebas en graph_ui, consumiendo endpoints de WS12; nada ejecutado. Dependencias: WS12 (contrato, capabilities y representación del origen), WS16 (gate humano de lectura); gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT. Validaciones futuras: persistencia tras recarga, origen tipado visible, ausencia de tarea implícita, permisos aplicados y prueba separada de drawer/protoátomo; aceptación humana y delta de escritura según WS12/WS16.

FUTURO
WS12 debe cerrar whitelist, canal, efectos y representación del origen, y resolver G_UI_WRITE/G_WRITE_CONTRACT; WS16 aporta G_HUMAN_READ. El TaskDoc de promoción fijará archivos, escenarios y textos; una persona autoriza la promoción. Nada de esto se ejecuta aquí.
