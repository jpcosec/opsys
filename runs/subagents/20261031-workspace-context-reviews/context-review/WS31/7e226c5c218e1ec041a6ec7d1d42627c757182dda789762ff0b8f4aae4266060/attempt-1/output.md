## REFORMULACION

**Propósito:** publicar el manual documental básico ya probado, integrando el índice/criterios de WS10, capturas reales y limitaciones, con instrucciones trazables a evidencia humana y a los contratos de navegación/operaciones.

**Resultado:** `docs/workspace-user-manual.md` en deskops, con `docs/assets/workspace-user-manual/`, navegación, edición, captura, trabajo manual y revisión demostradas; átomos vinculados por cada Pxx vigente y contrato; Scion solo como capítulo propuesto.

**Repo:** `deskops` (`output_base: deskops:repository_root/`), nodo delivery de documentación.

**Límites:** no atomizar permisos ni aceptación técnica inexistente; no bloquear el manual básico por personalización, modelos (G_HUMAN_MODEL/WS39) ni impacto (WS29); no presentar Scion como operativo; promoción `not_authorized` con preflight task-only.

## AMBIGUEDADES

1. «por cada contrato en contratos/ (navegacion.md, operaciones.md u otros de WS11/WS12)» — no se indica el repo dueño de `contratos/` ni prefijo de ruta (a diferencia de las actas, que llevan `graph_ui:`/`deskops:`). Obliga a inventar dónde localizar los contratos y qué inventario exacto compone «u otros de WS11/WS12».

2. «comprobar G_HUMAN_MODEL/WS29 o mantener etiqueta propuesta» — WS29 no es dependencia ni gate, carece de `evidence_ref` y su aceptación habla de «prueba propia»; no se nombra el artefacto que se comprueba ni su ubicación. Obliga a inventar el criterio de comprobación de WS29.

3. «etiquetas, links y atom->doc verificados» — no se nombra actor ni criterio de verificación (WS43 define enlace verificable; WS31 no). Obliga a inventar quién verifica y con qué umbral se declara verificado.

## DRY-RUN

**Lecturas previstas:** dag.yaml (WS31 y vecinos), borradores/manual.md (WS10), actas WS30/WS43, decisiones.md, contratos navegacion.md/operaciones.md, corpus WS40, índices WS17, evidencia G_HUMAN_MODEL.

**Cambios previstos:** crear/actualizar manual, assets y átomos enlazados en deskops.

**Dependencias:** WS30, WS10, WS43; gate `G_HUMAN_MANUAL` pendiente (resolver WS30).

**Validaciones futuras:** enlaces resuelven a paths existentes; atom->doc y etiquetas; referencias a actas; Scion marcado propuesto; personalización/impacto etiquetados o comprobados.

## FUTURO

WS30 produce el acta humana; WS43 produce acta y commit de publicación; WS38 añadirá capítulos Scion; WS39/WS29 aportan sus pruebas; una persona aprueba y el TaskDoc de promoción fija archivos y preflight.
