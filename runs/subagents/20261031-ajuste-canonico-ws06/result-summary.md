# Resultado del Executor: ajuste canónico del plan workspace tras WS06

Sin commits, sin `git add`, sin `context_review.py run`, sin comandos mutantes de `deskops`. Archivos editados: `brief.md`, `dag.yaml` (revisión 8 a 9, con `revision_note`), `reconciliacion.md` y `runs/subagents/20261031-ws06-reconciliacion/canonical-adjustments.md`; proyecciones regeneradas con `build_plan.py` y `render_diagram.py` (README, fichas `desk/drawer/tasks/workspace-documental/`, `dag.diagram.*`). `decisiones.md`, P01-P09, auditorías, código, validadores y `execution_authorized` (false) no se tocaron. Estado se mantiene en `final_plan_reviewed`.

## Antes y después por punto

**A, ViewDoc (C-50, ajuste 3, WS18).**
- Antes: C-50 pedía «ViewDoc portables, independientes del host» y dejaba abierto compartir la lógica del evaluador. WS18 aceptaba «vista portable (el mismo ViewDoc sin código específico del host)». El `output_scope` sldb/views/ se pasaba al dueño de spec2viz sin más.
- Después: C-50 es un delta de autoría de ViewDoc y NotationDoc concretos (WS09/WS11) y su comprobación sobre stores reales reutilizando C-37 y C-49. Fuentes abiertas: `projection_views.py:107` (`evaluate_view(store, view)`), `views_routes.py:9-10,56-82` (store por petición; `save_view` escribe en `store.parent/sldb/views/`), `test_projection_views.py:151-156` (dos stores, cambia filtros, no ejecutado: no prueba payload idéntico). Se retira «falta portabilidad/independencia del host» y toda extracción del evaluador. WS18 no pide servicio, CLI ni runtime fuera de graph_ui. `output_scope` `sldb/views/` con `output_base` spec2viz puede ser `spec2viz/sldb/views/`: ruta y registro según contrato, sin cambiar de dueño por el prefijo. Brief: ViewDoc es datos sin ruta de store; evaluador y rutas en graph_ui.

**B, revisión (C-41, ajuste 1, WS45).**
- Antes: el glosario decía «hash con que una escritura prueba...»; C-41 era un «CAS por version/content_hash» ausente y decía «WS20 solo nombra raw-source»; WS19.1 hablaba de «hash CAS del documento».
- Después: el glosario separa (1) before-image por valor `expected` con HTTP 409, (2) token publicado `version`/`content_hash`, (3) comparación o escritura pública con precondición compartida, aún no probada. No se niega la capacidad optimista, no se infiere frescura por CLI, no se fuerza CAS ni algoritmo; WS12 define representación, precondición, operaciones y escritores alcanzados; P03 no cambia. C-41 apunta a WS45 y deja de decir que WS20 solo nombra raw-source (WS20 conserva raw-source y C-42; el hueco de campos es separado). WS19.1/WS19 dejan de decir «hash CAS».

**C, captura (C-55, ajuste 2).**
- Antes: «nuevo delta: productor deskops de captura directa»; alternativa `message send` más `promote` por evaluar.
- Después: canal permitido de captura a drawer con origen preservado, sin tarea activa y colisiones controladas, pendiente del contrato WS12, que compara API SLDB existente (`sldb.api.documents.create_document`, `create_document.py:22`; sobrescribe archivos existentes), composición y eventual wrapper Deskops; `DrawerService` (`drawer.py:246-274`, candidato en `:261`, `why` en `:265`, rechaza destino existente). `message send` más `promote` no se aprueba (borra la nota, `why` apunta a una ruta borrada, fallo parcial, trabajo local en inbox). Productor Deskops explícito solo si falta conducta de workflow, antes de WS25.2. C-21, WS12 y WS25.2 alineados.

