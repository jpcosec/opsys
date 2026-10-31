# Revisar recursivamente DAG workspace con agentes baratos

id: task-revisar-dag-workspace-con-agentes-baratos
title: Revisar recursivamente DAG workspace con agentes baratos
why: El dueño pide revisar los 44 nodos y raíz del plan con agentes baratos nuevos
  que prueben la calidad del encargo, sin ejecutar producto.
goal: Revisar realmente raíz, paquetes explícitos y cada candidata WS01–WS44; corregir
  los encargos y descomponer cuando haga falta, conservando evidencia y bloqueos honestos.
scope: Solo desk/drawer/plans/workspace-documental/ y desk/drawer/tasks/workspace-documental/,
  y evidencia de esta tarea en runs/subagents/20261031-workspace-context-reviews/.
  No implementar UI, auditar ahora todos los repos, tocar cambios ajenos ni resolver
  decisiones humanas Pxx. Se permite modificar helpers/generadores del plan para materializar
  correctamente nuevos contratos/jerarquía/reviews y sus validaciones. No cambiar
  workflow oficial en esta tarea.
implementation_path: 'Executor independiente orquesta revisores baratos deepseek/deepseek-flash
  thinking low mediante un proceso Pi nuevo por nodo y por intento, --offline --no-session
  --no-context-files --no-skills --no-extensions --no-prompt-templates --no-tools
  --system-prompt explícito --print @input.md. No resume, historia, reviews anteriores
  ni instrucciones orales. Registrar proceso/argv, versión, SHA256 de bytes exactos,
  manifest de fuentes y salida/stderr/exit. Cada reviewer reformula, busca ambigüedades
  y produce dry-run detallado de lecturas/cambios/dependencias/validaciones SIN ejecutar.
  Rol explícito: evaluar claridad como plan, distinguiendo contratos que una dependencia
  futura debe producir de lagunas del propio encargo; no inventar API/decisiones.

  Primero mapear raíz y paquetes de tareas grandes en dag.yaml sin confundir jerarquía
  con aristas de ejecución ni fases. Usar agrupación por entregable/intención y pertenencia
  única de candidatas; contratos de interfaz explícitos. Revisar raíz, cada paquete
  y cada candidata/hijo añadido, incluyendo aristas entrantes/salientes y gates. Si
  un nodo grande tiene varias entregas separables, dividir en hijos con salida/dependencia/aceptación
  propia, no solo lista de pasos. Producir brief de ejecución no ejecutor autosuficiente
  por nodo, derivado del plan/fuentes ya existentes; rutas no comprobadas siguen como
  hipótesis a auditar, nunca APIs inventadas.

  Input por nodo contiene definición actual, glosario y límites mínimos, contratos
  relevantes de dependencias/sucesores/gates y fuentes pertinentes explícitas. No
  inyectar review previo. Primer intento prueba el texto actual (con contexto pertinente);
  luego coordinador compara con intención y corrige fuente escrita, reintenta fresh.
  Disposición por hallazgo: corregido con referencia al cambio, error del reviewer
  con justificación, o bloqueo real. No aprobar solo por APTO ni callar ambigüedades.
  Registrar por separado comprensión de planificación y preparación para ejecución:
  las candidatas siguen sin autorizar ejecución, pendientes TaskDoc real y preflight
  TaskDoc-only/cold bundle futuro. Dependencias aún no ejecutadas no son contratos
  completados. Revisión sin ambigüedad no satisface gates humanos ni externos.

  Evidencia ritual-context-review en runs/subagents/20261031-workspace-context-reviews/context-review/<node-id>/<bundle-sha256>/attempt-<n>/:
  input.md, manifest.json con fuentes/orden/hashes y argv/aislamiento/modelo/razón
  perfil flash barato, output.md, stderr.log, receipt.json, disposition.md. No afirmar
  precio mínimo global. Fallos de transporte separados; reintentar barato sin crédito
  ficticio. Guardar comparación objetiva con reformulación/dry-run antes de aceptar.
  Cambiar input/contrato invalida reviews afectados; al final verificar vigencia por
  hashes semánticos/inputs y volver a correr afectados. Evitar ciclos de vigencia
  por metadatos: excluir estados/evidencia de review del contrato semántico; documentar
  selección.

  Dag.yaml sigue fuente única de IDs/aristas/gates/jerarquía/estado. Añadir metadatos
  revisados con referencias verificables y resumen legible, regenerar fichas/README/diagrama
  mediante helpers y spec2viz si cambia DAG. Mantener expert council separado. No
  marcar revisado si quedan ambigüedades de encargo; blocked/deferred deben quedar
  visibles, con responsable/dependencia. No crear reviews falsos de nodos añadidos.
  No completar ni promover nodos de producto. execution_authorized=false, estados
  candidatos y gates pendientes conservados. Tester independiente comprueba integridad/cobertura/vigencia/coherencia/aislamiento
  y toma muestras de interpretación. Supervisor hace cierre oficial. Otra tarea Board
  sigue activa; no cerrar fase.'
validation:
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- 'Comprobar raíz + paquetes + 44 nodos originales + hijos nuevos: evidencia real,
  hashes, argv aislado, disposiciones, contrato vigente y cero autorización de producto'
- Tester independiente valida muestras de reformulación/dry-run contra encargos; reporta
  límites y fallos sin fingir gates humanos
- 'Para cambios helpers .py: pytest; registrar fallo baseline CLI ya conocido sin
  modificar código ajeno; no repetir suite si nueva evidencia no lo justifica'
done_when: Cada nodo tiene intento barato real y comparación; ambigüedades corregidas
  y re-revisadas hasta comprensión o bloqueo externo explícito; plan/generados/evidencia
  coherentes; tester independiente y cierre oficial. Ningún producto implementado
  ni decisión humana inventada.
pills:
- pill-001
- pill-005
- pill-007
references:
- desk/atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md
- desk/rituals/context-review.md
- desk/drawer/plans/workspace-documental/brief.md
- d7933e2
files:
- desk/drawer/plans/workspace-documental
- desk/drawer/tasks/workspace-documental
task_type: docs
closeout_evidence:
- commit
- document
