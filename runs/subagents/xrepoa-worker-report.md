# xrepoa worker report

Precondicion (2): presente en main. `RepositoryReferences` en deskops/services/closeout_gates.py y `load_repository_registry` en deskops/identity.py (commit 7a17d8bfd).

Implementacion: deskops/foreign_files.py (deteccion (i)-(iii), solo files, ruta relativa contra la raiz del repo del desk); aviso en `add task` (cli/commands/operations.py); alerta del doctor (cli/commands/doctor.py). Texto exacto del aviso segun disposicion (6).

Evidencia (8): los desks reales de AntonIA no son accesibles. El caso de la nota a79fe2d6 (task.code de Governance con codigo en Chatbot_Infra) se cubre con fixtures en tmp_path: dos repos registrados con `deskops repo register`; formas (i) `infra:src/app.py`, (ii) ruta absoluta bajo la raiz, (iii) `../infra/src/app.py`. No se confirma con ejemplos reales de los desks.

Tests: tests/test_task_files_of_other_repo.py (7). Sin cambios de goldens.
