REFORMULACION
Propósito: que `deskops graph` tome nodos y aristas del índice de sldb, asigne como `role` el campo de referencia de `TaskDoc`/`ReviewDoc` y deje de inferir aristas desde ids en prosa. Resultado: extractores regex retirados, snapshot versionado, `graph missing` sobre `unresolved_references`, `neighbors`/`reflect` adaptados, goldens y tests. Repo dueño: deskops. Límites: `output_scope` declarado; no toca sldb ni reimplementa su evaluador. GC11 es delivery code, no agregado.

AMBIGUEDADES
1. “Los nodos de archivos fuente… y las materializaciones se conservan si el índice de sldb no los cubre; el TaskDoc fija la lista tras el grep.” El criterio “si… no los cubre” y la lista quedan diferidos: el ejecutor debe inventar cómo medir cobertura y qué nodos conservar.
2. “una tarea task.code con depends_on, parent_id y un ReviewDoc produce aristas con role depends_on, parent_id, children y subject”. Una sola tarea con `parent_id` no garantiza una arista `children`; hay que inventar si se crea un padre agregado, otro hijo o qué documento la origina.
3. “de ReviewDoc (subject) aparecen con su nombre de campo como role” y `depends_on: [GC09]`: falta declarar de dónde sale `ReviewDoc` (GC02) o nombrarlo prerrequisito; el ejecutor tendría que inventar su modelo/contrato.

DRY-RUN
Lecturas: `dag.yaml` de GC11, guía, brief, alcance y decisiones; `extract_edges.py:22-34,245-310,631`; `snapshot.py`, `checks.py`, `self_reflection.py`, CLI `graph`; tests y fixtures. Cambios previstos: sustituir extracción regex por índice sldb, mapear roles, subir versión del snapshot, actualizar `neighbors`, `reflect` y `missing`, regenerar goldens. Dependencias: GC09 aporta `parent_id`/`children`; el índice de sldb; `ReviewDoc` debe existir (ver ambigüedad 3). Validaciones futuras: `graph build` en desk temporal, grep de `TASK_OR_ISSUE_RE`, `tests/test_graph_*.py`, diff de goldens y `CHANGELOG`.

FUTURO
GC09 entrega `parent_id`/`children`; GC02 u otro nodo, `ReviewDoc`; sldb, el índice y contratos. El TaskDoc de promoción fija la lista tras el grep y revisa el diff de goldens; un humano autoriza el plan y resuelve pendientes del dueño.
