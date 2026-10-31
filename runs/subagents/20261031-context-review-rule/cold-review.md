## Alcance de esta revisión

Revisión barata, sin historial y no ejecutora sobre el bundle explícito. No he leído artefactos fuera de este texto, no he ejecutado comandos y no declaro la tarea implementada. Todo lo que sigue se limita a lo presente en el bundle: TaskDoc, pills 001/005/007, átomos `atom-clean-subagent-ambiguity-review` y `atom-tasks-enable-zero-context-subagents`, y los rituales `execution.md` y `phase.md`.

---

## 1. Reformulación del encargo

La tarea pide **oficializar una política documental**: el “context review” barato, aislado, no ejecutor y recursivo del DAG. La idea central es que un revisor sin historial reciba un paquete explícito y devuelva:

1. reformulación del objetivo,
2. ambigüedades detectadas,
3. dry-run detallado de lo que implicaría ejecutar.

Ese revisor **no ejecuta**, **no edita fuentes** y **no sustituye** una revisión experta, una ejecución ni un tester. El coordinador compara la salida con la intención, corrige el encargo y, si el nodo es grande, lo descompone en hijos con aristas. Cada nodo/hoja se revisa con proceso nuevo; si la ambigüedad persiste, no se ejecuta.

La entrega debe materializarse en:

- un átomo nuevo: `desk/atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md`;
- un ritual nuevo: `desk/rituals/context-review.md` con id `ritual-context-review`;
- integración en `execution.md` y `phase.md`;
- actualización de `docs/workflow-policy-reference.md`;
- actualización de `.pi/skills/deskops-task-lifecycle/SKILL.md`;
- anotaciones/generación del paquete `workspace-documental` (`dag.yaml`, README, fichas, validadores);
- evidencias por nodo/revisión en `runs/subagents/<run-dir>/context-review/...`;
- validación de modelos SLDB y coherencia de enlaces;
- cierre documental propio mediante commit del coordinador.

La tarea **no debe** ejecutar ni aprobar las 44 revisiones del plan, no debe cerrar la fase y no debe tocar la otra tarea activa ni sus archivos dirty.

---

## 2. Qué contiene el bundle y qué falta por diseño

Presente:

- TaskDoc completo con Goal, Scope, Implementation Path, Validation, Done When.
- Pills 001, 005 y 007.
- Dos átomos sobre subagentes limpios y ambigüedad.
- `execution.md` y `phase.md` actuales.

Referenciado pero **no incluido** en el bundle, y por tanto no verificable aquí:

- `AGENTS.md`, `README`, `.pi/skills/use-deskops`.
- `docs/workflow-policy-reference.md`.
- `.pi/skills/deskops-task-lifecycle/SKILL.md`.
- `desk/drawer/plans/workspace-documental` y `desk/drawer/tasks/workspace-documental`.
- `dag.yaml`, `build_plan.py`, `validate_plan.py`.
- El contenido actual de los rituales `testing.md` y `closeout.md`.
- La otra tarea activa y sus archivos dirty.
- El esquema exacto de `AtomDoc` y `RitualDoc` en `deskops.models`.

Esto no es un fallo del revisor: el encargo dice explícitamente “paquete explícito sin historial” y “no leer fuera”. Pero sí condiciona qué ambigüedades pueden resolverse y cuáles deben quedar como requisitos faltantes.

---

## 3. Reglas actuales que esta tarea cambia

### 3.1. `execution.md`

Reglas actuales:

- Preflight de comprensión con subagente fresco usando **solo el TaskDoc**, guardado en `runs/subagents/<run-dir>/preflight.md`.
- Revisión de contexto frío del bundle de tarea (instrucciones, pills, átomos, archivos, validación) para detectar ambigüedad, guardarraíles faltantes y pills omitidas.
- Barrido y binding de pills antes de implementar.
- Gate de inicialización antes de cualquier implementación.
- Handoff explícito a testing.

