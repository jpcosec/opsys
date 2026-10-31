REFORMULACION
Propósito: definir WS23 como encargo de planificación para una vista que renderice RitualDoc/StepDoc/lifecycle como procedimiento navegable. Resultado: implementación en `graph_ui`, bajo `frontends/mindmap/views/workspace/procedure/; tests/`, con pruebas sobre corpus WS40 o store temporal real. Repo dueño: `graph_ui`. Límites: solo lectura del estado de pasos; este estado “solo viene de deskops” y “esta vista no lo escribe”; no auto-marcar pasos por leerlos; depende de WS13 y WS09; requiere G_UI_READ, pendiente de forma intencional; promoción no autorizada.

AMBIGUEDADES
1. Cita: “obligaciones, transiciones y fuentes navegables”. “Obligaciones” no está definido en el glosario ni en la aceptación. Obligaría a inventar qué obligaciones debe mostrar la vista, de qué campo/documento salen y cómo se comprueba que están bien representadas.

DRY-RUN
Lecturas: `dag.yaml#node:WS23`, guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y `reconciliacion.md`; no se revisan los bloques edge. Cambios previstos: ninguno; solo evaluación del nodo. Dependencias: WS13 aporta lector/contexto; WS09 precisa catálogo y contrato de renderizaciones; G_UI_READ condiciona el despacho; WS40 es corpus opcional y el store temporal real es alternativa. Validaciones futuras: el TaskDoc de promoción fijará archivos, pills y evidencia; WS30 validará el flujo manual; las pruebas de implementación usarán corpus WS40 o store temporal real. No se ejecuta nada.

FUTURO
WS09 debe producir el contrato/ficha de ritual y pasos; WS13, la integración de lectura; WS11, la aceptación de G_UI_READ con responsable designado. WS40 puede aportar corpus y WS30 validación humana. La promoción de WS23 exige preflight y autorización; cualquier decisión Pxx o designación de actor corresponde a un humano, no a este revisor.
