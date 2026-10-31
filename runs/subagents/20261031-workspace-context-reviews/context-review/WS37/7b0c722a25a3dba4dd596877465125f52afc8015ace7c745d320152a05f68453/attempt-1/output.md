## REFORMULACION
Propósito: revisar WS37 como encargo de planificación para validar UF06 con Scion real e intervención humana. Resultado: acta y evidencias en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/`, bajo `validacion-humana.md`. Repo dueño: `graph_ui`. Límites: no sustituir integración por mocks, no confundir `completed` con aprobación, no bloquear WS31 y no promover (`promotion: not_authorized`).

## AMBIGUEDADES
Ninguna. Las frases «con actor humano», «cierre por el handoff de WS28» y «G_SCION/G_EXEC» remiten a actores, gates o dependencias transitivas ya previstos; el guion detallado queda para el TaskDoc de promoción.

## DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, validación humana, user-flows y nodo/gates. Cambios previstos: ninguno; solo revisión. Dependencias: WS36 y WS30; gates `G_EXEC` y `G_SCION`; WS28 entra como prerrequisito transitivo para el handoff de cierre. Validaciones futuras: autorización externa de `G_EXEC`, probe de WS44 para `G_SCION`, acta versionada en `output_scope`, evidencia de actor humano y ausencia de mocks o aprobación automática. No se ejecuta nada.

## FUTURO
Deciden o producen otros: el humano resuelve `G_EXEC` y P08/WS07; WS44 comprueba la API Scion; WS36 implementa el adaptador; WS28 aporta el handoff; WS38 publica capítulos; el TaskDoc de promoción fija archivos, guion y pruebas.
