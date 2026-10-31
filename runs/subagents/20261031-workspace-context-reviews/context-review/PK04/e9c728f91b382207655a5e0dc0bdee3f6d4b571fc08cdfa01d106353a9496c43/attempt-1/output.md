## REFORMULACION

**Propósito:** revisar PK04 como encargo de planificación: una agrupación de revisión que declara cuándo está completa, sin ejecutar ni evaluar el producto.

**Resultado:** juicio sobre si PK04 se entiende y si su aceptación es comprobable; no un veredicto sobre sus hijos.

**Repo:** deskops, desde cuya raíz se ejecuta `context_review.py`; PK04 agrupa hijos con dueños graph_ui/spec2viz/deskops, pero sus aristas no se revisan aquí.

**Límites:** no ejecutar; no revisar bloques edge; no resolver propuestas Pxx; no promover nodos; no sustituir la revisión de cada hijo.

## AMBIGUEDADES

1. «cuyo hash de input y de contrato coinciden con los actuales»: no se define qué artefacto es el «contrato» —¿el bloque del hijo en `dag.yaml`, su `acceptance`, otro documento?— ni cómo se calcula su hash. Obliga a inventar la fuente y el algoritmo para declarar vigente una revisión.

2. «bloqueo explícito: `context_review.status=blocked` por causa externa (ajena al encargo del propio hijo)»: no hay criterio para separar una causa externa de una ambigüedad propia del hijo. Obliga a inventar la frontera y podría admitir como bloqueo lo que en realidad es un defecto del encargo.

3. «y dependencia en esa disposition.md»: no precisa qué dependencia debe registrarse —la del hijo bloqueado, la del responsable externo u otra— ni su formato mínimo. Obliga a inventar el contenido válido del registro.

## DRY-RUN

**Lecturas previstas:** guía, `dag.yaml` (nodo PK04 y estados `context_review` de sus hijos), `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`; los bloques edge solo como contratos de vecinos.

**Cambios previstos:** ninguno; esta revisión no escribe disposición ni modifica el DAG.

**Dependencias:** revisiones vigentes de WS17, WS18, WS22, WS23 y WS24; `context_review.py status`; hashes input/contrato; bloqueos externos con responsable y dependencia.

**Validaciones futuras:** comprobar hashes actuales, existencia de `disposition.md` por intento, ausencia de ambigüedad propia en cada hijo o bloqueo externo registrado con responsable y dependencia.

## FUTURO

La sesión de coordinación produce y actualiza las disposiciones de los hijos; WS07 designa responsables y operadores; WS11 y WS40 producen contrato y corpus; el humano resuelve P01–P09. Nada de ello es ambigüedad de PK04.
