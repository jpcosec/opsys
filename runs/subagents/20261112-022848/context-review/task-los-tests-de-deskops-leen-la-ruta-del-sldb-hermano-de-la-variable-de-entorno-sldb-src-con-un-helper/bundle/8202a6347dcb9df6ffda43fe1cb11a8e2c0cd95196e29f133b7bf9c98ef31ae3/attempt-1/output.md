## REFORMULACION
Encargo del nodo: en el repo deskops, sustituir en los tests la ruta fija del sldb hermano (`carpeta padre/sldb/src`) por un helper común que lea `SLDB_SRC`; sin variable, usar la ruta hermana actual solo si existe. Resultado: helper único, los 18 archivos de test sin repetir la línea fija, `SLDB_SRC` inexistente falla rápido, `CHANGELOG` actualizado y, si existe, una línea en docs. Límites: fuera el código de deskops y los dos tests que simulan un workspace con carpeta `sldb` (`test_scion_runtime` en su prueba del workspace y `test_doctor_model_registration`).

## AMBIGUEDADES
1. «test_scion_runtime» aparece en la lista de 18 y a la vez fuera de alcance: «los dos tests que arman un árbol de trabajo falso... test_scion_runtime en su prueba del workspace». Obliga a decidir si se edita el archivo entero o solo se excluye esa prueba.
2. «falla rápido con un mensaje que nombra la variable y la ruta (revisable)» no fija tipo de error, momento (import/colecta) ni texto exacto; obliga a inventar mensaje y comportamiento.
3. «Grep de la línea fija (carpeta padre, sldb, src)» no da patrón literal ni rutas esperadas; obliga a inventar la expresión de grep.
4. «los 4 pasos del CI de deskops los corre el coordinador» y «4 pasos del CI de deskops en clon limpio»: no se enumeran los pasos; obliga a inventarlos.
5. «si hay una sección de cómo correr los tests en docs, una línea sobre SLDB_SRC» choca con `files: tests/, CHANGELOG.md`; obliga a decidir si se modifica docs fuera de `files`.
6. «Suite completa de a un archivo desde /dev/shm» no aclara si es archivo por archivo o suite completa; obliga a interpretar el modo de ejecución.

## DRY-RUN
Lecturas: TaskDoc, los 18 tests, `conftest.py`, `pyproject.toml` (`pythonpath = [.]`), `CHANGELOG.md`, docs de tests. Cambios previstos: crear helper (conftest o módulo, a elección del worker), borrar el bloque fijo de cada archivo o importar el helper, conservar la inserción de la raíz del repo, añadir entrada de CHANGELOG. Dependencias: pytest, orden de carga de conftest, clon de sldb `origin/main` en `/dev/shm`, copia de deskops con `sldb` hermano. Validaciones futuras: grep vacío fuera del helper; tres corridas (con `SLDB_SRC`, sin variable con hermano, ruta inexistente); CI de 4 pasos. Nada se ejecuta aquí.

## FUTURO
El worker elige conftest o módulo y lo declara en su informe; el coordinador ejecuta los 4 pasos del CI; un humano revisa el mensaje fail-fast y la decisión del overlord.
