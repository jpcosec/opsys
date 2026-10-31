## REFORMULACION

**Propósito:** agrupar la revisión de WS29 y WS39 como extensiones independientes de Changes/modelos, con evidencia propia y sin convertirlas en prerrequisito del lector o manual básico.

**Resultado:** PK07 es una agrupación de revisión, no una entrega ejecutable. Se considera verdadera cuando cada hijo directo tiene `context_review` vigente —hash de input y contrato actuales más `disposition.md`— o un bloqueo externo con responsable registrado. No exige producto entregado ni aceptación conjunta.

**Repo:** `deskops` para la agrupación; los hijos pertenecen a `graph_ui`.

**Límites:** no ejecuta tareas, no autoriza trabajo, no añade aristas, no presume CST/Kimun y no convierte revisiones de comprensión en producto. La “completitud sustantiva” queda descrita como futura y separada de la condición de revisión.

## AMBIGUEDADES

ninguna

## DRY-RUN

**Lecturas previstas:** guía de context review, brief, alcance, decisiones, cobertura, nodo PK07 y contratos de sus hijos como contexto, sin revisarlos.

**Cambios previstos:** ninguno; PK07 no ejecuta ni modifica artefactos.

**Dependencias:** revisión vigente de WS29 y WS39; `review_completion` remite a `context_review.py status`. Los hijos dependen de WS15/WS24 y WS12/WS13 respectivamente, pero eso pertenece a sus encargos.

**Validaciones futuras:** comprobar hashes y `disposition.md` de cada hijo; admitir bloqueo externo con responsable; verificar en sus revisiones las aceptaciones de WS29/WS39, la etiqueta del manual y la ausencia de CST/Kimun supuestos. No se ejecutan ahora.

## FUTURO

WS29 y WS39 producirán sus implementaciones y evidencia; WS31 publicará el manual; el participante P08 y los gates humanos decidirán la aceptación de uso. La sesión de coordinación registrará bloqueos externos con responsable. Nada de esto es ambigüedad de PK07.
