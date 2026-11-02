REFORMULACION  
WS25.2 debe implementar en graph_ui la captura interna con destino explícito —candidato de drawer o protoátomo— mediante operaciones autorizadas por WS12, sin crear tarea implícita. Resultado: cada captura persiste tras recargar en el destino elegido, con origen tipado (ruta o mensaje), colisión no sobrescrita en silencio y permisos del contrato aplicados; ambos destinos se prueban por separado. Repo: `graph_ui`, en `frontends/mindmap/views/workspace/capture/`, endpoints autorizados y `tests/`. Límites: depende de WS12, WS46 y WS48; no crea API ni modelo por reflejo; no habilita mutaciones sin `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT`; no se cumple declarando la captura no disponible.

AMBIGUEDADES  
1. «con representación fijada por el contrato WS12»: WS12 dice «Es una propuesta: ningún test comprueba que se conserve». Obliga a inventar si el origen va en `references` o `provenance`, y su formato exacto.  
2. «endpoints autorizados por el contrato WS12»: WS12 registra la captura a drawer como HUE X02/HO-11 y no fija endpoint; obliga a inventar la ruta o asumir `/docs/create` antes de la prueba de WS46.  
3. «Permisos del contrato aplicados»: WS12 da whitelist y campos protegidos, pero no una matriz específica de captura; obliga a inventar qué se permite u omite por destino.  
4. «desarrollo y pruebas aisladas de API pueden avanzar» frente a `requires: G_HUMAN_READ`: no aclara si ese gate bloquea solo el uso real o también el cierre/entrega del nodo; obliga a decidir el criterio de aceptación.

DRY-RUN  
Un ejecutor futuro leería WS12 (secciones 3, 4.2, 5.9, 7 y 10.2), la prueba/inventario de WS46 y el módulo de admisión de WS48. Crearía la vista/controlador de captura con selector de destino, captura de origen ruta/mensaje, llamada a la composición pública probada por WS46 y comprobación previa en WS48; añadiría pruebas separadas para drawer y protoátomo. No modificaría deskops ni sldb salvo que WS46 ya haya completado allí la conducta faltante. Errores previstos: WS46 sin prueba por destino o WS48 ausente → bloqueo; endpoint no autorizado → no escribir; colisión → rechazo sin sobrescribir. Validaría en store temporal: persistencia tras recarga, origen visible, ausencia de tarea activa (Board y `list tasks`), colisión controlada y rechazo/handoff cuando WS48 no admite. Consumiría `G_WRITE_CONTRACT`, `G_UI_WRITE` y `G_HUMAN_READ`; sin ellos no habilitaría uso real.

FUTURO  
WS46 debe producir y probar la capacidad de captura con origen por destino; WS48 debe entregar la admisión común; root/P01 deben revisar WS12 y registrar el acta `G_UI_WRITE`; una persona debe autorizar la promoción y el uso de mutaciones en la UI.
