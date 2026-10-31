## REFORMULACION

**Propósito:** integrar en la UI de conocimiento las operaciones existentes de atoms split/merge y proto typing, con confirmación humana que muestre origen y efecto. **Resultado:** escenarios UF03 dividir/reunir/tipar con persistencia, referencias y conflictos reales; materializaciones existentes inspeccionadas/validadas sin crear destinos. **Repo:** graph_ui, en `frontends/mindmap/views/workspace/knowledge/`, endpoints solo whitelist WS12 y `tests/`. **Límites:** mutaciones UI solo tras G_HUMAN_READ; capabilities no soportadas se declaran no disponibles; no se simulan ni se inventan destinos.

## AMBIGUEDADES

1. «Invocar contratos reales de atoms split/merge y proto typing **cuando disponibles**»: no nombra quién produce esos contratos/API ni qué hacer si faltan. Aunque la aceptación ordena declarar no disponible, el ejecutor tendría que inventar el productor o decidir si WS12 basta.
2. «materializaciones existentes se inspeccionan y validan contra el **modelo SLDB registrado en el store de la tarea**» y «una materialización que no valida»: no se identifica qué store/versión ni la regla de validación aplicable; obligaría a inventar la fuente normativa o el criterio de validez.

## DRY-RUN

**Lecturas (sin ejecutar):** guía, brief, alcance, decisiones, cobertura, nodo WS42, bloques edge WS19/WS24/WS12/WS30 y gates.
**Cambios previstos:** implementación en knowledge/ de graph_ui, llamadas a endpoints whitelist WS12 y pruebas aisladas; sin generar materializaciones.
**Dependencias:** WS19 (agregado), WS24 y WS12; gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT, estos dos por delta.
**Validaciones futuras:** UF03 con persistencia/referencias/conflictos; materialización inválida mostrada y no operable; capability no soportada etiquetada no disponible; cobertura manual en WS30.

## FUTURO

WS12 debe publicar whitelist y contrato técnico por operación; WS24 aporta vista/modelo de grafo; WS30 ejecuta la validación manual; WS16 produce el acta G_HUMAN_READ; el responsable P01 emite recibos por delta de G_UI_WRITE/G_WRITE_CONTRACT. El TaskDoc de promoción fijará archivos, pruebas y textos, aún no autorizado.
