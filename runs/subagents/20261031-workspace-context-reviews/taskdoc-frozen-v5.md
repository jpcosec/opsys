---
id: task-revisar-dag-workspace-con-agentes-baratos
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md
- desk/rituals/context-review.md
- desk/drawer/plans/workspace-documental/brief.md
- d7933e2
depends_on: []
pills:
- pill-001
- pill-005
- pill-007
files:
- desk/drawer/plans/workspace-documental
- desk/drawer/tasks/workspace-documental
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-revisar-dag-workspace-con-agentes-baratos.md
closeout_evidence:
- commit
- document
---

# Revisar recursivamente DAG workspace con agentes baratos

## Rationale

_Explain why this task exists or the business driver behind it._

El dueño pide revisar los 44 nodos y raíz del plan con agentes baratos nuevos que prueben la calidad del encargo, sin ejecutar producto.

## Goal

_Describe the concrete result this task must produce._

Revisar realmente raíz, paquetes explícitos y cada candidata WS01–WS44; corregir los encargos y descomponer cuando haga falta, conservando evidencia y bloqueos honestos.

## Scope

_State what is in scope and what is out of scope._

Solo desk/drawer/plans/workspace-documental/ y desk/drawer/tasks/workspace-documental/, y evidencia de esta tarea en runs/subagents/20261031-workspace-context-reviews/. No implementar UI, auditar ahora todos los repos, tocar cambios ajenos ni resolver decisiones humanas Pxx. Se permite modificar helpers/generadores del plan para materializar correctamente nuevos contratos/jerarquía/reviews y sus validaciones. No cambiar workflow oficial en esta tarea.

## Implementation Path

_Outline the expected implementation route or affected surface._

