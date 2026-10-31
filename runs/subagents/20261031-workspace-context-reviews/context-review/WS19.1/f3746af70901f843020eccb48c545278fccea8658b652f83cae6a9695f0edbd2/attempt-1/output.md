REFORMULACION
Propósito: encargar a `graph_ui` un delta de edición de campos con revisión esperada y conflicto visible. Resultado: UI que reutiliza editores/API, guarda mediante CAS del documento, conserva texto local ante escritura obsoleta y muestra el rechazo como conflicto. Repo: `graph_ui`, en `frontends/mindmap/views/workspace/fields/` y `tests/`, consumiendo endpoints del contrato WS12 sin cambiarlo. Límites: campos workflow-protected no editables por este canal; mutación solo sobre desk en modo manual exclusivo (P03); otros modos read-only; no define contrato ni semántica nueva.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: nodo WS19.1, guía, brief, alcance, decisiones, cobertura, reconciliación, contratos vecinos WS12/WS16/WS19 y gates. Cambios previstos: implementación en el directorio de campos de `graph_ui` y pruebas; sin modificar contrato. Dependencias: contrato/whitelist y CAS de WS12; `G_WRITE_CONTRACT`; aceptación `G_UI_WRITE`; `G_HUMAN_READ` producido por WS16; agregado WS19. Validaciones futuras: guardar/recargar confirma dato real; escritura obsoleta no pierde texto local y muestra conflicto; campos protegidos no editables; modos distintos del manual exclusivo permanecen read-only.

FUTURO
WS07/P01/P03 deben registrar actor humano y política de escritura. WS12 produce whitelist, canal/CAS y evidencias de `G_UI_WRITE`/`G_WRITE_CONTRACT`. WS16 produce `G_HUMAN_READ`. La promoción autoriza TaskDoc, archivos, pruebas y evidencias; hasta entonces no hay ejecución.
