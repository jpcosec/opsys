## REFORMULACION

**Propósito:** agrupar la Entrega M: autoría manual segura, intake/trabajo y revisión/cierre por handoff verificables.

**Resultado:** paquete integrado cuyos hijos producen contrato operativo, precondición de escritura, guardado fuente, edición de campos, fuente/render, captura, tareas, diff/evidencia, handoff de cierre y operaciones de conocimiento; WS30 valida el recorrido humano UF02–05 y navegación.

**Repo:** `deskops` es dueño de la agrupación; los hijos se ejecutan en `graph_ui` y `sldb`.

**Límites:** PK05 no ejecuta ni autoriza tareas; termina cuando terminan sus hijos. Guardar no hace commit; no hay closeout HTTP; mutaciones UI esperan `G_HUMAN_READ`; con coordinador escritor, UI read-only/handoff.

## AMBIGUEDADES

ninguna.

## DRY-RUN

Ejecución hipotética por hijos, respetando aristas:

1. Contrato externo WS12 → habilita WS19, WS20, WS45, WS25, WS27, WS28 y WS42.
2. WS45 produce inventario/pruebas de precondición → `G_PAYLOAD_PRECONDITION`.
3. WS20 produce API fuente reversible y pruebas → `G_SOURCE`.
4. WS19 integra edición de campos/conflicto con precondición y before-image; su salida alimenta WS21 y WS42.
5. WS21 integra fuente/render usando WS19 + WS20/`G_SOURCE`; en editable exige además `G_PAYLOAD_PRECONDITION`.
6. WS25 integra captura/triage; WS26 integra autoría y contexto de tareas (WS26.1→WS26.2), con WS22+WS12.
7. WS27 integra diff/evidencia con WS13+WS12; WS28 integra verificación/handoff de cierre con WS27+WS12.
8. WS42 integra operaciones de conocimiento con WS19+WS24+WS12, sin paralelizarse con WS19.
9. Salidas de WS17/21/22/23/24/25/26/28/42 → WS30.

**Integración/validación:** WS30 ejecuta el recorrido humano sobre corpus WS40 e índices WS17, registra acta UF02–05 y navegación; un fallo bloquea el gate y se atribuye al nodo causante. El paquete se considera completo solo con aceptación de hijos e integración validada, no por tests aislados.

## FUTURO

- WS16 produce `G_HUMAN_READ`; sin él no se habilitan mutaciones UI.
- P01 receptor registra actas por delta al preparar cada efecto.
- WS12 fija representación, operaciones y escritores de la precondición.
- WS45/WS20 deciden reutilizar o completar capacidad existente.
- WS30 requiere participación humana y decide el resultado del gate.
- Promoción/TaskDoc fijan archivos, pruebas y textos de pantalla.
