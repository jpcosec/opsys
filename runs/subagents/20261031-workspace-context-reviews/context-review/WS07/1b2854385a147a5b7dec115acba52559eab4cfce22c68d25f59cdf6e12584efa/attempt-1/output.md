## REFORMULACION
Propósito: que un humano resuelva P01–P09 y designe responsables con identidad, registrando `source_mode`. Resultado: `decisiones.md` actualizado, `baseline_proposal`/`parameters.source_mode` sincronizados y gates G_PRODUCT/G_WRITE_POLICY registrados. Repo: `deskops`. Límites: no implementar, no editar nodos, no configurar/ejecutar Scion, no inventar aprobación ni conceder G_EXEC.

## AMBIGUEDADES
1. «Designar con identidad explícita a responsable de graph_ui, sldb y spec2viz» y «con identidad registrada por el solicitante en P01». No se define qué dato constituye identidad suficiente ni cómo consta la aceptación del designado. Obligaría a inventar el formato y el criterio de designación válida.

2. «registrar qué acceso read-only tiene» el operador Scion. No se delimita el objeto del acceso —API, Hub, configuración, logs— ni su granularidad. El ejecutor tendría que inventar qué alcance consignar para que WS44 pueda probar sin ambigüedad.

3. «El humano dueño del producto confirma o corrige P01–P09» frente a «solicitante humano de esta sesión o persona que designe explícitamente» en `decisiones.md`. No se aclara si «dueño del producto» es el solicitante u otro rol; obligaría a decidir por cuenta propia quién puede firmar cada Pxx.

## DRY-RUN
Lecturas previstas: `decisiones.md`, `validacion-humana.md` para P08, `dag.yaml` (`baseline_proposal` y `parameters.source_mode`), `reconciliacion.md` de WS06 y `brief.md`/`alcance.md` como límites. Cambios previstos: estados, actor, fecha, alternativa y evidencia por Pxx; designaciones P01; valor `source_mode`; nota de alcance según P04. Dependencias: WS06 debe haber producido la matriz; WS44 espera el registro de acceso. Validaciones futuras: G_PRODUCT y G_WRITE_POLICY solo por registro explícito; G_SCION pertenece a WS44. Sin ejecución.

## FUTURO
La decisión material de P01–P09 corresponde al humano; WS11/12 aceptan deltas por repo; WS44 ejecuta el probe read-only con G_PRODUCT y acceso registrado; G_EXEC lo autoriza fuera de este nodo. Nada de eso es ambigüedad de WS07.
