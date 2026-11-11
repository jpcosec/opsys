REFORMULACION

Propósito: corregir `deskops edit` para que una edición de campo de sección no guarde el párrafo placeholder de la plantilla como contenido, evitando que el render lo duplique. Resultado: edición idempotente, con exactamente un placeholder-ancla, venga o no incluido en el valor; tests, docs y CHANGELOG actualizados. Repo: deskops. Límites: no modificar render/extract de sldb; no limpiar TaskDocs cerrados; confirmar y documentar la causa raíz antes del arreglo. El nodo es ejecutable, no un agregado.

AMBIGUEDADES

1. «en un solo lugar que usen todos los subjects de edit»: no identifica módulo, función ni API; obligaría a inventar dónde centralizar la normalización.
2. «si existe ya un normalizador de placeholders en deskops (promote.py _TASK_SECTION_PLACEHOLDERS, workspace.py), se reutiliza o se unifica; no se duplica la lista»: no aclara cuál es canónico ni qué hacer si ambos difieren; obligaría a inventar la decisión de unificación.
3. «Al menos un subject además de task (por ejemplo atom o inbox-note) si su plantilla tiene placeholders»: no fija subject ni criterio de elección; obligaría a inventar cuál cubrir.
4. «con la causa raíz escrita en el informe antes del arreglo»: no define informe, ubicación ni formato; obligaría a inventar el destino del hallazgo.

DRY-RUN

Lecturas hipotéticas: TaskDoc; `deskops/operations.py`, `doc_access.py`, `workspace.py`, `cli/commands/promote.py`, `cli/commands/operations.py`; tests; `docs/operator-manual.md`; `CHANGELOG.md`; logs y test de reproducción. Confirmar primero la causa. Cambios previstos: normalizador único que elimine párrafos idénticos a placeholder de plantilla del campo; integración en todos los subjects de edit; reutilización/unificación de listas existentes; tests de caso 3, idempotencia, solo-placeholder y frase dentro de párrafo mayor; docs y CHANGELOG. Dependencias: definiciones de placeholders existentes, comportamiento de extract/render y fixture `lifecycle_desk`. Validaciones futuras: tests dirigidos de a uno desde `/dev/shm` con `wait-pytest`, suite completa por archivo, reproducción con conteos `[1,1,1]`, y CI de cuatro pasos por el coordinador.

FUTURO

El coordinador ejecuta los cuatro pasos de CI y acepta el cierre; un humano decide merge y si la hipótesis sldb se registra fuera. El ejecutor entrega informe de causa raíz y evidencia de tests.