Executor independiente orquesta revisores baratos deepseek/deepseek-flash thinking low mediante un proceso Pi nuevo por nodo y por intento, --offline --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates --no-tools --system-prompt explícito --print @input.md. No resume, historia, reviews anteriores ni instrucciones orales. Registrar proceso/argv, versión, SHA256 de bytes exactos, manifest de fuentes y salida/stderr/exit. Cada reviewer reformula, busca ambigüedades y produce dry-run detallado de lecturas/cambios/dependencias/validaciones SIN ejecutar. Rol explícito: evaluar claridad como plan, distinguiendo contratos que una dependencia futura debe producir de lagunas del propio encargo; no inventar API/decisiones.
Primero mapear raíz y paquetes de tareas grandes en dag.yaml sin confundir jerarquía con aristas de ejecución ni fases. Usar agrupación por entregable/intención y pertenencia única de candidatas; contratos de interfaz explícitos. Revisar raíz, cada paquete y cada candidata/hijo añadido, incluyendo aristas entrantes/salientes y gates. Si un nodo grande tiene varias entregas separables, dividir en hijos con salida/dependencia/aceptación propia, no solo lista de pasos. Producir brief autosuficiente de planificación por nodo, sin ejecutar, derivado del plan/fuentes ya existentes; rutas no comprobadas siguen como hipótesis a auditar, nunca APIs inventadas.
Input por nodo contiene definición actual, glosario y límites mínimos, contratos relevantes de dependencias/sucesores/gates y fuentes pertinentes explícitas. No inyectar review previo. Primer intento prueba el texto actual (con contexto pertinente); luego coordinador compara con intención y corrige fuente escrita, reintenta fresh. Disposición por hallazgo: corregido con referencia al cambio, error del reviewer con justificación, o bloqueo real. No aprobar solo por APTO ni callar ambigüedades. Registrar por separado comprensión de planificación y preparación para ejecución: las candidatas siguen sin autorizar ejecución, pendientes TaskDoc real y preflight TaskDoc-only/cold bundle futuro. Dependencias aún no ejecutadas no son contratos completados. Revisión sin ambigüedad no satisface gates humanos ni externos.
Evidencia ritual-context-review en runs/subagents/20261031-workspace-context-reviews/context-review/<node-id>/<bundle-sha256>/attempt-<n>/: input.md, manifest.json con fuentes/orden/hashes y argv/aislamiento/modelo/razón perfil flash barato, output.md, stderr.log, receipt.json, disposition.md. No afirmar precio mínimo global. Fallos de transporte separados; reintentar barato sin crédito ficticio. Guardar comparación objetiva con reformulación/dry-run antes de aceptar. Cambiar input/contrato invalida reviews afectados; al final verificar vigencia por hashes semánticos/inputs y volver a correr afectados. Evitar ciclos de vigencia por metadatos: excluir estados/evidencia de review del contrato semántico; documentar selección.
Dag.yaml sigue fuente única de IDs/aristas/gates/jerarquía/estado. Añadir metadatos revisados con referencias verificables y resumen legible, regenerar fichas/README/diagrama mediante helpers y spec2viz si cambia DAG. Mantener expert council separado. No marcar revisado si quedan ambigüedades de encargo; blocked/deferred deben quedar visibles, con responsable/dependencia. No crear reviews falsos de nodos añadidos. No completar ni promover nodos de producto. execution_authorized=false, estados candidatos y gates pendientes conservados. Tester independiente comprueba integridad/cobertura/vigencia/coherencia/aislamiento y toma muestras de interpretación. Supervisor hace cierre oficial. Otra tarea Board sigue activa; no cerrar fase.
Precisiones operativas v2: supervisor/coordinador acepta solo si la reformulación identifica propósito/resultado/repo/límites, el dry-run respeta autoridad y secuencia de dependencias, la aceptación es comprobable y no queda decisión de encargo sin dueño. Tester verifica esta rúbrica en raíz, TODOS los paquetes e hijos nuevos, y WS01/07/11/12/16/20/21/28/30/32/40/41/43/44. Fallar una muestra exige corregir y re-review barato de afectados. Discrepar con reviewer solo con cita de texto explícito del input que resuelva su duda, o argumento verificable de que pide ejecutar el trabajo futuro; sin cita/razón se corrige o queda bloqueado.
Conservar WS01–WS44 siempre; al dividir, original pasa a paquete no ejecutable cuyos hijos se nombran WSxx.1, WSxx.2...; la terminación del paquete exige hijos, y aristas externas siguen apuntando al paquete como agregador. Paquetes superiores usan PK01..., raíz ROOT. Toda candidata pertenece una vez a paquete superior; paquetes no sustituyen dependencias de ejecución ni crean tarea activa. El esquema exacto de jerarquía se escribe en dag.yaml antes de revisión.
Hash input es SHA256 de bytes exactos de input.md. Hash contrato de nodo es JSON UTF8 sort_keys=True,separators=(',',':'),ensure_ascii=False sobre definición de ese nodo excluyendo SOLO context_review; la proyección exacta se guarda en contract.json para poder reproducirlo. Bundle contiene snapshot del nodo, contratos de aristas relevantes y fuentes explícitas, ninguno con estado/evidencia de review; no se manda dag.yaml completo con metadatos recursivos. Contratos revisados/corregidos son fuente vigente y SÍ se suministran; lo excluido es output/disposición de reviewers anteriores. Manifest registra cada fragmento/proyección y hash, y vigencia compara fuentes/proyecciones actuales. Si cambia contrato de vecino suministrado, repetir review afectado. Metadatos de revisión nunca deben inyectarse como contrato de entrada. Referencias archivo completo sin modificación pueden congelarse con ruta/hash.
Los briefs por nodo sirven para evaluar planificación, no se preparan fingiendo TaskDoc ejecutable ni pruebas de API que aún debe producir auditoría. Preflight TaskDoc-only y cold-bundle de implementación siguen pendientes de promoción, con paths/contratos reales resultantes. Bloqueos de dependencias futuras se nombran con productor/artefacto/condición de aceptación; no son ambigüedad si el encargo define cómo obtenerlos y cómo detenerse cuando falten. Alcance helpers significa solo .py bajo desk/drawer/plans/workspace-documental/; workflow oficial bajo desk/rituals/, docs/ y skills no se modifica. execution_authorized es campo de dag.yaml y permanece false.
Fallo transporte es exit no cero, timeout o salida vacía; guardar stderr/receipt sin contarlo como review. Hasta 3 intentos técnicos baratos por input, luego bloqueo técnico explícito; correcciones semánticas no limitadas a 3. Si respuesta no contiene reformulación y dry-run, registrar fallo de comprensión y reescribir input o repetir modelo barato con motivo, no darle crédito. Distinguir HTTP/quota y bloqueo del contrato. Run-dir fijo identifica esta tarea aunque siga otro día; no sobrescribir intentos. d7933e2 es baseline documental precedente. La otra tarea activa a preservar es task-closeout-la-evidencia-exigida-depende-de-lo-que-la-tarea-toca-no-es-la-misma-para-todo. Integración/cierre los hace supervisor tras tester; no cerrar fase.

