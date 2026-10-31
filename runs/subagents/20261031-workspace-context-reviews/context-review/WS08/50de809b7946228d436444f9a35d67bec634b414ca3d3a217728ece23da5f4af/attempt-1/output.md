REFORMULACION
Propósito: precisar los user-flows como encargo de planificación, mapeando cada UF a operaciones reales y criterios observables. Resultado: `borradores/user-flows.md` revisado con entrada/salida, operación, error, nodo y gate humano por UF. Repo dueño: `deskops`. Límites: solo planificación; no implementa UI ni modifica tareas de otros repos; depende de WS07 y G_PRODUCT; UF08 solo lectura; ack local pendiente de WS12; operación ausente se marca hueco, no se inventa; promoción no autorizada.

AMBIGUEDADES
1. «Cada UF tiene entrada/salida, operación, error, nodo y gate humano»: usa singular, pero cobertura.md asigna a UF01 varios nodos y gates (WS16 y WS43). Obliga a inventar si se elige un nodo/gate o se listan todos, y cuál prevalece.
2. «cubrir manual, captura, revisión...»: «manual» no es una UF de user-flows.md. Obliga a inventar si se añade una UF, una sección no-UF o se reduce a UF05/UF10, y cómo se le aplica la aceptación.
3. La lista de scope omite UF06 (delegar/intervenir), que sí existe en user-flows.md. Obliga a inventar si WS08 debe mapearla con operaciones Scion no disponibles o excluirla y remitirla a WS32–36/WS37.
4. «modo degradado (UF07, fallo de backend/dependencia)»: no aclara si es tratamiento transversal por UF o solo parte de UF07. Obliga a inventar una variante degradada por flujo o una UF separada y qué fallos cubre.

DRY-RUN
Lecturas previstas: dag.yaml (WS08, WS07, G_PRODUCT), brief.md, alcance.md, decisiones.md, cobertura.md, validacion-humana.md, user-flows.md y auditorías vía WS06/WS07. Cambios previstos: solo `borradores/user-flows.md`; completar por UF las columnas exigidas y marcar huecos con repo dueño. Dependencias: G_PRODUCT, contratos WS11/WS12, auditorías e inventario de operaciones. Validaciones futuras: comprobar cada UF contra cobertura.md y validacion-humana.md, que ningún gate quede sin nodo y que no se prometa función fuera de alcance.

FUTURO
WS07 debe registrar decisiones, source_mode y responsables; WS11/WS12 producirán contratos; WS16/30/37/39 ejecutarán los gates humanos; WS40 aportará corpus. Un humano decide las ambigüedades y autoriza la promoción de WS08; este nodo no las resuelve.
