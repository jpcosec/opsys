## REFORMULACION
WS19.1 encarga implementar en graph_ui la edición de campos del workspace con conflicto visible: reutilizar editores y API, aplicar la precondición de escritura de payload que fija WS12 y verifica WS45, conservar el texto local ante rechazo y no editar campos protegidos por workflow. El resultado es un delta sobre el workspace a1b2b22 con guardado/recarga comprobable y conflicto mostrado. Límites: consumir endpoints del contrato WS12 sin modificarlo; mutación solo en desk en modo manual exclusivo; otros modos read-only; pruebas en `tests/`.

## AMBIGUEDADES
1. «Mutación restringida a desk en modo manual exclusivo (P03); otros modos read-only hasta contrato.» Obliga a inventar qué es «modo manual exclusivo», cómo se detecta y qué «contrato» habilita otros modos; sin ello el ejecutor podría habilitar escritura donde no corresponde o bloquearla de más.

## DRY-RUN
Un ejecutor futuro leería el contrato WS12 (`contratos/operaciones.md`) para obtener operaciones, campos editables, campos protegidos, representación de la precondición y modo permitido; la evidencia de WS45/G_PAYLOAD_PRECONDITION; y el código actual de `frontends/mindmap/views/workspace/`, guardado y editores existentes.

Cambios previstos: en `frontends/mindmap/views/workspace/fields/`, conectar el editor de campos a los endpoints del contrato WS12; manejar el rechazo por precondición conservando el buffer local y mostrando conflicto; excluir o deshabilitar campos protegidos; aplicar la restricción de modo; añadir pruebas en `tests/`.

Dependencias y gates: WS12 aporta contrato y whitelist; G_PAYLOAD_PRECONDITION exige WS45; G_HUMAN_READ solo habilita el uso de mutaciones en UI; G_UI_WRITE y G_WRITE_CONTRACT se consumen por delta. Si falta contrato, API, evidencia o gate, el ejecutor se detiene, registra el hueco con repo dueño y no crea sustituto. Validación esperada: store temporal real, guardar/recargar, escritura obsoleta rechazada sin pérdida de texto local, conflicto visible, campos protegidos no editables y otros modos en read-only.

## FUTURO
WS12 produce el contrato, la whitelist y la representación de la precondición; WS45 produce la evidencia de G_PAYLOAD_PRECONDITION; el receptor P01 emite el acta de G_UI_WRITE por delta; WS16 produce G_HUMAN_READ; el TaskDoc de promoción fija archivos, pruebas y textos exactos.
