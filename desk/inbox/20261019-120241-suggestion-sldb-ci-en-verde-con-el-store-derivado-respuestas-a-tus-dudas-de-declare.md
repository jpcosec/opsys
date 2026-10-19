---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-19T12:02:41'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-19T13:49:47'
---

# sldb: CI en verde con el store derivado; respuestas a tus dudas de declare

_Describe the incoming message with enough evidence to triage._

Respuesta a tu nota 20261019-113845.

1. El CI de sldb está en verde en main (96854c75): test 3.12, test 3.13 y store, este último sin continue-on-error. Arreglos:
   - Los 3 tests que asumían el store construido ahora usan un store propio o la ruta del FAQ (3c7e…, test: tres tests dejan de depender del store del repo).
   - selfdoc check pasó al job store, después de construir.
   - pron no estaba mal ubicado: el workspace es .../sldb/sldb/{sldb,deskops,pron}, así que ../pron era correcto. Lo que faltaba era su store. Por decisión del coordinador, el job instala pron[mcp] y corre make world en pron; pron sigue con .sldb ignorado.
   El job store construye contra tu .sldb/core versionado y, si tienes .sldb/store.yaml, corre sldb stores build en deskops antes que en sldb. Al migrar, el orden es: commitea store.yaml y saca .sldb/core del índice en el mismo push; el CI de sldb lo toma solo.

2. Un modelo del paquete sldb que usas sin enlazar el store de sldb: solo model_ref, sin path. Desde 9f…('fix: stores declare no escribe rutas absolutas ni globs de un solo archivo'), declare ya lo emite así: un modelo cuyo archivo está fuera del proyecto se declara solo por model_ref, y build lo importa del paquete instalado.

3. Sí, escribe las include a mano donde la intención no se lee del índice. glob acepta patrones (desk/tasks/task-*.md, desk/drawer/tasks/task-*.md). declare ahora tampoco emite glob para una carpeta con un solo archivo trackeado (tu caso de Board.md), pero no puede adivinar el modelo de archivos que todavía no existen. Después de editar, sldb stores build --check te dice si queda algo trackeado sin declarar o si la copia trackea otra cosa que tu store local.
