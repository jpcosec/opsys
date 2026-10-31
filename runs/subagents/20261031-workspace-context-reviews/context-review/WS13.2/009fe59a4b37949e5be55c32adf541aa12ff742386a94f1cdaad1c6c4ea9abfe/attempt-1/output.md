## REFORMULACION
Propósito: revisar WS13.2 como encargo de planificación, no como producto. Resultado esperado: veredicto sobre si propósito, resultado, repo dueño, límites, dependencias y aceptación son ejecutables sin inventar. Repo dueño: `graph_ui`. Límites: no ejecutar, no evaluar calidad del producto, no revisar contratos vecinos (bloques edge), no crear sustituto de contratos ni asumir aprobaciones.

## AMBIGUEDADES
1. «al añadir un documento al store temporal de prueba, aparece sin cambiar código». No define si «aparece» exige recarga manual, refresco automático o reinicio; el ejecutor tendría que inventar el criterio observable y el escenario de prueba.
2. «Explorador sobre documentos reales del store y Markdown no modelado del desk» frente a «al añadir un documento al store temporal de prueba, aparece sin cambiar código». La comprobación dinámica solo menciona el store; no aclara si un Markdown no modelado añadido al sistema de archivos del desk también debe aparecer sin cambio de código. Obliga a inventar el alcance de esa aceptación.
3. «sin conocer su ID ni usar índices nuevos». No precisa si el explorador puede apoyarse en el catálogo/filtro ya existente citado en reconciliación o debe listar por otra vía; fuerza a decidir el mecanismo aceptable.

## DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, reconciliación y nodo/aristas WS13.2, WS13, WS13.1, WS11 y gate G_UI_READ. Cambios previstos: ninguno; solo veredicto de revisión. Dependencias: WS11 (contrato de navegación/identidad y productor de G_UI_READ), WS13.1, agregado WS13; gate pendiente por delta. Validaciones futuras: prueba con store temporal real o corpus WS40, apertura de documento modelado y no modelado sin ID, alta dinámica, y recibo G_UI_READ propio. Sin ejecución.

## FUTURO
WS11 produce contrato de navegación, identidad y resolución repo/store. G_UI_READ se recibe por delta con actor P01, alcance, efecto y evidencia. WS13.1 entrega lectura base. La promoción fijará archivos, pruebas y textos en TaskDoc; su autorización y la recepción humana quedan fuera de este nodo.
