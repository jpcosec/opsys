## REFORMULACION
**Propósito:** planificar una vista read-only de diff Git e historial junto a la TaskDoc. **Resultado:** implementación en `graph_ui` bajo `frontends/mindmap/views/workspace/diff/`, usando rutas del contrato WS11 y `tests/`. **Repo dueño:** `graph_ui`. **Límites:** solo lectura; sin escribir ni revertir; sin hallazgos de integridad del store (WS29); la asociación a intento llega en WS35; no se adivinan repos ni se escribe cruzado.

## AMBIGUEDADES
1. **Asociación commit→repo no definida.** Cita: «Historial baseline = commits de TaskDoc.references resolubles y ordenados por fecha de commit, limitados a TaskDoc.files» y «una sección por cada repo alcanzado por TaskDoc.files». Obligaría a inventar en qué repo resolver cada commit, el orden de intento y qué hacer si resuelve en varios o en ninguno.
2. **Referencias no-commit.** Cita: «Base: commits listados en TaskDoc.references». Si `TaskDoc.references` admite referencias que no son commits, el ejecutor debe inventar el filtro y el tratamiento de esas entradas.
3. **Commits presentes pero no resolubles.** Cita: «sin commits se declara que no hay historial referenciado y se usa diff working tree→HEAD», frente a «commits […] resolubles». No se define si “sin commits” significa lista vacía o ausencia de commits resolubles; obligaría a inventar el estado y el fallback.
4. **Orden del historial.** Cita: «ordenados por fecha de commit». No fija ascendente/descendente; obligaría a inventar el criterio visible.

## DRY-RUN
**Lecturas previstas:** `dag.yaml` (WS27.1, vecinos WS13/WS12, gate G_UI_READ), guía, brief, alcance, decisiones, cobertura y TaskDoc de promoción cuando exista. **Cambios previstos:** vista de diff/historial read-only, resolución de repo/rutas vía WS11, estados sin historial/ruta no disponible y tests. **Dependencias:** WS13, WS12, contrato WS11 y G_UI_READ por delta. **Validaciones futuras:** diff real, ausencia de escritura/reversión, una sección por repo, casos sin commits, commits no resolubles y rutas sin repo; acta G_UI_READ del receptor P01. Nada ejecutado.

## FUTURO
WS27.2 aporta evidencia; WS35 asocia diff a intento; WS29 cubre integridad del store; WS11/WS12 producen contratos de rutas y operaciones; el receptor P01 emite el acta G_UI_READ por delta; la promoción fija archivos, escenarios y textos.
