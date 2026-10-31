## Reformulación del objetivo

Dejar constancia oficial (docs + skill + ritual + átomo) de que el *context review* es una prueba barata, aislada, no ejecutora y recursiva de la **calidad del encargo** (no una revisión experta ni una ejecución), y anotar en el paquete `workspace-documental` que sus 44 nodos tienen reviews baratos **pendientes** sin correrlos ni aprobarlos. Cierre: gate docs + commit propio, sin tocar la otra tarea activa ni cerrar la fase.

## Ambigüedades / decisiones que tendría que inventar

El encargo v3 está bastante cerrado. Residuos:

1. **Contenido exacto de payloads** (AtomDoc: `five_wh_one_plus=how`, `answer`, `tags`; RitualDoc: `steps`, `failure_modes`, etc.): el esquema está nombrado pero no su texto. Lo redactaría yo → decisión inventada, aunque acotada por el Goal y el punto 2.
2. **Composición exacta del bundle frío** ("TaskDoc+pills+átomos+rituales concretos"): qué átomos/rituales entran y en qué orden. El punto sobre `input.md` dice "concatenación explícita documentada por el coordinador", pero no fija la lista → la eligiría yo.
3. **Elección del perfil barato**: el comando `pi … deepseek-flash` está dado como "comprobado en esta máquina", pero no hay criterio de fallback si el modelo proveedor no está disponible (¿fallo de transporte aparte? el encargo lo insinúa pero no lo operacionaliza).
4. **Formato de `receipt.json` y de `input.md`** (cabeceras, orden, separadores): se describen campos, no estructura. Habría que inventar plantilla.
5. **Qué significa "tester independiente"** aquí: ¿otro proceso Pi, otra persona, un script? No se define el rol ni su input.
6. **`<solo-paths-del-alcance>`** para `closeout commit --paths`: la lista concreta de rutas no está enumerada (sí el criterio). La derivaría del Scope; es decisión mía.
7. **"Subject elegido por coordinador"**: correcto que no sea ambigüedad del executor, pero el revisor no sabe qué subject; no bloquea comprensión.
8. **Artefactos generados** (`README`/fichas del plan): se dice "regenerar, no editar a mano", pero no se listan los archivos ni los flags exactos más allá de `--check`.
9. **Validación de skill**: se da ruta a `quick_validate.py` pero no su contrato de salida esperado.
10. **Definición operativa de "aislamiento comprobado"** (sin historial/memoria/skills/contexto): se enumera, pero no cómo se demuestra en el recibo (¿flags del CLI bastan?).

Ninguna de estas es contradicción; son huecos de decisión acotados. Que yo no conozca el contenido de átomos/rituales/docs referenciados no es contradicción: el encargo autoriza inspeccionarlos al ejecutar.

## Dry-run (sin ejecutar nada)

1. Leer `AGENTS.md`, `README`, `.pi/skills/use-deskops`; abrir referencias explícitas (`atom-tasks-enable-zero-context-subagents`, `atom-clean-subagent-ambiguity-review`, `docs/workflow-policy-reference.md`, rituales existentes, `SKILL.md`, plan `workspace-documental`).
2. Redactar `AtomDoc` (`atom-cheap-zero-context-reviews-test-the-brief-recursively.md`) con `sldb docs create --model AtomDoc … --store .sldb --pythonpath .`; luego `sldb validate deskops.models:AtomDoc --input …`.
3. Redactar `RitualDoc ritual-context-review` en `desk/rituals/context-review.md` con la misma operación; validar con `sldb validate` equivalente.
4. Integrar el ritual en `execution.md`, `phase.md`, `docs/workflow-policy-reference.md` y `.pi/skills/deskops-task-lifecycle/SKILL.md` vía `sldb docs update <ref> <full-payload> --store .sldb --pythonpath .`; validar los tres RitualDoc; `quick_validate.py` sobre la skill local.
5. Ejecutar el preflight TaskDoc-only barato (v3 o sucesor) y un cold review con el comando Pi indicado; guardar `input.md`, `sha256`, `receipt.json`, salida (reformulación + ambigüedades + dry-run) y disposición bajo `runs/subagents/20261031-context-review-rule/context-review/<node>/<bundle-sha>/attempt-<n>/`. Fallos de transporte/quota → registro aparte, no “ambigüedad”.
6. Actualizar el paquete: `tasks[i].context_review = {status: pending, required_protocol: ritual-context-review, evidence: []}`, `hierarchy_context_review` idéntico, `council_review.scope` aclarando que APTO experto ≠ reviews baratos, `status = expert_reviewed_pending_cheap_context_reviews_and_decisions`; adaptar `build_plan.py` y `validate_plan.py` (esquema, `execution_authorized=false`, reporte 0/44), regenerar y `--check`.
7. Validaciones: `sldb validate` (AtomDoc + 3 RitualDoc), links, coherencia doc/skill/rituales, `build_plan.py --check`, `validate_plan.py --check`. Nada de pytest completo.
8. Tester independiente deja `stdout.log/stderr.log/validation.log/result-summary.md`.
9. Coordinador: `deskops closeout verify --task …` y `deskops closeout commit --task … --run-dir … --paths <scope>`; no stagea dirty previos, no toca la otra tarea, no cierra fase.

**Veredicto breve:** encargo comprensible y consistente para un revisor barato; los residuos son decisiones de redacción/composición acotadas, no contradicciones. No ejecuto ni autorizo.
