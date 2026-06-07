# Round 01 — Graph knowledge inconsistencies

**Source:** ST-03, ST-04

## Node IDs vs CLI expectations

- `graph neighbors atom-deskops` → `Error: graph node not found`
- `graph neighbors atom:atom-deskops` → funciona. Pero el usuario no sabe del prefijo `atom:`.
- El error no sugiere formatos válidos ni lista prefijos disponibles.

## Cero edges en nodos atom

- 253 nodos en total, 68 edges.
- Metadata es correcta (`node_count: 253`, `edge_count: 68`).
- Sin embargo, **todos los nodos `atom:*` tienen 0 edges**.
- Los 68 edges están en nodos con prefijos: `diagram:`, `doc:`, `source_file:`, `config_file:`, `issue:`, `spec:`, `test_file:`.
- Las conexiones semánticas entre átomos (declaradas en el contenido markdown) no se materializan como edges.

## graph missing

- Funciona correctamente: encontró una referencia dangling, muestra provenance con archivo:línea.
- El output es legible y accionable.

## graph build

- Es idempotente: rebuild produce exactamente los mismos 253 nodos y 68 edges.
- No hay indicación de progreso durante el build (silencioso hasta el final).
