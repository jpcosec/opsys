## REFORMULACION

WS41 es un encargo de implementación en `graph_ui`: habilitar lectura segura entre desks resolviendo aliases/roots explícitamente autorizados por el contrato WS11 y usando APIs públicas de stores. El resultado esperado es que una persona lea un segundo desk del corpus WS40, vea identidad/origen, siga enlaces authored entre desks y vuelva por la historia, sin mutaciones cruzadas ni cambiar globalmente `SLDB_STORE`. Límites: solo lectura; cada request conserva su proyecto/store; alias no autorizado, path escapado o store ausente deben dar error visible; no se declara federación por copiar contenido. Consume WS13, WS11 y WS40, y requiere G_UI_READ por delta.

## AMBIGUEDADES

ninguna

Las referencias a «aliases/roots explícitamente autorizados en contrato WS11», «APIs públicas de stores» e «identidad/origen visibles» tienen productor nombrado y alcance.md fija detenerse y registrar el hueco si falta contrato o API. Los textos exactos de pantalla quedan al TaskDoc de promoción.

## DRY-RUN

Un ejecutor futuro leería el contrato de navegación WS11, el manifiesto y corpus WS40, y la implementación WS13 en `graph_ui`. Cambios previstos: resolución de aliases/roots por request en `frontends/mindmap/source/`; presentación de store/origen, navegación entre desks y retorno por historia en `views/workspace/`; pruebas en `tests/`. No modificaría `SLDB_STORE` global ni escribiría en los stores.

Dependencias: WS11 debe aportar resolución repo/store, identidad y modo multidesk read-only; WS40, los dos repos temporales con commits, documentos y enlaces authored; WS13, lectura de documento/fuente, enlaces e historia. G_UI_READ debe tener recibo del delta WS41 antes de promoción/ejecución autorizada. Si falta contrato, API, ruta o alias autorizado, se detiene y registra el hueco con repo dueño, sin sustituto.

Validación esperada: sobre dos stores WS40, comprobar lectura del segundo desk, identidad/origen, enlaces cruzados y retorno; provocar alias no autorizado, path escapado y store ausente esperando error visible; verificar ausencia de mutaciones cruzadas y de cambio global de store. WS16 validará UF08 con humano real.

## FUTURO

El receptor P01 en `graph_ui` produce el acta G_UI_READ por delta. La promoción fija archivos, pruebas y textos de pantalla. WS16 ejecuta la validación humana de UF08 y registra fallos o tiempos; no corresponde a WS41 aprobar ni sustituir esa aceptación.