**D, Scion y recibos (C-64, ajuste 4).**
- Antes: «no se requiere WS05» (podía leerse como eliminar WS32 a WS05); WS06: «el receptor ... acepta por delta en WS11/12» y «WS11/12 obtienen aceptación específica».
- Después: WS06 puede clasificar y conservar la descomposición sin ejecutar WS05; WS32 y WS33 conservan dependencias (WS05 incluido) y gates (sin cambio en sus nodos). Recibos: acta del receptor P01; WS11/WS12 son fuente de contrato que solo enlaza. Sin firmas, gates ni recepción. «No designado en P01» queda como dato de esa tabla y no como permiso que frene trabajo local.

**E, coherencia.** Cláusulas viejas contradictorias reescritas, no preservadas como prefijo (tabla inicial de reutilización, bullets de «Lectura de la matriz», C-14, C-21, C-40, C-42, C-48, atomización, cobertura). Cobertura ahora de 64 nodos, con WS45 (C-41) y WS20 solo con C-42, WS05 y WS32 con nota. Conteo de clasificación recontado sobre las filas finales: 68 filas, 33 ya cubierto, 32 nuevo delta, 2 extender ticket, 1 no adoptado (sin filas nuevas).

## WS45 (nuevo, planificado)
sldb; `depends_on` WS12; `requires` G_SLDB_WRITE y G_WRITE_CONTRACT; estimate M; `output_base` sldb:repository_root/; paquete PK05 (con WS20); `status` candidate, `context_review` pending. Entregable: inventario con path, símbolo y commit más pruebas reales focalizadas; código solo si al ejecutarlo falta capacidad. Aceptación: precondición obsoleta rechazada sin cambios, vigente aplicada, rechazo observable. No depende de `source_mode`, no toca UI, no es productor condicional. Nada afirma implementación ni aceptación.

Gate técnico nuevo G_PAYLOAD_PRECONDITION (pending, `produced_by` WS45, evidencia concreta, sin satisfacer). `scope_nodes` de G_SLDB_WRITE (+WS45) y G_WRITE_CONTRACT (+WS45) actualizados.

## Consumidores conectados (por efecto real)
- WS19.1: guardado de campos con precondición (antes «hash CAS del documento»).
- WS19.2: alta/baja de relaciones con before-image sobre payload.
- WS19: agregado, espeja los requisitos de sus hijos.
- WS21: guardado por campos en ambas variantes de `source_mode`; sigue exigiendo G_SOURCE solo en editable.
Todos pasan a `requires` G_PAYLOAD_PRECONDITION. No se conectó ningún lector. WS42 (deskops operations) y WS25/WS26/WS28 no guardan payload por campos y quedan fuera; WS42 queda detrás de WS19 de forma transitiva.

## Nodos cuyo contrato cambió
- Nuevo: WS45.
- Con texto o requisitos nuevos: WS06, WS12, WS18, WS19, WS19.1, WS19.2, WS20 (frase de alcance: conserva raw-source), WS21, WS25.2.
- Agrupadores: PK05 (children, scope, acceptance), PK04 (acceptance: «ViewDoc portable» pasa a «ViewDoc concreto»).
- Gates: G_SLDB_WRITE, G_WRITE_CONTRACT (scope_nodes) y G_PAYLOAD_PRECONDITION (nuevo).
- Fuera de lo pedido (WS07-WS12): solo WS12, requerido por B y C. WS07, WS08, WS09, WS10 y WS11 sin cambio de contrato (su input cambia por brief.md).
- Otros ajustes mecánicos: `covered_work.evidence.sha256` de WS01 actualizado al nuevo `brief.md` (hash de recibo, sin tocar `context_review`); `revision_note` nuevo.

## Validación
- `build_plan.py --check`: PASS.
- `context_review.py status | wc -l`: 73 líneas: 72 nodos con `input changed` (todos los reviews existentes quedan vencidos por el cambio de brief.md, que es base común) y WS45 pending.
- `validate_plan.py --check`: falla solo por reviews vencidos (`assert not review_problems`). Ejecutado con esa aserción y la de `validation.txt` omitidas en una copia en memoria, el resto pasa (estructura, gates, ciclos, hashes de evidencia WS01, enlaces). El único otro motivo hallado fue el hash de WS01 sobre `brief.md`, ya corregido. `validation.txt` no se regeneró.
- Decisiones abiertas: ninguna; no se creó `open-decisions.md`.
