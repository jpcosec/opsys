REFORMULACION
Propósito: escribir entradas e índices authored para el desk ejemplo, sin producir el corpus. Resultado: plantillas Markdown versionadas en `ejemplo/nav/`, consumibles por el generador WS40. Repo: `deskops`, bajo `desk/drawer/plans/workspace-documental/`. Límites: no escribir repos reales, no copiar inventarios derivados, no duplicar el registry, no implementar lector/UI; puede ir antes de WS16 y WS30 las integra. Promoción no autorizada.

AMBIGUEDADES
1. «Mostrar el root/store de procedencia al resolver los dos desks del manifiesto WS40». No aclara si “mostrar” exige contenido concreto en las plantillas —formato, ubicación— o una comprobación/acta de aceptación. Obligaría a inventar el artefacto y podría exceder `documentation` hacia UI/renderer.
2. «recorrer links Markdown sin UI». No fija criterio ni método: ¿todos los enlaces deben resolver?, ¿solo los de los dos desks?, ¿inspección manual o script? El ejecutor tendría que inventar el umbral comprobable.
3. «source versionado y destino temporal no son registros independientes». No define observación verificable —identidad de contenido, ausencia de duplicados, hash—; obligaría a inventar cómo demostrarlo.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura y nodo/aristas WS11, WS40, WS30 y WS43. Cambios previstos: ninguno en esta revisión; si se promueve, crear plantillas bajo `ejemplo/nav/`. Dependencias: contrato de navegación WS11 y generador WS40; WS30 consume; WS16 no bloquea. Validaciones futuras: regenerar corpus temporal WS40 con `ejemplo/nav/`, recorrer enlaces sin UI, comprobar procedencia root/store de los dos desks, que fuente y destino temporal no dupliquen registros y que no se copie el registry.

FUTURO
WS11 fija el contrato de navegación; WS40 define cómo acepta la ruta de plantillas y emite el manifiesto; el TaskDoc de promoción fija archivos/pills; el humano o WS07 resuelve Pxx y autoriza; WS30 valida la integración; WS43 publica en el desk real.
