REFORMULACION
Propósito: versionar en `graph_ui` un generador reproducible del corpus Taller para validaciones posteriores. Resultado: un comando que crea/recrea dos repos temporales con desk, stores, documentos, commits git reales, instrucciones/entrada mínima y manifiesto JSON; además, un tercer repo sin desk y enlaces entre desks. Repo dueño: `graph_ui`; alcance de salida en `tests/fixtures/workspace_documental/`, script de seed y `tests/`. Límites: no tocar desk real, no usar servidor fake, usar contrato WS11 y CLI reales de deskops/sldb verificados en WS02/WS03; WS17 solo aporta plantillas opcionales; no implementa validación humana.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas: guía de revisión, brief, alcance, decisiones, cobertura, nodo WS40 y contratos vecinos WS11/WS08/WS16/WS17/WS41; no se revisan esos vecinos. Cambios previstos: añadir generador versionado, script de seed, fixtures y pruebas; al ejecutarse en el futuro, creará repos temporales aislados, stores/documentos, commits y manifiesto, sin tocar desks reales. Dependencias: WS11 aporta contrato de navegación/identidad; WS08 precisa flujos; WS02/WS03 quedan como verificación transitiva de CLI; G_UI_READ está pendiente y es per-delta. WS17 no es dependencia: sus plantillas son parámetro opcional posterior. Validaciones futuras: comando reproducible, aislamiento, commits reales, manifiesto JSON, entrada mínima/README y consumo por WS16/30/41. No se ejecuta nada.

FUTURO
WS17 escribirá plantillas authored y regenerará el corpus con ellas; WS16 y WS30 consumirán el manifiesto para validación humana; WS41 usará el segundo desk para lectura entre desks; P01/receptor de `graph_ui` decidirá el recibo `G_UI_READ` por delta al promover WS40.
