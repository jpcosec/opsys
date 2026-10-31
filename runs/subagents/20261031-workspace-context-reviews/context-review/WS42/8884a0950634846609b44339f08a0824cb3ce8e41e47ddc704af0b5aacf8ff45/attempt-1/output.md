## REFORMULACION

**Propósito:** que la vista de conocimiento de `graph_ui` invoque las operaciones reales de conocimiento (split/merge de átomos, tipado de protoátomos) mediante la whitelist de WS12, con confirmación humana previa que muestre origen y efecto.

**Resultado:** operaciones ejecutables con persistencia, referencias y conflictos reales; materializaciones existentes inspeccionadas/validadas sin crear destinos; capacidades ausentes declaradas no disponibles, no simuladas.

**Repo dueño:** `graph_ui` (`output_base: graph_ui:repository_root/`), alcance en `frontends/mindmap/views/workspace/knowledge/`, endpoints solo de la whitelist WS12, `tests/`.

**Límites:** no generar destinos arbitrarios; no simular capacidades; depende de WS19, WS24, WS12 y de los gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`.

## AMBIGUEDADES

1. «validan contra el modelo SLDB registrado en el store de la tarea» — no se identifica qué store («de la tarea» no coincide con «store temporal real»/«corpus WS40» de alcance.md) ni qué registro del modelo. Obliga a inventar la fuente de validación.
2. «una materialización que no valida se muestra como inválida» — no hay criterio de validación definido en las fuentes; el ejecutor tendría que inventar reglas y umbrales.
3. «bloquea solo el escenario de UF03 que la usa y su etiqueta de disponibilidad» — no existe mapa capability→escenario UF03 en las fuentes suministradas; obliga a inventar la correspondencia.
4. «ve el origen y el efecto de la operación antes de ejecutar» — «efecto» no se define (¿diff, lista de cambios, recuento?); obliga a inventar el contenido de la confirmación.

## DRY-RUN

- **Lecturas previstas:** `dag.yaml` (WS42 y vecinos), `contratos/operaciones.md` de WS12, salidas de WS19/WS24, `alcance.md`, fila UF03 de `cobertura.md`.
- **Cambios previstos:** solo `frontends/mindmap/views/workspace/knowledge/` y `tests/`; endpoints según whitelist.
- **Dependencias:** WS12 (contrato), WS19, WS24; gates pendientes resueltos por WS12/WS16.
- **Validaciones futuras:** WS30 (recorrido manual UF03) y validación del delta `G_UI_WRITE`.

## FUTURO

WS12 publica la whitelist y capabilities; WS07 resuelve P01–P06 con actor humano; el TaskDoc de promoción fija archivos, escenarios y textos; WS30 aporta el acta manual; la promoción de WS42 requiere autorización humana (`promotion: not_authorized`).
