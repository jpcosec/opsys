## REFORMULACION
Propósito: definir la vista de evidencia junto a la TaskDoc, mostrando estados declarada, encontrada y verificada sin crear un modelo de comentarios. Resultado esperado: UI en `graph_ui`, bajo `frontends/mindmap/views/workspace/evidence/`, con pruebas, capaz de abrir soportes Markdown del workspace y señalar rutas no soportadas. Repo dueño: `graph_ui`. Límites: depende de WS13 (lector) y WS12 (contrato de operaciones); requiere `G_UI_READ` por delta; no infiere evidencia por extensión; “verificada” es el resultado del gate vía `deskops closeout verify`, no prueba independiente; reporte ausente o fallo es no verificable con error; no hay mutaciones ni cierre nuevo; promoción no autorizada.

## AMBIGUEDADES
Ninguna. Los elementos que podrían parecer huecos tienen productor nombrado y tratamiento definido: rutas de lectura por WS11, correspondencia por tipo/artefactos y salida pública de `closeout verify` por WS12, y contrato ausente según “Reglas comunes de ejecución” de `alcance.md`. Los textos exactos, archivos y casos quedan delegados al TaskDoc de promoción.

## DRY-RUN
Lecturas previstas: nodo WS27.2, guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, aristas WS13/WS12/WS27 y gate `G_UI_READ`; sin revisar contratos vecinos.

Cambios previstos: solo si se promoviera, implementación en la ruta de evidencia de `graph_ui` y `tests/`; ningún cambio de contrato ni de otros repos.

Dependencias: WS13 para abrir soporte en lector; WS12 para tipos, artefactos y salida de verificación; WS11 para rutas; recibo `G_UI_READ` del delta concreto; reglas comunes si falta contrato.

Validaciones futuras: estados distintos para declarada/encontrada/verificada; evidencia ausente visible como ausente; declarada sin artefacto, artefacto no declarado y verificación fallida sin colapsar; apertura Markdown dentro del workspace; ruta y “no soportado” fuera de ese caso; reporte ausente/fallo como error no verificado. Nada se ejecuta ahora.

## FUTURO
WS12 debe publicar el contrato citado; WS11, las rutas de lectura; P01 emite el acta de recepción `G_UI_READ` por delta. La promoción fijará archivos, pruebas y textos mediante TaskDoc/preflight. La aceptación humana del delta y el cierre del agregado WS27 corresponden a nodos y actores posteriores, no a esta revisión.