Cambio que introduce la tarea:

- Añadir el ritual `ritual-context-review` como revisión **recursiva por nodo/hoja del DAG**, no solo del bundle de una tarea.
- Mantener separados el preflight TaskDoc-only y el bundle frío barato.
- Exigir revisión por nodo/hoja antes de seleccionar hojas listas o promover/ejecutar.
- Añadir evidencia por nodo/revisión y proceso nuevo por intento.

Riesgo de ambigüedad: no queda definida la relación exacta entre la “revisión de contexto frío del bundle” que ya existe y el nuevo “context review”. ¿Son la misma cosa a distinto nivel, o dos roles distintos? El texto dice que preflight y bundle frío “siguen separados”, pero no aclara si el context review sustituye, amplía o convive con la revisión de bundle existente.

### 3.2. `phase.md`

Reglas actuales:

- Identificar la capa de dependencias lista.
- Confirmar bundle de contexto fresco por tarea.
- Ejecutar el ritual de ejecución por tarea antes de implementar.
- Cierre por tarea con validación y commit propio.
- Validación de integración y reconciliación de pills al cerrar la fase.
- Commit descriptivo de cierre de fase.

Cambio que introduce la tarea:

- DAG multinivel con revisiones por nodo antes de seleccionar hojas listas.
- El context review se aplica a raíz, paquetes, hojas y aristas.
- No se debe atribuir contexto cero al concilio experto.

Riesgo: no se define cómo se representa un “nodo” o una “arista” en el bundle que recibe el revisor sin herramientas, ni cuál es el criterio de parada de la recursión.

### 3.3. Átomos actuales

- `atom-clean-subagent-ambiguity-review`: el subagente limpio devuelve la tarea si es ambigua en vez de improvisar.
- `atom-tasks-enable-zero-context-subagents`: las tareas deben ser modulares, testeables y con pills suficientes para que un subagente limpio ejecute sin improvisación.

Cambio: se añade un átomo que separa explícitamente **test del encargo** de **revisión experta**, y que hace recursiva la revisión barata. No se cambia el contenido de los átomos existentes, pero sí su marco: la revisión de ambigüedad deja de ser solo una compuerta de tarea y pasa a ser una práctica recursiva sobre el DAG.

### 3.4. Pills

- Pill-001: cierre con commit propio. La tarea lo preserva.
- Pill-005: un subagente fresco por tarea activa, con el coordinador como integrador y verificador final. La tarea lo preserva, pero añade múltiples revisiones baratas por nodo. No se indica si pill-005 debe reconciliarse con esa multiplicidad.
- Pill-007: gates explícitos de tarea y fase. La tarea lo preserva y refuerza el gate de revisión antes de ejecutar, pero no crea un nuevo estado lifecycle.

Riesgo: `context_review.status=pending` puede leerse como un nuevo estado de lifecycle, lo que chocaría con “sin crear nuevo estado lifecycle”. Hay que aclarar si es una anotación de plan, no un estado del ciclo de vida.

### 3.5. Reglas que la tarea dice preservar

- Preflight TaskDoc-only.
- Revisión de bundle con roles baratos distintos.
- Revisión experta, ejecución y tester como gates diferentes.
- No tocar código de producto, skill global, `.opencode`, dirty closeout ni la otra tarea.
- No cerrar la fase.
- No ejecutar ni aprobar las 44 revisiones.
- No prometer enforcement runtime.
- No usar pytest completo por cambio documental.

---

## 4. Ambigüedades y guardarraíles omitidos

### 4.1. Ambigüedades bloqueantes o de alto impacto

