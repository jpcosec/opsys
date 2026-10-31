REFORMULACION
Propósito: construir en graph_ui una vista de solo lectura que muestre la cadena tarea-intento-conversación-resultados-decisión y la trazabilidad de ejecución Scion en el workspace. Resultado: UI en `frontends/mindmap/views/workspace/execution/` con tests; cada mensaje/resultado bajo su intento, enlace a fuente y evidencia abierta en el lector, sin convertir `completed` en aprobado/cerrado. Repo dueño: graph_ui. Límites: solo lectura; depende de contratos/datos de WS33 y WS27 y de G_SCION/G_UI_READ; no autoriza promoción ni ejecución; no implementa dispatch/reply (WS36) ni sustituye contratos ausentes.

AMBIGUEDADES
1. Scope: «Lectura tarea-intento-conversación-resultados-decisión»; acceptance: «Cada mensaje y resultado se muestra bajo su intento; cada uno enlaza a su fuente; la evidencia abre en el lector.» La aceptación no cubre tarea, conversación ni decisión, aunque el scope las incluye. Obligaría a inventar si deben mostrarse, con qué jerarquía y cómo se comprueban.
2. «Cada mensaje y resultado se muestra bajo su intento» presupone que todo mensaje/resultado tiene intento; no define qué hacer con mensajes no ligados a un intento. Obligaría a inventar su agrupación, visibilidad u omisión.
3. «la evidencia abre en el lector» no identifica qué lector ni el contrato de apertura. Obligaría a inventar el destino y la integración.

DRY-RUN
Lecturas previstas: `task-ws35.md`, nodos WS35/WS33/WS27, gates y fuentes de alcance/decisiones; ninguna ejecutada. Cambios previstos: archivos UI y tests bajo el output_scope, ninguno fuera. Dependencias: WS33 (referencias y decisión), WS27 (diff/evidencia), G_SCION (API pública Scion vía WS44), G_UI_READ (aceptación graph_ui vía WS11). Validaciones futuras: gates resueltos; pruebas de mensajes/resultados agrupados y enlazados; evidencia abre en lector; `completed` no aprobado; WS36 podrá consumir WS35.

FUTURO
WS44 produce el probe G_SCION; WS11 acepta el delta G_UI_READ; WS33/33.1/33.2 y WS27.1/27.2 producen datos y evidencia; WS12 define el contrato de escritura para WS36; el TaskDoc de promoción fija archivos, textos y pruebas; un humano autoriza la promoción y las decisiones Pxx. WS36 consume esta vista para intervención.
