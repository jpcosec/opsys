## REFORMULACION

**Propósito:** ejecutar el gate humano temprano de lectura/descubrimiento sobre UF01, UF03 lectura, UF07 diagnóstico, UF08 lectura y UF10 arranque/ausencia de desk.

**Resultado:** acta versionable en `graph_ui:runs/subagents/workspace-documental-acceptance/lectura/acta.md`, que resuelve `G_HUMAN_READ`, con guion, versiones/commits, corpus/manifiesto, comandos, tiempos, observaciones y decisión humana.

**Repo dueño:** `graph_ui`. **Límites:** no implementa correcciones ni crea corpus (WS40); no muta el baseline; no sustituye la aprobación humana; no cubre edición/guardado (WS30), Scion, Changes ni índices ricos.

## AMBIGUEDADES

1. «el responsable del repo dueño del nodo que falló abre la tarea de corrección antes de edición». Falta criterio para atribuir un fallo observado a un nodo concreto (búsqueda, lectura, multidesk, arranque); obligaría a inventar el mapeo síntoma→nodo y, con ello, el dueño de la corrección.

2. «Reportar tiempos y pruebas técnicas por separado» junto a «objetivos iniciales aceptados por P08 (no mediciones obtenidas)». No se define si superar <=2 s de lectura/búsqueda o <=10 s de arranque es fallo de recorrido que bloquea `G_HUMAN_READ` o solo un dato registrado; obligaría a inventar el criterio de pase temporal.

## DRY-RUN

**Lecturas:** `dag.yaml` (WS16 y vecinos), guía, `validacion-humana.md`, brief/alcance/decisiones/cobertura, manifiesto WS40 y contratos WS11/WS41.

**Cambios previstos:** redactar y guardar el acta; registrar fallos y huecos; no tocar código, corpus ni tareas de corrección.

**Dependencias:** WS14 (búsqueda), WS15 (errores/orientación), WS08 (guiones), WS40 (corpus/manifiesto), WS41 (segundo desk); `G_UI_READ`; no requiere WS17/WS30.

**Validaciones futuras:** recorrido sin rutas memorizadas; 20 aperturas y 10 búsquedas; enlace roto/backend ausente; arranque y repo sin desk; lectura entre desks y vuelta; acta con commit/blob verificable.

## FUTURO

WS40 produce corpus y manifiesto; WS41 habilita lectura multidesk; WS14/WS15 materializan búsqueda y errores; el responsable del repo del nodo fallido abre la corrección; la promoción fija archivos, textos y casos; un humano firma el acta; WS30 validará edición. Nada de esto habilita mutaciones.
