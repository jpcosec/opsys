## Reformulación

**Propósito:** revisar recursivamente el DAG del workspace documental —raíz, paquetes, WS01–WS44 e hijos nuevos— mediante revisores baratos sin contexto, para corregir encargos y detectar ambigüedades, sin ejecutar producto.

**Resultado:** evidencia `ritual-context-review` por nodo/intento; disposiciones por hallazgo; `dag.yaml` con metadatos revisados; fichas/README/diagrama regenerados; validaciones `build_plan.py --check` y `validate_plan.py --check`; tester independiente; cierre del supervisor. Los nodos con ambigüedad no se marcan revisados; los bloqueos quedan visibles con responsable/dependencia.

**Repo/alcance de escritura:** `desk/drawer/plans/workspace-documental/` y `desk/drawer/tasks/workspace-documental/`; evidencia en `runs/subagents/20261031-workspace-context-reviews/`. No UI, no auditoría de todos los repos, no decisiones humanas Pxx, no workflow oficial (`desk/rituals/`, `docs/`, skills), `execution_authorized=false`.

**Límites:** no ejecutar producto; no inventar APIs; no aprobar solo por APTO; no crear reviews falsos; no promover nodos de producto; no cerrar fase.

## Ambigüedades del propio encargo

**Huecos que impiden entender/ejecutar sin inventar:**
- No se explicita la ruta de `dag.yaml` ni su esquema actual de jerarquía/paquetes. Sin él no puede mapearse raíz/paquetes ni saber cuántos PK existen.
- `expert council`, `spec2viz`, `TaskDoc`, `cold-bundle` y `preflight TaskDoc-only` se nombran sin definición ni referencia concreta dentro del brief.
- La rúbrica exige identificar “repo”, pero no se concreta si es `/home/jp/proyectos/SLDB_1/deskops`, los repos de producto o ambos.
- Las decisiones humanas `Pxx` no se enumeran ni se referencian.
- No se tipifican los “gates” humanos/externos que la revisión no satisface.
- Los “helpers/generadores” solo aparecen como `build_plan.py`, `validate_plan.py` y `spec2viz`; falta lista/contrato de invocación.
- Los campos mínimos de `manifest.json` y `receipt.json` no están en el brief; dependen de `desk/rituals/context-review.md`.

**Decisiones rutinarias delegadas (no bloquean):** nombres `WSxx.1`, `PK01`, `ROOT`; estructura de rutas de evidencia; modelo flash low; flags de aislamiento; 3 intentos técnicos; SHA256 y JSON canónico; no inyectar reviews previos; disposición corregido/error reviewer/bloqueo; separar comprensión de planificación y preparación de ejecución.

## Dry-run por roles — sin ejecutar

**Coordinador/executor:** leería `dag.yaml` y briefs; construiría por nodo un bundle con snapshot, contratos de aristas relevantes y fuentes explícitas —sin estado/evidencia de review—; calcularía hashes de input y contrato; generaría `input.md`; lanzaría Pi con `--offline --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates --no-tools --system-prompt`; capturaría argv, versión, stdout/stderr/exit; reintentaría solo fallos de transporte hasta 3 veces.

**Revisor barato:** reformularía propósito/resultado/repo/límites; señalaría ambigüedades; haría dry-run de lecturas, cambios, dependencias y validaciones sin ejecutar; distinguiría contratos que una dependencia futura debe producir de lagunas del encargo; no inventaría APIs.

**Coordinador:** compararía salida con intención; dispondría cada hallazgo como corregido con referencia, error del reviewer con justificación o bloqueo real; corregiría la fuente y relanzaría fresh; actualizaría metadatos en `dag.yaml`; regeneraría fichas/README/diagrama; verificaría vigencia por hashes semánticos.

**Tester independiente:** muestrearía raíz, todos los paquetes, hijos nuevos y WS01/07/11/12/16/20/21/28/30/32/40/41/43/44; comprobaría integridad, cobertura, vigencia, coherencia y aislamiento; un fallo de muestra exigiría corrección y re-review barato de afectados.

**Supervisor:** cierre oficial solo tras el tester; no cerraría fase.

## Veredicto condicionado

El encargo es comprensible en intención, resultado y límites, pero **no es autosuficiente** sin: ruta/esquema actual de `dag.yaml`, definiciones o referencias de `TaskDoc`, `cold-bundle`, `spec2viz` y `expert council`, concreción de “repo” y lista de `Pxx`/gates. Esos huecos impiden ejecutar sin inventar. Condición para aprobarlo como brief: incorporarlos al input o declararlos rutinarios con fuente verificable. No ejecuté ningún paso.
