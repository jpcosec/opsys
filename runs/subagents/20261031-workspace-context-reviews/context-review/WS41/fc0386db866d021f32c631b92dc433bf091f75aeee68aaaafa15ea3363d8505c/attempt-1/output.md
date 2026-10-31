## REFORMULACION
**Propósito:** implementar en `graph_ui` lectura segura entre desks, resolviendo aliases/roots autorizados por el contrato WS11 y usando APIs públicas de stores, sin mutaciones cruzadas ni cambio global de `SLDB_STORE`.  
**Resultado:** leer un segundo desk del corpus WS40 y volver, mostrando identidad/origen, links ida/vuelta y errores de acceso; rechazar roots arbitrarios o paths escapados.  
**Repo:** `graph_ui`. **Salidas:** `frontends/mindmap/source/`, endpoints de lectura por store, `views/workspace/`, `tests/`.  
**Límites:** solo lectura; no federación por copia; promoción `not_authorized`; depende de `G_UI_READ` pendiente.

## AMBIGUEDADES
1. «links ida/vuelta»: no define si son enlaces authored entre documentos/desks o retorno de navegación/historia. WS40 solo garantiza segundo desk y manifiesto. Obligaría a inventar si WS41 debe crear enlaces en el corpus —fuera de su `output_scope`— o solo probar la vuelta.
2. «endpoints de lectura por store» frente a «usando APIs públicas de stores»: no aclara si debe crear endpoints nuevos en `graph_ui` o solo consumir APIs existentes. Obligaría a inventar superficie API y alcance de tests.
3. «errores de acceso»: no concreta taxonomía ni presentación esperada. Obligaría a inventar qué casos son error de acceso y cómo se comprueban.

## DRY-RUN
**Lecturas previstas:** nodo WS41, contrato de salida WS11, manifiesto/corpus WS40, lector WS13, código y APIs de store existentes, tests de `graph_ui`.  
**Cambios previstos:** resolución read-only de aliases/roots autorizados, adaptador por store, vista con identidad/origen y vuelta, manejo honesto de errores, tests de rechazo de roots/paths.  
**Dependencias:** WS11, WS40, WS13 y gate `G_UI_READ`.  
**Validaciones futuras:** pruebas automatizadas de lectura entre dos stores; UF08 en WS16 con humano real. No se ejecuta nada.

## FUTURO
WS11 produce contrato y `G_UI_READ`; WS40 produce corpus y manifiesto; WS13 entrega lector; WS16 valida UF08 con humano. WS07 designa responsables y las Pxx siguen pendientes de decisión humana. La promoción de WS41 requiere autorización posterior.
