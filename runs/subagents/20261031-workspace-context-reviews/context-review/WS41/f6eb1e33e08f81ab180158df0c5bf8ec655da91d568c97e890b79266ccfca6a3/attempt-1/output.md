REFORMULACION
WS41 encarga implementar en graph_ui la lectura segura de un segundo desk desde el workspace/Mindmap. Resultado: resolver alias/roots autorizados por WS11 usando APIs públicas de store, conservar proyecto/store por request sin alterar el global SLDB_STORE, mostrar identidad/origen, seguir enlaces authored entre desks y volver por la historia. Límites: solo lectura, sin mutaciones cruzadas ni federación por copia, corpus WS40, rechazo de alias/root/path no autorizados; `promotion: not_authorized` y G_UI_READ pendiente por delta.

AMBIGUEDADES
1. `cobertura.md` dice «WS41 lectura multidesk, con WS13/14/15; WS40 corpus», pero `dag.yaml#node:WS41` solo declara `depends_on: WS13, WS11, WS40`. El ejecutor tendría que inventar si WS14 y WS15 son prerrequisitos de WS41 o piezas del recorrido UF08 que se validan aparte; WS16 ya depende de ambas.

DRY-RUN
Lecturas: contrato WS11 (aliases/roots, identidad/origen, APIs públicas citadas), manifiesto de WS40 (roots, stores, commits y documentos clave), salidas de WS13 y código actual del host. Cambios previstos: resolver alias/root por request; pasar store/proyecto a las APIs públicas; renderizar identidad/origen; navegar enlaces authored entre desks registrando historia; producir errores visibles para alias no autorizado, path escapado y store ausente; añadir tests de rechazo y de no mutación. Dependencias: WS13 cerrado, contrato WS11 publicado, manifiesto WS40 reproducible y recibo G_UI_READ del delta concreto; si falta contrato/API, detenerse y registrar el hueco según alcance.md. Validación esperada: tests con los dos stores temporales de WS40; comprobar que SLDB_STORE global no cambia, que no hay mutaciones cruzadas, que se sigue el enlace entre desks y se vuelve por historia, y que los tres errores son visibles. No se ejecuta nada ahora.

FUTURO
WS16 consumirá WS41 para la validación humana de UF08; el solicitante P01/receptor de graph_ui emitirá el acta G_UI_READ del delta; la promoción exige preflight task-only y fijar archivos/pills. Si se confirma que WS14/15 son prerrequisitos, un humano debe corregir `depends_on`.
