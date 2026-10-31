# Dictamen: plan workspace documental de Deskops

Revisión independiente con contexto cero. Solo lectura del repo; sin historial de la conversación que produjo el plan. Fecha de revisión: 2026-10-31.

## 1) Qué se pretende construir y qué no está decidido

- **Propósito legible:** un workspace de lectura/escritura sobre documentos Markdown del desk, con navegación de ecosistema, representaciones múltiples del mismo origen y trazabilidad opcional de ejecuciones Scion. Frontera correcta en `borradores/vision.md`: sldb = infraestructura documental (autoridad de lectura/escritura); Deskops = autoridad de workflow; graph_ui = shell; spec2viz = definición de vistas; Scion = ejecución/transporte.
- **Verificado:** `ViewDoc`/`NotationDoc` existen en `spec2viz/spec2viz/sldb_models.py`; `ViewDoc` es portable (modelos + `where` + relaciones + notación/layout, sin ids de nodo ni rutas de store) y graph_ui la evalúa vía sldb. `RepositoryDoc` existe (`deskops/models/repository.py`) con 6 repos registrados en `desk/registry/`. `docs/operator-manual.md` y `docs/atoms.md` existen. Existen tres tareas draft en `UIs/graph_ui/desk/tasks/` (workspace, changes, edición) enrutadas en `desk/tasks/Board.md`. Cada repo tiene su propio `.sldb`, y la UI actual (mindmap) abre un solo store vía `SLDB_STORE`.
- **No decidido:** backend inicial (sldb vs Kimun); identidad y resolución entre stores (hoy `RepositoryDoc` usa rutas absolutas y cada repo tiene su `.sldb`); modelo y ubicación de "entradas/índices" (¿documento authored, `RepositoryDoc`, consulta derivada?); persistencia de selección/layout; protocolo de conflicto de edición; transporte y matriz de autoridad de operaciones; proyecto de ejemplo; quién valida humanamente; contrato de identidad de intento Scion; frontend/ruta destino de D1.
- **Solapamientos conceptuales que el plan no cierra:** "vista" se usa como `ViewDoc`, como pantalla y como preferencia local (`borradores/vistas.md` mezcla Board/documento con "resultado de búsqueda"); "entrada/índice" puede ser documento o registro existente; "operación" puede ser comando CLI, acción de UI o mutación de workflow (`desk/drawer/tasks/workspace-documental/task-d4.md` no nombra la fuente). Consecuencia: A4, B2 y C2 pueden interpretar distinto y producir artefactos incompatibles.

## 2) Ambigüedades que un ejecutor no podría resolver sin inventar

- **Fuente inaccesible:** A2 exige "casos humanos contrastados con esta conversación" (`task-a2.md`; `borradores/vision.md:3`). Un ejecutor con contexto cero no tiene esa conversación. Consecuencia: parafrasea el borrador o inventa casos.
- **Destino de entregables:** `inventario.md`, `contrato-producto.md`, `contrato-navegacion.md`, `contrato-interaccion.md`, `borradores/*.md` no tienen directorio ni modelo destino. No se sabe si son artefactos del plan, `docs/` o átomos. Consecuencia: se escriben en el lugar equivocado o se pisan los borradores revisados (A2–A5 declaran como entregable el mismo archivo que el plan usa como semilla).
- **Alcance de D1:** "workspace funcional" no dice app, ruta ni si se edita la tarea existente en `UIs/graph_ui/desk/tasks/` o se crea otra. Consecuencia: implementación duplicada o fuera del shell real.
- **Entradas/índices:** C2 no dice si son Markdown sin modelo, un modelo nuevo o instancias de `RepositoryDoc`. El registro ya existe; C2 puede duplicarlo, contradiciendo "no replicar inventarios derivables".
- **Decisiones sin dueño:** `vision.md §Decisiones abiertas` remite a "A1/B1/B2/B3", pero ningún nodo acepta explícitamente "backend inicial", "identidad federada" ni "persistencia de selección". B2 describe el tema, no la autoridad de decisión.
- **Validación humana:** G1/G2 piden "persona entra a desk desconocido" y "agente real y desk temporal", sin participante, desk de prueba, guion ni evidencia admisible. Consecuencia: el gate no es ejecutable y H1 depende de él.
- **Labels del manual:** "disponible y comprobada / propuesta / bloqueada" no tiene definición operativa (¿mergeado? ¿probado? ¿verificado por humano?). H1 exige usarlas.
- **Autoridad de C1:** C1 puede "crear dependencias" en el DAG (`dag.yaml` C1 acceptance); no se dice quién aprueba esa mutación.
- **Transporte de operaciones:** D4 exige "operaciones existentes" sin decir si la UI invoca CLI, HTTP o escribe archivos; "nada de editar status" no nombra el camino permitido.

