**REFORMULACION**  
Propósito: revisar PK07 como agrupación de dos extensiones independientes —Changes/impacto (WS29) y modelos/Schema (WS39)— sin ejecución propia ni nuevas tareas o aristas. Resultado sustantivo: evidencia de que ambos hijos cumplen su aceptación, que el manual etiqueta cada extensión según evidencia y que ninguna se convierte en prerrequisito del lector o manual básico. Repo dueño: deskops para la agrupación; los hijos implementan en graph_ui. Límites: no ejecutar, no autorizar mutaciones, no reimplementar modelos, no presumir CST/Kimun, no bloquear lector/manual básico.

**AMBIGUEDADES**  
1. «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada» frente a «Un nodo `aggregate` no se ejecuta: termina cuando terminan sus hijos». Contradice el criterio de agregado o exige una integración no definida. Obligaría a inventar qué artefacto, comprobación u owner demuestra la «integración indicada», o si bastan las salidas de WS29/WS39.  
2. «Manual etiqueta cada extra según evidencia» no nombra productor, artefacto ni umbral de evidencia dentro de PK07. Obligaría a inventar quién actualiza el manual y qué cuenta como evidencia suficiente para etiquetar cada extensión.

**DRY-RUN**  
Hipotético: WS29 y WS39 no tienen arista entre sí; se ejecutan en paralelo tras sus prerrequisitos, no en orden secuencial. WS29 recibe lectura/vecindad de WS15/24 y G_UI_READ; produce vista Changes/impacto y errores de check/doctor/drift. WS39 recibe contrato WS12 y lector WS13; produce entrada Schema/editor y acta humana. Integración: confrontar ambos outputs contra su aceptación; no hay artefacto común ni dependencia mutua. Validación futura: mutación real a 1 hop en WS29; UF09 inspección/mutación y aceptación humana en WS39; manual etiqueta por evidencia sin presumir CST/Kimun.

**FUTURO**  
WS15/24/12/13/04 aportan insumos; WS31/manual y la persona P08 producen etiqueta/acta; G_HUMAN_MODEL decide disponibilidad. Nada se ejecuta ni aprueba aquí.