1. **Alcance de los scripts `build_plan.py` y `validate_plan.py`.**
   - El paso 5 exige que `build_plan.py` materialice advertencias y que `validate_plan.py` reporte falta de reviews baratos.
   - El Scope dice “anotaciones/generación del paquete workspace-documental” y “No tocar código de producto”.
   - La lista `files` del TaskDoc no incluye esos scripts.
   - No queda claro si modificar esos scripts está dentro del alcance o si solo se pueden añadir anotaciones que los scripts ya sepan leer. Es una decisión de alcance, no una suposición que el revisor pueda resolver.

2. **Esquema exacto de `dag.yaml`.**
   - `council_review.scope` “distingue experto de review barato”: no se dan claves, valores permitidos ni ubicación.
   - `context_review.status=pending`, `evidence=[]`, `required_protocol=ritual-context-review`: no se especifica si van por tarea, por nodo, por raíz, en una lista o en un mapa.
   - “root/hierarquía también quedan pendientes”: no se identifica qué objeto es la raíz ni cómo se representa la jerarquía.
   - Sin esquema, el paso 5 no es ejecutable sin inventar.

3. **Relación entre “cold bundle review” existente y “context review” nuevo.**
   - `execution.md` ya tiene una revisión fría del bundle.
   - La tarea añade un ritual recursivo por nodo.
   - No se aclara si el nuevo ritual reemplaza esa revisión, la envuelve o la complementa. Esto afecta a los pasos de `execution.md` y a la validación.

4. **“Los tres rituales” del paso 6.**
   - Probablemente `context-review`, `execution` y `phase`, pero no se enumera.
   - También podría incluir `testing` y `closeout` si se consideran afectados por la política.
   - La validación pide “equivalente RitualDoc para los tres rituales”; sin lista explícita, no se puede verificar.

5. **¿Esta tarea debe generar su propia evidencia de context review?**
   - El paso 4 define el layout de evidencias por nodo/revisión.
   - El paso 6 dice que el executor escribe logs en `runs/subagents/20261031-context-review-rule`.
   - “Preflight-only en preflight.md” sugiere que para esta tarea solo se hace preflight, no una revisión completa.
   - Pero Done When dice “comprensión barata guarda evidencia no ejecutora”.
   - No queda claro si el executor debe ejecutar un context review sobre el brief de esta propia tarea, o solo documentar el protocolo y dejar las 44 revisiones pendientes.

6. **`<run-dir>` frente al path fijo.**
   - El paso 4 usa `runs/subagents/<run-dir>/...`.
   - El paso 6 usa `runs/subagents/20261031-context-review-rule`.
   - No se afirma explícitamente que `<run-dir>` sea `20261031-context-review-rule`. Es inferible, pero no está declarado.

7. **Cómo obtener el “full-payload-file” para `sldb docs update`.**
   - Se pide actualizar documentos modelados con payload completo.
   - No se indica si el payload se obtiene con un comando de lectura, si se reconstruye a mano o si existe un archivo previo.
   - Tampoco se confirma que `execution.md` y `phase.md` sean documentos SLDB actualizables por `sldb docs update`, aunque su frontmatter lo sugiera.

8. **Criterio de aceptación del context review.**
   - Se dice “no aprobar por palabra APTO”.
   - Se dice que el coordinador compara con la intención.
   - No hay rúbrica objetiva: ¿basta con que la reformulación reproduzca el objetivo y no haya ambigüedades? ¿Qué cuenta como ambigüedad persistente? ¿Quién decide que un dry-run es “detallado”?
   - Sin rúbrica, el gate depende de juicio no especificado.

9. **Límites de la recursión.**
   - No se define profundidad máxima, número máximo de revisiones, presupuesto de coste/tokens ni criterio de parada.
   - “Recursivo” sin límites puede explotar en coste o generar revisiones innecesarias. Es un guardarraíl omitido relevante.

10. **Revisión de aristas.**
    - Se pide revisar “aristas”, pero el revisor no tiene herramientas y solo recibe un paquete explícito.
    - No se define cómo se textualiza una arista para el revisor, ni qué significa “ambigüedad en una arista”.
    - Sin formato de bundle, la revisión de aristas no es operacionalizable.