## 3) Defectos concretos del DAG

- **Referencias obsoletas/erróneas.** `dag.yaml:existing_work` y `README.md §Estado de referencias externas` declaran 4 archivos no disponibles. Al revisar existen contrapartes reales, con mtime 00:16–00:17 (posterior al sello 00:10 del plan): `UIs/graph_ui/desk/tasks/task-workspace-multiproyeccion-documento-grafo-local-codigo-y-contexto.md`, `.../task-vista-changes-arbol-de-hashes-staleness-e-impacto-en-conocimiento.md`, `.../task-edicion-contextual-de-relaciones-y-campos-con-control-de-concurrencia.md`. Además `dag.yaml:existing_work.kimun` y las condicionales de D2/F1 citan `...-modelos-desk.md` cuando el archivo real es `...-modelos-del-desk.md`. Consecuencia: D1/D2/F1 "refinan" un artefacto inexistente mientras el real queda huérfano; A1 no nombra esas rutas, así que puede cerrar sin resolverlo.
- **Prerrequisitos externos/condicionales no son aristas.** `external_prerequisites` (closeout activo en E1) y `conditional_prerequisites` (Kimun en D2/F1) son texto libre. `validation.txt` valida solo aristas internas y reporta PASS. Consecuencia: un planificador considera E1 "listo" tras B3 y puede despacharlo contra el servicio compartido que la tarea activa está tocando.
- **A1 no precede a A4/A5 pese a que ambos necesitan el estado real.** A4 "partir del borrador y ViewDoc existente"; A5 etiqueta disponibilidad. Consecuencia: B1 absorbe retrabajo o los borradores afirman capacidades sin verificar.
- **E1 acoplado a B3.** La identidad de intento Scion (backend/manifiesto) no depende del contrato de interacción de UI; depende de A1/B1 y del cierre del closeout. Consecuencia: serialización innecesaria del ramal opcional y bloqueo del único tramo que sí puede avanzar en paralelo.
- **F1 en la ruta crítica del manual.** G1→F1 exige staleness/impacto; F1 depende de una fuente de hashes no decidida (Kimun o procedencia sldb). Consecuencia: H1 queda bloqueado por una decisión de arquitectura sin nodo dueño, o se muestran diagnósticos inventados.
- **D4 sin arista al contrato de closeout en curso.** D4 expone lifecycle/cierre mientras la tarea activa (`desk/tasks/task-closeout-la-evidencia-exigida...`, status active, ritual-testing) cambia `TaskDoc`/evidence. Consecuencia: implementación obsoleta al integrarse.
- **Resolución entre stores sin nodo de infraestructura.** Navegar el ecosistema requiere identidad multi-store; B2/C1 solo deciden/clasifican y el DAG no contempla el trabajo resultante. Consecuencia: D1 se bloquea o simula federación con un solo store.
- **Granularidad no ejecutable.** A1 cubre cuatro repos en una tarea; C1 mezcla decisión, posible modelo nuevo y descomposición; D2 incluye migración condicional; B1/C1 tienen owner "repos dueños" (no despachable). Ningún candidato trae archivos, pills ni pruebas. El PASS documental no mide ejecutabilidad.

