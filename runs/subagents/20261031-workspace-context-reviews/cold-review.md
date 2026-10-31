**Reformulación de intención**

La tarea pide revisar recursivamente, con revisores baratos aislados, la raíz, los paquetes y las 44 candidatas WS01–WS44 del plan `workspace-documental`: comprobar que cada encargo se entiende, corregir ambigüedades, dividir nodos grandes en hijos con contrato propio y conservar evidencia verificable. No se implementa producto, no se autoriza ejecución, no se tocan workflows oficiales ni decisiones humanas, y no se cierra la fase. La revisión de candidatas es un gate documental; no equivale a preflight TaskDoc, cold-bundle de implementación, tester de producto ni aprobación humana.

**Hallazgos y huecos**

1. **Falta la fuente DAG en este paquete.** Solo tengo la task doc y referencias; no puedo verificar los 44 nodos, jerarquía, aristas ni gates. El bundle de cada reviewer debe incluir snapshot explícito y `manifest.json`; sin eso, la cobertura es incomprobable.
2. **Frase ambigua:** “brief de ejecución no ejecutor autosuficiente por nodo” admite dos lecturas. Debe reescribirse como “brief de planificación por nodo, no un ejecutor autosuficiente”.
3. **Hash del contrato:** se excluye solo `context_review`, pero no se define una allowlist exacta de metadatos de revisión. Conviene fijar en `contract.json` la proyección exacta y prohibir cualquier estado/output de review en el input.
4. **Tester independiente:** no se especifica identidad, aislamiento, modelo/perfil, evidencia ni criterio de independencia. Añadir que no comparte proceso con el coordinador y que registra muestras y límites.
5. **“Glosario y límites mínimos”:** no se indica fuente, plantilla ni mínimo exigible. Debe definirse por nodo o remitirse a una sección versionada.
6. **División WSxx:** aclarar que WSxx pasa a paquete no ejecutable y sigue siendo revisable como agregador; sus hijos WSxx.n se revisan de verdad, sin fabricar reviews. Las aristas externas apuntan al paquete.
7. **Invalidación:** falta distinguir cambio semántico de typo y cerrar qué nodos dependientes se re-revisan cuando cambia un contrato vecino.
8. **Estado:** revisión sin ambigüedad no satisface gates humanos/externos; `execution_authorized=false` y estados candidatos deben conservarse.

**Dry-run por roles — sin ejecutar**

- **Coordinador/Executor de revisión:** leerá task doc, `dag.yaml`, `brief.md`, helpers `.py`, validadores y baseline `d7933e2`; mapeará raíz, paquetes y WS01–WS44; construirá bundles mínimos con snapshot, contratos de aristas y fuentes explícitas; lanzará un proceso nuevo por nodo/intento con el perfil barato indicado; comparará reformulación/dry-run con la intención; corregirá textos o dividirá nodos; repetirá reviews afectados; regenerará fichas/README/diagrama; escribirá evidencia en `runs/subagents/20261031-workspace-context-reviews/context-review/<node-id>/<bundle-sha256>/attempt-<n>/` con `input.md`, `manifest.json`, `output.md`, `stderr.log`, `receipt.json`, `disposition.md`. No implementará UI ni tocará workflows oficiales.
- **Reviewer barato:** recibirá solo `input.md`; reformulará propósito, resultado, repo y límites; enumerará ambigüedades; describirá lecturas, cambios propuestos, dependencias y validaciones futuras; no ejecutará comandos, no leerá fuentes no suministradas y no editará archivos. Si no produce reformulación y dry-run, no recibe crédito.
- **Tester independiente:** leerá task, evidencia, `dag.yaml`, hashes y muestras; comprobará cobertura de raíz, paquetes, 44 originales y hijos nuevos; verificará argv aislado, manifiestos, disposiciones, vigencia por hashes y ausencia de autorización de producto; muestreará WS01/07/11/12/16/20/21/28/30/32/40/41/43/44. No corregirá fuentes.
- **Supervisor:** leerá informe del tester y diff; aceptará solo si no quedan ambigüedades de encargo ni reviews ficticios; mantendrá bloqueos visibles y hará cierre oficial, sin cerrar fase. El cierre exigirá commit propio y gates de pill-001/pill-007.

**Validaciones previstas, no ejecutadas**

`python desk/drawer/plans/workspace-documental/build_plan.py --check`; `validate_plan.py --check`; comprobación de hashes/argv/disposiciones/cobertura; `pytest` solo si se cambian helpers `.py`, registrando el fallo baseline conocido sin tocar código ajeno.

**Límite de esta revisión**

No he ejecutado comandos ni leído rutas no suministradas. No puedo afirmar que el DAG real tenga 44 nodos ni que los helpers funcionen. Esto revisa el encargo de candidatas; no implementa ni aprueba el producto futuro.