### 4.2. Ambigüedades operativas

11. **Lanzamiento del revisor barato.**
    - Se menciona “proceso efímero Pi deepseek-flash con no-session/no-context-files/no-skills/no-extensions/no-tools”.
    - No se dan flags exactos, id de modelo/proveedor, perfil, comando ni forma de comprobar aislamiento.
    - “Aislamiento comprobado” no define cómo se comprueba.

12. **Formato del paquete explícito.**
    - No se especifica qué contiene el bundle de un nodo: ¿TaskDoc? ¿fragmento de `dag.yaml`? ¿átomos? ¿pills? ¿archivos enlazados? ¿solo texto pegado?
    - Sin formato, el revisor sin herramientas puede confundir “contexto no incluido” con “ambigüedad del encargo”.

13. **Registro de fallos de transporte/quota.**
    - Se dice que se registran aparte, pero no dónde, con qué formato ni cómo se distinguen de una ambigüedad.

14. **Invalidación de reviews afectados.**
    - “Un nuevo input/contrato invalida reviews afectados”.
    - No se define cómo se calcula el conjunto afectado ni cómo se marca la invalidación en `evidence` o `status`.

15. **Valores de `context_review.status`.**
    - Solo se menciona `pending`. No se definen `approved`, `rejected`, `stale`, `invalidated` ni transiciones.
    - Sin valores, el plan no puede validarse de forma consistente.

16. **“Tester independiente confirma evidencias”.**
    - No se define qué tester, con qué criterio, qué evidencia revisa ni dónde deja su resultado.
    - La sección Validation no incluye un paso de tester; solo el Implementation Path lo menciona.

17. **`closeout_evidence: commit, document`.**
    - No se aclara qué “document” es evidencia: ¿el TaskDoc? ¿un `result-summary.md`? ¿la salida del revisor? ¿el commit incluye documentación generada?

18. **Archivos dirty de la otra tarea.**
    - Se prohíbe tocarlos, pero no se listan.
    - El executor necesitaría identificarlos antes de commitear; no se indica cómo.

19. **Paths exactos del closeout.**
    - `--paths <solo-paths-del-alcance>` exige una lista cerrada.
    - El alcance incluye directorios (`desk/drawer/plans/workspace-documental`, `desk/drawer/tasks/workspace-documental`) y archivos generados. No se aclara si se commitean proyecciones generadas, `dag.yaml`, scripts, evidencias de run o solo documentos fuente.

20. **Contenido de `docs/workflow-policy-reference.md`.**
    - No está en el bundle. No se puede saber si ya existe, qué estructura tiene ni qué sección debe actualizarse.

21. **Contenido actual de `SKILL.md` y expectativas de `quick_validate.py`.**
    - No está en el bundle. Se sabe la ruta de `skill-creator`, pero no las reglas de validación ni el formato esperado.

22. **“Chequear links”.**
    - No se especifica herramienta, alcance ni criterio de fallo.

23. **Transición de estado de la tarea.**
    - `current_node: ritual-execution`, `status: active`.
    - El executor no cambia Board/tarea; el coordinador cierra.
    - No se define en qué momento ni con qué comando se actualiza el TaskDoc/Board. El bundle no incluye el ritual de closeout.

### 4.3. Guardarraíles omitidos

