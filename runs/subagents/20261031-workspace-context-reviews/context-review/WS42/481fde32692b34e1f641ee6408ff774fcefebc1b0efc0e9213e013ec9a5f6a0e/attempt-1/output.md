## REFORMULACION

**Propósito:** integrar en la UI de conocimiento de `graph_ui` las operaciones existentes de atoms split/merge y proto typing, con confirmación humana que muestre origen y efecto, e inspeccionar/validar materializaciones existentes.

**Resultado:** capacidades invocables según la whitelist de WS12, materializaciones válidas operables y las inválidas marcadas como no operables; sin simulación. UF03 queda cubierto y validado por WS30.

**Repo:** `graph_ui`; salidas en `frontends/mindmap/views/workspace/knowledge/`, endpoints limitados a WS12 y `tests/`.

**Límites:** no crear destinos de materialización, no usar renderer propio para validar, no inventar operaciones/APIs. Si faltan, WS12 registra productor/hueco y la UI no está disponible. `G_HUMAN_READ` solo habilita uso de mutaciones en UI; desarrollo/pruebas aisladas de API pueden avanzar. Promoción no autorizada.

## AMBIGUEDADES

Ninguna. Las condiciones «cuando disponibles» y «si faltan» nombran productor —WS12, con inventario WS02 y APIs WS03— y fijan el comportamiento: registrar hueco y no ofrecer la operación. Los detalles de archivos, store temporal, escenarios y textos de pantalla quedan delegados al TaskDoc de promoción.

## DRY-RUN

- **Lecturas:** input suministrado: guía, brief, alcance, decisiones, cobertura, nodo WS42 y gates; contratos de vecinos solo como contexto. Sin herramientas.
- **Cambios previstos:** ninguno; esta revisión no modifica el nodo ni ejecuta su promoción.
- **Dependencias:** WS19, WS24 y WS12; gates `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT`; downstream WS30.
- **Validaciones futuras:** contrato/whitelist WS12 por delta; `G_HUMAN_READ` antes de mutaciones UI; `G_UI_WRITE` y `G_WRITE_CONTRACT` por recibo del delta concreto; pruebas API aisladas con store temporal real o corpus WS40; validación humana UF03 en WS30.

## FUTURO

WS12 produce contrato, whitelist y huecos. WS02/WS03 aportan inventario y APIs. El TaskDoc de promoción fija archivos, store temporal, pruebas y textos. El humano P01 emite actas de recepción por delta. WS16 produce `G_HUMAN_READ`. WS30 valida UF03 y, si falla el guion, bloquea el gate y abre tarea en el nodo causante. Nada de esto autoriza implementación.
