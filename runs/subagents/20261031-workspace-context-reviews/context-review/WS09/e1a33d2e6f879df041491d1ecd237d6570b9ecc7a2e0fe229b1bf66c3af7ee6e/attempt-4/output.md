## REFORMULACION
Propósito: convertir `borradores/vistas.md` en un catálogo preciso de renderizaciones, no implementar UI. Resultado: cada fila con origen, contrato, renderer, acción/dueño, error y estado, distinguiendo authored/derivado/preferencia local, más la ficha por fila. Repo dueño: `deskops`; salida limitada a `borradores/vistas.md`. Límites: nodo planning/candidate, sin ejecución autorizada; ViewDoc es grafo, no contrato universal de UI; no modificar otros repos ni sustituir contratos ausentes.

## AMBIGUEDADES
1. «disponibilidad actual viene de auditoria/ui.md»  
   No se identifica nodo, actor ni repo que produzca ese archivo, ni qué hacer si falta. Obliga a inventar el inventario de disponibilidad actual o a suponer que el artefacto existe.

2. «Estado = disponible/propuesto/bloqueado según WS10»  
   WS10 no figura en `depends_on` de WS09 y no se define su salida ni fallback. Obliga al ejecutor a inventar la regla de clasificación o a asumir un resultado de WS10 no suministrado.

## DRY-RUN
Lecturas previstas: guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `vistas.md`, nodo WS09 y contratos vecinos en `dag.yaml`. Cambios previstos: solo `borradores/vistas.md`; completar campos por fila y fichas. Dependencias: WS07 y `G_PRODUCT`; fuentes citadas WS10 y `auditoria/ui.md`, no declaradas como dependencias. Validaciones futuras: comprobar que toda fila tenga los seis campos, que los estados sean trazables a WS10, que la disponibilidad cite `auditoria/ui.md`, que no se inventen contratos y que WS11/WS18/WS22/WS23 puedan consumir el catálogo. Sin ejecutar.

## FUTURO
WS07 registra decisiones y `G_PRODUCT`; otro nodo debe producir `auditoria/ui.md` y la clasificación de WS10. WS11 consume el catálogo para navegación; WS18/WS22/WS23 lo usan como insumo. La promoción y el TaskDoc fijan archivos, pruebas y textos; la autorización de ejecución corresponde a un humano.
