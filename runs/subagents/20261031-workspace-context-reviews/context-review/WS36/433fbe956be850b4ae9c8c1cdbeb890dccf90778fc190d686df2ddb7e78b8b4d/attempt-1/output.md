## REFORMULACION

- **Propósito**: integrar en el workspace la delegación Scion y la intervención humana: invocar dispatch/reply y solicitud de decisión mediante el adaptador autorizado, mostrando actor y evidencia.
- **Resultado**: UI de ejecución en `frontends/mindmap/views/workspace/execution/` que confirma operación vinculada al intento y muestra honestamente ausencia de API/permisos.
- **Repo**: `graph_ui` (`output_base: graph_ui:repository_root/`).
- **Límites**: no autoaprueba ni simula; no ejecuta agentes; gates pending/unverified son intencionales; `promotion: not_authorized`; depende de WS34 (adaptador) y WS35 (lectura); fuera de alcance closeout HTTP, commits automáticos y despliegue distribuido.

## AMBIGUEDADES

1. `output_scope: frontends/mindmap/views/workspace/execution/; endpoints; tests/` — "endpoints" no dice qué endpoints, en qué repo ni quién los posee. WS34 declara el adaptador público en `deskops` y el scope de WS36 solo dice "Invocar solo adaptador autorizado". Obligaría a inventar si WS36 crea endpoints en `graph_ui`, excediendo el alcance o duplicando WS34.
2. `scope: Invocar solo adaptador autorizado para dispatch/reply y solicitud de decisión` — la "solicitud de decisión" no aparece en el scope/acceptance de WS34 (que cubre dispatch/reply, confirmación, timeout/errores). Obligaría a inventar el contrato/endpoint de decisión o a decidir por cuenta propia si se muestra como no soportado; falta dependencia o contrato (posible WS33/WS12).
3. `acceptance: ... ausencia de API/permisos visible` — no define dónde/como se comprueba esa visibilidad (estado UI, test, log). Obligaría a inventar el criterio de evidencia para un estado de error.

## DRY-RUN

- **Lecturas previstas**: `dag.yaml` (WS34, WS35, gates G_EXEC/G_SCION/G_UI_WRITE/G_WRITE_CONTRACT), `task-ws36.md`, contrato de WS12 y probe de WS44 cuando existan.
- **Cambios previstos**: vistas de intervención en `execution/` (solicitar decisión, enviar respuesta, revisión actor/evidencia, estados de error), endpoints solo si el contrato lo determina, tests.
- **Dependencias**: adaptador público de WS34; lectura de WS35; `G_UI_WRITE`/`G_WRITE_CONTRACT` de WS12; `G_SCION` de WS44; `G_EXEC` de humano.
- **Validaciones futuras**: respuesta vinculada al intento, operación confirmada, ausencia de API/permisos visible, no autoaprobación; aceptación real en WS37.

## FUTURO

WS12 produce acta y contrato; WS44 produce `G_SCION`; el humano autoriza `G_EXEC` y resuelve P01–P09; WS37 valida UF06 con agente real; la promoción exige preflight, archivos y evidencia.
