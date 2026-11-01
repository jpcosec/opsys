REFORMULACION
WS06 es un nodo de planificación en `deskops`. Debe proponer en `reconciliacion.md` una matriz que corresponda deltas/capacidades con repos dueños, clasificando cada fila como ya cubierto, extender ticket existente o nuevo delta, con path/símbolo/commit observado y responsable P01 cuando aplique; además, registrar la atomización propuesta y la cobertura de nodos. Límites: no implementa, no modifica el Board, no notifica/despacha, no crea gates, firmas ni recepción ficticia, no ejecuta WS05 ni autoriza Scion; WS11/12 solo enlazan actas del receptor P01. Depende de WS02–WS04.

AMBIGUEDADES
1. «Registrar en reconciliacion.md la atomización propuesta»: no fija granularidad ni criterio de agrupación/orden, y la aceptación solo exige «Matriz con una fila por delta o capacidad propuesta...». Obliga a inventar si la atomización es por fila C-nn, por repo, por fase o por secuencia de archivos, y cómo comprobar que está completa; la aceptación no la cubre.

DRY-RUN
Hipotético, sin ejecutar. Lecturas: guía, brief, alcance, decisiones, cobertura, `reconciliacion.md`, `dag.yaml` (WS06 y aristas WS02–04) y auditorías aprobadas WS02–04. Cambios: editar/crear `reconciliacion.md`; ajustar matriz por repo, atomización y tabla de cobertura; no tocar Board ni tareas externas. Dependencias: WS02–04 entregadas y aprobadas; designaciones P01 y límite de deskops («No designado en P01» como dato); WS11/12, WS20/WS45 y Scion quedan futuros. Gates: ninguno propio; no emitir recibos. Errores: falta de auditoría o commit → marcar «no comprobado» con causa; delta indefinido → no aprobarlo; si falta base imprescindible, detenerse y registrar hueco. Validación esperada: cada C-nn/nodo mapeado o justificado sin delta; una fila por capacidad; owner, commit y responsable; sin gates/recepción ficticia; atomización y cobertura presentes; Board intacto.

FUTURO
WS07 reutiliza el registro de decisiones; WS11/12 consumen filas y enlazan actas P01 por delta; P01 produce actas externas; la promoción de WS06 requiere TaskDoc y preflight; el operador Scion se designa al abordar el ramal E.
