REFORMULACION
Encargo ejecutable de código en el repo deskops (base origin/main 5e25164c): ampliar la evidencia de tests del closeout. El resultado es que `reference_points_to_test` acepte un `.py` existente, relativo al root y dentro de él, si algún directorio de su ruta se llama exactamente `tests` o si su ruta normalizada figura en `payload["files"]`; debe conservar rechazos de absolutas, escapes del root, inexistentes, no `.py`, rutas de terceros (`.venv`, `.git`, `.sldb`, `site-packages`, `node_modules`) y cadenas que solo parecen evidencia. Se entregarán cambios en `deskops/services/closeout_gates.py` (`reference_points_to_test`, `_test_path_candidates`, llamada desde `closeout_reference_evidence` para pasar `files`), un test nuevo `tests/test_closeout_test_paths.py` y una entrada en `CHANGELOG.md`. Límites: no tocar otras funciones, `reference_points_to_document`, `tests/test_closeout_gates.py` (CC35a), `desk/`, `.sldb/` ni notas de inbox; sin recorrer el disco ni leer `pyproject`/`testpaths`.

AMBIGUEDADES
1. «files del TaskDoc (payload["files"])»: no aclara si es el TaskDoc evaluado o este TaskDoc; obligaría a inventar de dónde salen las rutas declaradas.
2. «salvo un test de extremo a extremo opcional sobre una copia en /dev/shm»: obligaría a decidir si ese test entra, cómo copiar y qué verifica.
3. «los que leen mucho el desk, desde una copia en /dev/shm»: obligaría a inventar qué tests “leen mucho” y el procedimiento de copia.
4. «sufijo distinto de .py»: obligaría a decidir si `.PY` o `.Py` cuentan.
5. «cadenas que solo parecen evidencia»: fuera de los ejemplos, obligaría a inventar el límite exacto.

DRY-RUN
Un ejecutor leería `closeout_gates.py` (especialmente :89, :149, :210), tests existentes y `CHANGELOG.md`. Cambios previstos: ajustar candidatos y decisión para aceptar cualquier componente `tests` o ruta en `files`; rechazar según p2; actualizar docstring; crear el test nuevo con `tmp_path`; añadir `### Changed`. Dependencias: firma de `CloseoutGatesService`, `payload`, pytest; coordinación con CC35a. Validaciones futuras: ejecutar los cinco archivos de test indicados, uno a uno; grep sin `rglob`/`os.walk` nuevos; `wc -l`; revisar CHANGELOG. No es agregado ni paquete no ejecutable.

FUTURO
El coordinador integra, responde/ack a Chatbot_Infra y decide el cierre; CC35a aporta cambios en `tests/test_closeout_gates.py`; el gate de closeout valida el resultado final. La publicación del CHANGELOG queda para el flujo de release.
