FILE:desk/tasks/task-alinear-contrato-ws11-en-transporte-alias-canónico-preparación-y-ws15-1.md
---
id: task-alinear-contrato-ws11-en-transporte-alias-canónico-preparación-y-ws15-1
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/contratos/navegacion.md
- desk/drawer/plans/workspace-documental/dag.yaml
- runs/subagents/20261101-ws11-alineacion/review-source.md
- runs/subagents/20261101-ws11-correccion/freeze-final.md
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-001-task-closure-commit.md
files:
- desk/drawer/plans/workspace-documental/contratos/navegacion.md
- desk/drawer/plans/workspace-documental/dag.yaml
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-alinear-contrato-ws11.md
closeout_evidence:
- commit
- document
---

# Alinear contrato WS11 en transporte, alias canónico, preparación y WS15.1

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root final aceptó los puntos A-F, pero el fallback local no dice cómo viaja, la configuración admitiría sinónimos, §5.4 no nombra quién prepara los stores y shell/api.js queda fuera del output_scope de WS15.1.

## Goal

_Describe the concrete result this task must produce._

Aplicar en una pasada las cuatro precisiones de root en contratos/navegacion.md y en el output_scope de WS15.1, regenerar derivados y renovar solo las revisiones medidas como afectadas.

## Scope

_State what is in scope and what is out of scope._

Autoridad: runs/subagents/20261101-ws11-alineacion/review-source.md, que prevalece sobre este resumen. Lista cerrada.

1. Serialización: el local del desk del proceso sin alias configurado se serializa como ausencia del parámetro alias; sin excepción ?alias=local. URL e historia conocen la equivalencia. En el texto, local: sigue siendo el desk del documento origen. Un alias configurado para el desk del proceso es el canónico.
2. Alias canónico: WS41 valida que no haya dos entradas para el mismo (root.resolve(), store.resolve()). Sin sinónimos en el baseline. Sin modelo ni nodo.
3. §5.4: quién prepara stores fuera del request: generador de WS40, Executor del consumidor en sus pruebas, operador o responsable del desk en uso real. La UI no migra por una petición. Sin comando inventado ni productor automático.
4. output_scope de WS15.1 incorpora frontends/mindmap/shell/api.js para conservar estado HTTP y tipificar errores HTTP/red/JSON, manteniendo error.body y compatibilidad. Sin implementar, sin dependencias ni gates, sin cambiar aceptación. WS13.1 consume y no implementa.

Superficies: contratos/navegacion.md, output_scope de WS15.1 en dag.yaml, derivados de build_plan y render_diagram, punteros de context_review de lo medido como stale.

No tocar: vistas.md, guía, decisiones, helper, validadores, código, repos hermanos, rutas ajenas. Sin cerrar fase, WS12, UI, Scion, push ni suite general.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Editar contrato y DAG. 2. Regenerar derivados y medir staleness. 3. Congelar. 4. Tester focal con no regresión de A-F. 5. Revisión fresca WS13.1 y WS41. 6. Renovar lo medido, disposición contra contratos completos. 7. Checks, closeout y checkpoint root.

## Validation

_List the checks required before this task can close._

- test -s desk/drawer/plans/workspace-documental/contratos/navegacion.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente de solo lectura deja runs/subagents/20261101-ws11-alineacion/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: las cuatro precisiones aplicadas y ninguna más; Tester focal PASS sobre bytes congelados con no regresión de A-F; revisión fresca WS13.1 y WS41 sobre el contrato final; solo se renueva lo medido; build --check, validate --check y status en verde; contrato en borrador.


FILE:runs/subagents/20261101-ws11-alineacion/review-source.md
# Revisión root final de WS11, texto recibido

Fuente: mensaje de Codex `w3Y:p2` en el pane Claude `w3Y:p1`, 2026-11-01, sobre el closeout `1c9bb628`. Autorización de trabajo documental local; no es aprobación humana ni del cierre. Texto copiado sin normalizar.

Revisión root final de WS11 (contrato b9db651e…c789, HEAD1c9bb628): los arreglos A–F y los dos ajustes previos están aceptados como contenido; NO cierro aún WS11/fase ni activo WS12. Queda una alineación acotada de transporte, responsabilidad y alcance de consumidor. No es otro rediseño.

Verificación independiente: contrato SHA exacto; build/validate/status verdes; helper13passed/1.40s. Leí revisión fresca final WS13.1/WS41 y disposición, Tester completo anterior y focal final con sus límites. Ambos inputs frescos contienen íntegros los bytes finales, hashes input/output de receipts coinciden, stdin devnull, exit0 y flags de aislamiento. Recibos separados manuales no capturaronPID: declarar el límite, no rellenar datos retrospectivos ni repetir solo por ese metadato. status es solo vigencia del plan y no prueba lectura del contrato por las otras72.

