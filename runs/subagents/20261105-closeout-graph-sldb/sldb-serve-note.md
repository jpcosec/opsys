# Nota: `sldb serve` como proceso caliente para graph_ui (`frontends/desk/serve.py`)

Tarea: `task-el-grafo-del-closeout-se-lee-del-índice-de-sldb-no-reescaneando-el-repo`.
No se toca graph_ui. Medidas sobre el desk real de deskops con `measure_board.py` (este directorio).

## Lo que ya pasa hoy
- `serve.py` construye un `DeskView(root, herdr=...)` nuevo por petición. Lo que sobrevive
  entre peticiones son las cachés de módulo del proceso de `serve.py`:
  - sldb `compose_edge_index` (`_COMPOSED`, por firma de shards): índice de aristas del store propio;
  - sldb `project_graph` (`_PARSED` frontmatter por texto del bloque, `_METADATA` id/título por texto);
  - deskops `_DOC_PAYLOADS` (payload de modelo por texto del archivo).
- Con eso, el proceso de `serve.py` ya es un proceso caliente: un Board con `DeskView` nuevo
  tarda ~0.34 s (mediana), el mismo `DeskView` ~0.30 s; el primer Board del proceso ~1.7 s.
- Un `sldb serve` aparte no baja esos 0.34 s por sí solo: hoy no expone el grafo de proyecto,
  y el costo caliente que queda es de deskops/sldb dentro de la petición, no de arranque.

## Dónde se van los ~0.34 s calientes
- Recorrer el árbol del repo para los nodos de archivo (`ProjectFileWalk`, `os.walk`, ~0.15 s;
  `runs/` domina). Es lo único que se relee entero por petición.
- Nodos de documento (glob de superficies + lectura de texto; el parseo está cacheado).
- Compuertas del closeout por tarjeta (comandos `git` por tarea; fuera de este alcance).

## API que necesitaría `sldb serve` para servir el Board caliente
1. `GET /project-graph/nodes?config=<nombre>`: nodos (documentos y archivos) de un
   `ProjectGraphConfig` registrado en el servidor; invalidación por firma de directorios
   (mtime de cada directorio recorrido) para no recorrer el árbol en cada petición.
2. `GET /project-graph/edges?config=<nombre>&source=<id>` y `.../missing?source=<id>`:
   `ProjectGraph.edges_from` / `missing_from` con el `ProjectGraph` vivo entre peticiones,
   invalidado por `store_fingerprint` y por el texto de los documentos leídos.
3. `GET /edges?from=Ritual:<id>&include_linked=false`: ya existe `/edges`; las transiciones
   del ciclo de vida no necesitan nada nuevo.
4. Para registrar la configuración del desk en el servidor, `ProjectGraphConfig` tiene que ser
   dato puro: hoy `closed_document` es una función de deskops (issue cerrado). Con `RuleDoc`
   (GO06) pasaría a ser una regla declarada.
