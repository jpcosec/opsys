## REFORMULACION

**Propósito:** revisar PK07 como encargo de planificación: agrupación de revisión de las extensiones independientes WS29 (Changes) y WS39 (modelos), sin evaluar el producto ni a sus hijos.

**Resultado:** un veredicto de revisión sobre PK07 —encargo comprensible o ambigüedades concretas—, no una autorización de ejecución.

**Repo:** PK07 no declara `owner_repo`; es agrupación. Sus hijos pertenecen a `graph_ui`.

**Límites:** no revisar los bloques edge de vecinos (WS15, WS24, WS12, WS16); no ejecutar; no aprobar propuestas Pxx; no exigir gates de hijos; un gate pendiente es intencional.

## AMBIGUEDADES

1. «con input y contrato actuales y disposición guardada, según `context_review.py status`»: el input no indica repo/ruta del script, ni dónde ni con qué esquema se guarda la «disposición». Obligaría a inventar la ubicación de la herramienta y el formato de almacenamiento.

2. «con input y contrato actuales»: no se define el criterio de vigencia (¿coincidencia de hash?, ¿fecha?, ¿comparación con el `dag.yaml` vigente?). El ejecutor tendría que inventar cómo decidir si una revisión está «vigente».

3. «bloqueo explícito con responsable y dependencia en su disposición»: no se especifica el campo o formato donde constan responsable y dependencia. Obligaría a inventar el esquema de la disposición.

## DRY-RUN

- **Lecturas previstas:** nodo PK07 y aristas WS29/WS39 en `dag.yaml`; guía; `brief.md`; `alcance.md`; `decisiones.md`; `cobertura.md`.
- **Cambios previstos:** ninguno en código ni en `dag.yaml`; a lo sumo, registrar la disposición de PK07, fuera de este nodo.
- **Dependencias:** revisiones de WS29 y WS39 vigentes; disponibilidad y semántica de `context_review.py status`; formato de disposición.
- **Validaciones futuras:** consultar estado por hijo; comprobar correspondencia input/contrato con la versión actual; verificar que todo bloqueo tenga responsable y dependencia.

## FUTURO

- La revisión de WS29 y WS39 produce sus disposiciones; WS29 queda supeditada a `G_UI_READ` y WS39 a `G_HUMAN_MODEL`, acta humana y `G_WRITE_CONTRACT`.
- Las propuestas P04/P03/P06 las resuelve un humano en WS07, no este nodo.
- El repo dueño de `context_review.py` debe precisar ruta y esquema de disposición; si falta, PK07 no puede declararse verdadero por inferencia.
