---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-17T23:32:36'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Auditoría de empaquetado 2026-10-17: kgdb no declarado, rutas __file__ dependientes del checkout

_Describe the incoming message with enough evidence to triage._

Auditoría read-only de empaquetado (2026-10-17). Hallazgos en deskops:
1. kgdb no declarado en pyproject.toml:7-11 pero importado en deskops/cli/main.py:251-252 y deskops/graph/snapshot.py:119 (imports perezosos). kgdb solo existe como instalación git jpcosec/kgdb@1247139, sin release en índice.
2. Fuera de modo editable rompen rutas: deskops/bootstrap.py:200 (_package_root = Path(__file__).parents[1]) y deskops/lifecycle_migration.py:137 (pythonpath = parents[1]) asumen el checkout del repo.
3. pyproject.toml:3 = 0.1.0 sin tag v0.1.0; único tag v-stable-2026.08.29, HEAD 180 commits después. Sin __version__ ni CHANGELOG.
4. structuredLanguageDB>=0.1.9 (pyproject.toml:10) se cumple con lo instalado (0.1.9 editable); sldb HEAD es 0.1.10 sin tag.
5. deskops.egg-info/SOURCES.txt (2026-10-13) desfasado: faltan lifecycle.py, lifecycle_migration.py, runtime/task.py y lista 7 módulos borrados (models/checklist, condition, edge, hook, operator, routine; runtime/primitives).
6. Sin package-data (no hay datos no-Python dentro del paquete). Sin .github/workflows.
