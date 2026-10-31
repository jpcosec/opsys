## REFORMULACION
**Propósito:** cerrar el contrato de navegación e identidad del workspace documental, clasificando huecos de resolución entre documentos, nodos graph/code, foco, enlaces/historia y lectura multidesk read-only.  
**Resultado:** `contratos/navegacion.md`.  
**Repo dueño:** `deskops`.  
**Límites:** nodo de planificación; no implementa UI ni migra a Kimun implícitamente; no publica el contrato como cerrado sin recepción de `graph_ui` y `spec2viz`; depende de WS08/WS09 y `G_PRODUCT`.

## AMBIGUEDADES
1. «Resolver cada hueco como instancia/vínculo/consulta/API/renderer»: no se definen “instancia” ni “vínculo”, ni el criterio para asignar un hueco a cada categoría. Obligaría al ejecutor a inventar una taxonomía de clasificación y sus reglas de uso. El glosario define “consulta” y “renderización”, pero no esos dos términos.

## DRY-RUN
**Lecturas:** guía de revisión, brief, alcance, decisiones, cobertura y el bloque `dag.yaml#node:WS11`; los bloques edge solo como contratos vecinos.  
**Cambios previstos:** redactar el contrato de navegación/identidad; clasificar huecos; registrar dependencias acotadas si falta API; preparar evidencia de aceptación para `G_UI_READ` y `G_SPEC_VIEW`.  
**Dependencias:** WS08 y WS09 como entradas; `G_PRODUCT`/WS07 para responsables designados; aceptación de `graph_ui` y `spec2viz`.  
**Validaciones futuras:** acta con identidad/fecha, task receptora y no solapamiento; enumeración de `scope_nodes`, incluidos WS40 y WS41; coherencia con WS12, WS13, WS18 y WS41. Sin ejecutar nada.

## FUTURO
WS07 debe designar responsables de `graph_ui` y `spec2viz` y resolver las decisiones que alimentan `G_PRODUCT`. Los responsables receptores aceptan o rechazan los deltas; sin recepción, WS11 queda pendiente. WS12 consume el contrato de operaciones; WS13/18/40/41 implementan los deltas aceptados; WS16/30 validan lectura, corpus e índices. Nada de esto es ambigüedad del nodo.
