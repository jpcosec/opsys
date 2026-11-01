## REFORMULACION
**Propósito:** agrupar la integración de edición de campos y relaciones del workspace documental.  
**Resultado:** nodo agregado no ejecutable; se cierra cuando WS19.1 y WS19.2 cumplan su aceptación, reutilizando editores/API y la precondición que fije WS12, con conflicto visible y campos workflow-protected no editables.  
**Repo dueño:** graph_ui.  
**Límites:** no duplicar la base a1b2b22/f16fcd1/134a665; no crear semántica de relaciones en el componente; no habilitar mutaciones UI sin G_HUMAN_READ; los gates pendientes son intencionales.

## AMBIGUEDADES
ninguna.

## DRY-RUN
**Lecturas (sin ejecutar):** nodo WS19; gates G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE y G_WRITE_CONTRACT; bloques WS12/WS19.1/WS19.2/WS21/WS42 solo como dependencias; brief, alcance, decisiones y reconciliación.  
**Cambios previstos:** ninguno propio; el agregado reúne las salidas de WS19.1 y WS19.2.  
**Dependencias:** contrato WS12 (whitelist, precondición, canal/API), hijos WS19.1/WS19.2 y gates con resolutores WS16/WS45/P01/WS12.  
**Validaciones futuras:** aceptación de cada hijo, evidencia por gate, recibo G_UI_WRITE por delta concreto en graph_ui, verificación G_PAYLOAD_PRECONDITION en sldb y prueba de guardado/conflicto. No se ejecuta nada.

## FUTURO
La promoción decide entre delta o extensión del ticket existente de edición y fija archivos, casos y textos. WS12 publica la representación de la precondición y el contrato por operación; WS45 verifica esa precondición en sldb; WS16 produce el acta de lectura; el receptor P01 registra el acta G_UI_WRITE por delta. La aceptación efectiva de WS19.1/WS19.2 y del agregado queda para esos nodos y sus validaciones humanas/técnicas.
