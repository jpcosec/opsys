REFORMULACION
Propósito: integrar en graph_ui las operaciones de conocimiento ya existentes —split/merge de atoms, proto typing y validación de materializaciones— sobre el workspace documental, invocando contratos reales y no simulaciones.
Resultado: una superficie en `frontends/mindmap/views/workspace/knowledge/` que permite dividir, reunir y tipar con persistencia, referencias y conflictos reales, mostrando origen y efecto y pidiendo confirmación antes de ejecutar; las materializaciones existentes se inspeccionan y validan contra `MaterializationContractDoc` mediante API pública SLDB; lo no soportado se declara no disponible y bloquea solo su escenario UF03.
Repo: graph_ui (`graph_ui:repository_root/`). Depende de WS19, WS24 y WS12. Límites: endpoints solo whitelist WS12; no crear destinos de materialización ni renderer propio de validación; no simular capacidades; si falta contrato/API, WS12 registra hueco y la UI no queda disponible; mutaciones UI sujetas a G_HUMAN_READ, G_WRITE_CONTRACT y G_UI_WRITE por delta; aceptación final por WS30.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas: contrato WS12 (whitelist, operaciones, precondición, efectos), inventario WS02/APIs WS03 ya concretados por WS12, modelo `deskops/models/materialization.py`, vista de grafo/documento de WS24 y edición con conflicto de WS19, manifiesto Taller WS40/TaskDoc para el store temporal.
Cambios previstos: componentes en `.../knowledge/` que invocan endpoints whitelisted; confirmación UI con origen/efecto; inspección/validación de materializaciones vía API SLDB; tests de split/merge/typing, persistencia, referencias, conflictos y materialización inválida.
Dependencias/gates: consumir G_WRITE_CONTRACT por delta antes de invocar cada operación; G_HUMAN_READ antes de habilitar mutaciones UI; G_UI_WRITE como recibo del delta concreto; desarrollo/pruebas aisladas de API pueden avanzar sin acta de lectura. WS30 valida después con protocolo humano.
Errores: contrato/API ausente => detener, registrar productor/hueco, marcar no disponible; materialización que no valida => mostrarla inválida y no ofrecerla; fallo de persistencia/conflicto => no simular éxito, declarar límite.
Validación esperada: UF03 dividir/reunir/tipar con persistencia, referencias y conflictos reales; materializaciones existentes validadas contra el modelo registrado; etiquetas de disponibilidad por capability; acta WS30.

FUTURO
WS12 produce whitelist/contrato por delta; WS16 produce G_HUMAN_READ; el receptor P01 decide G_UI_WRITE por delta; WS40/TaskDoc fija store/manifiesto; WS30 ejecuta la validación humana; WS19 y WS24 entregan edición y vista de grafo; si falta API, WS12 registra hueco y productor.
