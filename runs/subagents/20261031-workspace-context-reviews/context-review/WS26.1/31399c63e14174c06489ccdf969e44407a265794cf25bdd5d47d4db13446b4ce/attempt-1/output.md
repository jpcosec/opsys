REFORMULACION
Propósito: implementar en `graph_ui` la autoría explícita de un candidato del drawer como TaskDoc, incluyendo evidencia declarada, dependencias y pills de contexto. Resultado: vista/acciones en `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados por WS12 y tests, con los datos visibles tras recargar. Repo dueño: `graph_ui`. Límites: no editar `status` para avanzar; no crear sustitutos si falta contrato Git/API (handoff y “no disponible”); ceñirse al output_scope y a los gates indicados.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas previstas: nodo WS26.1, aristas WS12/WS22 y gates; brief (drawer/candidato, `deskops add task`, TaskDoc); alcance (reglas comunes, UF04); cobertura UF04; decisiones P03/P04/P06; contrato futuro de WS12 y salida de WS22; código existente de `graph_ui` en authoring/tests y API/CLI pública de deskops.
Cambios previstos: añadir vista y acciones de autoría desde candidato; persistir evidencia, dependencias y pills mediante operaciones autorizadas por WS12; reflejar el estado tras recarga; tests de UI/flujo. Sin cambios fuera de `authoring/`, endpoints autorizados y `tests/`.
Dependencias: WS12 debe fijar whitelist, canal y efectos; WS22 aporta Board/lector y enlaces comunes. Gates: `G_CLOSEOUT`, `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`.
Validaciones futuras: UF04 sobre TaskDoc real; recarga conserva evidencia/dependencias/pills; no se edita status; operación Git sin contrato queda en handoff explícito y no disponible; preflight de promoción del nodo y no solapamiento.

FUTURO
WS12 produce y verifica el contrato técnico y acepta el delta de `graph_ui` (`G_UI_WRITE`); WS16 satisface `G_HUMAN_READ`; el closeout se resuelve por evidencia externa. WS26.2 cubre enrutamiento en Board. La promoción de este nodo (no autorizada) fijará archivos, pills, átomos, evidencia y preflight. Las propuestas P01/P03/P04/P06/P07 siguen pendientes de decisión humana en WS07.
