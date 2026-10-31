## REFORMULACION

**Propósito:** integrar en `graph_ui` la inspección y edición de modelos ya existentes, reutilizando `Schema` y las operaciones `draft/validate/promote` de `sldb`, sin reimplementar modelos.

**Resultado:** recorrido UF09 navegable desde documento/contexto, con mutación comprobada en store temporal real, errores/efectos verificados contra el contrato WS12 y acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/modelos/acta.md`.

**Repo dueño:** `graph_ui`; alcance de salida en `shell/dialogs.js`, `views/models/`, `tests/` y la ruta de acta.

**Límites:** no reimplementar modelos; no habilitar `promote` sin API/autoridad; mutaciones UI sujetas a `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT`; promoción no autorizada.

## AMBIGUEDADES

1. «Hacer navegables Schema/editar clases ya disponibles desde documento/contexto». No se define qué es “contexto” ni desde qué superficie se accede; la aceptación solo exige «UF09 inspección y mutación», sin comprobar el punto de entrada. El ejecutor tendría que inventar si es acción de documento, menú contextual, diálogo u otra ubicación, y qué significa “ya disponibles”.

2. «Extensión posterior al lector básico». No nombra nodo, gate ni contrato del “lector básico”, y `depends_on` solo contiene WS12. El ejecutor no puede saber si debe esperar a WS13/14/15/16, si basta con que exista el host, ni cómo verificar esa precedencia; podría inventar una dependencia o ignorarla.

## DRY-RUN

**Lecturas previstas:** `dag.yaml` (nodo WS39, gates y arista WS12), `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`.

**Cambios previstos:** implementación en `graph_ui` bajo `shell/dialogs.js`, `views/models/` y `tests/`; acta de prueba humana en la ruta indicada.

**Dependencias:** WS12 como contrato de operaciones; gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`; `G_HUMAN_MODEL` producido por WS39.

**Validaciones futuras:** UF09 con inspección/mutación en store temporal real, contraste de efectos/errores con WS12, acta con participante P08 y paso de `G_HUMAN_MODEL` antes de publicar el capítulo 15 en el manual de WS31. Sin ejecución.

## FUTURO

WS12 debe producir el contrato por delta y el recibo de `G_UI_WRITE`/`G_WRITE_CONTRACT`. WS16 produce `G_HUMAN_READ`. P08 fija al participante humano. WS31 publica el manual; WS39 produce el acta y `G_HUMAN_MODEL`. La promoción de WS39 sigue `not_authorized` y requiere TaskDoc/preflight y autorización humana separada.
