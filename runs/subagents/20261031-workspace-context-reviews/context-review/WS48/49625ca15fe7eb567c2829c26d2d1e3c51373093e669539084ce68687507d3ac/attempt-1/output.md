## REFORMULACION
WS48 es implementación en graph_ui: crear un punto común de admisión de escrituras UI en «modo manual exclusivo» (T-P03.1; contrato WS12 §5/5.9), con afirmación vigente externa a la petición y consultas de evidencia contraria; devuelve admitida o lectura/handoff con causa. Cubre POST /api/desk/advance y el botón Avanzar, rechazando en servidor antes de advance_task y conservando revision, gates y rechazos. No crea identidad, auth, lock, CAS ni lifecycle; no exige G_HUMAN_READ para desarrollar/probar. Repo graph_ui; output_scope frontends/mindmap/ y tests/. Límite: no habilita mutaciones reales.

## AMBIGUEDADES
1. «sin afirmación vigente o sin evidencia se rechaza» frente a «Con afirmación y sin evidencia contraria se admite»: «sin evidencia» no distingue consulta ausente de ausencia de contradicción; obliga a fijar criterio y podría bloquear toda admisión.
2. «sin evidencia contraria a una hora»: no fija ventana de vigencia; ¿«a la hora» o una hora? Obliga a inventar caducidad de la afirmación/evidencia.
3. «configuración confiable del responsable del desk, cargada por este nodo y sin valores reales en el repo»: faltan archivo, formato, canal de carga y definición de ese actor; obliga a inventar fuente y modelo de confianza.
4. «rechazo en el servidor antes de advance_task» con output_scope «frontends/mindmap/ ...; tests/»: si el servidor/advance_task no está ahí, el límite contradice el cambio exigido; obliga a ampliar alcance o inventar ubicación.
5. «Los consumidores ... dependen de este nodo y lo usan, ninguno lo reimplementa»: solo comprobable en nodos futuros; obliga a inventar una verificación o a omitirla.

## DRY-RUN
Ejecución hipotética. Leer: contrato WS12 §5/5.9, recibos per_delta de G_UI_WRITE/G_WRITE_CONTRACT para WS48, views/workflow/deskops/deskops-view.js, ruta POST /api/desk/advance y advance_task, config de prueba. Cambiar: módulo de admisión (archivo en TaskDoc), guard servidor antes de advance_task, estado/mensaje del botón, tests en store temporal. Dependencias: WS12 debe dar definición operativa, queries y respuesta ante ausencia; si falta, detener y registrar hueco con dueño deskops. Gates sin recibo: dejar pendiente, no declarar aceptado. Errores: contrato/query ausente o error, config inválida → lectura/handoff con buffer conservado. Validar: rechazo sin afirmación o evidencia; admisión con afirmación y sin evidencia contraria; evidencia posterior bloquea la siguiente; la ruta conserva revision/gates/rechazos.

## FUTURO
P01 emite el acta de recepción por delta; WS12 produce contrato, queries y definición operativa; los consumidores WS19.1–WS42 integran el módulo; WS16/G_HUMAN_READ habilita el uso de mutaciones. Son actores externos, no decisiones de este nodo.
