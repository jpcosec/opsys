# xrepo-worker: closeout resolved-by con referencias calificadas por repo

Rama `wt/xrepo`, rebasada sobre origin/main `e393c077`. Commits `XREPO: ...`. Sin push.

## Aceptación (Validation / Done When del TaskDoc)

| Línea | Evidencia |
|---|---|
| c1 parseo `<repo-id>:<valor>` | `RepositoryReferences.split` (`deskops/services/closeout_gates.py`): corta en el primer ':'; prefijo = id del registro del desk → (repo, valor); si no, la referencia entera es local; URL sigue siendo URL |
| c2 `--ref <repo>:<sha>` | `close_resolved_by` verifica con `CloseoutGatesService(raíz registrada).reference_points_to_commit` (hex minúscula, ancestro de HEAD de ese repo); raíz ausente → rc 1 `Registered repository <id> is not at <ruta> on this machine.` |
| c3 `--test <repo>:<ruta>` | `reference_points_to_test(valor)` en el otro repo, **sin** `files` (no amplían tests ajenos); acepta `::nodo` |
| c4 trailers | `Closeout-Ref: infra:<sha>` / `Closeout-Test: infra:tests/...::nodo` tal como se escribieron; commit, subject, Board e index.jsonl iguales a hoy |
| c5 tests | `tests/test_closeout_resolved_by_xrepo.py`: 12 passed (30 s) |
| Tests existentes de resolved-by y closeout verdes | suite completa, abajo |
| Docs + CHANGELOG | `docs/operator-manual.md` (sección de cierre), `CHANGELOG.md` (Added) |
| Opción a de la nota queda en drawer | sin cambios: ya estaba en el drawer; no toqué desk/ |
| Fuera de alcance intacto | `closeout verify`, `commit`, `supersede` sin tocar |
| 4 pasos del CI en clon limpio | los corre el coordinador |

Archivos tocados (todos del `files` del TaskDoc): `deskops/services/closeout_gates.py`, `deskops/services/closure.py`, `tests/test_closeout_resolved_by_xrepo.py`, `docs/operator-manual.md`, `CHANGELOG.md`. No fue necesario `identity.py` ni `cli/commands/closeout.py` (la ayuda del CLI y su golden no cambian; el golden `deskops_closeout_resolved-by.txt` sigue verde).

## Referencias probadas

| Forma | Repo | Resultado |
|---|---|---|
| `--ref infra:<sha8>` | infra (registrado) | acepta, trailer tal cual |
| `--ref infra:<sha completo>` | infra | acepta (mezclada con ref local) |
| `--ref https://.../pull/7` | — | acepta como URL |
| `--test infra:tests/test_infra.py::test_infra` | infra | acepta, trailer con `::nodo` |
| `--test infra:tests/test_infra.py` | infra | acepta |
| `--ref infra:<sha de rama no fusionada>` | infra | rechaza (`Unresolvable --ref`) |
| `--ref infra:<sha del desk>` | infra | rechaza |
| `--test infra:tests/test_missing.py` | infra | rechaza |
| `--test infra:src/infra.py` (no es test) | infra | rechaza |
| `--test infra:declared_check.py` (en `files` de la tarea) | infra | rechaza: `files` no amplía |
| `--test infra:../governance/tests/test_thing.py` | infra | rechaza (sale de la raíz) |
| `--ref nope:<sha>` / `--test nope:tests/...` | no registrado | se trata como local y falla como hoy |
| `--ref governance:<sha>` / `--test governance:checks/check_thing.py` | el propio desk | local, acepta (files amplía), trailer tal cual |
| `--ref gone:<sha>` / `--test gone:tests/...` | registrado, raíz ausente | rc 1 con el mensaje exacto, nada escrito |

## Casos probados (`tests/test_closeout_resolved_by_xrepo.py`, 12)

1. cierra con commit+URL+test del otro repo; trailers, commit, Board, index, árbol limpio
2. mezcla de ref/test local y calificado
3. prefijo con la identidad del propio desk = local
4. sha de rama no ancestro del HEAD del otro repo → rechaza
5. sha del desk calificado con el otro repo → rechaza
6. test inexistente / no-test / declarado en `files` / fuera de raíz (4 parametrizaciones) → rechaza
7. prefijo no registrado → como hoy (ref y test)
8. raíz registrada ausente (ref y test, 2 parametrizaciones) → rc 1, mensaje exacto

Cada rechazo verifica snapshot sha256 de `desk/` + `git status` + HEAD sin cambios y la tarea aún presente. Los repos se registran con `deskops repo register ... --store`.

## Suite completa

Desde `/dev/shm/deskops-xrepo` (copia del HEAD rebasado), un archivo a la vez con `wait-pytest.sh` antes (`xrepo/run1.sh`, `xrepo/suite.sh`; logs y `suite-summary.txt` en `~/proyectos/SLDB_1/coord2-ccconfig/xrepo/`):

- 99 archivos `tests/**/test_*.py`, **todos rc 0**; 987 passed, 3 skipped (`tests/e2e_agent/test_agent_scenarios.py`), 1 xfailed (`tests/test_review_doc.py`, preexistente). Sin failed ni error.
- `bash scripts/ci-knowledge-check.sh .` → rc 0 (imprime hallazgos de drift preexistentes que no fallan el CI, p. ej. `task-policy-leak` en un drawer).
- `python -m deskops graph missing --root .` → rc 0, `No missing graph references found.`
- Ningún golden cambió.

## Hipótesis para sldb

Ninguna bloqueante. El registro se lee con `identity.load_repository_registry(desk, root)`, que ya valida ids y raíces duplicadas; no hizo falta nada de sldb.

## Desvíos

- **Trailer de Co-Authored-By:** los commits 1-2 llevan `Claude Opus 5.5` (como el brief); este informe y lo posterior, `Claude Sonnet 5.5`, porque el harness cambió el modelo y su recordatorio de atribución lo sustituye.
- La espera de `wait-pytest.sh` llegó al tope de 1200 s por suites de otros workers (mepu, AntonIA, placeholder, cc35d); `run1.sh` reintenta hasta 4 veces, sin pgrep global.
- Regla nueva de coord2 sobre `~/proyectos/SLDB_1/sldb`: no se usó nunca; todo corrió con `PYTHONPATH=/dev/shm/deskops-xrepo:/dev/shm/sldb-main/src`.
- `identity.py` y `cli/commands/closeout.py` quedaron sin tocar: el parseo vive en `closeout_gates.py` y reutiliza `load_repository_registry`.
- Un registro ilegible (`SLDBStoreError`) rechaza con `Could not read the repository registry: ...`; solo se lee si alguna referencia tiene ':' y no es URL, así los cierres sin prefijo no dependen del registro.
