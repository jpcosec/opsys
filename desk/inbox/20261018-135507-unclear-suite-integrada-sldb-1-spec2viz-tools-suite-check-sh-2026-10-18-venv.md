---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-18T13:55:07'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Suite integrada SLDB_1 (spec2viz tools/suite-check.sh, 2026-10-18, venv 

_Describe the incoming message with enough evidence to triage._

Suite integrada SLDB_1 (spec2viz tools/suite-check.sh, 2026-10-18, venv limpio /tmp/suite-venv con Python 3.12.3, sldb/pron/deskops/spec2viz/graph_ui editables desde los checkouts). Comando: cd deskops && /tmp/suite-venv/bin/python -m pytest tests -q -p no:cacheprovider. Dos vueltas, resultados distintos: (1) 2 failed/447 passed: test_output_goldens.py::test_help_goldens (golden mismatch help/deskops.txt: el argparse de 3.12 envuelve 't,runtime} ...' en otra linea; el golden parece grabado con 3.13 o con otro ancho; COLUMNS no esta fijado) y test_taskdoc_read_without_overlay.py::test_read_doc_taskdoc_equals_extract_model_data (falla en la suite completa con 'assert paths, no TaskDoc fixtures found', pasa aislado). (2) 3 failed/446 passed: test_help_goldens otra vez, test_output_goldens.py::test_command_output_goldens (golden mismatch output/list_pills.json: el golden trae what/why vacios y la salida no) y test_doc_readability.py::test_unreadable_fields_are_detected_for_a_hand_written_document (assert 'what' in ['why']). Los tests que cambian entre vueltas apuntan a dependencia de orden o de estado compartido entre tests; el de help a un golden dependiente de la version de Python o del ancho de terminal. Logs: /tmp/suite-check/suite-deskops.log
