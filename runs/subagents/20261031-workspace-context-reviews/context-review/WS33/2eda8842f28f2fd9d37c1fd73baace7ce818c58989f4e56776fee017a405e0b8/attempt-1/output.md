REFORMULACION
Propósito: agregar la vinculación documental de mensajes, resultados y decisión humana al intento, con deduplicación y procedencia, sin editor UI. Resultado: agregado de salidas de WS33.1 y WS33.2. Repo dueño: `deskops`. Límites: backend documental, independiente de editor UI; no duplicar pipeline Scion (`never_parallel_duplicate`). Depende de WS32, WS11 y sus hijos; requiere G_SCION. Al ser `aggregate`, no se ejecuta: cierra cuando cierran sus hijos.

AMBIGUEDADES
ninguna.

Las referencias a Hub/proyecto/conversación/mensaje, al identificador de la fuente y a la decisión humana quedan delegadas a WS33.1/WS33.2 y al contrato G_SCION producido por WS44; no obligan al ejecutor de este agregado a inventar resultado, repo ni aceptación.

DRY-RUN
Lecturas: `dag.yaml` (WS33 y contratos vecinos como contexto), guía, brief, alcance, decisiones, cobertura y reconciliación. Cambios previstos: ninguno; no se promueve, no se escribe código ni se tocan tablas Scion. Dependencias: WS32, WS11, WS33.1 y WS33.2; G_SCION depende de WS44 y del operador designado en WS07. Validaciones futuras: aceptación de ambos hijos, probe G_SCION, preflight/TaskDoc de promoción y revisión de solapamiento con `scion`.

FUTURO
WS33.1 y WS33.2 producen adaptador, modelos/reportes y pruebas; WS44 resuelve G_SCION; WS07 designa el operador Scion; el TaskDoc de promoción fija archivos, escenarios y textos; WS34 consume WS33. Las propuestas Pxx no se dan por aprobadas.
