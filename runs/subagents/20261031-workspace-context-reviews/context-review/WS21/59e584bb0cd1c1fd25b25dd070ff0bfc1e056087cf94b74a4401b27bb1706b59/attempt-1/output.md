REFORMULACION
Propósito: integrar en el workspace una vista de fuente/renderizado que respete `source_mode`, la revisión esperada y un buffer sucio. Resultado: delta en `frontends/mindmap/views/workspace/` más pruebas, con alternancia fuente/render, conservación del buffer ante cambios sin guardar y guardado autorizado; la composición, si WS12 la admite, escribe solo en el documento dueño. Repo dueño: graph_ui. Límites: solo la variante elegida por P04 —hoy `editable`—; sin promoción con `pending`; no implementa otros repos ni sustituye contratos; en `editable` exige WS20/G_SOURCE y roundtrip/conflicto; el guardado por campos exige G_PAYLOAD_PRECONDITION en ambas variantes; no duplica en paralelo el ticket de edición; la fuente read-only no habilita guardado fuente.

AMBIGUEDADES
Ninguna. La variante está resuelta por P04 (`source_mode: editable`); WS20 y WS45 son productores nombrados de G_SOURCE y G_PAYLOAD_PRECONDITION; WS12 define la precondición y el soporte de composición; el comportamiento sin confirmación está fijado —conservar el buffer— y el mecanismo concreto de confirmación corresponde al TaskDoc.

DRY-RUN
Un ejecutor futuro leería el nodo y `task-ws21.md`, la salida aceptada de WS19, el contrato WS12 transitivo, G_SOURCE/WS20 y G_PAYLOAD_PRECONDITION/WS45. Cambiaría `views/workspace/` para añadir alternancia fuente/render sobre el mismo origen, estado de buffer sucio conservado, integración del guardado fuente autorizado y guarda de composición; añadiría pruebas en `tests/`. Consumiría WS19 y los gates citados. Si falta contrato, API o gate, se detendría, registraría el hueco con repo dueño y no crearía sustituto; un 409 de conflicto se mostraría sin descartar el buffer. Validaría roundtrip, conflicto, campos protegidos, conservación del buffer y ausencia de guardado fuente cuando corresponda; WS30 haría la validación humana.

FUTURO
WS30 valida el recorrido manual; WS45 produce G_PAYLOAD_PRECONDITION; WS20 produce G_SOURCE; WS12 fija contrato/efectos; el receptor P01 emite el acta por delta de G_UI_WRITE. La promoción y el TaskDoc concretan archivos, textos y escenarios.
