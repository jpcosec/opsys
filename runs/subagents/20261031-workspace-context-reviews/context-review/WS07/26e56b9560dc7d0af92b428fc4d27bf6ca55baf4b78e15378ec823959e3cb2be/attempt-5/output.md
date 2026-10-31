REFORMULACION  
Propósito: que el humano dueño confirme o corrija P01–P09, designe con identidad a responsables de graph_ui/sldb/spec2viz y al operador Scion, y registre `source_mode`. Resultado: `decisiones.md` actualizado y `parameters.source_mode` en `dag.yaml`. Repo: `deskops`. Límites: no inventar aprobación, no autorizar ejecución, gates solo por registro explícito, sin cerrar sin actor/fecha ni designaciones en P01.

AMBIGUEDADES  
1. «`baseline_proposal` de dag.yaml»: no se define qué es ni aparece en el fragmento suministrado, mientras `output_scope` solo admite «decisiones.md; parameters.source_mode en dag.yaml». Obligaría a inventar si WS07 puede modificar esa clave, qué contiene y si hacerlo excede el alcance de salida.  
2. «reconsiderar alcance según P04»: no se precisa si implica editar nodos, dependencias o variantes del DAG, o solo dejar constancia en `decisiones.md`. `output_scope` no incluye cambios en nodos. Obligaría a inventar el alcance real de esa reconsideración.

DRY-RUN  
Lecturas previstas: `decisiones.md`, `dag.yaml` (parámetros y nodo WS07), `brief.md`, `alcance.md`, `cobertura.md` y, si existe, la salida de WS06 (`reconciliacion.md`). Cambios previstos: registrar estado, actor, fecha, evidencia y alternativa elegida por Pxx; fijar `source_mode`; documentar designaciones en P01. Dependencias: decisión humana sobre P01–P09 e identidades de responsables. Validaciones futuras: G_PRODUCT y G_WRITE_POLICY por registro explícito; coherencia de `source_mode`; efecto en WS08–WS10 y WS44. Sin ejecutar nada.

FUTURO  
El humano confirma/corrige decisiones y designa identidades. WS11/12 obtienen aceptación por repo receptor. WS44 ejecuta el probe Scion con acceso autorizado. La promoción fija archivos, pruebas y textos en el TaskDoc; no corresponde a WS07.
