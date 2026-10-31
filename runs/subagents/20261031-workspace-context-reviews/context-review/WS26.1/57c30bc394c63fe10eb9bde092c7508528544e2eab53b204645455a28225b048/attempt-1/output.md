REFORMULACION
Propósito: fijar WS26.1 como encargo de planificación para autoría explícita desde un candidato del drawer, con evidencia, dependencias y pills de contexto, sin usar el status para avanzar. Resultado: en `graph_ui`, dentro de `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados por WS12 y `tests/`, un TaskDoc real de UF04 conserva evidencia, dependencias y pills tras recargar. Repo dueño: `graph_ui`. Límites: promoción `not_authorized`; archivos, pills, átomos y evidencia precisos quedan para la promoción; una operación Git sin contrato o dueño queda en handoff explícito y no disponible; no se edita status para avanzar.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas previstas: nodo WS26.1 y guía; brief, alcance, decisiones y cobertura; contratos vecinos WS12/WS22 solo como prerrequisitos, sin revisarlos. Cambios previstos: UI de autoría, endpoints autorizados y tests dentro del `output_scope`; nada ejecutado. Dependencias: WS12 aporta contrato/whitelist/capabilities; WS22 aporta Board/lector; gates G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT. Validaciones futuras: UF04 sobre TaskDoc real, persistencia tras recarga, status intacto, handoff si falta contrato Git, acta humana de G_HUMAN_READ y aceptación del delta de G_UI_WRITE. Si falta contrato, detenerse y registrar hueco con repo dueño.

FUTURO
WS12 produce contrato y capabilities; WS22, representaciones del Board; WS16, acta de lectura humana; WS07, decisiones y responsables; la promoción fija archivos, pills, átomos, evidencia y preflight; humanos aceptan gates y autorizan promoción.
