# Resultado: task-board-portable-references

Empezado por Codex (se quedó sin cuota a medio camino), terminado por Claude el 2026-10-21.

- `desk/tasks/Board.md`: pills y rituals por nombre de documento portable (`pill-…`, `ritual-…`), no por ruta; las
  tareas siguen por ruta para el ruteo local.
- `deskops/graph/extract_edges.py`: el grafo local (sin store) también resuelve un documento por el stem de su
  archivo, así `pill-001-task-closure-commit` llega al pill con id `pill-001`.
- `tests/test_board_portable_references.py`: proveedor y consumidor sldb reales con rutas que colisionan (las 11
  referencias del Board resuelven al proveedor, 11 aristas `contains`); grafo local, `next`, `show` y retiro aceptan
  el contexto portable. Ajustado al contrato real (aristas `sldb://document/…`, rol `pills`/`rituals`,
  `semantics.path`).
- Materializaciones: `materialization-board-portable-context`, `materialization-board-portable-references-regressions`.

Validación: suite completa de deskops 584 passed, 3 skipped (los 3 skips ya estaban). Commit del arreglo: dd31908.
