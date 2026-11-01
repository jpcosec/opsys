## REFORMULACION
Encargo: convertir el borrador de user-flows en un documento de planificación que mapee UF01–UF10 a operaciones reales, con entrada/salida, error, nodos del DAG y gate humano, marcando huecos sin inventar capacidades. Resultado: `borradores/user-flows.md`. Repo dueño: `deskops`. Límites: no implementa UI/API, no promete funciones fuera de alcance, no declara disponible el ack de UF02 (pendiente WS12), UF08 solo lectura, delegación documentada pero no habilitada, G_PRODUCT ya satisfecho.

## AMBIGUEDADES
1. «cubrir manual, captura, revisión, cambios (UF07/WS29), arranque, multidesk, schemas y modo degradado» frente a una aceptación que solo exige una fila por UF. El input no define si «manual» requiere sección, columna o guion propio, ni qué evidencia lo cubre. Obligaría a inventar si basta con que las UF respalden el manual o si debe añadirse una cobertura separada.

## DRY-RUN
Un ejecutor leería `borradores/user-flows.md`, `decisiones.md`, `cobertura.md`, `validacion-humana.md` y `auditoria/{deskops,infraestructura,ui}.md` ya producidas vía WS06/WS07; consultaría WS11/WS12 para el estado del ack y WS29/WS39/WS41 para los flujos asociados. Cambiaría solo `borradores/user-flows.md`: tabla por UF con entrada, salida, operación (canal y efectos), error esperado, lista de nodos y gate humano o «ninguno adicional», manteniendo UF02 con respuesta local y ack como hueco. No tocaría código, tasks ni Board. Si falta una operación, marcaría hueco sin sustituto; si falta un gate humano, escribiría «ninguno adicional»; si falta una UF, la incorporaría desde el borrador. Validaría las diez UF, ausencia de promesas fuera de alcance, listas completas y correspondencia con `cobertura.md`. La promoción fijará formato exacto.

## FUTURO
El TaskDoc de promoción (no autorizado) concreta archivos y pills; WS09/WS11/WS12 consumen el mapeo; los gates WS16/30/37/39 y la prueba WS29 deciden aceptación. Nada de esto es ambigüedad del nodo.
