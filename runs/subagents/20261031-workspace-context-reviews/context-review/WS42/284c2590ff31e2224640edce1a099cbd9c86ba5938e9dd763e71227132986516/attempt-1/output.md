## REFORMULACION

**Propósito:** que la UI de conocimiento de graph_ui invoque operaciones existentes de átomos (split/merge) y tipado de protoátomos, mostrando a la persona el origen y el efecto antes de confirmar, y que inspeccione/valide materializaciones existentes contra `MaterializationContractDoc`.

**Resultado:** escenarios UF03 de dividir/reunir/tipar con persistencia, referencias y conflictos reales; materializaciones inválidas visibles como tales y no operables; capabilities ausentes declaradas no disponibles, bloqueando solo su escenario.

**Repo dueño:** graph_ui.

**Límites:** endpoints solo dentro de la whitelist WS12; no se generan destinos arbitrarios ni renderer propio para materializaciones; operaciones y APIs vienen de WS02/WS03 concretadas por WS12; si faltan, WS12 registra hueco y la UI queda no disponible. G_HUMAN_READ habilita mutaciones en UI, no desarrollo/pruebas aisladas.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** nodo WS42 y gates en `dag.yaml`; guía, brief, alcance, decisiones y cobertura; contratos vecinos WS12 (whitelist/efectos), WS19 (edición/conflicto) y WS24 (vista de conocimiento); `deskops/models/materialization.py`; TaskDoc de promoción y corpus/Taller WS40 cuando existan.

**Cambios previstos:** en `graph_ui:frontends/mindmap/views/workspace/knowledge/`, endpoints limitados a whitelist WS12 y `tests/`; TaskDoc fijará archivos, escenarios y textos.

**Dependencias:** WS19, WS24 y WS12; gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT, estos dos por delta. Store temporal real definido por TaskDoc o manifiesto Taller.

**Validaciones futuras:** pruebas de split/merge/tipado con referencias/conflictos; validación de materializaciones por API pública SLDB; declaración de no disponibilidad por capability; aceptación humana WS30 (UF03) y lectura WS16.

## FUTURO

WS12 produce whitelist, contrato por operación y huecos con productor. WS19 y WS24 entregan edición con conflicto y vista de conocimiento. WS40 aporta corpus/Taller. El receptor P01 emite acta G_UI_WRITE por delta; WS12 verifica G_WRITE_CONTRACT. WS30 ejecuta la validación humana. La promoción fijará archivos, pruebas y textos exactos; WS45 cubre la precondición de payload.
