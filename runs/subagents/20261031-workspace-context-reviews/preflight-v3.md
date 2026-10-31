## Reformulación del encargo

**Objetivo**: revisar recursivamente raíz, paquetes y las 44 candidatas WS01–WS44 con revisores baratos aislados, corrigiendo encargos y descomponiendo cuando proceda, sin ejecutar producto.

**Resultado**: `dag.yaml` con jerarquía autorada (ROOT, PK01…, WSxx.1…), contratos corregidos y re-revisados, evidencia `context-review` por nodo/intento, generados regenerados, validaciones `--check`, tester independiente y cierre de supervisor.

**Límites**: solo `plans/workspace-documental/`, `tasks/workspace-documental/` y el dir de evidencia; helpers `.py` solo bajo ese plan; no tocar `rituals/docs/skills`, no implementar producto, no promover candidatas, no inventar APIs ni decisiones P01–P09, `execution_authorized=false`, preservar la otra tarea Board activa.

## Ambigüedades de ejecución detectadas

1. **Agregador vs. ejecución**: “aristas externas siguen apuntando al paquete como agregador” convive con “paquetes no sustituyen dependencias de ejecución”. No queda claro si las aristas se reescriben al paquete o se mantienen en hijos y solo se agregan en vista; afecta la proyección de contratos vecinos.
2. **`bundle-sha256`** en la ruta de evidencia no está definido (¿`input_sha256`, hash del bundle, combinación?), mientras el manifest define `input_sha256` y `node_contract_sha256`.
3. **ROOT**: se pide revisarla, pero v3 indica que hoy no hay jerarquía; no se aclara si ROOT existe ya o debe autorarse antes de su revisión.
4. **“Esquema exacto de jerarquía”**: ambiguo si alude a estructura YAML de campos o al contenido jerárquico; no se prescribe esquema.
5. **División**: al cambiar el contrato del original, sus reviews previos quedan inválidos y deben rehacerse paquete e hijos; el criterio “entregas separables” es juicio sin umbral explícito.

## Dry-run por roles (sin ejecutar)

- **Coordinador (previo)**: lee `dag.yaml` y fuentes; autora jerarquía y esquema; fija hashes; define inputs por nodo sin inyectar reviews previos.
- **Executor**: lanza por nodo/intento un proceso Pi aislado con argv fijado; guarda `input.md`, `manifest.json`, `receipt.json`, `output.md`, `stderr.log`; reintenta ≤3 fallos técnicos; no evalúa semántica.
- **Revisor barato**: reformula propósito/resultado/repo/límites y dry-run de lecturas/cambios/dependencias/validaciones, sin ejecutar ni inventar APIs.
- **Coordinador (post)**: compara con intención; corrige fuente con referencia, justifica error del reviewer o bloquea; re-revisa afectados y verifica vigencia por hashes.
- **Generadores**: `build_plan.py --check`, `render_diagram.py` si cambia diagrama, `validate_plan.py --check`.
- **Tester independiente**: muestrea raíz, paquetes, hijos nuevos y WS01/07/11/12/16/20/21/28/30/32/40/41/43/44; registra límites.
- **Supervisor**: cierre oficial; no cierra fase ni promueve producto.
