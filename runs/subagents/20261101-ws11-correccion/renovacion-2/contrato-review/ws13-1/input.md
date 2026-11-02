FILE:desk/drawer/plans/workspace-documental/contratos/navegacion.md
# Contrato de navegación e identidad del workspace documental (WS11)

Estado: borrador del Executor de WS11, 2026-11-01. No está revisado: «contrato básico revisado» exige Tester independiente PASS y revisión root. No hay actas de recepción (sección 12). `execution_authorized` global sigue en `false`; este documento no autoriza implementación, escritura en repos hermanos ni Scion. Corregido el 2026-11-01 tras la revisión root del checkpoint WS11 (`runs/subagents/20261101-ws11-correccion/review-source.md`, texto recibido; autorización de trabajo documental, no aprobación humana): la revisión no aprobó la versión anterior y esta sigue en borrador, sin aprobar y sin acta registrada.

## 0. Convenciones de cita y de estado

- Cada cita de código es `repo@commit ruta:línea` o `ruta:símbolo`, y corresponde a un archivo que el Executor abrió en el commit indicado (ver `runs/subagents/20261101-ws11-navegacion/result-summary.md` para el detalle de lo abierto). Dónde dice «auditoría» se cita `ui.md:N`, `infraestructura.md:N` o `deskops.md:N` = líneas de `auditoria/ui.md`, `auditoria/infraestructura.md`, `auditoria/deskops.md` de este directorio.
- Prefijos de ruta: `GU/` = `../UIs/graph_ui/frontends/mindmap/` (graph_ui `134a665`, árbol limpio salvo untracked); `SL/` = `../sldb/src/sldb/` (sldb `77bd6d0097f46efdec5e7eeb0e58d71d70b98be5`); `DK/` = este repo, leído en el HEAD `c19c6c0d` (las auditorías WS02 fijaron `215bf624`; solo se abrieron `deskops/models/*.py`, `deskops/identity.py` y `deskops/operations.py`, y el Executor no las comparó con `215bf624`; la revisión root informa que las comparó entre `215bf624` y `c19c6c0d` y que el diff es vacío, `review-source.md:7`, y el Executor de la corrección no repitió esa comparación).
- **existe** = el código leído lo muestra en ese commit. **aceptado** = tiene acta de recepción o revisión que lo diga. Hoy no hay ningún aceptado (sección 12). Toda fila de este contrato que diga «soportado» significa «existe en código»; nunca «aceptado» ni «ejecutado». No se ejecutó nada.
- `frontends/workspace/` de graph_ui (sin commit, `ui.md:158`) no es base ni se cita como evidencia.
- «No definido» siempre lleva productor o «sin productor en el DAG».
- **Leer, exponer, devolver**: «lee» = el código abre el archivo; «expone» = entrega a otra capa datos derivados de esa lectura; «devuelve» = entrega el texto. Una negación sobre «devuelve el texto» no se extiende a «lee» ni a «expone».
- **Negaciones**: cada negación de este contrato dice el alcance de su búsqueda (patrón y rutas; «en estas rutas»). Sin esa búsqueda no se afirma. Lo que hoy no existe en el código leído (inventario actual) no es la frontera de lo que se puede definir o construir: esa frontera la fijan las secciones 6 y 11 con sus productores.

## 1. Alcance y estado

**Qué fija este contrato** (lo que WS11 debe fijar según `dag.yaml:681-711`): identidad, origen y modelo opcional de un documento Markdown; nodos graph y code con origen; resolución explícita de repo/store; fuente propia frente a Code referenciado; navegación, enlaces e historia; el dominio de correspondencias que admiten foco compartido; errores de lectura y red; lectura multidesk de solo lectura; el límite de ViewDoc; clasificación de huecos; y el mapa de deltas que requieren recepción.

**Qué no fija**: escritura, guardado, whitelist, conflictos y fallos parciales (todo hueco de escritura va a WS12, `dag.yaml:723-796`); la implementación en graph_ui; Scion; Changes; ViewDoc opcional. La lectura no espera guardado ni WS12.

**Base observada**: graph_ui `134a665` (workspace integrado a1b2b22, cierre f16fcd1, `reconciliacion.md:3`); sldb `77bd6d0097f46efdec5e7eeb0e58d71d70b98be5`. Alcance heredado: `alcance.md:5` (Entrega L), `alcance.md:27` (recepción por delta).

**Dependientes directos de WS11 en `dag.yaml`** (recomputado leyendo `depends_on`): WS12, WS13, WS13.1, WS13.2, WS13.3, WS17, WS18, WS33, WS40, WS41. Son 10; la TaskDoc decía «trece nodos» y el Supervisor lo corrigió (`preflight-disposition.md`). WS15.1 consume este contrato por texto de su aceptación (`dag.yaml:1052-1092`), pero depende de WS13, no de WS11 directamente.

**Fuera de este contrato, por diseño**: el contrato básico no espera Changes (WS29), Scion (WS32-WS36, WS44), ViewDoc opcional (WS18/G_SPEC_VIEW) ni modelos (WS39).

## 2. Identidad y origen

### 2.1 Qué existe hoy

