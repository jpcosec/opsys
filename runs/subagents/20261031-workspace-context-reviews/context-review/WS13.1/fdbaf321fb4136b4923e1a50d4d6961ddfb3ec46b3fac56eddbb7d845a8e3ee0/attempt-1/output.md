REFORMULACION  
Propósito: encargar la lectura inicial de un documento en el workspace, con contexto, enlaces y Code local. Resultado: Markdown legible, panel de identidad/relaciones/origen, navegación por enlaces y foco compartido entre texto, graph y Code. Repo dueño: `graph_ui`. Límites: solo lectura; conservar rutas del host; no crear índices ni otro workspace; no exigir conocer IDs; el delta puede integrarse en el ticket draft si WS11 lo decide.

AMBIGUEDADES  
1. La aceptación remite a «la matriz de WS09 y el contrato WS11», mientras `integration_mode` afirma «matriz WS06 llega de forma transitiva por WS11/WS12». Si son matrices distintas, el ejecutor debe inventar cuál define las representaciones soportadas y, por tanto, qué debe probar al alternar texto/graph/code. Cita: «en las representaciones que la matriz de WS09 y el contrato WS11 declaren soportadas».

DRY-RUN  
Lecturas previstas: contrato/acta WS11, matriz de representaciones aplicable, ticket workspace draft y rutas actuales de `graph_ui`. Cambios previstos: solo bajo `frontends/mindmap/views/workspace/document/` y `tests/`, más las rutas de lectura que fije WS11. Dependencias: WS11 y gate `G_UI_READ`; WS09 llega de forma transitiva. Validaciones futuras: abrir Markdown sin modelo; comprobar identidad, relaciones y origen; seguir enlace; alternar representaciones; seleccionar en texto/graph/Code y verificar foco compartido sin abrir copia; no usar IDs ni índices nuevos. Sin ejecutar.

FUTURO  
WS11 produce el acta y el contrato que eligen entre delta o integración del ticket draft, fijan rutas y relaciones, y resuelven `G_UI_READ` mediante el responsable de `graph_ui` designado. La promoción fijará archivos, pruebas y textos concretos en el TaskDoc.
