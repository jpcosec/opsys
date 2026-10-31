# Correlacionar intentos Scion con RunDoc y closeout

Estado: candidato de implementación; auditoría de código del 2026-10-30. No promovido. No mezclar con cambios activos de evidencia de closeout.

## Resultado de la auditoría

- Tarea -> ejecución: `deskops/runtime/scion.py:record_scion_run` crea y trackea RunDoc con task_id, role_id, run_dir y scion://agent/<slug>. `deskops/cli/commands/runtime.py:_template` lo invoca opcionalmente con --task y --agent. Generar ese registro no demuestra que Scion haya aceptado o iniciado el agente.
- Identidad: id actual run-<agent_slug>, no distingue reintentos del mismo agente. Scion mantiene Agent.RunID y PreviousRunIDs en `../scion/pkg/store/models.go`; no inferir que ese campo interno esté expuesto por API sin verificar.
- Mensajes: Scion Message tiene id, projectId, agentId, conversationId, threadId, createdAt y dispatchState; el struct revisado no tiene runId. No atribuir automáticamente toda la conversación a un intento. `scion conversation messages` y get-message ofrecen lectura con permisos. No consultar tablas internas como integración.
- Resultados/cierre: `deskops/services/closure.py:close_from_run` mantiene run.yaml, hash de sesión, trailers e index.jsonl; no actualiza RunDoc. La docstring de RunDoc dice que nada lo escribe, pero quedó obsoleta frente a record_scion_run.
- Revisión humana: plantillas de coordinador esperan waiting_for_input y supervisor valida evidencia; no se encontró un recibo estructurado de aprobación humana dentro de RunDoc. Completed del agente no prueba aprobación ni cierre.
- UI: la nueva vista graph_ui muestra task/gates; no conecta RunDoc con conversaciones Scion.

## Primer entregable propuesto

Una identidad por intento y un manifiesto canónico que materialice RunDoc y los registros de closeout existentes. Separar identidad interna del intento, identidad del agente y referencia externa Scion. Registrar intención y confirmación de dispatch como hechos distintos. Reintentos nunca sobrescriben ejecuciones anteriores; finalizar debe actualizar exactamente el intento correcto, conservando timestamps y enlazando evidencia/commit sin duplicar decisiones de lifecycle. Resolver primero el contrato de identidad disponible en API Scion y compatibilidad con los registros heredados. Los campos/modelos se cambian por el flujo SLDB y validación de contratos.

Alcance previsto: runtime/scion, modelo RunDoc, servicio de cierre y sus pruebas. Depends-on: estabilizar la tarea activa de evidencia de closeout antes de tocar ese servicio. No implementar todavía transporte, otro broker, replicación Postgres de SLDB ni importación automática de conversaciones.

## Capas posteriores (dependen del entregable)

1. Vincular conversaciones/mensajes relevantes por IDs y origen Hub/proyecto, con deduplicación, checkpoint e importación idempotente; conservar procedencia y permisos, sin asumir que todos los mensajes de un agente pertenecen a la misma ejecución.
2. Relacionar evidencia/resultados y decisiones humanas explícitas con tarea/intento; distinguir completado, validado, aprobado y cerrado.
3. Proyectar esa cadena en UI, consultando la fuente dueña de cada dato.

## Validación requerida al promover

Pruebas reales en desk temporal: dos intentos del mismo agente, registro repetido idempotente, dispatch fallido, actualización de intento correcto, finalización repetida sin duplicación, referencias SLDB resolubles, consistencia RunDoc/manifiesto/índice, recuperación de fallo y compatibilidad heredada. Ejecutar pytest y CLI afectado. Pruebas de integración Scion requieren API real; no prometerlas solo con modelo o mock. No lanzar agentes ni enviar mensajes en la auditoría.

Referencias: deskops/models/run.py; deskops/runtime/scion.py; deskops/cli/commands/runtime.py; deskops/services/closure.py; tests/test_scion_runtime.py; ../scion/pkg/store/models.go; ../scion/docs-site/src/content/docs/reference/cli.md.
