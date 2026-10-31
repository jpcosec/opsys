## REFORMULACION
**Propósito:** convertir las propuestas P01–P09 y `baseline_proposal` en registro explícito del humano, designar responsables de graph_ui, sldb y spec2viz, y designar operador Scion con su acceso read-only.  
**Resultado:** `decisiones.md` actualizado y, en `dag.yaml`, `baseline_proposal` y `parameters.source_mode` confirmados.  
**Repo:** deskops.  
**Límites:** solo planificación; no editar nodos/aristas, no ejecutar Scion, no conceder `G_EXEC`, no inferir aprobación ni sustituir decisiones humanas.

## AMBIGUEDADES
**Ninguna.** Las identidades, el acceso Scion, `source_mode` y la confirmación de P01–P09 son decisiones humanas pendientes, no datos que el ejecutor deba inventar. La aceptación exige registro con actor/fecha y prohíbe cerrar por inferencia.

## DRY-RUN
- **Lecturas:** `decisiones.md`; `validacion-humana.md` para P08; `dag.yaml` (`baseline_proposal`, `parameters.source_mode`, variantes declaradas); `reconciliacion.md` vía WS06; límites en `alcance.md`/`brief.md`.
- **Cambios previstos:** registrar P01–P09 con estado, actor, fecha y evidencia; en P01, responsables graph_ui/sldb/spec2viz y operador Scion con acceso read-only; fijar `source_mode=editable|read_only`; actualizar `baseline_proposal` si el humano lo confirma. No editar nodos ni gates aquí.
- **Dependencias:** WS06 aporta la matriz y responsables “por designar”; WS11/12 aceptan deltas por repo; WS44 queda condicionada al registro de operador/acceso; `G_PRODUCT` y `G_WRITE_POLICY` dependen de este registro.
- **Validaciones futuras:** comprobar actor humano, fecha y evidencia por decisión; P04 reflejado exactamente en `source_mode`; P01 con las cuatro designaciones; no tratar `G_PRODUCT` como aprobación del plan completo ni P01 como autorización de ejecución.

## FUTURO
El humano confirma o corrige P01–P09, identidades, acceso Scion, P08 y `source_mode`. WS11/12 aceptan por repo receptor. WS44 ejecutará el probe solo tras el registro. WS08/09/10 consumirán `G_PRODUCT`. `G_EXEC` lo decide un actor externo. La promoción fijará archivos, pills y evidencias en TaskDoc.
