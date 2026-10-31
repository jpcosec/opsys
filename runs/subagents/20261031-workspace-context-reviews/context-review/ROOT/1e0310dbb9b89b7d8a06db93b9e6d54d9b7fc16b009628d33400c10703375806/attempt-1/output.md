## REFORMULACION

Propósito: revisar ROOT como encargo de planificación agregado del workspace documental, no como tarea ejecutable. Resultado: dictamen sobre si su propósito, alcance y aceptación son comprensibles y comprobables. Repo: `desk/drawer/plans/workspace-documental`, con `dag.yaml` como fuente de IDs y aristas. Límites: no se revisan los bloques edge vecinos (PK01–PK08), no se ejecuta nada, no se resuelven propuestas Pxx ni se juzga el producto.

## AMBIGUEDADES

1. «Verdadera cuando cada hijo directo tiene revisión vigente sin ambigüedad de encargo o bloqueo explícito con responsable.» — No se define qué hace «vigente» una revisión (fecha, autor, registro) ni dónde consta. El ejecutor/revisor debería inventar el criterio de frescura y la evidencia admisible.

2. «bloqueo explícito con responsable» — No se indica formato, canal ni identificación exigida del responsable. Obligaría a inventar cómo se declara y verifica un bloqueo.

3. «Cero nodos autorizados para ejecución.» — No se nombra el campo, registro o comprobación que acredita esa ausencia de autorización. Obligaría a inventar la fuente de verificación.

## DRY-RUN

Lecturas previstas: `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/vision.md`, nodo ROOT y bloques PK01–PK08 de `dag.yaml`. Cambios previstos: ninguno; esta revisión no muta archivos. Dependencias: las ocho agrupaciones PK como hijos directos; ROOT no se ejecuta y termina cuando terminen sus hijos. Validaciones futuras: contrastar que cada PK tenga revisión registrada o bloqueo con responsable identificado; confirmar que ningún nodo figura autorizado para ejecución; verificar que el alcance declarado no habilite implementación.

## FUTURO

La revisión de cada PK y sus descendientes la producen otros nodos de context review. La resolución de P01–P09 corresponde al solicitante humano o a quien designe. La promoción del plan y la reconciliación con tareas del repo receptor las decide un humano conforme a `alcance.md`. Nada de esto es ambigüedad de ROOT.
