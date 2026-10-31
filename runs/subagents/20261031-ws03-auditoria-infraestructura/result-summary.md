# WS03 Executor: resumen de resultado

Entregable: desk/drawer/plans/workspace-documental/auditoria/infraestructura.md (secciones 1-7). Sin commits, sin closeout, sin ediciones fuera del entregable y de este directorio. `git status --short` de los tres repos se midió al inicio y al final (4/0/0, sin cambios).

## Qué se hizo
Lectura de código y de la ayuda de los CLIs de sldb, pron y spec2viz; filas por capacidad, repo y mecanismo con archivo:línea o salida de comando. `commands.log` lista los comandos en orden (las lecturas de archivos con Read están resumidas en una línea).

## Decisiones de formato (el encargo las dejó al Executor)
- Las tablas de capacidad 1, 3, 4 y 5 usan las columnas pedidas. La de concurrencia (sección 2) usa columnas propias (mecanismo, qué protege y granularidad, qué pasa al chocar, qué queda fuera, estado, evidencia) porque el encargo pide ese contenido; no se perdió ninguna de las columnas obligatorias salvo «capacidad/repo/operación expuesta», que en la sección 2 van en el título de subsección (repo) y en la ubicación.
- Citas de la forma `sldb/…`, `pron/…`, `s2v/…` abrevian `../sldb/src/sldb/`, `../pron/src/pron/`, `../spec2viz/spec2viz/` (explicado en el encabezado).
- «Por lectura» marca comportamiento deducido del código y no ejecutado.

## Marcado «no comprobado» (cambia un resultado si se ejecuta)
Carreras reales entre procesos, pérdida de edición externa, `create_document` sobre archivo ya registrado, semántica POSIX de `lockf`, embedder del corpus, pruebas pytest, graph_ui. Causa en la sección 7 del entregable: ejecutar exigía escribir en repos ajenos.

## Qué revisar (para el Tester)
- Filas de la sección 2.1: lock que no cubre la escritura del .md (`payload_save.py:47-48` vs `payload_save_steps.py:87-96`), verificación optimista por igualdad de payload (`save_plan.py:50,58`), ausencia de `expected` en API/CLI.
- ViewDoc (sección 5.2): modelo presente en spec2viz, sin evaluador ni renderer; ausente en sldb y pron.
- Discrepancias con el plan: sección 6 (ViewDoc «contrato existente… renderiza», «hash CAS»).