- **Presupuesto de coste y límite de recursión** para las revisiones baratas.
- **Regla de completitud del bundle**: el revisor debe recibir todo el contexto necesario o declarar explícitamente qué contexto falta, para no confundir ausencia de contexto con ambigüedad del encargo.
- **Separación entre “ambigüedad” y “contexto faltante”** en la salida del revisor.
- **Integridad de evidencia**: hash, timestamp, versión de modelo, comando, parámetros y forma de reproducir.
- **Protección contra secretos** en los bundles enviados al revisor.
- **Manejo de salida malformada** del revisor: ¿se reintenta, se registra, se escala?
- **Criterio de escalado** de revisión barata a revisión experta.
- **Reconciliación de pill-005** con múltiples revisiones por nodo, si aplica.
- **Protección de archivos dirty** de la otra tarea mediante lista explícita o comprobación previa.
- **No hand-editing de proyecciones generadas** ya está dicho, pero falta el criterio de qué se considera proyección y qué se considera fuente.
- **Concurrencia y rate limits** si se ejecutan revisiones en paralelo.
- **Rollback o recuperación** si una actualización SLDB o una generación falla a mitad.
- **Definición de “barato”**: modelo, límite de tokens, coste máximo aceptable.

---

## 5. Dry-run de ejecución por pasos

Dry-run descriptivo. No se ejecuta nada. Los pasos son condicionales a que se resuelvan las ambigüedades bloqueantes.

### Paso 0. Auditoría previa de solo lectura

**Lecturas propuestas:**

- `AGENTS.md`, `README`, `.pi/skills/use-deskops` (rutas oficiales indicadas por el TaskDoc).
- `git status` y rama actual; confirmar `main` y checkout actual.
- Lista de archivos dirty de la otra tarea activa.
- `desk/drawer/plans/workspace-documental/dag.yaml`.
- `build_plan.py` y `validate_plan.py`.
- `docs/workflow-policy-reference.md`.
- `.pi/skills/deskops-task-lifecycle/SKILL.md`.
- Esquema de `AtomDoc` y `RitualDoc` en `deskops.models`.
- Contenido actual de `execution.md`, `phase.md`, `testing.md` y `closeout.md` si se necesita para coherencia.
- Estado de `.sldb`.

**Cambios:** ninguno.

**Validación:** confirmar que no se tocarán archivos de la otra tarea y que el árbol de trabajo permite un commit acotado.

**Dependencias:** resolver antes las ambigüedades de alcance de scripts, esquema YAML y “tres rituales”.

---

### Paso 1. Crear el átomo

**Cambios propuestos:**

- Crear `desk/atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md` mediante `sldb docs create --model AtomDoc`.
- Payload con `id`, `title`, `five_wh_one_plus=how`, `answer`, `tags`.
- El `answer` debe recoger la regla del Goal y la distinción entre revisión experta y context review barato.

**Validación:**

- `sldb validate deskops.models:AtomDoc --input <atom-path> --pythonpath .`.
- Lectura roundtrip del documento creado.

**Dependencias:** esquema de payload disponible; ninguna otra edición depende del átomo, pero el ritual y los docs deben ser coherentes con él.

---

### Paso 2. Crear el ritual `ritual-context-review`

**Cambios propuestos:**

- Crear `desk/rituals/context-review.md` con `id: ritual-context-review`.
- Campos: `title`, `id`, `purpose`, `trigger`, `preconditions`, `steps`, `validation`, `failure_modes`, `completion`, `tags`.
- Contenido mínimo descrito por la tarea: revisor barato explica objetivo, enumera ambigüedades y produce dry-run de lecturas/cambios/validación/dependencias; no ejecuta ni edita; el coordinador compara, corrige y descompone; cada nodo/hoja se revisa; proceso nuevo por intento; fallos mejoran el encargo; no se aprueba por “APTO”; si persiste ambigüedad, no se ejecuta; no es un nuevo estado lifecycle.

**Validación:**

- `sldb validate deskops.models:RitualDoc --input desk/rituals/context-review.md --pythonpath .`.
- Coherencia con el átomo y con `execution.md`/`phase.md`.

**Dependencias:** decisión sobre relación con la revisión fría existente; decisión sobre límites de recursión y rúbrica de aceptación para que el ritual sea operativo.

---

### Paso 3. Integrar en `execution.md` y `phase.md`

**Cambios propuestos:**

