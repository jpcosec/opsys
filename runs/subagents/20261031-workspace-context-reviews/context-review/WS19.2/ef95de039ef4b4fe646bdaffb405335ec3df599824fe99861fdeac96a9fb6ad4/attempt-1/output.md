REFORMULACION

Encargo: implementar en graph_ui el alta y baja de relaciones permitidas por contrato dentro del workspace, sin crear semántica de relaciones en el componente. Resultado: módulo bajo `frontends/mindmap/views/workspace/relations/`, llamadas a endpoints autorizados por WS12 y pruebas; alta/baja persistentes y confirmadas tras recargar, con rechazo visible de relación no permitida, revisión obsoleta o tipo/relación protegida. Límites: usar API real y la precondición que fije WS12; la baja de RelationDoc solo se habilita si el canal borra de verdad documento e índice; si el modo solo destrackea, se declara no habilitada. No duplicar `editing` ni ejecutar en paralelo. Repo dueño: graph_ui.

AMBIGUEDADES

1. «por el canal público de sldb (/save delete con expected)» frente a «la precondición de escritura que fije WS12». WS12 declara que elegirá la representación —`expected` por valor, token publicado u otra—; si elige otra, el ejecutor debe inventar si usa `expected` literalmente o la representación contractual, y qué aceptación prevalece.

DRY-RUN

Leería `dag.yaml`, el contrato WS12, los resultados de WS47 y WS48 y la base workspace ya integrada. Cambios previstos: módulo de relaciones, llamadas al canal autorizado, pruebas; sin tocar semántica de relaciones ni reimplementar editores. Consumiría de WS12 whitelist, precondición y adapter; de WS47 la guarda de contenido; de WS48 la admisión de escritura. Gates: G_WRITE_CONTRACT y G_UI_WRITE por delta; G_PAYLOAD_PRECONDITION vía WS45; G_HUMAN_READ solo para uso real de mutaciones. Si falta contrato o endpoint, se detiene y registra el hueco con repo dueño, sin sustituto. Validaría con store temporal: alta y baja persisten tras recarga; obsoleto da error visible —409 si aplica—; relación no permitida y protegidos se rechazan; la baja de RelationDoc borra documento e índice o queda deshabilitada y declarada. WS19.1 y WS19.2 comparten `views/workspace/`; se integran sin duplicarse, sin orden entre hermanos.

FUTURO

WS19 cierra cuando ambos hijos cumplen. WS16 produce G_HUMAN_READ; el receptor P01 emite G_UI_WRITE por delta; WS12, G_WRITE_CONTRACT; WS45, G_PAYLOAD_PRECONDITION. La promoción y su TaskDoc fijan archivos, textos y escenarios concretos.
