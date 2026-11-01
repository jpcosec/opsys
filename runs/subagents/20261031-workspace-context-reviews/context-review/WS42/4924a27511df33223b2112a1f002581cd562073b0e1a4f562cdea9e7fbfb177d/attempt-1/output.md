## REFORMULACION
**Propósito:** convertir WS42 en un encargo ejecutable que integre en la UI de conocimiento las operaciones existentes de atoms split/merge, proto typing y la inspección de materializaciones, con confirmación humana que muestre origen y efecto.

**Resultado:** vista/operaciones en `frontends/mindmap/views/workspace/knowledge/`, usando solo la whitelist de endpoints de WS12 y pruebas en `tests/`; una capability ausente se declara no disponible, sin simularse.

**Repo dueño:** `graph_ui`. WS42 es candidato, sin promoción ni ejecución autorizada.

**Límites:** no crear destinos arbitrarios ni renderer propio para materializaciones; validarlas por API pública SLDB contra `MaterializationContractDoc`; el desarrollo puede avanzar sin acta de lectura, pero el uso de mutaciones en UI requiere `G_HUMAN_READ`. Aceptación final cubierta por WS30.

## AMBIGUEDADES
1. «modelo MaterializationContractDoc de deskops/models/materialization.py registrado en el store temporal real seleccionado por TaskDoc (o manifiesto Taller WS40), versión/commit registrados». No se dice quién registra ese modelo en el store ni de qué artefacto se registran «versión/commit» (modelo, store o materialización), ni dónde. El ejecutor tendría que inventar el actor y el registro.

2. «no se generan destinos arbitrarios» frente a la aceptación «sin crear destinos». La primera frase admite implícitamente destinos no arbitrarios; la segunda los prohíbe todos. El ejecutor debería decidir si existe algún caso permitido de creación de destino.

## DRY-RUN
**Lecturas previstas:** nodo WS42; contrato/whitelist WS12; inventarios WS02/WS03 referidos; vista y registro de WS24; conflicto de edición WS19; manifiesto/corpus WS40; gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT por delta; TaskDoc de promoción.

**Cambios previstos:** archivos de la vista de conocimiento y pruebas; invocación de contratos reales, confirmación previa con origen/efecto, inspección/validación de materializaciones y declaración de no disponibilidad.

**Dependencias:** WS12 debe publicar operaciones y huecos; WS19 y WS24 deben estar integrados; WS40/TaskDoc deben aportar store temporal; WS30 valida UF03.

**Validaciones futuras:** pruebas con store temporal real o corpus WS40; split/merge/tipado con persistencia, referencias y conflicto; materialización inválida mostrada como tal; aceptación humana en WS30.

## FUTURO
WS12 produce el contrato por operación y registra huecos; el receptor P01 emite actas por delta; WS16 satisface G_HUMAN_READ; WS30 ejecuta la validación humana; TaskDoc fija archivos, pruebas y textos; la promoción de WS42 requiere autorización separada.
