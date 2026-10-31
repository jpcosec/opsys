REFORMULACION  
Propósito: inventariar, sin ejecutar, identidad y API pública de Scion para separar slug/agente/intento/dispatch/mensaje/conversación y permisos. Resultado: `auditoria/scion.md`. Repo dueño: `deskops`; depende de WS01. Límites: lectura de código/docs en `deskops` y `../scion`, RunDoc/templates y configuración sin secretos; sin endpoints vivos, credenciales, creación de agentes, mensajes ni cambios de configuración; no muestra tokens; no produce G_SCION, que corresponde a WS44.

AMBIGUEDADES  
1. «separar slug/agente/intento/dispatch/mensaje/conversación y permisos» frente a una aceptación que solo exige «No usar tablas internas como interfaz; señalar los campos internos… y capacidades que requieren API real». Obligaría a inventar qué matriz o evidencia demuestra la separación completa y si el inventario de permisos forma parte de la aceptación.  
2. «API pública de Scion (endpoints/SDK documentados o exportados; no tablas ni funciones internas)» frente a «API pública definida en el scope». Obligaría a inventar la precedencia cuando documentación y exports discrepan, o el criterio para decidir si un símbolo exportado pero auxiliar cuenta como API pública; sin ello, el límite «no funciones internas» no es plenamente operable.

DRY-RUN  
Lecturas previstas: brief, alcance, decisiones y DAG; en ejecución, código/docs de `deskops` y `../scion`, RunDoc/templates y configuración sin secretos. Cambios previstos: solo `auditoria/scion.md`; ninguno en código, configuración o Scion. Dependencias: WS01 como prerrequisito; WS07/WS44 y G_SCION son posteriores, no requisitos para cerrar WS05. Validaciones futuras: revisión del informe contra aceptación, probe real de WS44 y promoción/TaskDoc por otro actor. Nada ejecutado.

FUTURO  
WS07 designa operador y acceso Scion; WS44 ejecuta el probe read-only y produce G_SCION o queda bloqueada; WS32/33 consumen las capabilities inventariadas. La promoción de WS05 y su TaskDoc corresponden a otro nodo o decisión humana; las Pxx siguen pendientes. WS05 puede cerrar el inventario sin API viva.