Acepto las tres frases adicionales sobre local relativo al documento origen, carga/formato deconfiguración porWS41 yE7casoparticulardeE4. Acepto el fallback `local` como decisión técnica para el desk propio sin configuración: no debe hacer que WS13.1 espereWS41. Pero falta cómo viaja, pues §3.2/8.5 rechazan el alias explícito sinconfig.

ALINEACIÓN AUTORIZADA, una sola pasada:

1. Serialización inequívoca: `local` devuelto como identidad del desk del proceso, cuando no hay alias configurado para él, se serializa como AUSENCIA del parámetro alias. No agregar excepción nueva `?alias=local` que contradiga la regla actual de rechazo. Historia/URL deben saber esta equivalencia. Dentro del texto, `local:` sigue siendo el desk del documento origen, nunca cambia el componente desk de la clave a la cadena local si el documento pertenece al alias externo b. Configuraciónconfiable puede designar el desk del proceso con su alias yentoncesseusa esealiascanónico. No nuevas fuentes de permisos.

2. Alias canónico: validar que no haya dos entradas autorizadas para el MISMO par `(root.resolve(), store.resolve())`; sinónimos para el mismo desk no están en baseline. Una identidadfísica normalizada tiene un aliascanónico devuelto y usado en sesión/historia; no abrir dos identidadesdel mismo documento porconfigduplicada. Esta validación perteneceWS41, no nuevo modelo/nodo. No inventar valores concretos. Si en el futuro se quieren sinónimos, será un delta explícito.

3. §5.4: nombrar quién prepara stores FUERA del request, no dejar actor desconocido. CorpusWS40: su generador/fixture los prepara; pruebas propias deWS13.1/WS41: Executor delconsumidor prepara fixture antesdeGET; uso real: operador o responsable del desk prepara/migra manualmente con autorización antesdeatenderlecturasHTTP. El TaskDoc consumidor identifica operación pública/versión y evidencia delapreparación sin inventar un comandoaquí. La UI no migra a causa de una petición. Si la API escogida no cumple ausencia de escrituras bajo lasprecondiciones, hueco/intake en repo dueño y caso bloqueado, no workaround. No crear productor automático de preparación ni rolScion extra.

4. Output_scope WS15.1: incorporar explícitamente `frontends/mindmap/shell/api.js` para conservar estadoHTTP y tipificar erroresHTTP/red/JSON, manteniendo error.body y compatibilidad con consumidores. Esto estáyaasignado por §7.3/H09 yno entraen el output_scope actual. Es una alineación canónica documental, sin implementar código y sin nuevas dependencias/gates ni cambiar aceptación. NO mover eltrabajo aWS13.1: su lector consume elresultado; tipificacióncompleta es deWS15.1 y no convierte WS13.1→WS15.1 en dependencia circular. En la revisión frescaWS13.1 el dry-run menciona request()preservastatus: hacer inequívoco en lacomparación que no autoriza aeseExecutor a implementar fuera de sualcance. Si despuésdeaclarar el productor un revisor atribuye el código explícitamente aotro nodo, no aceptarlo como paráfrasis.

Simulé SOLOenmemoria el cambio del output_scopeconhelper: afecta WS13, WS15, WS15.1. Medir nuevamentealhacerelparche,noasumirestos3como límite. Regenerar fichas/proyecciones que corresponden y renovar solo inputsrealmente afectados. La fuentevistas no necesitavolveracambiar: WS09 vigente se conserva si su inputpermaneceidéntico. Contrato/guía/decisionescomunes no deben reescribirse porcosmética. No introducirhelpers/cambiosvalidador para forzarverde.

Completarlo en tarea correctivaDOCS acotada bajo workflow (estadoanterior ya cerrado: capturar/promover/TaskDoc/ejecución/Tester/closeout correspondientes, sin falsificar cronología). Superficies necesarias: contratos/navegacion.md, output_scope WS15.1 enDAG, derivadosyregistros devalidación. No cambia código ni otrosalcances. Estas4precisiones están autorizadas; no hace falta otra congelación intermedia esperando autorización sobre lo mismo.

DespuésdecongelarTODO: Testerfocal sobre los4puntos y no regresión de A–F, revisión fresca no ejecutora decontrato final conWS13.1/WS41, renovaciónDAGmedida y disposicióncontra contratos completos. No repetir73 porinercia: dependerá de hashes; tampoco ocultarstaleness. Los ensayos de ausencia de escrituras/readiness quedan comoobligaciones de losconsumidores, no afirmar runtimeahora. Mantener reseña de Testercompleto+focal con bytes respectivos, sin declarar que último completo probó frases posteriores.

Entregarcheckpointroot con diff final/hash/alcance deinvalidación/recibos/disposiciones y checks. Mantenerborradorhasta revisiónrootfinal. No cerrar fase ni activarWS12/UI/Scion/push; no suitegeneral ni archivosajenos. No pedir alhumano repetirdecisiones. Esto cierra los dospuntos abiertos delhandoffy laasimetriadealias; no abre revisión general denuevo.
