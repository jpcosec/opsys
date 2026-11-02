# Resultado del Executor — corrección de fichas de WS09

Archivo editado: `desk/drawer/plans/workspace-documental/borradores/vistas.md`. Las 23 fichas `### F` siguen presentes. Ningún campo Estado fue tocado: las 23 conservan `bloqueado`. Sin commits, closeout, revisiones, build, validate ni suite.

## Ítem 1 — F05 (Error, Origen, Campos)
- Cambio: se quitó «con 0 StepDoc el procedimiento carece de pasos que mostrar». Error dice que la inexistencia de instancias StepDoc no implica ausencia de pasos y que `RitualDoc.steps` son prosa inline. Origen y Campos añaden una frase sobre esos pasos, sin reordenar.
- Fuentes abiertas: `deskops/models/ritual.py` línea 11 («# Ordered prose steps; not document references») y 65-67 (`steps: list[str]`, «Ordered prose steps ... not document references»). `desk/rituals/testing.md` (campo `steps`, 8 cadenas de prosa; comentario de plantilla «List of step-xxx paths» pero los valores son texto). `desk/rituals/execution.md` (línea 9 «Ordered prose steps; not document references», `steps:` con cadenas de prosa).
- Evidencia de F05 ampliada con `ritual.py:11,65-67`, `testing.md` y `execution.md`.

## Ítem 2 — F16 (Error)
- Cambio: «0 StepDoc» solo niega esas instancias, no los pasos de `RitualDoc.steps`. Evidencia ampliada con las mismas tres fuentes.
- Fuentes: las del ítem 1.

## Ítem 3 — F18a (Clase, y Origen)
- Cambio: Clase separa spec YAML fuente = authored; definición de notación `s2v/notations/*.yml` = authored; SpecDoc/SpecNodeDoc materializados por `diagram sync` = derivado regenerable, no fuente a editar. NotationDoc en el store: «derivado regenerable no comprobado». Origen precisa que las 8 notaciones builtin se definen en `s2v/notations/*.yml`.
- Fuentes abiertas: `infraestructura.md:35` (la fuente es un spec YAML; `diagram sync` lo materializa como SpecDoc/SpecNodeDoc). `:100` (referencia SpecDoc a NotationDoc, comandos `diagram sync`, `notation sync`; no dice qué escribe `notation sync`). `:132` (8 notaciones builtin en `s2v/notations/*.yml`, comandos `notation list|validate|sync|view`; no dice que sync materialice NotationDoc). Por eso, siguiendo preflight-disposition, NotationDoc en el store queda «no comprobado».
- Evidencia: ya citaba 35, 100 y 132; no se cambió.

## Ítem 4 — F18b (Destino de escritura)
- Cambio: la ruta `sldb/views/` queda «prevista, pendiente de confirmación y registro en WS18 al promover (`dag.yaml:1222-1224`)», sin decir confirmada. Se conserva el repo owner spec2viz del nodo WS18 y el recibo `save_view ... sin expected (ui.md:105)`. Se aclara que el prefijo no determina el repo y que no se afirma que `save_view` de graph_ui escriba en spec2viz.
- Fuente abierta: `dag.yaml:1222-1224` (`output_scope: sldb/views/ (ruta y registro confirmados según el contrato al promover; con output_base spec2viz ... puede ser spec2viz/sldb/views/ y el prefijo textual no cambia el dueño)`). Leí también `owner_repo: spec2viz` en la línea 1221 (fuera del rango pedido).
- Evidencia: se añadió `dag.yaml:1222-1224`.

## Ítem 5 — F12 (Acción/dueño y Destino de escritura)
- Cambio: la vista lee resultados; ejecutar un comando de diagnóstico se clasifica por sus efectos, no es lectura segura ni GET por ser diagnóstico. Efecto conocido: `atoms validate` llama `ensure_workspace` y puede crear andamiaje y `tag-namespaces.yaml`. WS12 debe considerarlo. No se asume que la UI invoque el comando, no se crea endpoint, no se quita ninguna operación del catálogo. La advertencia de `stores check` se conserva como no corroborada.
- Fuentes abiertas: `deskops.md:113` (atoms validate: ensure_workspace puede crear andamiaje y tag-namespaces.yaml; además `.deskops.log`). `deskops.md:266` (sorpresa (b): `validate_atoms` y `reorganize --dry-run` llaman `ensure_workspace`). `user-flows.md:179` (`stores check` puede escribir caché o journal: no se leyó; `desk update` y `atoms validate` pueden crear andamiaje). Leí además `deskops.md:265`.
- Evidencia: se añadieron `deskops.md:266` y `user-flows.md:179`.

## Ítem 6 — F03 (Campos y relaciones)
- Cambio: «ningún comando la calcula» pasó a «entre lo auditado no se encontró un comando que la calcule».
- Fuente abierta: `user-flows.md:101` («`deskops.md` no audita un cálculo de "capa lista sin solapamiento"»). Sin cambio de Evidencia, que ya citaba esa línea.

## Ítem 7 — F12 (Acción/dueño)
- Cambio: `Corpus.rank` y `GET /corpus/rank` existen, sin CLI, 409 si falta índice, fallback `difflib`, embedder instalado no comprobado. WS14 admite capacidad parcial o degradada; no se promete semántica.
- Fuente abierta: `infraestructura.md:115` (hueco: sin CLI; 409 `corpus no indexado` con `refresh=0`; sin embedder usa `difflib`; embedder instalado no comprobado).
- No verifiqué la afirmación «WS14 admite capacidad parcial o degradada»: viene de la TaskDoc, no abrí el nodo WS14 del DAG.

## Ítem 8 — F12 (Identidad)
- Cambio: «consulta guardada con `where`: ausente», y eso no niega toda selección persistida: `ProjectionDoc` es una capacidad vecina distinta, no equivalente a un `where` guardado.
- Fuente abierta: `infraestructura.md:121` (el grep solo niega esos nombres; `ProjectionDoc` es documento persistido que selecciona stores, modelos, relaciones, alias y verbos; sin campo `where`).

## Ítem 9 — Nota final
- Cambio: sección `## Candidaturas sin productor` al final del archivo, con las ocho candidaturas, la aclaración de que no son prerrequisito ni capacidades comprometidas, que la lectura básica de FAQ, issues y roles reutiliza el lector Markdown o modelado, que se conservan para WS11, que exigen alcance y productor real si se adoptan, y que no crean nodos nuevos.
- Fuente: texto de la TaskDoc. No añadí citas.

## Ítem 10 — Evidencia, Clase, Renderer
- Evidencia actualizada en F05, F16, F12 y F18b (arriba). F03 y F18a no necesitaron cita nueva. Clase solo en F18a. Renderer sin cambios. Estados sin cambios.

## Verificación de alcance
- `git diff -U0` contra HEAD: hunks solo en las líneas 94 (F03), 125, 128, 133, 137 (F05), 262, 267-268, 273 (F12), 337, 341 (F16), 363, 373 (F18a), 387, 392 (F18b) y 4 líneas añadidas al final (nota). El texto previo a «Fichas por fila» y las demás fichas no cambian. `grep -c "^### F"` da 23 antes y después.
- El worktree ya tenía otros cambios previos (`desk/inbox/*` modificados, archivos sin seguimiento) que no son míos.

## No pude verificar
- Las afirmaciones de WS14 (ítem 7): no abrí el nodo.
- Qué escribe `notation sync` (ítem 3): las líneas citadas no lo dicen.
- Que `build_plan.py --check`, `validate_plan.py --check` y `context_review.py status` pasen: no se ejecutaron, por instrucción.
- No abrí `desk/rituals/testing.md` ni `execution.md` más allá del campo `steps` (testing completo hasta línea 20; execution hasta línea 22).
- Las rutas `deskops/models/ritual.py` y los rituales se citan como en la instrucción; las líneas de las auditorías se abrieron una a una con `sed`, no con Read.

## Ítem 11, añadido por el Supervisor tras Tester PASS

Claude Opus 5.5, pane `w3Y:p1`, sin Executor. Fuera de la lista cerrada de la TaskDoc, y declarado aquí. El Tester señaló que F15 conservaba «con 0 documentos no hay orientación que mostrar», el mismo patrón que root marcó en F05: negar por conteo de instancias. Se corrige en F15, campo Error, citando `deskops.md:33,188,233` y `dag.yaml:2690`. `docs/faq.md` existe en el repo. Estados sin cambio.