## 4) Documentos que se pueden redactar ya vs requieren decisiones

- **Redactables ya:** cuerpo conceptual de visión (superficies verificadas en `desk/`, separación documento/representación, autoridad sldb/Deskops); reglas de `vistas.md` ("no segunda base de verdad", derivado vs authored, autoridad fuera del renderer); índice y convención editorial del manual; narrativa de UF01–UF08 a nivel de intención.
- **Requieren decisión previa:** matriz de vistas con dueño/contrato/error (necesita identidad, federación y persistencia); criterios de aceptación de user-flows ligados a operaciones reales; capítulos del manual con pasos, labels y capturas; contrato de entradas/índices y su relación con `RepositoryDoc`; capítulo Scion.
- **No redactable honestamente hoy:** instrucciones de UI con nombres de controles; backend inicial; resolución de conflictos de escritura; permisos/efectos de acciones; "disponible" sin A1.

## 5) Omisiones de recorridos humanos o superficies

- **Bootstrap:** no hay flujo para crear un desk/proyecto nuevo; UF01 asume entrada existente y C2 escribe entradas sin recorrido humano asociado.
- **Mover/renombrar documentos** y reescritura de referencias; **undo/historial** de un documento; solo existe diagnóstico (UF07) y staleness (F1).
- **Modo degradado/offline:** caída de sldb, `kimun serve` o backend del shell; sin flujo, la promesa "leer Markdown sin UI" queda sin verificar en fallo.
- **Adjuntos no-Markdown** (imágenes/PDF referenciados) y exportación/compartición; el workspace documental los necesita y no aparecen.
- **Superficies existentes omitidas:** `desk/logbook`, `desk/faq`, `desk/features`, `desk/primitives`, `desk/materializers`, y **KGDB** (`docs/knowledge-graph/`). La lista de `vision.md §Superficies` no las cubre, así que "Referencia de superficies" del manual nace incompleta.
- **Proyección Code:** el átomo y la tarea existente de workspace incluyen `Document/Graph/Code/Changes`; `vistas.md` y D3 omiten Code. Consecuencia: el plan redefine el producto sin declararlo.
- **Concurrencia/roles en uso:** hay `RoleDoc`/runtime profiles, pero ningún flujo multi-ventana, multi-agente o multi-usuario; G1 solo menciona teclado y latencia.

## 6) Veredicto y correcciones prioritarias

No es aprobable como plan ejecutable: expresa una intención de producto coherente y bien delimitada en autoridad, pero el DAG es un esqueleto de candidatos con referencias desactualizadas, decisiones sin dueño y gates que no pueden satisfacerse como están escritos. Corregir, en orden:

1. **Reconciliar reuse antes de promover:** apuntar D1/D2/F1 a las tareas reales de `UIs/graph_ui/desk/tasks/`, corregir el nombre Kimun, y hacer de A1 (o B1) un prerrequisito explícito de A4/A5 y de la promoción de D1/D2/F1.
2. **Crear un nodo de decisión antes de B2/D2** (backend, identidad multi-store, persistencia de selección, conflicto de escritura) con dueño nombrado y artefacto de decisión; convertir Kimun en arista condicional real.
3. **Modelar closeout y prerrequisitos externos como nodos/gates** para que el chequeo de readiness no diga PASS ignorándolos.
4. **Fijar destinos y labels:** ruta/modelo de cada entregable, definición de "disponible", proyecto de ejemplo y protocolo/participante de G1/G2; sin eso H1/H2 no son verificables.
5. **Dividir A1 por repo y atomizar D1–D4/F1** con archivos y validación, asignando un solo repo dueño por tarea; añadir o declarar fuera de alcance bootstrap, mover/renombrar, modo degradado, adjuntos, Code y KGDB.
