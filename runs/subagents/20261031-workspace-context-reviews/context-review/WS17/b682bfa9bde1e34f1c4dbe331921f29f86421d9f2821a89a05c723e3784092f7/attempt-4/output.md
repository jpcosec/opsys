## REFORMULACION
Propósito: redactar entradas e índices authored del desk de ejemplo como plantillas Markdown versionadas. Resultado: contenido en `ejemplo/nav/` dentro del paquete del plan, apto para que WS40 lo materialice en su corpus temporal. Repo dueño: `deskops`. Límites: WS17 no produce el corpus, no copia inventarios derivados, no escribe repos reales y puede ejecutarse antes de WS16; WS30 integra los índices.

## AMBIGUEDADES
Ninguna que obligue al ejecutor de WS17 a inventar resultado, aceptación, repo, actor, dependencia o límite.

## DRY-RUN
- Lecturas previstas: guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo WS17 y contratos de vecinos como contexto, sin revisarlos.
- Cambios previstos: crear plantillas Markdown authored bajo `ejemplo/nav/`; no tocar corpus WS40 ni repos reales; no duplicar registry ni inventarios derivados.
- Dependencias: contrato de navegación/identidad de WS11 y generador/corpus de WS40.
- Validaciones futuras: regenerar el corpus WS40 con `ejemplo/nav/`, recorrer links Markdown sin UI, comprobar resolución de dos desks y procedencia, y confirmar que no hay registro duplicado. WS30 integra estos índices.
- Sin ejecución: no se crean archivos ni se lanzan comandos.

## FUTURO
WS11 debe cerrar el contrato de navegación e identidad; WS40 debe aceptar y materializar las plantillas en su root temporal; WS30 valida la integración en el recorrido manual; WS43 publica la navegación validada en el desk real. P09 y los gates humanos quedan fuera de esta revisión y no se asumen aprobados.
