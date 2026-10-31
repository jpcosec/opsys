REFORMULACION: Propósito: versionar en graph_ui un generador reproducible del corpus Taller. Resultado: un comando crea/recrea un entorno aislado con dos repos/desks temporales y un tercer repo sin desk, documentos con Markdown no modelado, Code local y referencia rota, commits git reales, instrucciones/README, entrada mínima y manifiesto JSON. Repo dueño: graph_ui. Límites: usa contrato WS11 y CLI reales deskops/sldb verificados, sin servidor fake; nunca toca desk real; plantillas WS17 son opcionales y WS40 cierra sin ellas.

AMBIGUEDADES: ninguna.

DRY-RUN: Lecturas: dag.yaml (WS40, WS11, WS08, gates), guía de revisión, brief, alcance, decisiones y cobertura. Cambios previstos: script de seed, tests/fixtures, repos temporales y manifiesto dentro de output_scope; sin ejecutar. Dependencias: WS11/WS08 directas; WS02/WS03 transitivas vía WS11; G_UI_READ pendiente; WS17 no bloquea. Validaciones futuras: reproducibilidad del comando, aislamiento, commits reales, manifiesto con roots/stores/commits/documentos, no escritura en desk real y consumo por WS16/30.

FUTURO: WS11 produce/acepta el contrato y G_UI_READ; WS17 aporta plantillas authored y regenera; WS16/30 consumen el corpus; el humano decide la promoción (no autorizada) y la aceptación del gate.