| Concepto | Qué hace el código | Evidencia |
|---|---|---|
| Identidad canónica de documento modelado | `Model:name`. El catálogo la arma como `f"{model_name}:{name}"`; la ruta de nodo la resuelve por `Model:name`, por `Model/name` o por nombre solo | `GU/workspace_routes.py:118`, `:251-269` (`_resolve_document`) |
| Nombre ambiguo | Un nombre presente en más de un modelo responde 400 «Identidad ambigua… Use Model:name» | `GU/workspace_routes.py:264-267`, `:299-300` |
| Guardia de identificador | Rechaza vacío, `..` en cualquier posición y prefijo `/` o `\` con 400. Es un criterio textual: también rechazaría un nombre legítimo que contenga `..` | `GU/workspace_routes.py:134-135` |
| Ruta del documento | Cada nodo del catálogo lleva `path` (`str(getattr(d,'path',''))`), el nodo lo repite y el contexto lo repite | `GU/workspace_routes.py:125`, `:237`, `:209` |
| Resolución de respaldo (documento que no valida) | Intenta `resolve_runtime_doc`; si falla, busca en `load_edge_index` y marca el nodo `is_degraded` con `degraded_reason`; solo busca frontmatter en rutas fijas bajo `desk/tasks`, `desk/contexts`, `desk/rituals`, `desk/roles`, `desk/runs`, `desk/relations` | `GU/workspace_routes.py:271-352` (candidatos `:314-322`) |
| Hash de campos y de archivo | `content_hash` = `doc_version(doc)` (hash de campos); `file_revision` = sha256 de los bytes del archivo si está dentro de `repo_root`, no es `.git` y no está ignorado por git | `GU/workspace_routes.py:173-198`; `SL/api/documents/document_serialization.py:24-32` (`doc_version`) |
| Qué es un documento en sldb | Un archivo Markdown con frontmatter y secciones, registrado en el store; el payload se extrae con el codec del modelo | `infraestructura.md:29-30` |

Esto **existe** y está **sin aceptar**. No hay en graph_ui un concepto de «proyecto» o «desk» en la identidad: el catálogo es de un solo store (sección 3).

### 2.2 Markdown modelado frente a no modelado

- **Modelado** = archivo vinculado a un modelo por `.sldb/store.yaml` (`include:`), nunca inferido por carpeta (`deskops.md:212`, «Reglas» de la sección C). Identidad: `Model:name`. Modelo: el del store. Hoy son 17 modelos (`deskops.md:181`, `deskops.md:185-201`).
- **No modelado** = Markdown del desk sin modelo (p. ej. issues, FAQ de `docs/`, candidatos del drawer, `desk/contexts/README.md`): 118 archivos en el universo auditado (`deskops.md:226`; la cifra es del HEAD `215bf624`). **No es corrupción** (`user-flows.md:176`). Los candidatos de drawer con forma de TaskDoc tampoco están modelados (`deskops.md:217`).

**Regla de identidad para un Markdown no modelado** (definición de este contrato; es lo que WS13.1/WS13.2 deben implementar, y no existe hoy):

1. Identidad = par `(repo, ruta)` donde `repo` es el alias del desk (sección 3) y `ruta` es la ruta relativa al root de ese repo, normalizada, con `/`. No lleva `Model:`.
2. El modelo es **opcional**: ausente significa «no modelado». La UI no lo infiere por carpeta ni por forma del contenido; si el store lo trackea, la identidad pasa a `Model:name` y la ruta queda como origen.
3. Un mismo archivo no puede tener dos identidades: si el store lo trackea, `Model:name` prevalece y el explorador no lo repite como no modelado.
4. Una ruta que no resuelve dentro del root del repo, que cae en `.git`, en un archivo ignorado por git o fuera del criterio de la sección 3.3 no tiene identidad: se muestra el error, no el contenido.

**Qué no existe hoy** (búsqueda de `read_text`, `read_bytes`, `open(` y `focus` en `GU/workspace_routes.py` y `GU/views/workspace/`, y de `read_text`/`read_bytes` en `GU/*.py`; léase «en estas rutas»): ninguna ruta del workspace de graph_ui **devuelve** a la UI el texto del archivo propio de un documento (modelado o no) como tal, ni lista Markdown no modelado. Qué **lee**, **expone** y **devuelve** hoy, para no confundirlo:

- *Lee el archivo propio y devuelve un hash*: `read_bytes` solo para `file_revision` (`GU/workspace_routes.py:196`).
- *Lee el archivo propio y devuelve datos derivados*: `read_text` en la resolución de respaldo, solo para extraer el frontmatter, bajo las rutas fijas de `:314-322` (`:326-331`); y el IR: `workspace_node` llama `editor_store.document_ir` (`:156`), que lee el archivo (`GU/sldb_adapter.py:202`) y construye el IR con `build_document_ir_json` (`:203`). Ese IR **llega entero al cliente** en `projections.document.ir` (`:157`, `:244`), incluido `surface` con el `text` de cada nodo del parser (sección 4); la UI no lo muestra.
- *Lee y devuelve texto*: `_inspect_file_reference` lee con `read_bytes` y devuelve `content` íntegro de cada archivo nombrado en `files`/`references` que pase las guardias de 3.3 (`:539-560`). Es Code referenciado (sección 2.4); si un documento se nombrara a sí mismo en esas listas, su texto llegaría por ahí, y eso no es una lectura de fuente propia ni se cuenta como tal.

`_build_code_projection` lee solo `files`/`references` del payload (`:441-451`; `ui.md:55`); `workspace_nodes` lista solo `editor_store.documents()` (`:102-127`). Sin coincidencias de `focus` en `GU/workspace_routes.py` ni en `GU/views/workspace/`. Producción: lectura de fuente propia, WS13.1; árbol y refresco, WS13.2 (huecos H-01 y H-02).

### 2.3 Nodos graph con origen

- Un nodo graph es un documento: `GU/workspace_routes.py:395-413` arma cada nodo con `id` (`Model:name`), `name`, `model_name`, `title`, `status`, `depth`. Una arista lleva `source`, `target`, `type`, `origin`, `relationDoc` (`:387-393`). El **origen de una arista** es `origin` ∈ {`relation_doc`, `schema`, `structural`} según `DocumentEdge` (`SL/api/edges/document_edge.py:17`; `EdgeRecord.metadata` documenta además `alias`, `SL/store/models/edge_record.py:16`). Para aristas `schema` el registro de sldb guarda el campo del documento que las declara y el valor tal como se escribió (`SL/store/edge_index/declared_references.py:68`, `field=field, declared=value`; también `allowed_models`, `:66`); las de composición llevan `field`, `source_field`, `ref_path` y `ref_index` (`SL/store/edge_index/composition_edges.py:55`); el índice compuesto conserva esa metadata (`SL/store/edge_index/declared_resolution.py:45`). **`DocumentEdge` no la expone** (campos `id, source, target, type, origin, relation_doc`, `SL/api/edges/document_edge.py:13-18`), la ruta de graph_ui tampoco (`GU/workspace_routes.py:387-393`) y además colapsa aristas por `(source, target, type, relation_doc)` (`:384`). Ver filas C8 y C9 de la sección 6.
- Los nodos de los extremos que no son documentos (etiquetas, modelos, campos, el store) quedan fuera de `document_edges` (`SL/api/edges/document_edges.py:18`, `:36-39`).
- El grafo es la vecindad a 1 o 2 saltos (`GU/workspace_routes.py:365-376`; `depth` solo admite 1 o 2, `:86-91`).

### 2.4 Nodos code con origen

- Un nodo code es una referencia a archivo del payload (`files` o `references`), con estados `ok`, `no_es_ruta`, `sin_repo_root`, `fuera_del_repo`, `no_existe`, `protegido`, `directorio`, `demasiado_grande`, `binario`, `error_lectura` (`GU/workspace_routes.py:481-575`). Su **origen** es la cadena original (`reference`), la ruta relativa al repo (`path`) y, si la cadena termina en `:N`, `fragment_line`, `fragment_content`, `fragment_span` (±5 líneas) (`:487-493`, `:565-571`).
- Límite de tamaño 256 KB (`GU/workspace_routes.py:19`); lenguaje por extensión, con `text` por defecto (`:20-37`, `:553`).
- Las referencias a código **no** llevan el nombre del campo de origen ni su posición en la lista: `files` y `references` se concatenan en una sola lista y los elementos que no son texto o están vacíos se omiten antes de inspeccionarse (`:441-451`); cada tarjeta lleva solo `reference` (la cadena) y su resultado (`:481-575`). Ver C4 y C4b.
- Las anclas `code:<ruta>::<símbolo>` de sldb son otra capacidad (`SL/api/anchors/record_anchor.py:15`, `infraestructura.md:94`, requiere extra `[code]`); graph_ui no las consume en estas rutas (sin coincidencias de `anchors` en los `.py`, `.js` y `.mjs` de `GU/`, fuera de `fixtures/`). No hay CST supuesto (Tree-sitter diferido, `ui.md:46`).

## 3. Resolución de repo y store

### 3.1 Lo que existe

- graph_ui resuelve **un solo store por proceso**: `WorkspaceRoutes.__init__` guarda `store_path` y `repo_root = store.parent` (`GU/workspace_routes.py:68-71`, `:612-617`); el servidor lo construye una vez con `store or SLDB_STORE` (`GU/serve.py:506-515`; default: el `.sldb` de graph_ui, `:507`, `:512`). Las rutas de Deskops resuelven una sola raíz (`DESKOPS_ROOT` absoluto o el padre del store) (`GU/deskops_routes.py:129-137`; `ui.md:87`).
- El workspace no existe en modo remote: responde 501 (`GU/serve.py:320-322`).
- La API pública de sldb **sí** recibe el store por llamada: `open_store(store, mode)` acepta un directorio `.sldb` o el alias de un enlace (`SL/api/stores/open_store.py:16-39`; `SL/api/stores/store_discovery.py:67-76`, `_resolve_store_arg`). `load_edge_index(store, include_linked=False)`, `doc_status(store, ref)`, `search(store_path, term, …)` y `document_history(store, doc_ref)` toman el store como argumento (`SL/api/edges/edge_reading.py:14`, `SL/api/stores/doc_status.py:18`, `SL/api/search.py:26`, `SL/api/documents/document_history.py:23`). No hace falta cambiar `SLDB_STORE` para leer otro store.
- **`open_store` no es solo lectura**: si el store existe, migra el layout cuando no está ya canónico (`SL/api/stores/open_store.py:37-38` → `SL/store/migration.py:72-80`, que escribe índices fuera del caso «ya canónico», `:75-76`) y agenda un re-chequeo por operación (`open_store.py:40-41`). El argumento `mode="readonly"` solo se usa cuando no se da store, para el descubrimiento y su respaldo global (`open_store.py:26-27`, `:35`); con un store explícito no cambia nada. Ver 5.4. Y `_resolve_store_arg` acepta cualquier ruta que sea un store (`SL/api/stores/store_discovery.py:69-71`) y, si no lo es, busca el argumento como alias de un enlace en los stores ancestros o global del entorno (`:72-75`, `_alias_registries`, `:58-64`): **sldb no limita roots**; cualquier límite lo pone el llamador, y un alias de sldb no es una autorización.
- Precedente en sentido contrario: `GU/views_routes.py:29-33` (`_store`) acepta del cliente cualquier directorio `.sldb` de la máquina (`store` en query o body) y las vistas pueden **escribir** ahí (`:56-66`). Eso es lo que la lectura multidesk **no** debe replicar.
- El registro de repos de deskops: `RepositoryDoc` con `name`, `id`, `path` (relativa al root del ecosistema), `status`, `description`, `tags` (`DK/deskops/models/repository.py:35-52`); `load_repository_registry` lee `desk/registry/repo-*.md`, resuelve el root y rechaza ids o roots duplicados (`DK/deskops/identity.py:65-88`); `_resolve_registered_root` acepta rutas absolutas y relativas con `..` **sin comprobar contención** (`DK/deskops/identity.py:256-262`). Hay 6 `RepositoryDoc` (`deskops.md:195,220`). `deskops list tasks --include-repos` ya lee los Boards de los repos registrados (`DK/deskops/operations.py:364-394`; `deskops.md:76`) con su propio filtro de rutas de tareas (`:1196-1210`).

### 3.2 Regla del contrato

1. **Explícita por petición.** Cada petición de lectura nombra el desk con un **alias** (cadena de un conjunto cerrado), nunca con una ruta ni con un store. El servidor traduce alias a `(root, store)` consultando el conjunto cerrado. Una petición sin alias usa el desk del proceso, y el alias que lo designa se devuelve en la respuesta.
2. **Aliases y roots autorizados: el contrato del input, no los valores** (decisión root de 2026-11-01, `review-source.md:13`). Los aliases reales son **configuración confiable suministrada por el operador** al arrancar o al seleccionar el despliegue; no son un documento que haya que generar automáticamente.
   - **Reparto**: WS11 (este contrato) fija el contrato del input; WS41 lo consume y lo valida; WS40 da la instancia temporal con la que se prueba.
   - **Contrato del input**: un conjunto cerrado de entradas `alias → (root, store)`, suministrado fuera de la petición (el cliente nunca lo aporta). Cada entrada: un `alias` (cadena que debe poder escribirse como prefijo `alias:` de una referencia, es decir cumplir `[A-Za-z0-9][A-Za-z0-9._-]*`, `SL/api/stores/doc_ref.py:17,19`; `local` ya significa «el store local» en esa sintaxis, `:18,38-39`, y está reservado en la sintaxis de enlaces, queda fuera del conjunto y el operador no puede redefinirlo: WS41 rechaza una entrada con ese alias; ver 5.2, paso 3a), el `root` del repo y el `store` (directorio `.sldb`). Los valores concretos los pone el operador: este contrato no inventa ninguno. El soporte, el formato y el punto de carga de la configuración son implementación de WS41, con estas condiciones: conjunto cerrado, fuera de la petición y sin valores reales en el repo de graph_ui ni en el corpus.
   - **Validación (WS41)**: alias único; `root` y `store` existen; cada petición resuelve alias → `(root, store)` consultando solo ese conjunto; la contención de toda ruta contra el `root` de la entrada sigue el criterio de 3.3. Al abrir el store se pasa el **directorio** resuelto, no el alias como cadena, porque `open_store` resolvería una cadena que no es directorio como alias de enlaces del entorno (3.1).
   - **Sin configuración confiable no se habilita la lectura cruzada**: toda petición con parámetro explícito de alias da E-MD1 (8.5); un prefijo escrito en un enlace de texto sigue 5.2, paso 3c, y solo se sirve el desk del proceso.
   - **Registro de deskops**: `desk/registry` da **identidad** (id, path, name) y **puede ser la fuente que el operador designe explícitamente** para armar la configuración; no es autorización automática, y que su `path` admita rutas absolutas o relativas con `..` sin comprobar contención (`DK/deskops/identity.py:256-262`) obliga a que la contención la valide el consumidor (WS41), pero no impide que el operador lo designe.
   - **Instancia de prueba (WS40)**: el generador crea dos desks temporales y su manifiesto JSON (roots, stores, commits, documentos clave; `dag.yaml:2683-2698`). Ese manifiesto es evidencia derivada (sección 10); la configuración confiable de las pruebas de WS41 la suministra la prueba como lo haría un operador. WS41 se prueba contra los dos stores de WS40 (`dag.yaml:2725-2731`); la publicación real (WS43) no define aliases.
   - No se inventan valores de alias ni de roots, ni modelo, ni productor, ni decisión humana nueva en este contrato (H-10, H-11).
3. **Sin cambiar `SLDB_STORE` global** ni abrir un store por una ruta recibida del cliente. Cada petición conserva su `(root, store)`; no hay estado compartido entre peticiones.
4. **Alias no autorizado, ruta que escapa y store ausente** dan error visible con su causa (sección 7, E-MD1 a E-MD3). El estado de un enlace de sldb (`ok` / `missing` / `not-a-store`) está en `SL/api/stores/store_links.py:15-39` y el de una referencia (`ok` / `missing` / `ambiguous` / `link-missing` / `link-broken`) en `SL/api/stores/doc_ref_status.py` y `doc_status.py:18-33`.

### 3.3 Rutas seguras: el criterio sale del código existente

Criterio mínimo, tomado de lo que ya hace `_inspect_file_reference` (`GU/workspace_routes.py:481-575`). Esta tabla son las **guardias generales** de toda lectura de archivo por UI (fuente propia, FAQ, contextos, Board, Code, explorador). Las guardias propias de las referencias de TaskDoc están aparte, en «Guardias específicas», y no se aplican al resto:

| Criterio | Qué hace el código | Evidencia |
|---|---|---|
| Contención | Resuelve (`resolve()`, sigue symlinks) y exige `is_relative_to(repo_root)`; si no, `fuera_del_repo` | `:501-518` |
| `.git` | Cualquier parte `.git` de la ruta → `protegido` | `:521-524` |
| Ignorado por git | `git check-ignore -q` con timeout de 2 s; si falla la verificación, **falla cerrado** (`protegido`). Si el repo no tiene `.git`, no evalúa nada | `:460-479` |
| Directorio | `directorio`, no se lista | `:531-532` |
| Tamaño | Más de 256 KB → `demasiado_grande` | `:536-537` |
| Binario | Un byte nulo → `binario` | `:540-541` |
| Codificación | UTF-8 con reemplazo marcado (`utf-8-replaced`) | `:543-549` |
| URL externa | `http(s)://` → `no_es_ruta`, no se abre | `:484-485` |

**Guardias específicas de referencias de TaskDoc** (no son criterio general): `DeskRoutes.board` valida cada entrada de `Board.tasks` y exige estar dentro del root, dentro de `desk/tasks`, sufijo `.md` y nombre distinto de `Board.md` (`GU/deskops_routes.py:36-40`, la condición en `:39`). Otra copia con el mismo propósito, para los Boards de repos registrados, exige además que el nombre empiece por `task-` y que el archivo exista (`DK/deskops/operations.py:1196-1210`). Ambas responden a «¿esta referencia del Board es una tarea?» y **no** deben aplicarse a la lectura de FAQ, contextos, Board, fuente propia ni explorador: bloquearían archivos legítimos fuera de `desk/tasks`. `_inspect_file_reference` no las aplica (`GU/workspace_routes.py:481-575`, sin ninguna comparación con `desk/tasks`). Un lector que quiera restringir por tipo de documento lo declara en su propia lista de permitidos (WS13.2), no hereda ésta.

**No cubierto por el código existente** (por lo tanto, hueco o decisión de WS13.2/WS41, no inventado aquí):

- Una **lista de permitidos** de carpetas o extensiones: cualquier archivo de texto no ignorado dentro del repo se lee, aunque no sea del desk; las extensiones desconocidas se leen como `text` (`:553`). No hay criterio sobre archivos sensibles que no estén en `.gitignore`.
- La verificación `check-ignore` no existe fuera de un repo git (devuelve «no ignorado»): en el corpus sin repo git no protege nada.
- Condiciones de carrera entre `resolve()` y la lectura (TOCTOU): no tratadas.
- La guardia del identificador de nodo (`'..' in ident`) es textual (`:134`).
- Resolución de enlaces `[[destino]]` de sldb: `resolve_link_target` prueba el destino contra el store, contra el directorio del documento y contra `Path(destino)` absoluto o relativo al directorio actual del proceso (`SL/links/resolver.py:33-35`), y `recover_links` lee el destino con `#ancla` antes de retornar (`SL/links/recovery.py:13-14`) y recursa si `depth > 1` (`:29-30`). Reaplicar la contención **después** de `recover_links` llega tarde: el destino ya se resolvió y se leyó. El orden obligatorio está en 5.2 (analizar y autorizar antes de cualquier lectura o recursión).

El **criterio que este contrato fija** para toda lectura de archivo por UI: todos los de la tabla de guardias generales; más, para el explorador de no modelados (H-02), que el WS13.2 declare su lista de permitidos antes de implementar. No se declara hoy cuál es.

## 4. Fuente propia frente a Code referenciado

- **Fuente propia** = el archivo Markdown del documento (modelado o no). **Code referenciado** = los archivos que el documento nombra en `files`/`references`. Son cosas distintas y no se mezclan en una pestaña.
- Hoy `projections.code` es solo Code referenciado (`GU/workspace_routes.py:431-458`). La fuente propia **no tiene proyección**. `file_revision` solo hashea el archivo propio, no lo entrega (`:180-198`).
- La pestaña Documento muestra el IR (secciones) y los campos, y badges de línea `L<ini>-<fin>`; no muestra el texto crudo (`GU/views/workspace/node/workspace-view.js:41-52`, `:325-379`; `GU/shared/document-ir.mjs:11-26`).
- sldb entrega, junto al IR, `surface`: los nodos crudos del parser con su `text` y su rango de líneas (`SL/api/records/utils.py:10-19`; `SL/core/ir/document_ir.py:8-14`). `workspace_node` ya recibe ese IR (`GU/workspace_routes.py:153-161`; `SL/api/documents/document_ir_serialization.py:13`). Que `surface` reconstruya el texto íntegro **no está verificado**: no se afirma, y la reserva se mantiene (`surface.text` no prueba fuente íntegra). `render_document_markdown` **no** es la fuente: renderiza el payload por la plantilla del modelo (`SL/api/documents/document_render.py:19-28`).
- **En sldb, quién lee el archivo del documento y qué entrega** (búsqueda de `read_text`, `read_bytes` y `.open(` en `SL/api/`, `SL/links/` y `SL/cli/serve/`; léase «en estas rutas»; las lecturas de modelos, índices y plantillas no se enumeran). *Lee y entrega datos derivados*: IR y secciones en `SL/cli/serve/document_routes.py:62`, `SL/cli/serve/sections_routes.py:46`, `SL/api/documents/document_ast.py:22` y `SL/api/records/ast_target.py:38`; procedencia en `SL/api/documents/document_serialization.py:20`; registros de búsqueda en `SL/api/records/iter_records_docs.py:35,44`. *Lee para uso interno*: payload anterior al guardar (`SL/api/documents/payload_save.py:54`), validación al registrar (`SL/api/documents/track_document_file.py:47,48,68`), texto previo al estampar (`SL/api/documents/provenance_stamp.py:31`). *Lee y devuelve texto*: `compose_document` (`SL/links/composer.py:9-31`, exportada por `sldb.links`, `SL/links/__init__.py:6,15`; no por `sldb.api`) lee el archivo con `read_text` y devuelve su `markdown` con las transclusiones `![[…]]` expandidas, siguiendo enlaces a otros archivos con `resolve_link_target`; no es una lectura de bytes del archivo ni segura para un destino no autorizado. En estas rutas no se encontró otra operación que devuelva el texto del archivo del documento tal cual. La capacidad de **guardado** raw-source no existe (`infraestructura.md:33`, productor WS20) y no se confunde con la de lectura.
- Lectura de fuente propia (modelada o no): hueco H-01, clase API (la ruta de lectura no existe en graph_ui; graph_ui puede leer el archivo con el criterio de la sección 3.3, sin pedir nada a sldb), dueño graph_ui, productor WS13.1.
- **«Mismo origen»** (`dag.yaml:841-871`): el render y la fuente salen **de la misma lectura o revisión**, no solo de la misma ruta. Observable: la respuesta que entrega ambos lleva la revisión (hash de bytes) de la lectura de la que salieron los dos, o los dos se derivan de una sola lectura de bytes, y si difieren se ve. Hoy no se cumple por construcción: el IR lee el archivo en `GU/sldb_adapter.py:202` (llamado desde `GU/workspace_routes.py:156`) y el hash de revisión lo lee otra vez, después, en `GU/workspace_routes.py:196`; una edición entre ambas lecturas daría un `file_revision` distinto del texto del que salió el IR. El mecanismo es de WS13.1; no hay dos copias del documento: la copia es una instancia con el mismo origen, no cada representación (`dag.yaml:871`).
- La edición de fuente espera WS20/WS21 y es de WS12; esta lectura no la necesita.

## 5. Navegación, enlaces e historia

### 5.1 Navegación y historia que existen

- Estado en URL: `?id=&depth=&tab=`; cada cambio de nodo, profundidad o pestaña hace `pushState` (`GU/views/workspace/node/workspace-view.js:71-86`, `:213-226`); `popstate` vuelve a leer la URL (`:88-100`, `:196-199`). Las pestañas son `document`, `graph`, `code` (`GU/views/workspace/node/workspace.mjs:5` `TABS`): son **proyecciones** del mismo documento, no pestañas de documentos.
- Seguir una relación o un nodo del grafo cambia el documento activo (`workspace-view.js:222-226`, `:419`, `:537`). El catálogo se carga al montar; «Actualizar» recarga el nodo, no el catálogo (`:102-136`, `:296`; `ui.md:56`).
- Filtro local por id, título y modelo (`workspace.mjs:11` `filterCatalog`); filtro de aristas por tipo (`:83`).
- **La URL no lleva repo ni alias**: no puede distinguir dos desks (H-12, API, graph_ui, WS41; con WS13.3 para la historia).

### 5.2 Enlaces

- **Sintaxis de enlace en el texto que admite sldb hoy** (`SL/links/parser.py:6-7`; `infraestructura.md:88-90`): `[[destino]]`, `![[destino]]` (transclusión) y `[pred:: [[destino]]]`. El `destino` es cualquier texto sin `]`, recortado (`parser.py:6,11,15`); `parse_links(markdown, predicate_types)` es una función pura que no abre archivos (`parser.py:17-20`). `split_anchor` separa `base#Sección` por el primer `#` (`SL/links/sections.py:15-18`; la sección se compara sin distinguir mayúsculas, `:30-37`). `parse_links` se exporta en `sldb.links` (`SL/links/__init__.py:3,11`); `split_anchor` vive en `sldb.links.sections` y no se reexporta.
- **Referencias públicas con prefijo de store** (`SL/api/stores/doc_ref.py`, `split_doc_ref` exportada por `sldb.api`, `SL/api/__init__.py:64,126`; `doc_status`, `:66`): `alias:referencia`, con alias `[A-Za-z0-9][A-Za-z0-9._-]*` (`doc_ref.py:17,19,22-25`) y `referencia` = `name`, `Model/name` o ruta rastreada (`:33`, `matches_doc_ref`, `:43-45`). `split_doc_ref` solo da alias si el store de lectura tiene un enlace directo con ese nombre (`stores add --name`) y, si no, deja la referencia entera (`:6-7`, `:40`); `local:` nombra el store local (`:18,38-39`). Los IDs de la GUI `Model:name` tienen la misma forma `x:y`, pero **no son** referencias de sldb: `Model:name` es el export id del índice de aristas y del catálogo (`GU/workspace_routes.py:118`; `declared_references.py:84-86`), mientras que `matches_doc_ref` compara con `Model/name` (`doc_ref.py:45`).
- **El parser admite el prefijo; el resolutor no.** `[[alias:Model/name]]`, `[[alias:name]]` y `[[alias:ruta#Sección]]` parsean como un único `destino` (`parser.py:6`), sin obstáculo sintáctico. Pero `resolve_link_target` no tiene rama de alias: prueba `alias:x` como nombre rastreado, como ruta relativa al documento y como `Path` absoluto o relativo al directorio actual del proceso (`SL/links/resolver.py:33-35`). Además `_tracked_documents` indexa por `name` solo, no por `Model:name` (`:13`). Por eso `recover_links` (`SL/links/recovery.py:23-31`) y `audit_links` (`SL/links/audit.py:10`) **no sirven como resolutor de la UI** ni para sanear después (3.3): `recover_links` lee el destino con ancla (`:13-14`) y recursa (`:29-30`) tras resolver, y `resolve_link_target` toca el sistema de archivos con el destino tal cual.
- **Tratamiento obligatorio de un enlace de texto** (para WS13.1 con el desk propio y para WS41 entre desks; fija sintaxis y orden para que WS40 y WS17 puedan authorar enlaces reales). Orden: (1) tomar el texto ya leído con las guardias de 3.3 y extraer enlaces con `parse_links`; (2) `split_anchor`; (3) clasificar el prefijo de la base con la gramática de `doc_ref.py:19`, en este orden y una sola vez: (a) `local:` se reconoce **antes** que cualquier alias: está reservado y fuera del conjunto del operador, designa el **desk del documento que contiene el enlace, que es el de la petición que lo leyó y ya está autorizado** (no el desk inicial del proceso si se está viendo otro desk) y se retira una sola vez; (b) si no, un prefijo que coincide con un alias autorizado de 3.2 designa ese desk y se retira; (c) si no, no es alias: la cadena entera es un nombre local en el desk de origen (regla de `doc_ref.py:6-7`), también sin configuración confiable, y si no resuelve se informa como referencia rota con origen y causa (E5), **no** como E-MD1. Lo que queda tras retirar un prefijo es `resto` y no se vuelve a interpretar como alias ni como `local:`; (4) **autorizar el root del desk destino antes de leer nada**; (5) normalizar el resto y, si es una ruta, comprobar contención contra el root autorizado antes de pasarla a cualquier API (E-MD2); (6) resolver sobre el **store objetivo explícitamente autorizado**: `doc_status(<directorio del store>, "local:" + resto)`, con `resto` en la forma `Model/name`, `name` o ruta rastreada (nunca `Model:name`, que sin `local:` `doc_status` informaría como `link-missing`, `SL/api/stores/doc_status.py:31-32`). El prefijo `local:` es **obligatorio**, también para un destino local: `doc_status` llama por dentro a `split_doc_ref` (`doc_status.py:26`), que seguiría cualquier enlace directo de ese store cuyo nombre coincida con lo que hay antes de los dos puntos (`doc_status.py:27-28`, `doc_ref.py:40`), es decir un store que el operador no autorizó; con `local:` el resto queda entero y solo se busca en ese store (`doc_ref.py:38-39`; `doc_status.py:29`). Como `doc_ref.py:38-39` quita solo el primer prefijo, `local:foo:bar` designa literalmente `foo:bar`: por eso el `local:` del autor se retira en (3a) y el del envoltorio se pone una sola vez, sin `local:local:` salvo que el `resto` literal empiece así. Por lo mismo, tampoco se llama `split_doc_ref` con el store de origen; (7) validar también la contención del `path` del resultado (`DocRefStatus.path`, `SL/api/stores/doc_ref_status.py:16`) antes de abrirlo; (8) solo entonces leer con la lectura protegida de WS13.1/13.2, y comprobar la ancla con `extract_section` sobre el texto leído (`SL/links/sections.py:30-37`); (9) `include_linked=False` en toda lectura de índice (el defecto de `load_edge_index` es `True`, `SL/api/edges/edge_reading.py:14`) y sin federación automática. `doc_status` cubre documentos rastreados; un Markdown no modelado se resuelve con la resolución protegida de archivo de WS13.1/13.2, no con un modelo falso. Una referencia rota o un destino no resuelto se muestra con su origen y su causa y no abre nada.
- **Ejemplos del tratamiento** (por lectura de `doc_ref.py:38-40` y `doc_status.py:26-29`; no se ejecutó nada). Documento de origen en el desk `A`, visto con `A` autorizado; `b` es alias autorizado del desk `B`; `foo` no es alias autorizado y `A` puede tener un enlace de store llamado `foo`:

| Destino escrito | Clasificación | Llamada | Resultado esperado |
|---|---|---|---|
| `[[TaskDoc/x]]` | Sin prefijo, desk `A` | `doc_status(A, "local:TaskDoc/x")` | Busca solo en `A` |
| `[[local:TaskDoc/x]]` | (3a), desk de origen | `doc_status(A, "local:TaskDoc/x")` | Igual al anterior. **Nunca** `local:local:TaskDoc/x` |
| `[[local:TaskDoc/x]]` en un documento de `B` | (3a), desk `B` | `doc_status(B, "local:TaskDoc/x")` | Busca en `B`, no en el desk inicial del proceso |
| `[[local:foo:bar]]` | (3a), resto literal `foo:bar` | `doc_status(A, "local:foo:bar")` | Literal `foo:bar` en `A`; no salta al enlace `foo` |
| `[[foo:bar]]` | (3c), nombre local | `doc_status(A, "local:foo:bar")` | Literal en `A`; si no resuelve, E5. No salta al enlace `foo` ni da E-MD1 |
| `[[b:TaskDoc/x]]` | (3b), desk `B` | `doc_status(B, "local:TaskDoc/x")` | Busca solo en `B` |
| `[[b:local:x]]` | (3b), resto literal `local:x` | `doc_status(B, "local:local:x")` | Literal `local:x` en `B`; el resto no se reinterpreta |
| `[[b:TaskDoc/x]]` sin configuración confiable | (3c), nombre local | `doc_status(A, "local:b:TaskDoc/x")` | Literal en `A`; si no resuelve, E5 |
| Parámetro explícito de alias `zzz` en una petición | No es enlace de texto | Ninguna | E-MD1; no se abre nada |
- La auditoría de enlaces del store (`audit_links`, `GET /lint`) informa enlaces no resueltos (`SL/links/audit.py:10`; `SL/cli/serve/lint_routes.py:25,58`).
- **graph_ui no consume `[[…]]` ni `sldb.links` en estas rutas**: sin coincidencias de `sldb.links` en los `.py` de `GU/`; las coincidencias de `[[` son literales de arreglos en módulos de notación, la de `/lint` son los comentarios de proxy de `GU/serve.py:10,241` y la de `recover` es `GU/compilation.py:65` (no relacionadas). Seguir un enlace de texto, hoy, no existe en el workspace (H-06: integración de lectura en graph_ui por la composición de arriba, productor WS13.1; la referencia rota la consume WS15.1).
- **Enlaces entre desks**: ver sección 8.4.
- Referencias por campo: aristas `references` y `contains` declaradas por el modelo (`SL/store/edge_index/declared_references.py:38-71`); el workspace las muestra como relaciones entrantes y salientes (`GU/workspace_routes.py:200-201`; `workspace-view.js:518`, `:537`).
- Backlinks: `incoming_relations` del contexto (`GU/workspace_routes.py:200`) son las aristas entrantes de la vecindad (1 o 2 saltos), no un cálculo con la API de grafo completa (`ui.md:69`). Los backlinks por `edges_to` o `graph` no se consumen (`SL/api/edges/edge_reading.py`, `reconciliacion.md` C-44).

### 5.3 Historia

- **Historia de navegación** = la del navegador (arriba) y, cuando WS13.3 la entregue, la de documentos abiertos de la sesión. Es disposición local (P07, `decisiones.md:31`); no es documento compartido. «Volver sigue el orden inverso» y la restauración de foco son aceptación de WS13.3 (`dag.yaml:933-973`); no existen hoy.
- **Clave de sesión de modelado** (historia, documentos abiertos y foco guardado por documento de WS13.3): se compone de **alias del desk** e **identidad local del documento** (`Model:name` para un modelado; la ruta relativa al root para uno no modelado, 2.2) y los dos componentes viajan juntos, de modo que dos desks con el mismo `Model:name` no colisionen. Este contrato fija los componentes y que no colisionen; **no fija una sintaxis de cadena** (`runs/subagents/20261101-ws11-correccion/preflight-disposition.md`). Hoy la URL y el estado de sesión usan solo el `Model:name` (5.1): la clave con alias es lo que H-12 incorpora.
- **Historial Git** = otra cosa. `document_history(store, doc_ref)` devuelve las versiones comprometidas de un documento; fuera de git devuelve vacío (`SL/api/documents/document_history.py:1-7,23`; `infraestructura.md:60`). graph_ui no lo usa en el workspace. El diff por tarea y repo es WS27.1 (H-13).

### 5.4 Efecto de lectura

Lo que el código leído muestra (no se ejecutó nada; los efectos son los que dicen el código y las docstrings, sin confirmar):

- `_build_graph_neighborhood` llama a `document_edges` (`GU/workspace_routes.py:356-359`), que invoca `rebuild_edges(..., wait=True)` antes de leer (`SL/api/edges/document_edges.py:30`). `rebuild_edges` abre el store en modo por defecto, toma el lock del store y reconstruye los índices semántico, de secciones y de aristas que se movieron (`SL/api/edges/rebuild_edges.py:33-38`); su docstring dice que sobre un store al día no escribe nada (`:20-21`). La docstring de `workspace_routes.py:3` dice «Strictly read-only»; con esta cadena de llamadas la lectura puede escribir archivos derivados y puede esperar el lock.
- `load_edge_index` documenta que «Reading never rebuilds» (`SL/api/edges/edge_reading.py:14-26`) y los módulos de composición del índice que se abrieron no escriben (búsqueda de `write`/`save`/`dump`/`mkdir`/`unlink` en `SL/store/edge_index/compose.py`, `shard_reading.py`, `shard_signature.py`, `edge_index.py` y `cache_keys.py`: sin coincidencias de escritura). Pero **no evita la migración transitiva**: `load_edge_index` llama `open_store(store, mode="readonly")` (`edge_reading.py:28`) y `open_store` migra el layout si el store existe y no está ya canónico (`SL/api/stores/open_store.py:37-38`; `SL/store/migration.py:72-80`). `_check_problems_for_node` de graph_ui también pasa por `load_edge_index` (`GU/workspace_routes.py:584`) en cada respuesta de nodo.
- `doc_status` y `document_history` tienen la misma entrada: `open_store(store, mode="readonly")` (`SL/api/stores/doc_status.py:25`; `SL/api/documents/document_history.py:26`). La docstring de `doc_status` («Asking never writes») se refiere a que el store consultado no gana entradas, modelos ni hashes de los documentos que referencia (`doc_status.py:3-4`); **no garantiza cero escrituras** del propio `open_store`. `mode="readonly"` controla el descubrimiento y su respaldo global, no las escrituras (`open_store.py:26-27,35`).

**Obligación de este contrato (lectura sin mutaciones)**: (a) los stores que se leen están preparados y canónicos **fuera del request**; ninguna petición de lectura migra ni reconstruye como efecto de leer; (b) no se asume que `mode="readonly"` ni `load_edge_index` basten; (c) al ejecutar cada consumidor se comprueba de verdad que las llamadas escogidas no escriben; **criterio observable: tras la lectura, el store (sus archivos y su estado de versión) no cambió**. El medio de la comprobación es de los consumidores. Si con la API pública no puede sostenerse (c), queda como **hueco con dueño** y el caso se bloquea antes de implementar; no se resuelve con un workaround sobre el formato interno ni con una API inventada, y si se prueba una falta de capacidad, el intake explícito en el repo dueño y su tarea van **antes** del workaround (no se agrega una tarea de SLDB por reflejo). **Dueños**: el caso del store propio pertenece al delta de lectura de WS13.1 y a la ruta que consuma WS24; el segundo desk lo verifica WS41. Ver H-14.

## 6. Foco y correspondencias

**Dominio de la tabla**: selecciones que una persona puede hacer en un documento abierto (texto, graph, code) y el destino en otra representación **del mismo documento** o en otro documento. «Foco» = elemento seleccionado **dentro** de un documento (`dag.yaml:857-859`); el documento activo identifica la pestaña. **Navegación** = cambiar el documento activo: es otra cosa y no demuestra foco interno. **Regla**: sin mapeo no hay correspondencia, y ninguna fila se da por soportada por omisión; cada representación muestra solo la correspondencia que realmente existe y no se inventa un resaltado equivalente donde falta.

Cada fila separa tres cosas, que no se mezclan: **datos disponibles** (qué entrega ya sldb o graph_ui, con su procedencia), **interacción existente** (qué hace hoy la UI con eso) y **comportamiento futuro comprometido** (qué compromete este contrato, con su productor). «Existe» indica solo que el código lo muestra; nada está aceptado (sección 12).

**Estado del foco hoy**: no hay estado de foco. Sin coincidencias de `focus` en `GU/workspace_routes.py` ni en `GU/views/workspace/` (búsqueda); el único estado de selección es `selectedId` (un documento) más `depth` y `tab` (`workspace-view.js:57-59`). La tabla describe, por tanto, el **dominio definible** (la frontera de lo realizable con datos reales, no el inventario de lo que la UI hace hoy) y lo que falta para cada fila.

| # | Selección origen | Destino | Correspondencia real | Evidencia | Estado |
|---|---|---|---|---|---|
| C1 | Nodo vecino en el graph | Documento activo (misma identidad `Model:name`) | El `id` del nodo del grafo es la identidad canónica del catálogo | `GU/workspace_routes.py:118`, `:395-413`; `workspace-view.js:222-226`, `:419` | **Navegación**, no foco. Datos: `id` = `Model:name`. Interacción existente: el clic cambia `selectedId` y la URL (existe, no aceptado). Futuro: ninguno propio; no demuestra foco interno |
| C2 | Relación entrante o saliente del contexto | Documento origen o destino | Las aristas llevan `source`/`target` = `Model:name` | `GU/workspace_routes.py:200-201`, `:387-393`; `workspace-view.js:518`, `:537` | **Navegación**, no foco. Datos: `source`/`target`. Interacción existente: el botón cambia `selectedId` (existe, no aceptado). Futuro: ninguno propio |
| C3 | Opción del catálogo | Documento activo | Mismo id | `workspace-view.js:260-264` (selector `onChange`→`handleSelectNode`) | **Navegación**, no foco. Interacción existente: cambia `selectedId` (existe, no aceptado). Futuro: ninguno propio |
| C4 | Entrada de `files`/`references` en el texto/payload | Tarjeta Code de esa referencia | Cada tarjeta lleva `reference` (la cadena original) y `fragment_line` si hay `:N`; las dos listas se concatenan en orden (`files`, luego `references`) y se omiten los elementos vacíos o no textuales | `GU/workspace_routes.py:441-451`, `:487-493`, `:565-571`; `workspace-view.js:15-39`, `:454-456` | **Tarjeta derivada pasiva.** Datos: la tarjeta y su `reference`. Interacción existente: **ninguna** entre el texto y la tarjeta; `CodeFileView` recibe solo `file`, sin callback de selección (`:15`, `:455`), y el campo mostrado en la pestaña Documento no apunta a la tarjeta (`:351-363`). No es una interacción texto→Code existente. Futuro: foco de la referencia con procedencia real (documento, campo, posición, valor), WS13.1, depende de H-03 |
| C4b | Tarjeta Code | Campo (`files` o `references`) del documento | El campo de origen y la posición se pierden: las dos listas se concatenan antes de inspeccionarse. El IR sí tiene un nodo por campo, pero una lista es **un** nodo con toda la lista como valor (`flatten_payload` no desagrega listas) | `GU/workspace_routes.py:441-451`; `SL/api/records/flatten.py:3-10` | **Sin correspondencia hoy**: datos perdidos en la ruta. Futuro: preservar `files`/`references` y la posición de cada elemento antes de concatenar (H-03); identificar la referencia por documento, campo, posición y valor. Hueco H-03 |
| C5 | Sección del texto (IR `structure`) | Rango de líneas del Markdown propio | Cada sección lleva `span.line_start/line_end` (el fin se extiende hasta la siguiente sección de igual o mayor rango, `extract.py:52-59`); cada nodo `surface` lleva `text` y `span` | `SL/api/records/build_ir.py:39`, `:64`; `SL/api/records/extract.py:41-59`; `SL/api/records/utils.py:10-19` | Datos reales de sldb, ya enviados al cliente (`GU/workspace_routes.py:157`). Interacción existente: solo el badge `L<ini>-<fin>` (`workspace-view.js:41-52`); no hay vista de texto con líneas ni foco. Futuro: foco por sección y span de **la misma fuente** (lectura o revisión, sección 4), WS13.1. Hueco H-04 (documentos modelados) |
| C5b | Sección o línea de un Markdown **no modelado** | Estructura | En graph_ui no hay hoy ninguna ruta que produzca estructura para un Markdown sin modelo: `workspace_node` obtiene el IR sobre un documento resuelto del store. En sldb, `extract_sections(markdown)` recibe solo el texto (`SL/api/records/extract.py:6-13`; importable de `sldb.api.records`, `records/__init__.py:12,28`) y `build_document_ir_json` está exportado (`SL/api/__init__.py:14`). El builder no consulta el registro de modelos ni exige un modelo registrado, ni por lectura un valor de modelo no nulo: consume un descriptor con las claves `store`, `path`, `name`, `payload`, `model` y `semantic_tags` (`SL/api/records/build_ir.py:20-21`, `:38`, `:62-63`, `:69-74`, `:81-82`); `MeaningNode.model` admite `None` (`SL/core/ir/meaning_node.py:9`) y `context.semantic` acepta valores arbitrarios (`SL/core/ir/document_context.py:6`) | `GU/workspace_routes.py:151-165`; `GU/sldb_adapter.py:178-215`; `SL/api/records/extract.py:6-13`; `ui.md:55` (solo para la ausencia de Markdown sin modelo en el workspace) | **Sin ruta actual en graph_ui; reutilización por verificar.** No se inventa un modelo para satisfacer una exigencia que el builder no tiene. No se afirma compatibilidad ejecutada ni una API de sldb lista para este caso: la reutilización con un descriptor y `model=None` se verifica al implementar WS13.1, y falta la ruta de graph_ui. Futuro: la estructura y el foco de un no modelado dependen de H-01 y de verificar esa reutilización (WS13.1). Hueco H-01/H-04 |
| C6 | Campo del payload (`field_path`) | Sección que lo contiene | `owning_section` por campo, **opcional**: `str \| None` con defecto `None` (`SL/core/ir/meaning_node.py:12-14`); se asigna `field_section_map.get(field_path)` (`build_ir.py:75`) y el mapa es `{}` si la plantilla y el documento renderizado no corresponden (`SL/api/records/map_fields.py:43-56`, `:59-74`); se deriva del encabezado previo al marcador de la plantilla (`:15-20`, `:39-40`). No es un dueño garantizado ni el rango exacto del campo | `SL/api/records/build_ir.py:68-78`; `SL/api/records/map_fields.py:22-26`, `:43-74`; `GU/shared/document-ir.mjs:8-9`, `:11-17` | Dato opcional de sldb; la UI no lo usa (`irFields` no lo lee, `document-ir.mjs:11-17`; el comentario de `:8-9` dice que en el shape observado viene `null`, sin que el Executor lo haya ejecutado). Futuro: foco de campo y de contenedor cuando el dato exista (WS13.1); si es `None`, no hay resaltado de sección. Hueco H-04 |
| C7 | Campo del payload | Rango de líneas | `_build_field_nodes` no asigna `span` a los campos (queda el `SourceSpan` por defecto, `SL/core/ir/meaning_node.py:15`); la UI ya asume líneas nulas para el frontmatter (`document-ir.mjs:18-22`) | `SL/api/records/build_ir.py:68-78` | **Sin soporte**: el span exacto por campo no existe. **No bloquea** el foco de campo ni de contenedor (C6). Hueco H-05 |
| C8 | Campo de referencia o contención del texto | Arista del graph | sldb guarda el campo y el valor declarado en el registro de arista (`field`, `declared`, `allowed_models`; en composición `field`, `source_field`, `ref_path`, `ref_index`); `DocumentEdge` y la ruta de graph_ui los omiten, y la ruta **deduplica** por `(source, target, type, relation_doc)`: varios campos hacia el mismo destino con el mismo tipo colapsan en una arista | `SL/store/edge_index/declared_references.py:64-71`; `SL/store/edge_index/composition_edges.py:55`; `SL/api/edges/document_edge.py:13-18`; `GU/workspace_routes.py:384`, `:387-393` | **Sin correspondencia hoy en la UI.** Datos: `load_edge_index(...).edges[].metadata` (`SL/api/edges/edge_reading.py:14`; `SL/store/models/edge_record.py:16`); solo las aristas `schema` llevan campo, las `relation_doc` no. Futuro: foco de la arista con **todas** sus procedencias (campo y valor), preservando multiplicidad. Hueco H-03b |
| C9 | Arista del graph | Campo del texto que la declara | Inverso de C8, pero no uno a uno: por la deduplicación de `:384` una arista mostrada puede venir de **varios** campos, y un campo con lista produce varias aristas | `GU/workspace_routes.py:384`; `SL/store/edge_index/declared_references.py:64-71` | **Sin correspondencia hoy.** Futuro: mostrar el conjunto de campos que la declaran; **no se elige arbitrariamente un campo inverso** cuando hay varios. Hueco H-03b |
| C10 | `[[doc]]` en el texto | Documento destino | El parser admite `[[destino]]` (con `alias:` y `#Sección` dentro del destino), pero `recover_links` y `resolve_link_target` no son un resolutor seguro para la UI (5.2); graph_ui no consume `sldb.links` | `SL/links/parser.py:6-7`; `SL/links/resolver.py:33-35`; `SL/links/recovery.py:13-14`, `:29-30`; búsqueda en `GU/` sin consumo (5.2) | **Sin interacción hoy** (existe en sldb la sintaxis, no un resolutor seguro). Futuro: seguir el enlace por la composición de 5.2 (parse, ancla, autorización, `doc_status` o lectura protegida), WS13.1 (desk propio) y WS41 (entre desks). Hueco H-06 |
| C11 | Línea o archivo en Code | Sección, campo o nodo graph | Dos casos distintos. (a) **Foco de la referencia explícita**: la tarjeta es una entrada de `files`/`references`; su correspondencia con el campo y la posición en el texto puede definirse cuando H-03 conserve campo y posición. (b) **Mapeo semántico de las líneas de un archivo externo** a una sección, un campo o un nodo del grafo: no hay correspondencia; el archivo de Code no es un nodo del grafo ni se atribuye a uno | `GU/workspace_routes.py:431-458`; `dag.yaml:857-859` | (a) **Futuro comprometido** por la aceptación de WS13.1 (`dag.yaml:860-871`): seleccionar la tarjeta fija el foco de su referencia en el texto con la procedencia de C4 y C4b; en el graph solo si existe una arista con esa procedencia (C8), nunca por atribuir el archivo a un nodo. (b) **Sin soporte**, sin productor y sin compromiso. Hueco H-05b |
| C12 | Línea o sección del texto | Línea de Code | No hay mapeo texto→código (prohibido inventarlo, `dag.yaml:857-859`) | — | **no soportado, declarado así**. Sin productor y sin compromiso de producirlo |
| C13 | Nodo graph de otro desk | Documento de otro desk | No existe: el workspace tiene un store y la URL no lleva repo | `GU/workspace_routes.py:68-71`; sección 3 | **no soportado hoy**. WS41 (H-12, H-10) |
| C14 | Rango de líneas dentro de un archivo Code (F17) | Rango en el texto | Hay `fragment_line` y `fragment_span` de ±5 líneas: `:N` es **contexto** alrededor de una línea, no un rango elegido por la persona (el cliente repite el ±5, `workspace.mjs:31-61`) | `GU/workspace_routes.py:565-571`; `GU/views/workspace/node/workspace.mjs:31-61` | Se separan dos cosas. (a) **Rango local de Code** (archivo, revisión, líneas): F17 pide «archivo o rango» (`vistas.md:345`); hoy solo existe el contexto `:N±5` y la selección de rango por la persona no existe; es del delta de WS13.1. (b) **Traslado de ese rango al Markdown**: no está comprometido por F17 (`vistas.md:349,351`: no se inventa mapeo texto-código); sin productor. H-05b |

### 6.1 Dominio de foco de WS13.1: lo que existe y lo que este contrato compromete

**Lo que existe hoy** no es foco: C1-C3 solo cambian `selectedId` y navegan a otro documento; C4 es una tarjeta derivada pasiva sin callback de selección. Ninguna de las cuatro filas demuestra un foco interno por documento.

**Dominio futuro comprometido de WS13.1** (decisión root 1 de 2026-11-01, `review-source.md:10`): un **foco interno por documento, distinto de la navegación**, definido solo con **procedencia real**:

1. *Sección y span de la misma fuente*: `structure[].span` del IR, calculado de la misma lectura o revisión que el texto mostrado (C5; sección 4, «mismo origen»).
2. *Campo / `field_path`*: el nodo `field` del IR, con su `owning_section` solo cuando exista (C6) y sin span exacto (C7, que no bloquea el foco de campo ni de contenedor).
3. *Referencia de archivo*, identificada por **documento, campo, posición y valor** (C4, C4b, C11a; requiere que H-03 conserve campo y posición antes de concatenar).
4. *Arista `schema`* con sus procedencias: campo y valor declarado, o `source_field`/`ref_path`/`ref_index` en composición, y todas las que colapsen en una arista mostrada (C8, C9).

Cada representación (texto, graph, Code) muestra **solo la correspondencia que existe** para ese elemento y no inventa un resaltado equivalente donde falta: el archivo externo no se atribuye a un nodo del grafo (C11b), no hay mapeo texto→código (C12) y no hay span por campo (C7). WS13.3 **conserva y restaura** ese foco por documento (clave de sesión, 5.3; `dag.yaml:945-950`). Todo esto cabe en componentes y rutas de graph_ui ya previstos (`dag.yaml:850-852`) y no requiere inventar una API semántica en sldb: los datos salen de `ir`, `load_edge_index` y las listas `files`/`references`, que ya entregan sldb y graph_ui.

### 6.2 Nota de alcance (WS13.1)

La aceptación de WS13.1 dice que «seleccionar en Code, texto o graph actualiza ese foco y las demás representaciones del mismo documento lo comparten» (`dag.yaml:865-867`), y su alcance admite compartir foco «solo donde exista correspondencia real de origen definida WS11» (`dag.yaml:857-859`). **Root decidió no reducir WS13.1 a C1-C4 actuales**: ese conjunto es el inventario actual, no la frontera de lo realizable; los datos reales de 6.1 definen un **delta futuro acotado en graph_ui**. Este contrato compromete ese dominio; lo que queda fuera (C7, C11b, C12 y el traslado de C14b) no se compromete y no bloquea el foco de 6.1. Mientras ese delta no tenga su recibo propio (sección 12), WS13.1 no puede declararse cumplido en foco texto/code/graph.

## 7. Errores de lectura y estados de red (consumidor: WS15.1)

### 7.1 Respuestas del servidor que existen

| Código | Cuándo | Evidencia |
|---|---|---|
| 200, `ok:true` | Nodo o catálogo; la proyección puede traer su propio fallo (abajo) | `GU/workspace_routes.py:92`, `:94` |
| 400 | `id` ausente; `depth` distinto de 1 o 2; identificador con `..` o prefijo de ruta; identidad ambigua | `:84-91`, `:134-135`, `:264-267`, `:299-300` |
| 404 | Documento no encontrado; ruta de workspace desconocida | `:352`, `:96` |
| 405 | Método distinto de GET | `:74-75` |
| 500 | Error no previsto; error al cargar documentos del catálogo | `:99-100`, `:108-109` |
| 503 | `El store no está disponible.` (sin store, store inexistente o sin `editor_store`) | `:104-105`, `:131-132` |
| 501 | Workspace en modo remote | `GU/serve.py:320-322` |
| Forma | `{ok:false, error:<texto>}` con el estado HTTP | `:75`, `:98`, `:100`; `GU/serve.py:json_response` |

### 7.2 Fallos dentro de un 200

- `projections.document.ok=false` + `error`: el IR no se construyó (`GU/workspace_routes.py:152-164`). La UI muestra el payload y un aviso (`workspace-view.js:325-332`).
- `projections.graph.ok=false` + `error` (`:422-429`).
- `projections.code`: `ok=false` con `error` si el documento está degradado (`:432-439`); y cada archivo con `status` (`:481-575`).
- Documento degradado: `is_degraded` y `degraded_reason` en `node` y `context` (`:217-218`, `:240`, `:309-346`).
- `documents_error` si el catálogo del store no se pudo listar al resolver un nodo (`:139-145`, `:216`, `:242`).
- `content_hash_error` y `file_revision_error` (`:173-198`).
- Problemas del índice de aristas: `{ok, problems, store_problems_count, error}` (`:577-609`) y su lectura `formatProblems` en cuatro estados `clean`, `node_problems`, `store_problems`, `error` (`workspace.mjs:63-81`). No sustituye `sldb stores check`, `deskops doctor` ni `drift check` (`reconciliacion.md` C-06).

### 7.3 Cliente

`request()` lanza `Error(body.error || 'No se pudo completar la operación')` cuando la respuesta no es 2xx o `ok===false`, adjunta `error.body`, y aplica timeout de 60 s (`GU/shell/api.js:4-13`). **Descarta `response.status`**: lo usa solo para decidir si lanza (`response.ok`, `:7`) y no lo guarda en el error (`:8-10`); el código HTTP no llega al consumidor y, como `response.json()` se evalúa antes (`:6`), una respuesta de error que no sea JSON tampoco conserva su estado. `loadCatalog` y `loadNode` muestran `err.message` en el panel (`workspace-view.js:126-130`, `:185-189`, `:316-317`). Una caída del backend o una respuesta no-JSON llega como la excepción nativa de `fetch`/`json()`: **por lectura de `api.js` y por el comportamiento estándar de `fetch`; no se ejecutó**. No hay forma normalizada de «sin respuesta»: la persona ve el mensaje del navegador.

**Delta de WS15.1 en el wrapper cliente** (además del renderer, sin API nueva de sldb): `request()` debe tipificar y conservar el estado HTTP y distinguir error de red (rechazo de `fetch` o vencimiento del timeout), error HTTP con cuerpo `{ok:false,error}` y respuesta no-JSON, de modo que E1-E3 sean distinguibles y E2 pueda mostrar el código (7.5). Es la razón de que H-09 deje de ser solo un renderer.

### 7.4 Fallo de carga CDN

`index.html` declara un `importmap` con `esm.sh` para react, react-dom, @xyflow/react, htm, dagre, elkjs y lucide, y una hoja de estilos de `esm.sh` (`GU/index.html:7-8`). Búsqueda de `onerror`, `onError` y `import(` en `index.html`, `app.js` y `shell/*.js`: sin manejo de fallo de carga (solo `try/catch` de `localStorage` e `history`). Como el árbol de módulos se resuelve por el importmap antes de que exista cualquier panel React, **un panel dentro de la aplicación no puede informar ese fallo**; el diagnóstico tiene que vivir fuera del árbol que no cargó. Eso es decisión de implementación de WS15.1; el contrato fija lo observable, no el mecanismo. El empaquetado offline está fuera de alcance (`alcance.md:21,23`); no se afirma funcionamiento sin red.

### 7.5 Estados que WS15.1 debe distinguir (observable)

| Estado | Se reconoce porque | Qué debe verse | Qué debe conservarse |
|---|---|---|---|
| E1 Sin respuesta del backend | `fetch` rechaza o vence el timeout | «Backend sin respuesta» y reintento | Pestañas, foco, historia, último nodo |
| E2 Respuesta de error | HTTP no-2xx con `{ok:false,error}` | El `error` del servidor y el código (hoy el código se descarta en `GU/shell/api.js:5-11`: el wrapper debe conservarlo, 7.3) | Ídem |
| E3 Respuesta ilegible | No es JSON | Mensaje distinto de E2 | Ídem |
| E4 Éxito con fallo de proyección o documento degradado | 200 con `ok:false`/`is_degraded` | Aviso en el panel afectado; el resto sigue | Ídem |
| E5 Referencia rota | `[[x]]` no resuelto por la composición de 5.2 (no por `recover_links`/`audit_links`, que no son el resolutor de la UI) o estado `no_existe`/`fuera_del_repo`/`protegido` en Code | Origen y causa | Navegación |
| E6 Documento ausente | 404 | «Documento no encontrado» + id | Historia |
| E7 Fallo de IR o documento degradado | `projections.document.ok=false` con su `error` (`GU/workspace_routes.py:152-164`), `is_degraded` (`:309-346`) o 422 de la lectura del IR (`GU/sldb_adapter.py:204-205`) | La **causa recibida** tal cual, sin renombrarla. La etiqueta «modelo no importable» se reserva a una causa **corroborada** | Ídem |
| E8 Fallo CDN | Módulos no cargan | Diagnóstico visible; sin prometer offline | No aplica (la app no arrancó) |
| E9 Fuente sin capacidad de edición | Límite read-only | Límite visible, **no** fallo de lectura | Ídem |

**E7 es el caso de E4 sobre el propio documento**: se reconocen igual, y E7 solo añade qué causa se muestra. **Lo recibido no identifica por sí solo un modelo no importable.** El 422 de `sldb_adapter.document_ir` cubre cualquier excepción al leer el archivo o construir el IR (`GU/sldb_adapter.py:201-205`, `except Exception`), es decir también el roundtrip roto, un fallo de lectura u otras excepciones, y la ruta del workspace guarda solo `str(exc)` en `projections.document.error` sin tipo (`GU/workspace_routes.py:162-164`); `is_degraded` por «Fallo al validar documento en disco» tampoco nombra la causa (`:309-310`). Ni el IR no construible, ni `is_degraded`, ni el 422 distinguen la causa; el contrato **no inventa un discriminante que el backend no entrega**: se muestra la causa recibida y la etiqueta de modelo no importable se usa solo si la causa lo corrobora.

No se inventa respuesta del backend ausente: E1 y E8 se prueban simulando la ausencia, no suponiendo qué devolvería. «Reintentar» tras restaurar el backend: el botón Actualizar ya conserva `selectedId`, `tab` y `depth` porque llama `loadNode(selectedId, depth)` sin tocar el estado (`workspace-view.js:296`); el catálogo solo se carga al montar (`:196`).

### 7.6 Qué distingue «error, conflicto, cambio y pérdida de soporte»

`user-flows.md:177` pide un criterio visible. Este contrato fija solo la parte de **lectura**: error (E1-E3, E6), degradado (E4, E7), pérdida de soporte (E5, estados de Code `no_existe`/`fuera_del_repo`/`protegido`). **Conflicto** (409 de guardado, `infraestructura.md:51`) es de WS12/WS19; **cambio** (drift, staleness) es de WS29. Hueco H-15.

## 8. Lectura multidesk de solo lectura (consumidor: WS41)

### 8.1 Alcance

Solo lectura: no hay mutaciones cruzadas, ni envío (`message send` está fuera del baseline, `deskops.md:38`; `user-flows.md:198`), ni copia de documentos ajenos para aparentar navegación federada (`user-flows.md:189`). P07: multidesk inicialmente solo lectura con rutas y aliases explícitos (`decisiones.md:31`, T-P07).

### 8.2 Mecanismo (ver 3.2)

Alias cerrado → `(root, store)`; sin rutas del cliente; sin tocar `SLDB_STORE`. Cada respuesta incluye el alias del desk y el store resuelto, para que «identidad y origen sean visibles».

### 8.3 Lo que sldb ofrece para leer otro store

`open_store(alias_o_ruta)`, `load_edge_index(store, include_linked=False)`, `doc_status(store, ref)` y `search(store_path, …)` reciben el store como argumento (sección 3.1). `doc_status` devuelve `ok/missing/ambiguous/link-missing/link-broken` (`SL/api/stores/doc_status.py:18-33`). **Su docstring («Asking never writes») solo dice que el store consultado no gana entradas, modelos ni hashes de los documentos que referencia (`doc_status.py:3-4`); no garantiza cero escrituras**: `doc_status` abre el store con `open_store(store, mode="readonly")` (`:25`), que migra el layout (`open_store.py:37-38`, sección 5.4). Un enlace a store (`stores add --name`) se resuelve solo si es **directo** (`SL/api/stores/doc_ref.py:1-8`). Las referencias entre stores se escriben `alias:ref` (`doc_ref.py:28-40`), con el alias de un enlace del store de lectura, que no es el alias de operador de 3.2. `load_runtime_documents` federa los stores enlazados solo con `include_linked=True` (`SL/store/query.py:73,76-101`; defecto `False`, `SL/api/documents/runtime_documents.py:17`); graph_ui lo llama sin ese argumento, es decir sin federar (`GU/sldb_adapter.py:386-388`). Por el contrario, el defecto de `load_edge_index` es `include_linked=True` (`SL/api/edges/edge_reading.py:14`): WS41 debe pasar `False` explícito, como ya hace graph_ui (`GU/workspace_routes.py:288`, `:584`).

### 8.4 Cosas que **no** existen y que el contrato registra

- **Ruta de lectura por alias en graph_ui**: `WorkspaceRoutes` tiene un solo store (`workspace_routes.py:68-71`). Hueco H-12, clase API (graph_ui), productor WS41. La URL y la clave de sesión llevan el alias (5.1, 5.3).
- **Enlace de texto entre desks** (decisión root 2 de 2026-11-01, `review-source.md:11`): se resuelve **por composición en graph_ui dentro de WS41**, con el parser y las referencias públicas reales y validación previa; **no se amplía sldb** por faltar un resolutor de wikilinks con alias. Hechos: el parser admite el prefijo dentro del destino y no hay obstáculo sintáctico (`SL/links/parser.py:6`); `resolve_link_target` no tiene rama de alias y trata `alias:x` como nombre o ruta (`SL/links/resolver.py:33-35`); `doc_status` resuelve *referencias* con prefijo de enlace de store, no enlaces de texto (`doc_ref.py:28-40`). La sintaxis y el orden de tratamiento están fijados en 5.2 («Tratamiento obligatorio de un enlace de texto»), para que WS40 y WS17 puedan authorar enlaces reales. H-16 queda como **integración/API de graph_ui en WS41**, con la salvedad independiente de lectura sin mutaciones (abajo). Si la prueba real de WS41 mostrara una falta de capacidad en la API pública de sldb, se actúa como dice 5.4: intake explícito en el repo dueño y su tarea antes del workaround.
- **Lectura sin mutaciones**: `document_edges` reconstruye índices y `open_store(readonly)` migra el layout (sección 5.4); `mode="readonly"` no basta. Obligación y criterio observable en 5.4. Segundo desk: lo verifica WS41; store propio: delta de lectura de WS13.1 y ruta consumida por WS24. Hueco H-14.
- **Configuración confiable de aliases del desk real**: contrato del input en 3.2; no es un documento a generar (H-11).
- **Forma del error multidesk**: ver 8.5.

### 8.5 Errores visibles (la aceptación de WS41 los exige)

| Error | Causa | Contenido mínimo | Fuente del dato |
|---|---|---|---|
| E-MD1 Alias no autorizado | Parámetro explícito de alias de una petición fuera del conjunto cerrado de la configuración confiable, o configuración ausente. No aplica al literal de un enlace de texto que 5.2 (paso 3c) clasifica como nombre local: ese caso es E5 | alias recibido; «no autorizado» | configuración confiable del operador (sección 3.2) |
| E-MD2 Ruta escapada o root arbitrario | Parámetro con ruta, `..`, ruta absoluta o fuera del criterio 3.3 | ruta rechazada y criterio violado | `fuera_del_repo`/`protegido` (`GU/workspace_routes.py:511-529`) |
| E-MD3 Store ausente | El alias autorizado no tiene store | alias y ruta esperada | `store_links` (`missing`/`not-a-store`, `SL/api/stores/store_links.py:15-39`) o 503 (`workspace_routes.py:104`) |
| E-MD4 Documento ausente en el desk destino | `doc_status` ≠ `ok` | `status` y `detail` | `SL/api/stores/doc_ref_status.py` |

La forma JSON sigue la de 7.1 (`{ok:false,error}` + estado HTTP); el campo adicional con el alias es parte de la implementación de WS41, no se fija aquí.

### 8.6 Registro de desks

`RepositoryDoc` da `id`, `path`, `name`, `status`, `description`, `tags` (`DK/deskops/models/repository.py:35-52`). Sirve para **explicar** el directorio de desks (F10) y da identidad; no es autorización automática, aunque el operador puede designarlo como fuente de la configuración confiable (3.2). `list_repo_task_routes` ya lee los Boards de repos registrados en el CLI (`DK/deskops/operations.py:364-394`); graph_ui no lo usa.

## 9. ViewDoc: solo grafo

- ViewDoc es un modelo de spec2viz (datos, sin ruta de store) con `nodes` (`{model, where}`), `relations`, `direction`, `notation`, `layout` (`infraestructura.md:149`; `reconciliacion.md` C-48). **No es contrato universal de UI** ni define formularios, pestañas o tableros (`brief.md:24`).
- Evaluación y rutas **existen en graph_ui, solo en modo local**: `evaluate_view(store, view)` une los documentos de cada `nodes[].model` que cumplen su `where`, filtra aristas por `relations` y `direction`, y toma `layout` de la vista o de la notación (`GU/projection_views.py:107-124`, `:41-62`); `list_views` (`:127`); rutas `GET /api/views`, `/api/views/evaluate`, `POST /api/views/save` (`GU/views_routes.py:69-87`); en modo remote responde 501 (`GU/serve.py:147-150`). `save_view` escribe en `store.parent/sldb/views/<name>.md` y no pasa `expected` (`GU/views_routes.py:56-66`). Notación: delega en `resolve_documents` de spec2viz; sin spec2viz, `notation.error` lo dice (`GU/projection_views.py:85-104`). Todo **existe**, no está aceptado, no se ejecutó.
- **Selección mínima concreta y notación para WS18**: **no hay evidencia en este paquete que fije una selección**. Ni `vistas.md` (F18b: «Selección mínima concreta: no fijada aquí»), ni `user-flows.md` (ninguna UF menciona ViewDoc), ni la reconciliación nombran qué modelos y predicados debe seleccionar un ViewDoc concreto. Las capacidades de evaluación están (arriba), pero elegir qué subgrafo ver sería inventarlo, y `dag.yaml:1212-1244` lo prohíbe («No inventar selección aquí»). **Declaración: la promoción de WS18 se detiene** hasta que un cambio de alcance o una decisión de producto, de root o del solicitante P01, fije la selección y la notación. Root confirmó el 2026-11-01 (decisión 3, `review-source.md:12`) que WS18 sigue detenida por la selección y la notación mínimas no fijadas, que es **opcional**, que no bloquea el contrato básico, el lector ni el manual, que no se elige un subgrafo por reflejo y que **no requiere una nueva pregunta al humano ahora**. WS18 no es prerrequisito del lector ni del manual básico (`alcance.md:27`; `dag.yaml:1565-1590`, WS24 no espera ViewDoc).
- Ruta `sldb/views/` prevista y repo de escritura: pendiente de confirmación al promover (`dag.yaml:1222-1224`); `save_view` de graph_ui escribe bajo `store.parent/sldb/views/`, que es la carpeta del proyecto dueño del store, y eso no prueba que sea del repo spec2viz (`reconciliacion.md` C-50).
- G_SPEC_VIEW: ver sección 12.

## 10. Authored, derivado y preferencia local

| Clase | Qué es | Ejemplos de este contrato |
|---|---|---|
| **Authored** | Texto o estructura escrita por persona o agente como fuente | Un Markdown no modelado; un documento modelado **cuya fuente la escribe una persona o un agente** y sus campos; el RepositoryDoc; las entradas y el mapa de P09 (`decisiones.md:33`); las plantillas, el generador y la definición del corpus de WS40 |
| **Derivado** | Calculado desde otras fuentes; se regenera | Catálogo, vecindad, `incoming_relations`, backlinks, `content_hash`, `file_revision`, IR, lista de issues por estado, lista de desks, el árbol del explorador, el progreso de lectura; SpecDoc y SpecNodeDoc materializados desde el YAML del spec; el manifiesto generado de WS40 (roots, stores, commits, documentos), aunque se versionara |
| **Preferencia local** | Estado de sesión o disposición, no documento compartido (P07, `decisiones.md:31`) | Foco, pestañas, divisiones, profundidad, filtro, historia de la sesión |

Reglas:

1. **El runtime volátil no es documento compartido por defecto** (`vistas.md` reglas a precisar; `brief.md`): estado de workers, intentos y conversaciones se leen del runtime (`deskops.md:140-141`). Un RunDoc authored es otra cosa que su estado operativo.
2. **Sin modelo nuevo** para organizar entradas ni listas derivables: un índice de issues, de FAQ o de desks se calcula (consulta) o se escribe como Markdown authored con enlaces; no se crea un modelo por reflejo (`vistas.md` reglas; `dag.yaml:1170-1198`, índice authored = texto curado, no copia de listados).
3. **Preferencia local** no se persiste como documento. La disposición de WS13.3 es por sesión de navegador, sin exigir persistencia tras recargar (`dag.yaml:933-973`).
4. Las entradas y el mapa del desk (P09) son authored, en deskops, y se **publican** con WS43; el contrato de identidad no las crea (WS17 las escribe como plantillas, WS43 publica). Cuando los listados dependan de lo que ya resuelve una consulta, no se copian.
5. **Authored no equivale a «modelado»**: que un documento esté registrado en un store no lo hace fuente. SpecDoc y SpecNodeDoc materializados por `spec2viz diagram sync` son derivados del YAML del spec, que es la fuente (`vistas.md` F18a, `infraestructura.md:35`); el manifiesto generado por WS40 es evidencia derivada aunque se versione, y la fuente authored son las plantillas, el generador y la definición del corpus. No hay modelo nuevo por esta distinción.

## 11. Huecos

Clases: **instancia** = documento concreto que falta escribir; **vínculo** = referencia o enlace que falta entre documentos existentes; **consulta** = selección o lista derivable sin operación pública para obtenerla; **API** = operación pública ausente en el repo dueño; **renderer** = representación ausente en graph_ui con datos ya disponibles. Cuando aplican dos, se elige la que falta primero y se dice. «Productor» = nodo de `dag.yaml`. Hueco de escritura → WS12. Una candidatura sigue siendo candidatura.

| ID | Hueco | Clase (y por qué esa) | Dueño | Productor |
|---|---|---|---|---|
| H-01 | Lectura del archivo propio de un documento (fuente íntegra + render, modelado o no), con el mismo origen (render y fuente de la misma lectura o revisión, sección 4) | API: en estas rutas no hay lectura que devuelva el texto del archivo propio (`workspace_routes.py:431-458`; sección 2.2); falta antes que el renderer | graph_ui | WS13.1 |
| H-02 | Explorador y árbol de Markdown no modelado del desk, con refresco explícito del catálogo y lista de permitidos (3.3) | API: no hay operación de listado en graph_ui ni en sldb (`workspace_routes.py:102-127`); falta antes que el renderer | graph_ui | WS13.2 |
| H-03 | Campo de origen (`files` o `references`) y posición de cada tarjeta Code: preservarlos antes de concatenar, para identificar la referencia por documento, campo, posición y valor | API: la ruta concatena y pierde el campo y la posición (`workspace_routes.py:441-451`) | graph_ui | WS13.1 |
| H-03b | Campo ↔ arista (C8/C9), con multiplicidad: el campo está en el registro de arista de sldb, la ruta de graph_ui no lo entrega y la deduplica por `(source, target, type, relation_doc)` (`workspace_routes.py:384`) | API (ruta de graph_ui); luego renderer. sldb ya tiene el dato en `load_edge_index` | graph_ui | WS13.1 (delta futuro comprometido por la decisión root 1; ver 6.1 y 6.2) |
| H-04 | Foco por sección y campo en texto (C5, C5b, C6), con la vista de texto con líneas; `owning_section` es opcional (C6) | renderer: los datos ya llegan al cliente (IR); para no modelados, antes falta H-01 y verificar la reutilización de C5b | graph_ui | WS13.1 |
| H-05 | Rango de líneas por campo (C7) | API: `_build_field_nodes` no asigna `span`; no bloquea el foco de campo ni de contenedor | sldb | sin productor en el DAG; no comprometido |
| H-05b | Tres capacidades distintas, no una sola imposible: (a) foco de la referencia explícita de una tarjeta Code en el texto (C11a); (b) rango local de Code, archivo/revisión/líneas, con selección por la persona (C14a); (c) mapeo semántico de las líneas de un archivo externo a texto/graph (C11b) y traslado del rango de Code al Markdown (C14b) | (a) y (b): API/renderer de graph_ui con datos reales, (a) depende de H-03; (c): no hay correspondencia | graph_ui | (a) y (b): WS13.1. (c): **sin productor y sin compromiso** (F17 no lo compromete, `vistas.md:349,351`) |
| H-06 | Seguir `[[…]]` y mostrar referencia rota desde el texto | API: graph_ui no consume `sldb.links` en estas rutas y `recover_links`/`audit_links` no sirven como resolutor de la UI (5.2); falta antes que el renderer; se compone `parse_links` + `split_anchor` + `doc_status` o la lectura protegida, con autorización antes de leer | graph_ui | WS13.1 (seguir enlace en el desk propio); WS41 (entre desks); WS15.1 (referencia rota) |
| H-07 | Pestañas, divisiones y foco por documento (disposición local) | renderer | graph_ui | WS13.3 |
| H-08 | Diagnóstico de fallo CDN (E8) | renderer: los «datos» (la carga fallida) viven fuera del árbol React, ver 7.4 | graph_ui | WS15.1 |
| H-09 | Estados E1-E3 distinguibles (con el código HTTP en E2) y reintento sobre catálogo; E7 muestra la causa recibida | API del cliente + renderer: `request()` descarta `response.status` (`GU/shell/api.js:5-11`), así que el dato falta antes que el renderer; el wrapper cliente lo tipifica y conserva sin API nueva de sldb (7.3) | graph_ui | WS15.1 |
| H-10 | Instancia temporal de prueba de WS40 (dos desks y su manifiesto: roots, stores, commits, documentos clave); el manifiesto generado es evidencia derivada (sección 10) | instancia: documento concreto que falta | graph_ui | WS40 |
| H-11 | Aliases reales del desk **real**: configuración confiable suministrada por el operador al arrancar o seleccionar el despliegue (contrato del input en 3.2); no es un documento a generar | Fuera de las cinco clases documentales: es configuración de entrada, no un documento pendiente; **no es una instancia a escribir** ni lleva clase, modelo ni nodo nuevo. Los valores no se inventan | operador (suministra); graph_ui WS41 (consume y valida) | WS11 fija el contrato del input (3.2); WS41 lo consume; sin productor de documento |
| H-12 | Ruta de lectura por alias y URL con repo/alias; clave de sesión con alias (5.3) | API: el workspace tiene un store (`workspace_routes.py:68-71`) | graph_ui | WS41 (historia en WS13.3) |
| H-14 | Lectura sin mutaciones: stores preparados fuera del request y comprobación real al ejecutar los consumidores de que las llamadas escogidas no escriben (5.4); `load_edge_index` en vez de `document_edges`, sabiendo que `open_store(readonly)` aún migra | API: `document_edges` reconstruye índices y `open_store` migra (`workspace_routes.py:356-359`; `open_store.py:37-38`); si no puede sostenerse con la API pública: hueco con dueño y bloqueo del caso antes de implementar | graph_ui | Store propio: delta de lectura WS13.1 y ruta consumida por WS24. Segundo desk: WS41. Si se prueba falta de capacidad: intake explícito en el repo dueño y tarea antes del workaround |
| H-16 | Resolver un enlace de texto entre desks (`[[alias:Model/name]]`, `[[alias:name]]`, `[[alias:ruta#Sección]]`) | API/integración de graph_ui por composición (5.2): `parse_links` + `split_anchor` + autorización + `doc_status`; el resolutor `resolve_link_target` no se usa (`resolver.py:33-35`). No se amplía sldb (decisión root 2) | graph_ui | WS41; salvedad independiente de lectura sin mutaciones (H-14) |
| H-17 | Enlaces authored entre los dos desks del corpus, con la sintaxis de 5.2 | vínculo (se escriben entre documentos que WS40 genera) | graph_ui | WS40; WS17 para las plantillas |
| H-13 | Diff Git por tarea y repo | renderer/API: `document_history` existe (por documento); el diff por tarea no | graph_ui | WS27.1 |
| H-15 | Criterio visible error/conflicto/cambio/pérdida de soporte (parte de lectura fijada en 7.6) | renderer | graph_ui | WS15.1 (error), WS29 (cambio); conflicto: WS12/WS19 |
| H-18 | Tablero, dependencias y apertura de TaskDoc/pills en el lector | renderer: `GET /api/desk/board` y `/task` existen (`DeskRoutes.board` y `DeskRoutes.dispatch` en `GU/deskops_routes.py`; `board` desde `:31`) | graph_ui | WS22 |
| H-19 | Procedimiento: renderer de RitualDoc/StepDoc | renderer | graph_ui | WS23 |
| H-20 | Vista genérica de conocimiento, clasificación y backlinks completos | renderer, luego consulta | graph_ui | WS24 |
| H-21 | Progreso de paso de un procedimiento | API: ningún campo de progreso en `RitualDoc`/`StepDoc` (`DK/deskops/models/ritual.py:57-82`, `step.py:31-38`; búsqueda de `progress`, `done`, `status`, `complete` y `checked` en esos dos archivos: la única coincidencia es la descripción de `completion`, que es un criterio, `ritual.py:77-79`). `RitualDoc.steps` es una lista de prosa **ordenada** (`list[str]`, `ritual.py:65-68`): tiene orden y posición, sin `StepDoc` enlazado ni progreso. WS23 declara que no se marca por leer (`dag.yaml:1540-1545`) | deskops | sin productor en el DAG; no comprometido |
| H-22 | Campo faltante de `InboxNoteDoc`, `MaterializationContractDoc`, `PillDoc`, `StepDoc`, `DeskFAQDoc`, `RepositoryDoc` | **resuelto por lectura** (ver 13, punto 5) | — | — |
| H-23 | Búsqueda con estados distintos por API | API (sldb ofrece `search`, `SL/api/search.py:26`, y `GET /find`, `SL/cli/serve/find_routes.py:1-12`; en estas rutas graph_ui no los consume: sin coincidencias de `/api/find` ni `.search(` en los `.py`, `.js` y `.mjs` de `GU/`, fuera de `fixtures/`) | graph_ui | WS14 |
| H-24 | Orientación de proyecto sin desk | renderer | graph_ui | WS15.2 |
| H-25 | Captura, ack, respuesta local (inbox), autoría de tareas y edición de campos | **escritura**: remitido a WS12 | deskops / graph_ui | WS12 (contrato); WS25.x, WS26.x, WS19.x, WS21 (UI) |

**Candidaturas sin productor** (siguen como tales, `vistas.md` sección «Candidaturas sin productor»; no son prerrequisito del lector ni compromisos): consulta guardada y búsqueda por significado sin CLI (`infraestructura.md:115,121`; dueño sldb); edición de `RoleDoc` y `RuntimeProfileDoc` (excluida por UF09; dueño deskops); navegación de preguntas de `DeskFAQDoc`; lista de issues en la UI (dueño graph_ui; `issue list` existe como CLI de deskops, `deskops.md:49`, y la UI no tiene ruta que lo llame); renderer de roles; vista Specs embebida en el lector. **Genérico Markdown o modelado no implica renderer especial** de FAQ, issues, roles o Specs. Hallazgo sobre Specs: la vista **Specs sí existe en graph_ui** como vista de primer nivel (`notationView`, `GU/views/specs/notation/notation-view.js:356`, registrada en `GU/shell/registry.js:16`); la auditoría `ui.md` no tiene fila para ella (candidatura de vistas.md). Lo que sigue sin productor es **integrarla en el lector** (candidatura); la vista misma no está aceptada, y de ella se abrieron solo su declaración (`notation-view.js:356`) y su registro (`registry.js:16`), no todo el renderer.

## 12. Mapa de deltas graph_ui que requieren recepción

**Regla** (`dag.yaml` gates `G_UI_READ`, `G_UI_WRITE`, `G_SLDB_WRITE`, `G_SPEC_VIEW`; `reconciliacion.md:27`; `alcance.md:27`): cada delta tiene su propio recibo; `evaluation: per_delta`; `accepted_scope_nodes: []` en todos. El **actor** que registra el acta es el solicitante designado en P01 (`decisiones.md:25`), receptor del repo dueño, al preparar o promover ese delta. El Executor de WS11 no escribe ni commitea actas interrepo y este contrato no afirma que alguna se haya recibido. «Efecto» = qué desbloquea el recibo, según el nodo. **Todas las filas: sin acta registrada** (búsqueda en graph_ui: no existe `runs/subagents/workspace-documental-acceptance/`; `ls` sin resultados).

### 12.1 Lectura: gate G_UI_READ (contrato fuente: este documento)

| ID | Efecto | Actor | Gate | Acta |
|---|---|---|---|---|
| WS13 (agregado) | Se cumple cuando WS13.1-3 cumplen; sin recibo propio | P01 | G_UI_READ | sin acta registrada |
| WS13.1 | Documento/fuente solo lectura, contexto, enlaces, foco | P01 | G_UI_READ | sin acta registrada |
| WS13.2 | Explorador de modelados y no modelados | P01 | G_UI_READ | sin acta registrada |
| WS13.3 | Pestañas, divisiones, historia | P01 | G_UI_READ | sin acta registrada |
| WS14 | Búsqueda por API pública con estados distintos | P01 | G_UI_READ | sin acta registrada |
| WS15 (agregado) / WS15.1 / WS15.2 | Errores de lectura y modo degradado (WS15.1); orientación sin desk (WS15.2) | P01 | G_UI_READ | sin acta registrada |
| WS22 | Board como trabajo navegable en el lector | P01 | G_UI_READ | sin acta registrada |
| WS23 | Procedimiento de rituales y pasos, solo lectura | P01 | G_UI_READ | sin acta registrada |
| WS24 | Vista genérica de conocimiento; no espera ViewDoc | P01 | G_UI_READ | sin acta registrada |
| WS27 (agregado) / WS27.1 / WS27.2 | Diff Git; evidencia declarada/encontrada/verificada | P01 | G_UI_READ | sin acta registrada |
| WS29 | Changes/Integrity (extensión independiente) | P01 | G_UI_READ | sin acta registrada |
| WS35 | Trazabilidad de ejecución (ramal E; además exige G_SCION) | P01 | G_UI_READ (+G_SCION) | sin acta registrada |
| WS40 | Generador del corpus Taller | P01 | G_UI_READ | sin acta registrada |
| WS41 | Lectura segura entre desks | P01 | G_UI_READ | sin acta registrada |

Los IDs son los nodos con `owner_repo: graph_ui` que declaran `G_UI_READ` en `requires` (recomputado leyendo `dag.yaml`: WS13, WS13.1, WS13.2, WS13.3, WS14, WS15, WS15.1, WS15.2, WS22, WS23, WS24, WS27, WS27.1, WS27.2, WS29, WS35, WS40, WS41), que coinciden con `scope_nodes` del gate.

### 12.2 Escritura: solo remisión a WS12

Nodos graph_ui que declaran `G_UI_WRITE` (y `G_WRITE_CONTRACT`): WS19, WS19.1, WS19.2, WS21, WS25, WS25.1, WS25.2, WS26, WS26.1, WS26.2, WS28, WS36, WS39, WS42. Sus huecos de escritura **se remiten a WS12** (H-25) y su contrato de efectos lo produce WS12 (`dag.yaml:723-796`); este contrato no define operación alguna. Receptor: P01. Gates: `G_UI_WRITE` y `G_WRITE_CONTRACT`, con `contract_source: WS12`. Sin acta registrada. En sldb, `G_SLDB_WRITE` cubre WS20 y WS45; también remitido a WS12.

### 12.3 G_SPEC_VIEW (opcional, aparte)

`G_SPEC_VIEW`: alcance WS18 (owner spec2viz), `evaluation: per_delta`, `contract_source: WS11`, receptor P01, `state: pending`, sin acta registrada. Se obtiene al preparar WS18, **no bloquea** la navegación base, ni WS24, ni el manual. La selección que WS18 necesita no está fijada (sección 9).

## 13. Trazabilidad

Cada punto de «Lo que WS11 deberá precisar» de `runs/subagents/20261101-ws09-vistas/result-summary.md`:

| # | Punto | Resolución | Dónde |
|---|---|---|---|
| 1 | Identidad, ruta y modelo opcional del Markdown no modelado (entradas, drawer, issues, FAQ) | **Resuelto como regla**: `(repo, ruta)` con modelo opcional. La implementación (lectura, explorador) es hueco con productor | 2.2; H-01, H-02 |
| 2 | Correspondencia real de origen texto/graph/code, foco compartido, rango dentro de un archivo (F17) | **Resuelto como dominio y tabla**: C1-C3 son navegación y C4 una tarjeta pasiva; el foco interno por documento es un dominio futuro de WS13.1 con procedencia real (decisión root 1: no se reduce WS13.1 a C1-C4); C7, C11b, C12 y el traslado de C14b quedan sin compromiso | 6; 6.1; 6.2; H-03 a H-05b |
| 3 | Selección mínima de ViewDoc y notación (F18b) | **Resuelto como declaración**: no hay evidencia; la promoción de WS18 se detiene | 9 |
| 4 | Vista Specs de Mindmap sin fila en `ui.md` | **Parcialmente resuelto**: la vista existe en graph_ui (`notationView`); integración en el lector sigue siendo candidatura sin productor | 11 (hallazgo) |
| 5 | Campos de `RepositoryDoc`, `InboxNoteDoc`, `MaterializationContractDoc`, `PillDoc`, `StepDoc`, `DeskFAQDoc` | **Resuelto por lectura de modelos** en `DK` (c19c6c0d): `RepositoryDoc` — name, id, path, status, description, tags (`models/repository.py:35-52`); `InboxNoteDoc` — kind (`unclear`/`suggestion`), sender_project, target_project, created_at, status (`open`/`closed`), acknowledged_by, acknowledged_at, title, body (`models/inbox.py:37-61`); `MaterializationContractDoc` — id, title, source_atoms, target_kind, target_identity, intent, validation, tags, provenance (`models/materialization.py:31-61`); `PillDoc` — title, id, status, summary, current_node, history, what, why, when, where, how, how_not, tags (`models/pill.py:59-80`); `StepDoc` — title, id, action, outcome, tags (`models/step.py:31-38`); `DeskFAQDoc` — title, body (`models/faq.py:19-22`). Son campos del modelo, no contrato de UI | 8.6; 13 |
| 6 | Progreso de paso en un procedimiento | **Hueco**: ningún campo de progreso en `RitualDoc`/`StepDoc` (búsqueda acotada a esos dos archivos); `RitualDoc.steps` es prosa ordenada sin `StepDoc` ni progreso; WS23 no marca por leer | H-21 |
| 7 | Aliases y roots autorizados; forma de errores de lectura multidesk | **Resuelto como contrato del input** (decisión root 4): los aliases reales son configuración confiable del operador; WS11 fija el input, WS41 lo consume y valida, WS40 da la instancia de prueba; los valores no se inventan. Enlaces entre desks por composición en graph_ui dentro de WS41 (decisión root 2) | 3.2; 5.2; 8; H-10, H-11, H-16 |
| 8 | Criterio visible error/conflicto/cambio/pérdida de soporte | **Parcial**: la parte de lectura se fija; conflicto y cambio quedan en WS12/WS19 y WS29 | 7.6; H-15 |
| 9 | Forma de errores de API y red (backend ausente, CDN) | **Resuelto como tabla de estados**; mecanismo CDN lo decide WS15.1 | 7 |


FILE:desk/drawer/plans/workspace-documental/dag.yaml (líneas 841-891, extracto del nodo WS13.1)
- id: WS13.1
  title: Leer documento, contexto y enlaces
  status: candidate
  kind: implementation
  depends_on:
  - WS11
  requires:
  - G_UI_READ
  owner_repo: graph_ui
  output_scope: frontends/mindmap/views/workspace/ (reutilizar node/workspace-view.js
    y componentes Document/Graph/Code/contexto existentes); rutas de lectura contrato
    WS11; tests/
  scope: Documento/fuente solo lectura, panel de contexto (identidad, relaciones y
    origen), enlaces y Code local con selección por documento/nodo. Mantener rutas
    del host; no requerir índices nuevos. Implementación o delta conciliado sobre
    el workspace integrado a1b2b22, según contrato WS11 y recibo externo del delta.
    Foco = elemento/nodo seleccionado dentro del documento; documento activo identifica
    pestaña. Compartir foco solo donde exista correspondencia real de origen definida
    WS11; no inventar mapeo texto→código.
  acceptance: 'Markdown sin modelo tiene render de lectura y fuente cruda íntegra
    legibles (ambas), con mismo origen; el panel de contexto muestra identidad, las
    relaciones que declare el contrato WS11 y la ruta de origen reales; seguir un
    enlace y alternar entre texto/graph/code, en las representaciones que el catálogo
    WS09 (borradores/vistas.md) y el contrato WS11 declaren soportadas, preserva origen.
    La selección por documento/nodo fija el foco del documento abierto: seleccionar
    en Code, texto o graph actualiza ese foco y las demás representaciones del mismo
    documento lo comparten, sin abrir otra copia. No depender de conocer un ID; no
    crear otro workspace independiente.  La base a1b2b22 es punto de partida reutilizable;
    el cierre de este delta exige SU evidencia de aceptación ampliada Markdown no
    modelado/fuente, enlaces y foco. Ni cierre f16fcd1 ni commit previo sustituyen
    esa evidencia. Una copia es instancia documental con mismo origen, no cada representación.'
  estimate: M
  task_file: desk/drawer/tasks/workspace-documental/task-ws13-1.md
  promotion: not_authorized; precise changed files/pills/atoms/evidence and task-only
    preflight required
  context_review:
    contract_sha256: 358c1c04d30e81e4e57c04ad2db25b6342e467e999788c6e3c8bb45d31355a3d
    evidence:
    - runs/subagents/20261031-workspace-context-reviews/context-review/WS13.1/de918fd823b60d8b9aeef1c00a7fd1d827089dd6d5cec7a243b38fb56ea59570/attempt-1
    input_sha256: de918fd823b60d8b9aeef1c00a7fd1d827089dd6d5cec7a243b38fb56ea59570
    required_protocol: ritual-context-review
    status: reviewed
  output_base: graph_ui:repository_root/
  node_role: delivery
  parent_id: WS13
  overlap_with: workspace
  integration_mode: delta_or_existing_ticket; matriz WS06 llega de forma transitiva
    por WS11/WS12; never_parallel_duplicate
  reconciliation: 'reconciliacion.md: base a1b2b22/f16fcd1/134a665 reutilizable; acceptance
    de este nodo/delta pendiente, no duplicar implementación ni inferir cierre por
    commit'

FILE:desk/drawer/plans/workspace-documental/borradores/vistas.md (extracto F17)
### F17 — Código local referenciado

- **Propósito humano**: ver, solo lectura, el archivo o rango que un documento referencia, junto a su soporte.
- **Origen**: `files` y `references` del payload del documento (`ui.md:55`; `reconciliacion.md:51`). Las anclas `code:<ruta>::<símbolo>` son otra capacidad (`infraestructura.md:94`).
- **Identidad**: ruta del archivo con límites de repo, gitignore, binario y tamaño (`reconciliacion.md:5,51`). Identidad de rango y correspondencia nodo-código: no definido; productor de contrato WS11 (`dag.yaml:857-859`).
- **Contrato**: sin contrato.
- **Campos y relaciones**: lee `files`/`references`, no el archivo propio del documento (`ui.md:55`). Mapeo texto-código: no definido; productor WS11; no se inventa.
- **Renderer existente o requerido**: base existente: `_build_code_projection` y `_inspect_file_reference` en la pestaña Código (`ui.md:55,77`; `reconciliacion.md:51`). Soporte de rango dentro del archivo: no leído; no definido; productor WS11. Sin CST supuesto; Tree-sitter queda diferido (`ui.md:183`).
- **Navegación**: foco compartido entre Code, texto y graph solo donde exista correspondencia real de origen definida por WS11 (`dag.yaml:857-859,865-867`); no se inventa mapeo texto-código.
- **Acción/dueño**: leer. Sin edición; el anclaje y la edición de código están en un candidato diferido (`ui.md:46`).
- **Destino de escritura**: ninguno.
- **Error**: condicionado a WS11 y WS13.1: archivo excluido por repo, gitignore, binario o tamaño (`reconciliacion.md:5`). Mensaje y forma: no definido; productor WS11.
- **Estado**: bloqueado. La base existente no basta: origen y foco necesitan el contrato WS11 y WS13.1 (`dag.yaml:841-871`).
- **Clase**: derivado (proyección del archivo referenciado); preferencia local (foco y selección).
- **UF**: ninguna lo usa de forma explícita. UF07 nombra anclas a código (`user-flows.md:171`) y UF05 la apertura de soporte (`user-flows.md:126`); no se afirma equivalencia con esta fila.
- **Evidencia**: `ui.md:46,55,77,183`; `reconciliacion.md:5,51`; `infraestructura.md:94`; `dag.yaml:841-871`; `user-flows.md:126,171`.

