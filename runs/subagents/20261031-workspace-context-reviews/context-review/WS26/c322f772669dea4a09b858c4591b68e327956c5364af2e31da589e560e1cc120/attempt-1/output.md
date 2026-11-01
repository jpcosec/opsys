## REFORMULACION

**Propósito:** evaluar si WS26 está bien planteado como encargo de planificación, no si el producto es bueno.

**Resultado:** WS26 es un agregado no ejecutable: se entiende cumplido cuando WS26.1 y WS26.2 cumplen su aceptación; sus dependientes siguen apuntando a WS26.

**Repo dueño:** `graph_ui`.

**Límites:** agregado de autoría, evidencia, dependencias, contexto/pills, enrutamiento en Board y capa lista; no implementa promoción nueva, no edita `status` para avanzar y no habilita mutaciones UI sin `G_HUMAN_READ`. Los gates son `per_delta`; el estado global no exige aceptación conjunta.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** nodo WS26, hijos WS26.1/WS26.2, vecinos WS12 y WS22, guía, brief, alcance, decisiones y cobertura. No se revisan los bloques edge como contratos a corregir.

**Cambios previstos:** ninguno en WS26; es agregado. WS26.1 produciría `frontends/mindmap/views/workspace/authoring/` y WS26.2 `frontends/mindmap/views/workspace/routing/`, con endpoints autorizados por WS12 y tests.

**Dependencias:** contrato WS12, representación Board/lector WS22 y ambas salidas hijas. `G_CLOSEOUT` está satisfecho; `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT` siguen pendientes por delta.

**Validaciones futuras, sin ejecutar:** aceptación de cada hijo; persistencia tras recarga de evidencia/dependencias/pills; `deskops show board` tras enrutar; separación visual entre capa lista, ejecución y bloqueos; recibos por delta en repo receptor; acta humana de lectura antes de uso de mutaciones UI. La promoción queda sujeta a TaskDoc y preflight, no autorizada aquí.

## FUTURO

WS26.1 y WS26.2 producen la implementación y sus pruebas. WS12 publica el contrato técnico por operación. El receptor P01 emite actas `G_UI_WRITE`/`G_WRITE_CONTRACT` por delta concreto. WS16 produce `G_HUMAN_READ`. La promoción y el preflight de TaskDoc corresponden al flujo de promoción, no a este nodo.
