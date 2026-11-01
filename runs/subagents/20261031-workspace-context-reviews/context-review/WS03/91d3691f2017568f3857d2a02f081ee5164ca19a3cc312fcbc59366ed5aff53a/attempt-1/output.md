## REFORMULACION
WS03 es un encargo de planificación para auditar en solo lectura la persistencia, consultas y notaciones reales de sldb/pron/spec2viz. Debe producir una única salida documental en `deskops:desk/drawer/plans/workspace-documental/auditoria/infraestructura.md`, sin cambios interrepo, distinguiendo API comprobada con lectura citada, ausencia y hueco. Límites: no implementar, no modificar otros repos y tratar Kimun solo como referencia. Depende de WS01 (brief/glosario).

## AMBIGUEDADES
1. «distinguir API comprobada (lectura citada del estado actual), ausencia y hueco». No se define qué separa «ausencia» de «hueco»; el ejecutor tendría que inventar una taxonomía para clasificar hallazgos y decidir cuándo algo es capacidad no expuesta frente a falta de contrato/dato.

## DRY-RUN
Un ejecutor futuro leería el nodo en `dag.yaml`, su `task_file`, brief/alcance/decisiones y el código o documentación observable de sldb/pron/spec2viz, sin escribir en ellos. Previsto: crear o actualizar solo `auditoria/infraestructura.md` en deskops, con secciones de fuente/payload, conflictos y locks, referencias documentales, búsquedas e índices, y alcance ViewDoc, citando lecturas y separando comprobado, ausente y hueco. Consumiría WS01 como prerrequisito documental. Si falta WS01, un repo o una fuente necesaria, se detendría y registraría el hueco con repo dueño, sin sustituto. Validación esperada: revisar que la salida sea documental, no haya cambios interrepo, cada afirmación comprobada tenga cita y las tres categorías de aceptación estén distinguidas. WS03 no produce gates.

## FUTURO
WS06 consume esta auditoría para su matriz de correspondencia por repo dueño. La promoción queda no autorizada hasta que un TaskDoc fije archivos, pills y evidencia, con autorización humana separada; ningún recibo técnico existe aún.
