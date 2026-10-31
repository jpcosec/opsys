## REFORMULACION

Propósito: verificar si sldb ya permite guardar un documento raw-source de forma reversible y, si falta, completar esa capacidad. Resultado: guardado por API pública con revisión, preservación de campos protegidos y pruebas de roundtrip, conflicto, recuperación y campos protegidos; sin sobrescribir Markdown desde browser. Repo dueño: sldb (`src/sldb/api/documents/`, `src/sldb/cli/serve/`, `tests/`). Límites: solo aplica con `source_mode=editable`; depende de WS12, G_SLDB_WRITE y G_WRITE_CONTRACT; si la capacidad existe, no se duplica código.

## AMBIGUEDADES

1. Cita: «Si la capacidad existe, esos tests bastan» frente a `requires: G_SLDB_WRITE`. Obligaría a inventar si la rama de solo verificación puede cerrar sin acta de alcance sldb o si el gate es previo a cualquier trabajo. La aceptación lo exime; el nodo lo exige.

2. Cita: «Si falta, se implementa en sldb mediante tarea propia aceptada en G_SLDB_WRITE». Obligaría a inventar si WS20 ejecuta la implementación o solo registra/entrega esa tarea a otro ejecutor; cambia el resultado y los cambios previstos.

3. Cita: «recuperación tras fallo». Obligaría a inventar qué fallos cubre (conflicto, validación, caída, escritura parcial) y qué evidencia demuestra recuperación; sin elegirlo, la aceptación no es comprobable.

4. Cita: «conserva campos y secciones sin pérdida». Obligaría a inventar si exige roundtrip byte-idéntico o solo semántico (orden, comentarios, formato); determina qué pruebas demuestran reversibilidad.

## DRY-RUN

Lecturas previstas: dag.yaml (WS20, WS12, gates, `source_mode`), `contratos/operaciones.md` si existe, `task-ws20.md`, alcance/brief y estado del repo sldb (API documents, cli serve, tests). Cambios previstos: ninguno ejecutado; si la capacidad existe, ajustar/añadir solo tests; si falta, implementar API y tests bajo tarea aceptada, sin tocar browser. Dependencias: WS12, G_SLDB_WRITE, G_WRITE_CONTRACT, `source_mode=editable`, G_SOURCE. Validaciones futuras: roundtrip, conflicto, recuperación, campos protegidos, revisión; cierre de G_SOURCE y no duplicación.

## FUTURO

P04/WS07 fija `source_mode`; WS12 produce whitelist/contrato y acepta el delta sldb; un humano designa al responsable sldb; el TaskDoc de promoción fija archivos y escenarios; si falta capacidad, otro ejecutor o tarea receptora la implementa.
