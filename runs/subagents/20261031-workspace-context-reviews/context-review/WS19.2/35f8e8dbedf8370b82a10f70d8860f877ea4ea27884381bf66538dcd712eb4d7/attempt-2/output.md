**REFORMULACION**  
Propósito: encargo de implementación para alta/baja de relaciones permitidas en la UI del workspace, usando API real y before-image, sin crear semántica de relaciones en el componente. Resultado: ambos cambios persisten y se confirman tras recargar; una relación no permitida o una revisión obsoleta se rechaza con error visible. Repo dueño: `graph_ui` (`frontends/mindmap/views/workspace/relations/`; endpoints autorizados por WS12; `tests/`). Límites: depende de WS12 y de G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE y G_WRITE_CONTRACT; no duplicar el ticket `editing`; promoción no autorizada.

**AMBIGUEDADES**  
1. Cita: «usando API real y before-image». El contrato WS12 dice que la precondición puede ser «before-image por valor, token publicado o CAS solo si el contrato lo fija», y G_PAYLOAD_PRECONDITION habla de la «representación que fije WS12». Si WS12 no adopta before-image, el ejecutor debe inventar si WS19.2 exige esa representación concreta o si debe usar token/CAS. Es una contradicción entre el alcance del nodo y el contrato que lo gobierna.

**DRY-RUN**  
Lecturas: guía, brief, alcance, decisiones, nodo WS19.2, edges WS12/WS19 y gates. Cambios previstos: ninguno; esta revisión no ejecuta ni modifica archivos. Dependencias: contrato WS12 y gates G_HUMAN_READ (WS16), G_PAYLOAD_PRECONDITION (WS45), G_UI_WRITE (receptor P01 por delta) y G_WRITE_CONTRACT (WS12 por delta). Validaciones futuras: WS12 debe publicar whitelist de relaciones/endpoints y fijar la representación de la precondición; WS45 debe verificar G_PAYLOAD_PRECONDITION; WS16 debe producir el acta de lectura; el receptor P01 debe emitir el acta por delta. Pruebas esperadas, no ejecutadas: alta/baja persisten tras recarga; rechazo visible de relación no permitida y de revisión obsoleta.

**FUTURO**  
WS12 produce el contrato de operaciones y la representación de la precondición; WS45 verifica la precondición de payload; WS16 aporta el acta humana de lectura; el receptor P01 registra la aceptación por delta; el TaskDoc de promoción fija archivos, pills, evidencia y casos concretos. WS19 solo cierra cuando cierran sus hijos. Nada de esto se ejecuta aquí.
