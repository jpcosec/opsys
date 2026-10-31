## REFORMULACION

Propósito: implementar en `graph_ui` el alta/baja de relaciones que autorice el contrato de WS12, sin crear semántica nueva. Resultado: operaciones persistentes confirmadas tras recarga y rechazo visible de una relación no permitida o una revisión obsoleta. Repo: `graph_ui`, bajo `frontends/mindmap/views/workspace/relations/` y `tests/`, usando endpoints del contrato WS12. Límites: solo relaciones permitidas; API real y before-image; no crear semántica de relaciones; promoción no autorizada; gates pendientes.

## AMBIGUEDADES

ninguna.

## DRY-RUN

Lecturas: guía, nodo WS19.2, brief, alcance, decisiones, cobertura, reconciliación y bloques contractuales de WS12/WS16/WS19/gates. Cambios previstos: en `graph_ui`, integrar alta/baja con la API y before-image que fije WS12, más pruebas; no se ejecuta nada. Dependencias: WS12 —whitelist, endpoints y contrato—; WS16 —G_HUMAN_READ—; G_UI_WRITE y G_WRITE_CONTRACT; matriz WS06 transitiva por WS11/WS12. Validaciones futuras: persistencia tras recarga; error visible ante relación no permitida o revisión obsoleta; pruebas y preflight task-only.

## FUTURO

WS12 produce whitelist, capacidades, endpoints y evidencia de G_WRITE_CONTRACT/G_UI_WRITE. WS16 produce el acta humana de G_HUMAN_READ. WS07 y el humano designan actores y registran P04/source_mode. El humano aprueba los gates. La promoción fija archivos, pills, atoms, evidencia y escenarios de prueba. WS19 cierra cuando cierren sus hijos. Nada de esto es ambigüedad del nodo.
