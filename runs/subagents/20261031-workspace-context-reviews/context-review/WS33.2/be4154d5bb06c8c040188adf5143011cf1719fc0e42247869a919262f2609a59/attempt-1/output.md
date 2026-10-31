REFORMULACION
Propósito: registrar una decisión humana —aprobar o pedir corrección— sobre un intento Scion, con actor y referencia al intento y, por él, a su tarea.
Resultado: un registro de decisión con resultado explícito; la corrección exige su texto. No debe confundirse `completed` del agente con aprobación.
Repo dueño: `deskops`, con salidas en `runtime/`, modelos/reportes y `tests/`.
Límites: este nodo solo escribe la decisión; no escribe estados de testing/closeout ni tablas Scion. Promoción no autorizada.

AMBIGUEDADES
1. «Registrar la decisión humana (aprobar o pedir corrección) con actor»: no se nombra el canal ni quién produce la decisión (endpoint de deskops, CLI, payload de Scion u otro). Obliga a inventar interfaz, autorización y validación; `G_SCION` cubre el contrato de Scion, no la captura de la decisión.
2. «con actor»: no se define de dónde sale ni cómo se verifica la identidad del actor. Obliga a inventar si es cadena libre, identidad autenticada o referencia externa, y qué aceptación tendría.
3. «asociada al intento y, por él, a su tarea»: no se explicita quién garantiza el vínculo intento→tarea ni qué ocurre si un intento no resuelve tarea. WS33.1 vincula mensajes/resultados, no esa asociación.

DRY-RUN
Lecturas previstas: guía, `dag.yaml` (nodo y vecinos WS32, WS33.1, WS11, gate G_SCION), brief, alcance, decisiones, cobertura y reconciliación; después, el TaskDoc de promoción.
Cambios previstos: implementación del registro de decisión en `deskops`, modelos/reportes y pruebas, sin ejecutar.
Dependencias: WS32 (identidad/cierre de intento), WS33.1 (vínculo mensajes/resultados), WS11 (contrato de identidad) y G_SCION.
Validaciones futuras: decisión con actor, intento y resultado; corrección con texto obligatorio; `completed` nunca aprobado; ausencia de escritura de estados testing/closeout.

FUTURO
WS44 y el operador designado en WS07 deben probar G_SCION. WS32.1/WS32.2 fijan identidad de intento y cierre. El humano o WS12 deben resolver el canal y la identidad del actor. La promoción fijará archivos, escenarios y textos exactos.
