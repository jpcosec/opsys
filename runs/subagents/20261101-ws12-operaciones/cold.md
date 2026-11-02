## REFORMULACION

**Objetivo:** producir `desk/drawer/plans/workspace-documental/contratos/operaciones.md` con las 13 secciones obligatorias (matriz operación/modelo/campo/canal/actor/revisión/Git/efectos; protegidos; adapter; coordinador T-P03.1; precondición de escritura; captura drawer/protoátomo; ack/inbox; Git/closeout; recepción por delta; ramal E; huecos; trazabilidad), separando capacidad existente con evidencia citable de hueco con dueño/productor.

**Alcance:** solo lectura de fuentes y código citado; escritura limitada a `operaciones.md` y `runs/subagents/20261101-ws12-operaciones/result-summary.md`. Sin commits, revisiones, mutaciones, actas ni cambios en `dag.yaml`, fuentes comunes, helper o validadores. Repos hermanos solo lectura. Sin preguntar al solicitante.

**Repo:** deskops (`owner_repo: deskops`), `output_base: deskops:desk/drawer/plans/workspace-documental/`.

**Límites:** `execution_authorized` global sigue `false`; G_WRITE_CONTRACT sigue pendiente de root; no se habilitan mutaciones ni se crea API/modelo.

## AMBIGUEDADES

1. «Autoriza: `runs/subagents/20261101-ws11-disponibilidad/review-source.md`, última parte, que prevalece sobre este resumen» (Scope). No delimita dónde empieza «última parte»; obligaría a inventar el corte.
2. «commits observados» (sección 1 obligatoria). No fija commit para deskops ni aclara si se heredan GU `134a665`, SL `77bd6d0…`, DK `c19c6c0d` de `navegacion.md`; obligaría a elegir.
3. «G_WRITE_POLICY registrado» (acceptance de `dag.yaml`) frente a «G_WRITE_CONTRACT sigue pendiente de root» (Done When). No dice quién registra G_WRITE_POLICY ni con qué evidencia; obligaría a inventar actor o acta.
4. «Comprobado requiere API o prueba existente citada» (Scope). No define dónde buscar pruebas (tests, CI, runs) ni qué cuenta como prueba existente; obligaría a inventar criterio.
5. Sección 11: «política y umbral de timeout… Sin valor nuevo ahora». No aclara si debe contener umbral o solo declarar que se fijará al preparar WS34.1/34.2; obligaría a elegir.

## DRY-RUN

1. Leer `navegacion.md` (contrato aprobado, hash `6a4f…`), `navegacion-aprobacion.md`, `decisiones.md` (T-P03.1), nodo WS12 en `dag.yaml`, auditorías, `user-flows.md`, `vistas.md`, `root-decision-20261101.md`, `promotion-notes.md` y `review-source.md`.
2. Abrir el código real citado en los commits fijados (GU/SL/DK) y localizar símbolos de deskops; anotar `path:línea`/`símbolo`.
3. Redactar las 13 secciones en orden, con tabla de huecos y trazabilidad.
4. Escribir `result-summary.md` con fuentes abiertas y clasificación lectura estática/runtime.
5. Errores esperados: falta de evidencia → hueco con dueño; contradicción real → detener y reportar; checks rojos → corregir formato; Tester ausente → no cerrar. Resultado esperado: `operaciones.md` no vacío, `build --check`, `validate --check` y `status` verdes, Tester independiente PASS, G_WRITE_CONTRACT aún pendiente.