- `execution.md`: añadir el ritual `ritual-context-review` sin fusionarlo con el preflight TaskDoc-only ni con el bundle frío; dejar explícito qué rol hace cada revisión; añadir revisión por nodo/hoja y evidencia.
- `phase.md`: introducir DAG multinivel, revisión por nodo antes de seleccionar hojas listas, y separación entre concilio experto y review barato.
- Actualizar `steps`, `preconditions`, `validation` y `failure_modes` de ambos rituales.

**Validación:**

- `sldb validate deskops.models:RitualDoc` para `execution` y `phase`.
- Comparación manual de la regla en átomo, ritual nuevo, `execution.md` y `phase.md`.

**Dependencias:** ritual nuevo creado; decisión sobre si los rituales son documentos SLDB y cómo obtener el payload completo.

---

### Paso 4. Actualizar política y skill Pi

**Cambios propuestos:**

- Actualizar `docs/workflow-policy-reference.md` con la regla durable y la distinción experto/context review.
- Actualizar `.pi/skills/deskops-task-lifecycle/SKILL.md` usando las instrucciones de `skill-creator`; editar solo la skill local Pi, no la global ni `.opencode`.
- Validar la skill con `quick_validate.py`.

**Validación:**

- `quick_validate.py` sobre la skill local.
- Chequeo de enlaces y coherencia con el ritual y el átomo.

**Dependencias:** contenido de `docs/workflow-policy-reference.md` y `SKILL.md` disponible; criterio de “links” definido.

---

### Paso 5. Anotar/generar el paquete `workspace-documental`

**Cambios propuestos:**

- En `dag.yaml`: `council_review.scope` distingue experto de review barato.
- Añadir por tarea `context_review.status=pending`, `evidence=[]`, `required_protocol=ritual-context-review`; raíz/jerarquía también pendientes.
- No cambiar aristas ni decisiones del producto.
- No simular reviews de los 44 nodos.
- Si el alcance lo permite, ajustar `build_plan.py` para materializar la advertencia en README y fichas, y `validate_plan.py` para reportar falta de reviews baratos sin convertir PASS estructural en execution-ready.
- Ejecutar generadores existentes y verificar `--check` sin editar proyecciones a mano.

**Validación:**

- `python desk/drawer/plans/workspace-documental/build_plan.py --check`.
- `python desk/drawer/plans/workspace-documental/validate_plan.py --check`.
- Inspección de README y fichas generadas.
- Confirmar que no se modificaron aristas/decisiones.

**Dependencias:** esquema YAML resuelto; decisión sobre si modificar scripts está en alcance; decisión sobre cómo añadir campos a 44 nodos sin simular reviews.

---

### Paso 6. Evidencias de revisión

**Cambios propuestos:**

- Crear `runs/subagents/20261031-context-review-rule/`.
- Si corresponde, guardar `preflight.md` con la reformulación TaskDoc-only.
- Si corresponde, crear `context-review/<node-id>/<bundle-sha256>/attempt-<n>/` con input explícito/hash, modelo/proveedor/perfil, aislamiento comprobado, salida del revisor y comparación del coordinador.
- Registrar aparte fallos de transporte/quota.
- No ejecutar las 44 revisiones.

**Validación:**

- Existencia y estructura de los archivos.
- Que la salida del revisor contenga reformulación, ambigüedades y dry-run.
- Que no se haya ejecutado ningún comando de implementación desde el revisor.

**Dependencias:** decisión sobre si esta tarea requiere su propia revisión; método de lanzamiento aislado; formato del bundle; criterio de hash.

---

### Paso 7. Barrido de validación documental

**Cambios:** ninguno adicional.

**Validación propuesta:**

- `sldb validate` de AtomDoc y de los tres RitualDoc.
- Chequeo de enlaces.
- Comparación de la regla en `docs/workflow-policy-reference.md`, `SKILL.md`, `context-review.md`, `execution.md` y `phase.md`.
- `build_plan.py --check` y `validate_plan.py --check`.
- Revisión de `git diff` para confirmar que solo se tocaron paths del alcance.
- No ejecutar pytest completo.

