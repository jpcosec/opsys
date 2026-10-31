REFORMULACION  
Propósito: revisar PK06 como encargo de planificación de una agrupación de revisión para la publicación básica. Resultado: PK06 será verdadero cuando WS31 y WS43 tengan `context_review` vigente, con input/contrato actuales y disposición guardada, sin ambigüedad de encargo o con bloqueo explícito que indique responsable y dependencia. Repo: no aplica; PK06 no es deliverable ni se ejecuta. Límites: no ejecutar, no promover, no resolver Pxx y no revisar los bloques edge de WS31/WS43 como contratos propios.

AMBIGUEDADES  
ninguna.

DRY-RUN  
Lecturas previstas: esta guía, el nodo PK06 en `dag.yaml` y el estado `context_review` de WS31 y WS43 según `context_review.py status`. Cambios previstos: ninguno; PK06 solo agrupa revisión. Dependencias: las revisiones de sus hijos directos; sus dependencias operativas pertenecen a esos hijos. Validaciones futuras: comprobar que cada review sea vigente respecto de input y contrato, que la disposición esté guardada y que todo bloqueo tenga responsable y dependencia explícitos. Sin ejecución.

FUTURO  
La obtención de reviews vigentes o bloqueos de WS31 y WS43, la validación manual previa y las decisiones humanas asociadas —incluida P09 y los gates de esos nodos— corresponden a otros nodos o al humano; no son ambigüedades de PK06.
