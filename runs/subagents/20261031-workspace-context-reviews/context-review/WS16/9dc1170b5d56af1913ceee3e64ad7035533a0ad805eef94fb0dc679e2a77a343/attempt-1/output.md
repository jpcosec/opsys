## REFORMULACION
**Propósito:** validar con una persona real el recorrido de lectura y descubrimiento del workspace documental.
**Resultado:** acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/lectura/acta.md` y resolución del gate `G_HUMAN_READ`.
**Repo dueño:** `graph_ui`.
**Límites:** no sustituir aprobación humana; no mutar el baseline antes del gate; UF08 solo lectura, sin mutación interdesk; el corpus lo produce WS40; renderizaciones read-only pueden avanzar en paralelo sin implicar aceptación.

## AMBIGUEDADES
1. **Alcance del corpus/ejemplo.** Cita: «desk ejemplo y protocolo en validacion-humana.md» y «Preparar corpus por WS40». La primera frase puede leerse como que WS16 prepara el desk de ejemplo; la segunda y validacion-humana.md asignan a WS40 el rol de «productor único». Obliga a inventar si WS16 crea/edita el corpus o solo consume su manifiesto.
2. **Mediciones aplicables.** Cita: «Reportar tiempos y pruebas técnicas por separado» junto a «Medir al menos 20 aperturas, 10 búsquedas y 10 guardados». WS16 es lectura y no puede mutar antes de `G_HUMAN_READ`; obliga a inventar si debe medir guardados, omitirlos o registrar “N/A”.

## DRY-RUN
**Lecturas previstas:** guía, brief, alcance, decisiones, cobertura, validacion-humana, user-flows y contratos de vecinos en `dag.yaml` (WS08, WS14, WS15, WS40, WS41).
**Cambios previstos:** ninguno de código; producir acta de lectura con participante, versión, guion, resultados y tiempos; consumir manifiesto/corpus de WS40; ejecutar recorrido UF01/UF03 lectura/UF07/UF08 lectura/UF10.
**Dependencias:** WS14 búsqueda, WS15 errores/modo degradado, WS08 criterios observables, WS40 corpus, WS41 lectura multidesk.
**Validaciones futuras:** acta versionada en `graph_ui`, commit verificable, fallos convertidos en correcciones, revisión humana de evidencia, paso de `G_HUMAN_READ` antes de mutaciones.

## FUTURO
- P08: persona y umbrales los confirma el solicitante humano.
- WS40 genera corpus y manifiesto; WS41 implementa lectura entre desks; WS14/WS15 implementan soporte.
- WS17 enriquece navegación después de WS16.
- WS30 ejecuta la prueba de edición.
- Fallos detectados abren tareas de corrección en el repo dueño.
- Un humano resuelve `G_HUMAN_READ`; ningún agente lo sustituye.
