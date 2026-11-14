# sldbsrc worker report
Commits (wt/sldbsrc): 907e9548 (tarea A), dd879196 (tarea B).
Helper: vive en tests/conftest.py (resolve_sldb_src), porque conftest carga antes que cualquier modulo de test, tambien con un archivo suelto; los 18 archivos solo borran su bloque. SLDB_SRC inexistente -> pytest.UsageError "SLDB_SRC=<ruta> does not exist" (probado). Grep literal vacio.
Suite completa: INCOMPLETA al entregar; /dev/shm/suite.sh sigue corriendo y escribe runs/subagents/sldbsrc/suite.txt (termina con linea DONE).
No hecho: corridas (a)/(b) desde copia en /dev/shm con clon de sldb.
