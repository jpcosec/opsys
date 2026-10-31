**REFORMULACION**  
Propósito: definir un adaptador público restringido para dispatch en el workspace documental, con confirmación por respuesta de la API de Scion, identidad de intento, timeout/errores y autoridad del coordinador. Resultado: implementación en `runtime/`, `cli/commands/runtime.py` o la API que fije WS12, con pruebas. Repo dueño: `deskops`. Límites: no shell arbitrario, no duplicar transporte, no ejecutar en esta revisión y promoción no autorizada.

**AMBIGUEDADES**  
Ninguna.

**DRY-RUN**  
Lecturas: guía, brief, alcance, decisiones, cobertura y nodo WS34.1; los bloques de WS33/WS12 se usan solo como contratos de dependencia. Cambios previstos: ninguno, es revisión. Dependencias: WS33 como agregado terminado por sus hijos, WS12 como contrato de operaciones, y gates G_EXEC, G_SCION y G_WRITE_CONTRACT. Validaciones futuras: que G_SCION/G_EXEC pasen; que un agente real demuestre un dispatch aceptado y uno rechazado o vencido por timeout; que no haya shell arbitrario ni transporte duplicado. Si falta contrato, API, dato o permiso, aplica la regla común: detenerse y registrar el hueco con repo dueño.

**FUTURO**  
WS12 produce la whitelist, canal, efectos, autoridad del coordinador y criterios de timeout/error; WS44 produce la evidencia de G_SCION; un humano resuelve G_EXEC y las decisiones Pxx aplicables; WS33 aporta identidad y vínculo del intento. La promoción fijará archivos, pills, átomos y evidencia, y requerirá autorización humana.
