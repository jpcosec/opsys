REFORMULACION
Propósito: corregir que `deskops edit <subject>` guarde como contenido el párrafo placeholder de la plantilla y el render lo anteponga, duplicándolo en cada edición. Resultado: una edición deja exactamente un placeholder-ancla, venga o no dentro del valor, y es idempotente. Repo: deskops (main 9035ca60; reproducción en `/dev/shm`). Límites: solo `edit_artifact_field` y la normalización previa a escribir, para todos los subjects/modelos con placeholders; incluye tests, `operator-manual` y `CHANGELOG`. Fuera: render/extract de sldb (solo hipótesis en el informe) y limpiar TaskDocs ya cerrados.

AMBIGUEDADES
1. “se reutiliza o se unifica” (r2): no fija cuál normalizador es fuente de verdad ni si `workspace.py` contiene placeholders de sección; obligaría a inventar ubicación y API.
2. “para todos los modelos del desk con párrafos placeholder en su plantilla”: no enumera modelos ni campos; obligaría a inventar el alcance.
3. “un valor que es solo placeholder deja el campo vacío”: no define “vacío” para campos no string ni su tratamiento en frontmatter; obligaría a inventar semántica.
4. “Al menos un subject además de task (por ejemplo atom o inbox-note) si su plantilla tiene placeholders”: condicional sin lista; obligaría a decidir qué subject cumple.
5. “la causa raíz escrita en el informe antes del arreglo”: no define informe, formato ni destino; obligaría a inventar el artefacto.
6. “4 pasos del CI de deskops”: no los enumera; obligaría a inventar comandos.

DRY-RUN
Lecturas: `edit_artifact_field`, `_parse_field_value`, `write_doc`, modelos/plantillas, `promote._TASK_SECTION_PLACEHOLDERS` y referencias a placeholders en `workspace.py`. Cambios previstos: helper único que elimine párrafos exactamente iguales al placeholder del campo antes de `write_doc`, aplicado a todos los subjects; reutilizar o unificar la lista; tests del caso 3, idempotencia, solo-placeholder y frase embebida; docs y CHANGELOG. Dependencias: extracción/render de sldb y plantillas. Validaciones futuras: tests nuevos, suite completa por archivo desde `/dev/shm` y 4 pasos de CI. Sin ejecutar.

FUTURO
El worker produce el informe con la causa raíz antes del arreglo y ejecuta tests y suite; el coordinador corre los 4 pasos del CI en clon limpio. Si la causa resulta de sldb, otro nodo o un humano decide y no se escribe en sldb.
