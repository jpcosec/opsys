# Executor comparison — WS26.2

State: requires_contract_correction_rereview

## Reformulación examinada

## REFORMULACION
**Propósito:** revisar WS26.2 como encargo de planificación para enrutar tareas en el Board y representar la capa lista.  
**Resultado:** UI de enrutamiento explícito y vista separada de capa lista; tests en `graph_ui`.  
**Repo:** `graph_ui`, con endpoints autorizados por el contrato WS12.  
**Límites:** no ejecutar; no autoriza promoción, commits ni mutaciones UI sin `G_HUMAN_READ`; depende de WS12, WS22 y WS26.1; aceptación per_delta.

##

## Comparación con intención / hallazgos

1 conservador: normalización/expansión contrato WS12; igualdad/contención solapan, glob/no-resuelto no comprobado y supervisor revisa antes ready. 2 no inventar promoción: operación completa WS12 o preparar handoff mostrando pendiente.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
