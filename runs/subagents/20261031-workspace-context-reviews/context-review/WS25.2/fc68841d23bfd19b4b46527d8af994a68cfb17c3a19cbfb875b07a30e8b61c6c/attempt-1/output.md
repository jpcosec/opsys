REFORMULACION  
Propósito: encargo de implementación para captura interna en UI, con destino elegido explícitamente por la persona usuaria: candidato de drawer o protoátomo, usando operaciones permitidas por WS12 y sin exigir tarea. Resultado: una captura persiste tras recargar en el destino elegido, con origen tipado —ruta o mensaje— registrado y mostrado, sin tarea implícita y con permisos del contrato aplicados; cada destino se prueba por separado. Repo: `graph_ui`, alcance `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`. Límites: no ejecutar; depende de WS12; requiere G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT; no inventar endpoints ni tareas; promoción aún no autorizada.

AMBIGUEDADES  
ninguna.

DRY-RUN  
Lecturas: nodo WS25.2, aristas WS12/WS25, gates, guía, brief, alcance, decisiones y cobertura.  
Cambios previstos: UI de captura en `graph_ui` y pruebas de persistencia por destino, origen ruta/mensaje, ausencia de tarea implícita y permisos. No se modifican vecinos ni contratos.  
Dependencias: contrato WS12; G_HUMAN_READ producido por WS16; G_UI_WRITE por recibo per-delta del receptor P01; G_WRITE_CONTRACT por WS12. Si falta contrato, API o permiso, detenerse y registrar hueco con repo dueño, sin sustituto.  
Validaciones futuras: recarga real, destino elegido, origen tipado visible, no creación de tarea, permisos aplicados, prueba separada drawer/protoátomo; acta humana antes de habilitar mutaciones en UI. Nada de esto se ejecuta aquí.

FUTURO  
WS12 publica el contrato de operaciones; WS16 produce el acta de lectura; el receptor P01 emite recibos G_UI_WRITE por delta; WS12 verifica G_WRITE_CONTRACT por delta; el TaskDoc de promoción fija archivos, escenarios y textos; una persona decide autorización de promoción y aceptación.
