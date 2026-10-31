**Reformulación de intención**
Revisar de forma recursiva el plan del workspace documental con revisores baratos aislados: raíz, paquetes y las 44 candidatas WS01–WS44, incluyendo hijos nuevos si se dividen. Cada revisor debe reformular el encargo y hacer un dry-run de lecturas, cambios, dependencias y validaciones **sin ejecutar producto**. El Executor autora previamente jerarquía, guía y briefs; corrige encargos ambigüos y conserva evidencia verificable. No se autoriza ejecución, no se promueven nodos, no se cierran gates humanos/externos y no se toca workflow oficial.

**Ambigüedades que exigirían inventar**
No veo ambigüedades bloqueantes en el texto suministrado. Los puntos abiertos están delegados explícitamente:
- Mapa exacto de PK01… y splits: lo propone el Executor con criterios de corte y lo acepta el supervisor.
- Contenido exacto de `context-review-guide.md`, briefs y metadatos de revisión: rutina delegada, no decisión humana.
- Selección exacta de fragmentos por nodo: se gobierna por pertinencia, manifest y hashes.
- Umbral numérico para “bloqueo externo” tras correcciones semánticas: no está cuantificado; si se exigiera un número sería invención. El texto ya exige que el bloqueo quede visible con responsable/dependencia.

**Dry-run por roles, sin ejecutar**
- **Reviewer barato:** recibe solo `input.md`; reformula propósito/resultado/repo/límites; señala ambigüedades; produce dry-run de lecturas/cambios/dependencias/validaciones; no usa herramientas, historial ni reviews previos. No ejecuta.
- **Executor/coordinador:** autora ROOT/PK, esquema de jerarquía y guía antes del lote; prepara bundles, lanza procesos Pi aislados por nodo/intento; compara salidas; corrige fuentes y repite reviews afectados; registra manifests, receipts, disposiciones y hashes. No implementa producto ni autoriza ejecución.
- **Tester independiente:** sin fork del Executor; verifica cobertura, integridad, vigencia, aislamiento y coherencia; muestrea raíz, paquetes, hijos nuevos y WS01/07/11/12/16/20/21/28/30/32/40/41/43/44; registra límites y fallos.
- **Supervisor:** revisa disposiciones y pruebas; hace cierre oficial tras tester; no cierra fase ni altera la otra tarea activa.

**Rutinario delegado vs. trabajo futuro vs. ambigüedad**
Delegado: jerarquía/splits, guía, briefs, correcciones, metadatos y regeneración con helpers.
Futuro: ejecutar reviews reales, preflight TaskDoc-only/cold-bundle, concilio experto, gates humanos/externos y producto.
Ambigüedad real: ninguna identificada; solo falta de umbral numérico para bloqueo semántico, que no debe inventarse.

No he ejecutado nada ni verificado hashes.