Fuentes y términos explícitos v3: cwd /home/jp/proyectos/SLDB_1/deskops, repo coordinador; owner_repo de cada nodo define repo de eventual producto según repo_roots de desk/drawer/plans/workspace-documental/dag.yaml. Este YAML existe: nivel superior tasks (44 candidatas), gates (15), repo_roots, parameters.source_mode, hierarchy_context_review pending; hoy NO tiene paquetes ni jerarquía explícita, la tarea debe authorarlos. Fuentes a leer: desk/drawer/plans/workspace-documental/{dag.yaml,brief.md,alcance.md,decisiones.md,cobertura.md,reconciliacion.md,validacion-humana.md,borradores/*.md}. Glosario viene de brief.md y límites de alcance.md; incluir fragmentos con encabezados/rutas/hash según pertinencia al nodo. Decisiones P01–P09 y resolución humana están en decisiones.md; gates humanos/externos y sus productores/contratos están en dag.yaml. El review de la tarea no audita ahora esos contenidos; son lecturas explícitas del trabajo del Executor.
TaskDoc = tarea activa modelada, autorizada/ruteada en Board; candidatas drawer no lo son. Preflight TaskDoc-only = review barato de TaskDoc sola; cold-bundle = otro review barato de TaskDoc más fuentes/guardarraíles explícitos. Concilio experto = reviews de alta capacidad previos, evidencia distinta. spec2viz = dueño de generación desde spec: ejecutar helper existente python desk/drawer/plans/workspace-documental/render_diagram.py tras build_plan.py si diagrama cambia; leer helper antes de invocar. Los dos comandos build_plan.py --check y validate_plan.py --check comprueban proyecciones sin escribir.
manifest.json mínimo: node_id, role, attempt, input_sha256, ordered_sources [{path,sha256,projection}], node_contract_sha256, edge_contracts [{id,sha256}], provider, model, thinking, selection_reason, isolation_flags, argv. receipt.json mínimo: argv, cwd, pi_version, start/end UTC, PID, returncode, input_sha256, output_sha256, technical_failure; sin secretos. contract.json guarda JSON canónico exacto como definido. No agregar a contrato campos de review salvo context_review; otros datos de review viven dentro de ese único campo o fuera del contrato, nunca en campos semánticos. Toda variación de bytes de fuente suministrada o contrato vecino invalida su review (regla conservadora, incluso typo en ese fragmento); typo en fuente NO suministrada no invalida ese nodo. Guía breve de planificación es fuente escrita, sin memoria previa.
Tester es nuevo subagente independiente del Executor y coordinador, sin fork de historial, recibe solo task + handoff/fuentes/rutas explícitas, no edita producto ni plan. Registra muestras/resultados/limitaciones en validation.log y result-summary.md. Puede usar modelo por defecto; NO cuenta como review barato ni experto sustituto. Las firmas/models se verifican en sus tareas futuras. Se acepta que reviewer diga que no ha visto fuentes a leer, pero debe poder describir orden/roles/límites; pedir auditoría de contenidos futuros no bloquea comprensión del encargo de esta tarea.

Precisiones v4: bundle-sha256 en ruta ES input_sha256. Executor autora ROOT y paquetes antes de review; esquema hierarchy: {root: {id: ROOT, title, scope, acceptance, children: [PK...]}, packages: [{id: PK01, title, scope, acceptance, children: [WS...]}]}; cada objeto contiene context_review (único campo excluido de contrato). Raíz/PK son agrupaciones de revisión, no nuevas dependencias operativas. Las tareas partidas siguen en tasks: padre original node_role=aggregate con children=[WSxx.1,...], hijos node_role=delivery,parent_id=WSxx. Original WSxx conserva ID y aristas externas: sus dependientes siguen dependiendo WSxx, y WSxx ahora depende de todos sus hijos para declarar entrega completa. Cada hijo depende de prerrequisitos originales pertinentes, nunca del padre; esto impide ciclo padre-hijo. Contratos de vecinos incluyen condición de terminación agregada. Si no se divide, node_role=delivery sin children.
Criterio de corte: dividir cuando hay dos o más resultados que pueden verificarse/aceptarse independientemente, con operaciones o contratos distintos (p.ej. campos y relaciones); no dividir lecturas/pruebas de una misma entrega como trabajo separado ni por tamaño estimado. Executor propone esquema/contenido jerárquico y splits dentro del encargo explícito; supervisor acepta integración tras pruebas. Coordinador/Executor de ESTA tarea puede redactar y comparar propuestas contra intención escrita; solo reviewer barato carece de herramientas y no interpreta resultados de otros intentos. Supervisor revisa disposiciones y tester las contrasta. Formato validation.log libre legible con comandos/exit/resultados; identidad/versiones/hashes en manifests/receipts descritos.
Guía breve de planificación = documento nuevo bajo desk/drawer/plans/workspace-documental/context-review-guide.md que el Executor redacta desde brief.md/alcance.md con reglas de lectura y criterios anteriores; su ruta/hash se suministra si forma parte del input. El esquema y guía se congelan antes de lote final; cambios invalidan solo nodos que los recibieron. TaskDoc de esta tarea contiene todo el encargo; se pueden leer fuentes de producto en el paso de planificación sin pedir al reviewer que las haya auditado ahora.

Precisiones v5 (resuelven cold-v4): nodos nuevos. Hijo WSxx.n en tasks: id, title, status=candidate, kind y owner_repo del padre salvo que el corte exija otro repo, output_base, output_scope, scope, acceptance propios, estimate S|M, node_role=delivery, parent_id, depends_on con prerrequisitos pertinentes, requires con los gates pertinentes del padre, task_file desk/drawer/tasks/workspace-documental/task-wsxx-n.md, promotion igual que las candidatas y context_review. Padre partido: node_role=aggregate, children, conserva id, status, requires y aristas originales, añade sus hijos a depends_on; su acceptance es que todos sus hijos cumplan la suya. Gates con scope_nodes incluyen a los hijos que los requieren.

packages[].children lista solo candidatas originales WS01–WS44; cada hijo pertenece a su padre por parent_id y no se repite en un paquete. La pertenencia única se comprueba así.

ROOT y PK son agrupaciones de revisión: su acceptance es verdadera cuando cada hijo directo tiene revisión vigente sin ambigüedad de encargo o bloqueo explícito con responsable. Su contrato es su objeto de hierarchy excluyendo context_review. El reviewer recibe ese objeto más los contratos de sus hijos directos y sus aristas con otros paquetes.

Gates: los 15 son contratos de arista, no nodos revisables. No tienen bundle ni intento propio; su definición se incluye en el input de cada nodo que los requiere o los produce, y cambiarla invalida esos nodos.

Brief autosuficiente de nodo = input.md de esa revisión; no se crea otro artefacto. context-review-guide.md es obligatoria y va en todo input.

## Validation

_List the checks required before this task can close._

- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- Comprobar raíz + paquetes + 44 nodos originales + hijos nuevos: evidencia real, hashes, argv aislado, disposiciones, contrato vigente y cero autorización de producto
- Tester independiente valida muestras de reformulación/dry-run contra encargos; reporta límites y fallos sin fingir gates humanos
- Para cambios helpers .py: pytest; registrar fallo baseline CLI ya conocido sin modificar código ajeno; no repetir suite si nueva evidencia no lo justifica

## Done When

_Name the observable condition that makes the task complete._

Cada nodo tiene intento barato real y comparación; ambigüedades corregidas y re-revisadas hasta comprensión o bloqueo externo explícito; plan/generados/evidencia coherentes; tester independiente y cierre oficial. Ningún producto implementado ni decisión humana inventada.
