## REFORMULACION
**Propósito:** agrupar la exposición de un adaptador público restringido para dispatch/reply Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador.  
**Resultado:** agregado no ejecutable; se cumple cuando WS34.1 y WS34.2 cumplen su aceptación. Sus dependientes siguen apuntando a WS34.  
**Repo dueño:** `deskops`.  
**Límites:** nodo `aggregate`, sin ejecución autorizada (`promotion: not_authorized`); depende de WS33, WS12 y sus hijos; requiere G_EXEC, G_SCION y G_WRITE_CONTRACT, aún pendientes.

## AMBIGUEDADES
Ninguna. El nodo define propósito, resultado agregado, repo, dependencias y aceptación comprobable mediante sus hijos. La autoridad del coordinador remite a WS12 y el timeout/errores a los contratos/hijos; no obliga a inventar un resultado propio del agregado.

## DRY-RUN
**Lecturas:** nodo WS34, guía de revisión y fuentes suministradas (`brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `dag.yaml`).  
**Cambios previstos:** ninguno; esta revisión no modifica el plan ni ejecuta WS34.  
**Dependencias:** WS33, WS12, WS34.1 y WS34.2; gates G_EXEC `pending`, G_SCION `unverified`, G_WRITE_CONTRACT `pending` con `accepted_scope_nodes: []`.  
**Validaciones futuras:** aceptación de ambos hijos; evidencia de gates; preflight de promoción con archivos, pills, átomos y evidencia precisos, solo si se autoriza.

## FUTURO
WS12 debe publicar el contrato de operaciones y autoridad; WS33 debe aportar el vínculo de mensajes, resultados y decisiones; WS34.1 y WS34.2 deben implementar y demostrar dispatch/reply. WS44/operador designado produce G_SCION; un humano autoriza G_EXEC; el receptor verifica G_WRITE_CONTRACT por delta. La promoción/TaskDoc fijará archivos y pruebas; WS36 consumirá el adaptador. Nada de esto es ambigüedad del nodo ni autoriza ejecución.
