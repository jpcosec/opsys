## 1. Reformulación del objetivo (lo que entiendo)

Revisar recursivamente, con revisores baratos aislados (sin contexto, sin tools, sin sesión), la raíz, los paquetes explícitos y cada nodo WS01–WS44 del DAG `workspace-documental`, más cualquier hijo nuevo que surja de descomponer encargos. Para cada nodo: reformular, detectar ambigüedades del encargo y producir un dry-run detallado (lecturas/cambios/dependencias/validaciones) **sin ejecutar producto**. El coordinador corrige el texto fuente, re-revisa con proceso fresco y deja disposición por hallazgo (corregido / error del reviewer justificado / bloqueo real). `dag.yaml` sigue siendo fuente única; se regeneran fichas/README/diagrama. Un tester independiente valida integridad/cobertura/vigencia/aislamiento y muestras; un supervisor cierra. Nada de producto implementado, decisiones humanas (Pxx) resueltas ni nodos promovidos.

## 2. Ambigüedades del encargo

1. **Criterio de "comprensión"** (done_when): "hasta comprensión o bloqueo externo" no tiene rúbrica. ¿Quién dictamina comprensión: coordinador, tester, ambos? Sin criterio, "APTO" puede colarse como aprobación.
2. **Criterio de "calidad del encargo"** (why): no se define qué distingue un encargo claro de uno ambiguo (¿contratos de interfaz completos? ¿aceptación verificable? ¿dependencias nombradas?). El reviewer podría inventar el estándar.
3. **Frontera "review previo" vs "contrato vigente"**: input excluye review anterior pero incluye "contratos relevantes de dependencias/sucesores/gates". Si un review anterior ya modificó ese contrato, ¿se inyecta o no? No queda operacionalizado.
4. **Dos conceptos de hash**: `bundle-sha256` (path) y "hashes semánticos/inputs" (vigencia). Su proyección y relación no se definen; qué exactamente se excluye del contrato semántico (¿solo estados/evidencia?) queda a criterio del ejecutor.
5. **Cardinalidad e IDs al dividir**: si un nodo grande se parte en hijos, ¿el original permanece? ¿los "44 originales" cuentan igual si uno se reemplaza? No se fija estabilidad de IDs.
6. **Frontera "helpers/generadores del plan" vs "workflow oficial"**: se permite tocar helpers `.py` pero "no cambiar workflow oficial". `build_plan.py`/`validate_plan.py` pueden ser ambos; el límite no está trazado.
7. **"preflight TaskDoc-only / cold bundle futuro"**: se menciona como no-objetivo, pero el encargo no aclara si el brief por nodo debe prepararse para ese preflight o solo declararlo pendiente.
8. **Disposición "error del reviewer con justificación"**: sin rúbrica, es la vía fácil para descartar hallazgos legítimos.
9. **Selección de muestras del tester**: "toma muestras" sin tamaño, criterio (aleatorio/riesgo) ni qué cuenta como fallo vs límite declarado.
10. **Fallos de transporte vs fallos del reviewer**: "reintentar barato sin crédito ficticio" no define qué evidencia distingue uno de otro ni cuántos reintentos hay antes de declarar bloqueo.
11. **`execution_authorized=false`**: no se dice dónde vive (campo de `dag.yaml`, task doc, hijo). Esquema no especificado; un helper futuro debe producirlo.
12. **"Otra tarea Board sigue activa; no cerrar fase"**: referencia externa sin ID; el ejecutor no puede verificarlo.
13. **`d7933e2` en references**: rol no declarado (¿baseline? ¿commit de origen?).
14. **Ruta de evidencia con fecha fija** (`20261031-...`): no se dice qué pasa si se re-ejecuta otro día.

## 3. Dry-run por rol (sin ejecutar)

**Executor independiente**
- *Lee*: `desk/drawer/plans/workspace-documental/{dag.yaml,brief.md,build_plan.py,validate_plan.py,fichas}`, `desk/drawer/tasks/workspace-documental/*`, átomo/ritual referenciados.
- *Enumera*: raíz → paquetes explícitos → WS01–WS44 → hijos añadidos; distingue jerarquía de aristas y fases.
- *Produce por nodo*: `input.md` (definición actual + glosario + límites + contratos de dependencias/sucesores/gates + fuentes explícitas, sin review previo), `manifest.json` (fuentes, orden, hashes, argv, aislamiento, modelo/perfil), `output.md`, `stderr.log`, `receipt.json` (proceso/versión/SHA256 de bytes exactos/exit).
- *Cambios permitidos*: solo plan/tasks/helpers del plan y evidencia de esta tarea; nada de producto ni workflow oficial.
- *No hace*: aprobar, promover nodos, resolver Pxx, afirmar precio mínimo global.

**Coordinador / editor**
- *Lee*: `output.md` vs intención del nodo y fuentes vigentes.
- *Decide por hallazgo*: corregir fuente (con referencia al cambio) / marcar error del reviewer (con justificación) / declarar bloqueo (responsable/dependencia visibles).
- *Cambios*: edita texto fuente, descompone si hay entregas separables (hijo con salida/dependencia/aceptación propia), regenera fichas/README/diagrama vía helpers si cambia el DAG.
- *Invalidación*: cambio de input/contrato invalida reviews afectados; al final verifica vigencia por hashes y re-ejecuta afectados; evita ciclos excluyendo estados/evidencia del contrato semántico (selección documentada).

**Tester independiente**
- *Comprueba*: integridad y hashes, cobertura (raíz+paquetes+44+hijos), vigencia, coherencia plan↔generados↔evidencia, aislamiento (`--offline --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates --no-tools`, system-prompt explícito), `execution_authorized=false` y gates intactos.
- *Muestrea*: reformulación/dry-run contra encargos; reporta límites y fallos sin fingir gates humanos.
- *Helpers*: si se tocó `.py`, corre `pytest`; registra fallo baseline CLI conocido sin tocar código ajeno; solo repite suite si nueva evidencia lo justifica (justificación explícita).

**Supervisor**
- *Cierre oficial*: valida que ninguno de los no-objetivos ocurrió (producto, Pxx, promoción de nodos, cierre de fase Board) y que bloqueos quedan visibles con responsable/dependencia. No convierte "revisión sin ambigüedad" en gate humano ni externo.

**Riesgos de ejecución detectados (no del producto futuro)**: (a) que "error del reviewer" absorba hallazgos reales; (b) que la doble noción de hash derive en ciclos de vigencia; (c) que el brief por nodo se vuelva autosuficiente solo en apariencia sin criterio de suficiencia; (d) que `execution_authorized=false` quede como prosa y no como campo verificable.
