## Reformulación del objetivo

Entiendo que la tarea busca **oficializar un “context review” barato, aislado, no ejecutor y recursivo**: un revisor sin contexto previo reformula el encargo, señala ambigüedades y produce un dry-run, sin implementar ni aprobar por capacidad experta. Debe quedar distinguido de otros gates: preflight solo-TaskDoc, bundle frío, revisión experta, ejecución y tester independiente.

Además, el plan `workspace-documental` debe reflejar que sus nodos tienen **reviews baratos pendientes**, sin ejecutarlos ni simularlos. Esta tarea solo valida la comprensión de **su propio encargo** y cierra su entrega documental; no cierra la fase ni revisa los 44 nodos.

## Ambigüedades reales

1. **“Roles distintos y baratos”**: precisar si aplica solo a preflight vs. bundle frío, o también al tester. No hace falta fijar texto literal, pero sí quién usa qué rol.
2. **Denominador del plan**: se dice “0/44 reviews baratos” y también que `root/hierarchy_context_review` queda pendiente. Aclarar si `validate_plan.py` reporta 44 tasks y aparte el root, o si el root entra en otro conteo, para evitar doble cómputo.
3. **Tester independiente**: confirmar que puede ejecutar comandos de validación/check y que su independencia basta como proceso nuevo sin historial de implementación, aunque use un perfil barato similar.
4. **Alcance de “reconocer revisiones pendientes”**: confirmar que solo implica metadata, README/fichas generadas y validaciones, sin cambiar aristas ni decisiones del producto. Está casi explícito, pero conviene fijarlo.

## Dry-run por rol

**Coordinador**
- Prepara el input preflight con solo la TaskDoc; invoca un revisor barato, sin tools, en proceso nuevo; guarda comando, `sha256` y `receipt.json`.
- Compara la reformulación/dry-run con la intención; corrige el encargo si hay ambigüedad real.
- Prepara el bundle frío con la lista congelada, lo hashea y obtiene la segunda review barata.
- Solo si ambos gates son aceptables, despacha al executor. Si persiste ambigüedad, reescribe/descompone y reintenta con proceso nuevo.
- Al final, ejecuta `closeout verify`, stagea solo paths del alcance, artefactos generados y evidencia del run; no toca cambios dirty ajenos ni cierra la fase.

**Executor**
- Inspecciona los archivos listados y referencias explícitas.
- Crea átomo y ritual con `sldb docs create`; actualiza documentos modelados con `sldb docs update`.
- Integra la regla en `execution.md`, `phase.md`, política y skill local Pi; edita la skill como texto si no está modelada.
- Añade al plan el esquema `context_review` pendiente y regenera README/fichas con los generadores existentes.
- Ejecuta validaciones y checks; escribe `stdout.log`, `stderr.log`, `validation.log` y `result-summary.md`.
- No commitea, no stagea, no modifica Board/tarea, no ejecuta reviews de los 44 nodos ni crea evidencia ficticia.

**Tester independiente**
- Proceso nuevo sin historial de implementación.
- Verifica documentos, links, `sldb validate`, `quick_validate.py`, generación/checks del plan y que el plan muestre reviews pendientes y `execution_authorized=false`.
- Deja evidencia en `validation.log` y `result-summary.md`; no edita fuentes ni aprueba los 44 nodos.

No ejecuté comandos. Revisión limitada a la TaskDoc; no exijo prosa editorial literal ni el contenido completo de los archivos que el executor podrá inspeccionar.
