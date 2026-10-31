**Reformulación**  
Con solo el input suministrado: revisar con procesos Pi aislados y baratos (deepseek-flash/low; sin sesión, contexto, skills, tools ni historial) raíz, paquetes, WS01–WS44 e hijos nuevos. Cada reviewer reformula propósito/resultado/repo/límites, señala ambigüedades y simula lecturas/cambios/dependencias/validaciones sin ejecutar. El coordinador compara, corrige, divide y guarda evidencia con hashes; tester muestrea y supervisor cierra. Sin producto, sin autorización de ejecución ni decisiones Pxx.

**Ambigüedades que exigirían inventar**  
1. Nodos nuevos: v4 fija `node_role/parent_id/children`, pero no estado/lifecycle, `owner_repo`, gates, files, validation ni plantilla de acceptance de hijos, agregados y paquetes. Sin esto, `dag.yaml` no se escribe sin inventar.  
2. Hijos divididos: “toda candidata pertenece una vez a paquete” no aclara si `WSxx.1` va en `packages[].children`, solo bajo `WSxx` o ambos.  
3. ROOT/PK: son agrupaciones de revisión, no entregables; no se define qué hace verdadera su `acceptance`, si su contrato es el objeto `hierarchy` menos `context_review` ni qué snapshot recibe el reviewer (¿solo objeto o hijos?).  
4. Gates: se pide revisarlos, pero no hay bundle/intento para los 15; ¿nodos revisables o solo contratos de arista? La lista obligatoria no los incluye.  
5. ¿“Brief autosuficiente” = `input.md` o artefacto aparte? ¿La guía es obligatoria? No se fija dueño de esa decisión.

**Rutinarias delegadas**  
Agrupar por entregable/intención, proponer splits y esquema, elegir fuentes pertinentes, redactar guía, construir argv/manifests/receipts, numerar intentos, separar transporte de comprensión, regenerar diagrama y ajustar helpers `.py`. Supervisor acepta integración; tester muestrea.

**Futuro, no ambigüedad**  
TaskDoc real, preflight TaskDoc-only, cold-bundle, auditoría de repos, concilio experto, gates humanos/externos, verificación futura de firmas/models, ejecución y cierre de fase. Bloqueos con productor/artefacto/condición quedan definidos.

**Dry-run por roles, sin ejecutar**  
- Coordinador: leería task/dag/fuentes; congelaría esquema y guía; por nodo generaría input/contract/manifest con hashes, lanzaría Pi nuevo, compararía reformulación/dry-run, corregiría y repetiría afectados.  
- Executor: redactaría ROOT/PK/hijos en `dag.yaml` y briefs; correría solo checks de proyección; no tocaría producto.  
- Reviewer: solo input; reformularía, listaría ambigüedades y dry-run sin tools ni edición.  
- Tester: contrastaría muestras, hashes, argv aislado, disposiciones y vigencia; registraría límites.  
- Supervisor: aceptaría disposiciones e integración; preservaría la otra tarea; no cerraría fase.

**Disposición**  
No daría APTO. Ambigüedades 1–4 bloquean autoría de jerarquía/hashes hasta aclaración; 5 exige convención del owner. Resto es ejecución futura. No he ejecutado ni leído fuentes no suministradas.
