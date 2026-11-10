## REFORMULACION

Propósito: corregir dos defectos de deskops ante desks con semillas del ciclo de vida anteriores a CC31. Resultado: `doctor` reporta semillas managed desactualizadas con el fix `deskops desk update --apply` (d1), y `advance` falla antes de escribir nombrando la arista y el `sets.status` faltante o divergente (d2), sin ValidationError de pydantic. Repo: deskops. Límites: fuera el validador CC37, la migración del kit Chatbot_Infra y la gramática del CLI; se aplican las reglas comunes (tests de a uno con `TMPDIR=/dev/shm`, guarda pgrep, nada a mano, nunca `git add -A`) y las decisiones b1–b7. Es un nodo ejecutable (`task.debug`), no un agregado.

## AMBIGUEDADES

1. «con causa raíz escrita antes del arreglo»: no indica dónde ni en qué formato se registra. Obligaría a inventar ubicación (comentario, docs, informe) y extensión.
2. «doc en docs/ (manual de operador: doctor y advance)»: no fija archivo ni sección. Obligaría a inventar ruta y estructura.
3. «CHANGELOG»: no fija entrada, versión ni redacción. Obligaría a inventar el formato del cambio.
4. «El worker corre los archivos que toca y los que usan lo que cambia (test_lifecycle*, test_doctor*, test_cli, test_output_goldens)»: los globs no se resuelven. Obligaría a inventar la lista exacta de archivos.

## DRY-RUN

Lecturas: TaskDoc, `runs/subagents/20261110-repro-advance/repro.log`, decisiones b1–b7, los archivos listados, tests y goldens existentes. Cambios previstos: `doctor_findings.py`/`doctor.py` para d1 usando `seed_desk(root, apply=False, restore_managed=True)`; `lifecycle.py` (`advance`) para d2 comparando la arista leída con `lifecycle_table()` antes de aplicar efectos o escribir; `workspace.py`, `desk.py` y `tasks.py` solo si la comparación lo exige; tests de reproducción y doctor; docs y CHANGELOG. Dependencias: `restore_managed` y la caché de `lifecycle_table()`. Validaciones futuras: pytest por archivo con guarda b4 y `TMPDIR=/dev/shm`; goldens de ayuda idénticos y nuevos goldens de salida para d1/d2; los 4 pasos del workflow en clon limpio, a cargo del coordinador. Sin ejecutar nada.

## FUTURO

El coordinador corre los 4 pasos en clon limpio. El dueño del kit Chatbot_Infra ejecuta `deskops desk update --apply`. Un humano revisa la justificación de severidad del informe y aprueba los goldens nuevos. El validador CC37 queda intacto.
