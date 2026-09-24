---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-09-24T00:14:25'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Handoff sldb: arreglos en main, retiro de la capa runtime/edges (afecta contrato publico) y registro roto de deskops

_Describe the incoming message with enough evidence to triage._

Handoff sldb -> deskops. Tres cosas: (1) arreglos que ya entraron a main de sldb y os afectan, (2) una capa que vamos a RETIRAR y que toca contrato publico, (3) un bug vuestro de registro.

## 1. Arreglos ya en main de sldb (5 merges, suite 1015 passed / 0 failed)

- `models add` ahora tiene salida de error limpia y codigos estables: ref invalida rc1 con lista de modelos disponibles, store ausente rc2 diciendo la ruta intentada, duplicado rc0 con "already registered", sin tracebacks. Esto cierra la nota que deskops nos mando (20260614-000001) y arregla lo que veia el usuario en `deskops init`.
- Los relpaths de indice ya NO hardcodean '.sldb': se derivan del directorio real del store. Un store renombrado (.sldb_custom) deja de ser invisible. OJO: `models_index_relpath`/`documents_index_relpath`/`sections_index_relpath` CAMBIARON DE FIRMA, ahora reciben `store_path` como primer argumento. Si los llamais directo, hay que actualizar.
- El cache de documento ahora firma por el `hash_b` del modelo: un contrato que gana un campo ya no devuelve el payload viejo para siempre.
- `fields add` ya no corrompe modelos cuyo .py no termina en newline (quedaba SyntaxError sin via de recuperacion por CLI).
- `docs delete` existe: untrack + borrar el .md + purgar la entrada de cache.

## 2. AVISO DE RETIRO: la capa `runtime/edges/` se elimina

Decision tomada. Es un derivado desnormalizado (un YAML por documento) que duplica lo que ya hace la capa de grafo networkx/KGDB. Evidencia: en una KB real de 1027 documentos, `runtime/edges/` pesa 16MB y el snapshot equivalente `runtime/graphs/*.nx.json` pesa 350KB para el mismo grafo.

Por que os importa: `sldb/api/__init__.py` se declara contrato publico para "pron, kgdb, deskops", y ~20 simbolos de edges que exporta MUEREN con la capa (`check_edges`, `edges_from/to`, `edge_node`, `edge_nodes_of_type`, `load_edge_index`, `init_relations`, `rebuild_edges`, `EdgeIndex`, `EdgeCheckReport`, `EdgeRebuildReport`, serializers y los node-id helpers `doc_node_id`/`tag_node_id`).

Lo que necesitamos de vosotros: confirmad si deskops consume ALGUNO de esos simbolos. Nuestro grep de vuestro repo dice que hoy solo usais `sldb.api.documents.{track_document_file,untrack_document}` (deskops/operations.py:2133-2162) y el resto son imports directos a `sldb.store.*` / `sldb.cli.*` / `sldb.runtime.validation`, o sea que el retiro NO deberia tocaros. Confirmadlo antes de que ejecutemos.

Cuando se retire, un store con la capa vieja fallara al abrirse con un error que incluye el comando de porte: `sldb stores migrate-legacy-edges --store <path>` (convierte al formato nuevo y borra `runtime/edges/`, idempotente).

Plan completo en `docs/architecture/edges-retirement-plan.md` de sldb: inventario de 19 consumidores clasificados, mapa de equivalencias y 6 gaps que bloquean el retiro.

## 3. Bug vuestro: `deskops` no encuentra su propio registro desde el repo sldb

Corriendo `deskops inbox list` (y `deskops next`) dentro de /home/jp/proyectos/hum-ecosystem/tools/sldb:

    Error: Repository id 'sldb' not found in registry at '.../sldb/desk/registry'

No existe `desk/registry/` en el repo sldb; solo hay `desk/config.json` (que SI declara `project_identity: sldb`). El comando busca un directorio de registro que la estructura de desk no crea. Eso deja el triaje de inbox inoperable desde el repo destino: tuvimos que cerrar las notas editando el frontmatter a mano en vez de usar vuestra CLI.

Dato adicional: `deskops doctor` SI funciona en ese mismo repo y ahora reporta "Desk is healthy. No issues found." tras reparar la deriva (faltaba `desk/rituals/phase.md`, habia ~40 primitives sin trackear y 5 notas invalidas por data_mutation).

## 4. Contexto extra que os puede servir

Auditamos codigo superseded en sldb (`docs/architecture/superseded-code-audit.md`). Hallazgo relevante para el ecosistema: la direccion del merge kgdb->sldb ya esta instalada (kgdb/contracts/{node,io,base}.py son shims que re-exportan desde sldb.store.graph), pero `kgdb/contracts/persistence.py` (PersistenceEntry/TransactionManifest) quedo sin heredero en sldb y sin importadores en ningun repo. Si deskops dependia de ese contrato de persistencia de grafo, decidlo ahora.
