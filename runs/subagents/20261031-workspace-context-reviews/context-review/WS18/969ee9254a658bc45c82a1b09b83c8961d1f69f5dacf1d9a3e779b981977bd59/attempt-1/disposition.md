# Executor comparison — WS18

State: requires_contract_correction_rereview

## Reformulación examinada

## REFORMULACION
- **Propósito:** declarar proyecciones de grafo reutilizables mediante ViewDoc y su NotationDoc, limitadas a selecciones y notación ya soportadas por spec2viz, sin inventar UI declarativa.
- **Resultado:** una vista portable (mismo ViewDoc, sin código de host) que renderiza sobre un store real la selección declarada, coincide con ella y documenta qué selecciona.
- **Repo:** `spec2viz` (`owner_repo`); salida en `sldb/views/` (rutas a confirmar por su dueño al promover) y `tests/`.
- **Límites:** no crear UI pages ficticias; no modificar su repo desde este plan; promoción no autorizada; gate `G_SPEC_VIEW` obligatorio, evaluado por delta; este revisor no ejecuta nada.

##

## Comparación con intención / hallazgos

1 aclarado futuro TaskDoc en spec2viz por supervisor/Executor, paquete deskops no escribe interrepo. 2 selección mínima viene catálogo WS09+WS11 contrastado WS03; sin ella parar/corregir productor antes de promoción, no selección inventada. Recepción externa por delta.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
