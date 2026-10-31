# Informe Tester v2 — WS02 (segunda ronda)

Lectura propia de fuentes; no se heredan veredictos de v1.

## Comprobaciones de la ronda

| # | Objeto | Evidencia real leída | Resultado |
|---|---|---|---|
| R1 | La fila B cita `models-list.txt` | `deskops.md:181` cita `runs/subagents/.../models-list.txt` como salida de `sldb models list --store .sldb` | PASS |
| R2 | `models-list.txt` tiene los 17 modelos | `models-list.txt:1-18`: cabecera + 17 líneas (AtomDoc…TaskDoc); coinciden nombre a nombre con las 17 filas B y con los conteos «docs» (`145, 1, 1, 0, 14, 6, 29, 0, 3, 17, 6, 7, 3, 2, 2, 0, 3`) | PASS |
| R3 | El store declara 17 modelos | `.sldb/store.yaml:11-58`, 17 entradas `- name:` | PASS |
| R4 | `commands.log` declara reconstrucción | `commands.log:1`: «Reconstruido despues de la ejecucion a partir de lo recordado; no fue capturado en vivo.» | PASS |
| R5 | `commands.log` con un comando por línea | `commands.log:44` (`grep -n same en deskops/domain_tree.py`) y `:92` (`idem con fase y fase -i`) son prosa, no comandos; `:23-24` son `python -c "...; ..."` con elipsis, no reproducibles. El resto son un comando por línea | PASS con hallazgo menor |
| S1 | `repo register` | `repo.py:35-113` preflight (modelo, archivo, id/raíz duplicados), `:118-120` escritura, `:124` tracking; sin git | PASS |
| S2 | `repo remove` | `repo.py:139-167`; borrado+untrack vía `doc_io.DocTransaction.delete` en `:165`; sin git | PASS |
| S3 | `atoms create` | `atoms.py:60-80`; `services/atoms.py:183-256` (exige 5wh+ y una fuente pill/graph/diagram, `_write_new_doc`, track en `:246`); sin git | PASS |
| S4 | `atoms delete` | `atoms.py:82-91`; `services/atoms.py:167-181` (guarda de referencias entrantes, `transaction.delete`); sin git | PASS |
| S5 | `atoms split` | `atoms.py:93-113`; `services/atoms.py:258-320` (≥2 ids, crea y trackea nuevos `:305-308`, reescribe original como stub `:311-313`); sin git | PASS |
| S6 | `atoms merge` | `atoms.py:115-137`; `services/atoms.py:322-379` (ambigüedades, `_rewrite_inbound_atom_references`, stub `:370-371`); sin git | PASS |
| S7 | `atoms reorganize` | `atoms.py:139-153`; `services/atoms.py:102-152` (`ensure_workspace`, `path.rename`), `:809-828` (untrack/track); `--dry-run` no mueve; sin git | PASS |
| S8 | `desk replace` | `desk.py:145-156`; `services/replace.py:44-91` (exige archivo bajo `desk/`, rechaza documento modelado, `transaction.untrack/track` si estaba trackeado); sin git | PASS |
| S9 | `desk migrate` | `desk.py:182-213`; `workspace.py:130-163` (`scaffold_desk`, `_write_or_patch_config`, adopted/preserved/still_manual); sin git | PASS |
| S10 | `runtime template` | `runtime.py:70-110`; `scion.py:83-90` (`.scion/templates/<rol>`), `:314-345`, `:355-396` (`RunDoc` en `<run_dir>/run.md` con write+track); sin git | PASS |

## Hallazgos

- Menor: `commands.log` no cumple literalmente «un comando por línea» (2 líneas de prosa, 2 comandos con `...`). No invalida el contenido: los 113 comandos, 24 métodos y 17 modelos se pueden re-derivar leyendo `registry.py`, `operations.py` y `.sldb/store.yaml`.
- Menor: `commands.log:107,112,158` invocan scripts en `/tmp/ws02aud/` que no están archivados; esas líneas no son reproducibles.
- Menor: `testing-handoff.md` sigue citando como congelado el hash `e4b2ee57…`; el entregable de esta ronda es `14fc6c94…`. Documento de traspaso desactualizado, no el entregable.
- Dato del Supervisor (no verificado aquí): sha256 `14fc6c94a6b7642492743ec3ccf554ba57bf1c06a44d8ced302c665e6754d890` del entregable; `wc -l models-list.txt` = 18; hashes del anexo `file-inventory.tsv`.
- No verificado: conteos que exigen bash (192 filas del TSV, 239 documentos de `.sldb/core/documents`, 3560 de `.sldb/runtime`, 169 carpetas de `runs/subagents`).
- Sin filas «comprobado» sin evidencia en las filas muestreadas; las 10 filas nuevas (8 mutadores no probados en v1) cuadran con su código citado.

RESULTADO: PASS
