## REFORMULACION
WS07 es un encargo de planificación en `deskops`: el humano dueño del producto confirma o corrige P01–P09, deja registro explícito de actor/fecha/alternativa, designa responsables de graph_ui/sldb/spec2viz y operador Scion con su acceso read-only, y fija `source_mode`. Resultado: `decisiones.md` actualizado y `parameters.source_mode` sincronizado. Límites: no ejecutar, no configurar Scion, no conceder G_EXEC, no editar nodos y no inferir aprobación; los gates solo pasan por registro explícito.

## AMBIGUEDADES
1. «output_scope: decisiones.md; `baseline_proposal` y parameters.source_mode en dag.yaml» frente a «leyendo ... `baseline_proposal` de dag.yaml». El input no define `baseline_proposal` ni aclara si WS07 debe modificarlo o solo leerlo. Obliga a inventar su contenido y si entra en el cierre.
2. «reconsiderar alcance según P04 dentro de las variantes ya declaradas en dag.yaml, sin editar nodos aquí». No se indican las variantes concretas ni dónde registrar esa reconsideración. Obliga a inventar el artefacto y el alcance del ajuste.
3. «registrar qué acceso read-only tiene» el operador Scion frente a «No cerrar sin registro de designación de responsables ... y operador Scion en P01». La aceptación solo exige identidad, no el nivel de acceso que el scope pide registrar. Obliga a inventar si el acceso debe constar y cómo se verifica.

## DRY-RUN
Lecturas: `decisiones.md`, `validacion-humana.md`, `dag.yaml` (`parameters`, nodo WS07, gates), `brief.md` y `alcance.md`. Cambios previstos: entradas Pxx con estado, actor, fecha, evidencia y alternativa; `parameters.source_mode=editable|read_only`; eventual `baseline_proposal` según se aclare. Dependencias: matriz de WS06 y confirmaciones humanas. Validaciones futuras: G_PRODUCT exige P01/P02/P07/P08/P09 y designaciones; G_WRITE_POLICY exige P03–P06; WS11/12 aceptarán por repo; WS44 hará el probe real. Sin ejecución.

## FUTURO
El humano decide las Pxx y designa identidades; WS11/12 aceptan deltas por repo; WS44 produce G_SCION tras su probe; WS08/09/10 y el contrato de escritura de WS12 dependen de estos registros.