**Dependencias:** todos los cambios anteriores; lista de “tres rituales” resuelta.

---

### Paso 8. Tester y closeout

**Cambios propuestos:**

- Tester independiente confirma evidencias según el criterio que se defina.
- Executor escribe `stdout.log`, `stderr.log`, `validation.log` y `result-summary.md` en `runs/subagents/20261031-context-review-rule`; no cambia Board/tarea ni commitea.
- Coordinador revisa, elige subject y ejecuta `deskops closeout commit --task task-oficializar-context-review-barato-recursivo --run-dir runs/subagents/20261031-context-review-rule --paths <solo-paths-del-alcance>`.
- No cerrar la fase mientras la otra tarea siga pendiente.

**Validación:**

- Tester independiente confirma.
- Commit acotado a los paths del alcance.
- La otra tarea y sus archivos dirty permanecen intactos.
- La fase no se cierra.

**Dependencias:** criterio de tester definido; lista de paths cerrada; archivos dirty de la otra tarea identificados.

---

## 6. Decisiones requeridas antes de ejecutar

Para no resolver por suposición, quedan explícitamente pendientes:

1. ¿Se pueden modificar `build_plan.py` y `validate_plan.py`, o solo anotar `dag.yaml`?
2. ¿Cuál es el esquema exacto de `council_review` y `context_review` en `dag.yaml`?
3. ¿El context review sustituye, amplía o convive con la revisión fría de bundle ya existente en `execution.md`?
4. ¿Cuáles son exactamente “los tres rituales”?
5. ¿Esta tarea debe producir su propia evidencia de context review o solo el preflight?
6. ¿`<run-dir>` es exactamente `20261031-context-review-rule`?
7. ¿Cómo se obtiene el payload completo para `sldb docs update`?
8. ¿Cuál es la rúbrica de aceptación del context review?
9. ¿Cuáles son los límites de recursión, coste y número de intentos?
10. ¿Cómo se textualiza un nodo y una arista para un revisor sin herramientas?
11. ¿Qué flags/comando/modelo exacto usa el revisor barato y cómo se comprueba el aislamiento?
12. ¿Dónde y cómo se registran fallos de transporte/quota?
13. ¿Cómo se calculan y marcan reviews invalidados?
14. ¿Qué valores puede tomar `context_review.status`?
15. ¿Qué tester independiente, con qué criterio y qué evidencia?
16. ¿Qué “document” es evidencia de closeout?
17. ¿Qué archivos dirty de la otra tarea deben protegerse?
18. ¿Qué paths exactos entran en el commit?
19. ¿Qué contenido y estructura tienen `docs/workflow-policy-reference.md` y `SKILL.md`?
20. ¿Cómo se actualiza el estado del TaskDoc/Board si el executor no puede tocarlo?

---

## 7. Conclusión de la revisión

El encargo es comprensible en su intención: separar la revisión barata del encargo de la revisión experta y hacerla recursiva sobre el DAG, con evidencia no ejecutora. También es claro en sus prohibiciones: no ejecutar las 44 revisiones, no cerrar la fase, no tocar la otra tarea, no tocar código de producto ni skill global.

Pero **no está listo para ejecución sin decisiones adicionales**. Las ambigüedades más importantes son el alcance sobre `build_plan.py`/`validate_plan.py`, el esquema de `dag.yaml`, la relación entre la revisión fría existente y el nuevo ritual, la identidad de “los tres rituales” y la rúbrica de aceptación del revisor. Sin resolver esas cuestiones, el executor tendría que improvisar o elegir por suposición, lo que contradice el propio Goal de la tarea.

Esta salida es solo un context review: no implementa, no aprueba y no declara la tarea terminada.
