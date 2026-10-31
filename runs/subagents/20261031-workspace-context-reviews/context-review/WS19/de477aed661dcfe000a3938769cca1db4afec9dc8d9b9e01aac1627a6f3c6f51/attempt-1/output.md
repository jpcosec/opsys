## REFORMULACION
**Propósito:** integrar en el workspace la edición de campos con revisión/conflicto visible y el alta/baja de relaciones autorizadas, reutilizando editores y API existentes.  
**Resultado:** nodo `aggregate` no ejecutable; se considera cumplido cuando WS19.1 y WS19.2 cumplen su aceptación. Sus dependientes siguen dependiendo de WS19.  
**Repo dueño:** `graph_ui`, con `output_scope` agregado de las salidas de WS19.1 y WS19.2.  
**Límites:** delta sobre ticket draft; no crear semántica de relaciones en el componente; campos workflow-protected no editables por este canal; mutaciones sujetas a contrato WS12 y gates.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas previstas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`, nodo WS19 y contratos vecinos WS12/WS16/WS19.1/WS19.2/WS21 y gates.  
**Cambios previstos:** ninguno; esta revisión no modifica el plan ni ejecuta código.  
**Dependencias:** WS12 debe producir whitelist/canal por campo y operación; WS16 debe producir G_HUMAN_READ con acta humana; WS19.1 y WS19.2 deben cumplir sus aceptaciones; G_UI_WRITE y G_WRITE_CONTRACT siguen pendientes y acotados por `scope_nodes`.  
**Validaciones futuras:** comprobar que el TaskDoc de promoción fije archivos, pruebas y textos dentro de la aceptación; verificar que las mutaciones usen API real y before-image; confirmar que una escritura obsoleta conserva el texto local; confirmar persistencia de relaciones tras recarga y rechazo visible de relaciones no permitidas u obsoletas.

## FUTURO
WS12 produce y verifica el contrato técnico y resuelve G_UI_WRITE/G_WRITE_CONTRACT; WS16 aporta la aprobación humana de lectura; WS07 designa responsables y `source_mode`. La promoción fija archivos, pills, átomos y evidencia, y el humano autoriza ejecución. Nada de esto se decide en este nodo.
