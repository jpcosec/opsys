REFORMULACION
Propósito: revisar si WS34.1 se entiende como encargo de planificación para un adaptador público restringido de dispatch Scion. Resultado: implementación en `deskops` (`runtime/`, CLI/API según WS12, `tests/`) con confirmación, identidad de intento, timeout/errores y autoridad del coordinador; aceptación con G_SCION/G_EXEC y agente real que demuestre dispatch aceptado y otro rechazado o vencido, sin shell arbitrario ni duplicar transporte. Repo dueño: `deskops`. Límites: no revisar vecinos, no ejecutar, gates pendientes intencionales y Pxx no aprobadas.

AMBIGUEDADES
1. «timeout/errores» y «vencido por timeout»: no fija umbral, política de timeout ni formato de error. WS34.2 sí dice «con el umbral del contrato WS12», pero WS34.1 no lo remite. Obligaría a inventar cuándo vence y cómo se reporta.
2. «identidad de intento»: no indica si la produce Scion, WS33 o el adaptador, ni su formato/unicidad. Aunque depende de WS33, el nodo solo remite expresamente la autoridad del coordinador a WS12 («Autoridad del coordinador según contrato WS12»). Obligaría a inventar fuente y semántica.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, nodo WS34.1, vecinos WS33/WS12/WS34/WS34.2 y gates. Cambios previstos: ninguno; es revisión. Dependencias: WS33 (agregado de vínculos), WS12 (contrato de operaciones) y gates G_EXEC, G_SCION, G_WRITE_CONTRACT. Validaciones futuras: gates satisfechos, agente real con dispatch aceptado y rechazado/timeout, ausencia de shell arbitrario y de transporte duplicado; la promoción fijará archivos, pruebas y evidencia.

FUTURO
WS07 designa actores y resuelve Pxx; WS44 produce el probe y G_SCION; el humano resuelve G_EXEC; WS12 produce G_WRITE_CONTRACT; los hijos de WS33 aportan vínculos de intento; la promoción fija TaskDoc, archivos y evidencia; WS34.2 cubre reply. Nada de esto se decide aquí.
