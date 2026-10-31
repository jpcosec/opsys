# Executor comparison — WS11, final per-effect contract input

State: accepted_current

## Reformulación examinada

## REFORMULACION
**Propósito:** cerrar el contrato de navegación e identidad del workspace documental.  
**Resultado:** `contratos/navegacion.md`, con identidad/origen, foco, enlaces/historia, lectura multidesk y clasificación de huecos, más mapa de recepciones por delta.  
**Repo dueño:** `deskops`.  
**Límites:** nodo de planificación; no implementa, no escribe actas interrepo, no afirma recibos recibidos, no habilita mutaciones ni depende de Changes, Scion o ViewDoc opcional.

##

## Hallazgos/disposición contra intención

1 foco/historia/disposición locales es decisión técnica P07 específica; APIs reales soportan identidad/origen/documentos/links, no exige persistir preferencias en store ni backend nuevo. Contrato debe documentar ambos: API comprobada y estado local. 2 revisión es workflow de TaskDoc deskops (supervisor/Tester/evidencia en run), no firma humana adicional; se concreta en promoción. Scope limita solo contrato/enlaces, nunca aprobar recepción por autochequeo.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
