# Matriz de completitud de productores — WS08

Estado leído: user-flows.md y cobertura.md ya con la lista cerrada aplicada. «(parche)» marca los IDs que esta pasada añadió. Fuente de los IDs: solo las secciones **Operación** y **Error** de cada UF. «Cubierto por WSxx» = el agregado figura en el campo, y un agregado cubre a sus hijos. Agregados según dag.yaml (`node_role: aggregate`): WS13, WS15, WS19, WS25, WS26, WS27, WS32, WS33, WS34. No se enumeran dependencias transitivas ni IDs citados solo para excluirlos. Clases: productor necesario, extensión opcional, citación contextual.

## UF01

| ID | Dónde se cita | Clase | En Nodo | En cobertura.md |
|---|---|---|---|---|
| WS22 | Operación, lectura Board/tarea en UI (base parcial) | citación contextual | no (a propósito: base existente citada, no bloquea WS16) | no (a propósito) |
| WS13.1 | Operación, hueco pestañas/foco | productor necesario | sí, cubierto por WS13 | sí, cubierto por WS13 |
| WS13.2 | Operación, hueco Markdown no modelado | productor necesario | sí, cubierto por WS13 | sí, cubierto por WS13 |
| WS13.3 | Operación, hueco pestañas/foco | productor necesario | sí (explícito) | sí, cubierto por WS13 |
| WS17 | Operación, hueco entradas/índices authored | productor necesario | sí | sí |
| WS43 | Operación, hueco entradas/índices (publicación real) | productor necesario (publicación, no gate) | sí | sí (columna Gate) |
| WS11 | Error, no definido | productor necesario | sí | sí |
| WS15.1 | Error, no definido (consumidor de WS11) | citación contextual | sí, cubierto por WS15 | sí, cubierto por WS15 |

## UF02

| ID | Dónde se cita | Clase | En Nodo | En cobertura.md |
|---|---|---|---|---|
| WS12 | Operación (promoción, huecos ack/responder) y Error | productor necesario | sí | sí |
| WS25.1 | Operación, huecos ack local y responder (UI); Error vía WS25 | productor necesario | sí, cubierto por WS25 (también explícito) | sí, cubierto por WS25 |
| WS25.2 | Operación, hueco captura directa | productor necesario | sí, cubierto por WS25 (también explícito) | sí, cubierto por WS25 |
| WS25 | Error, no definido (UI) | productor necesario | sí | sí |

## UF03

| ID | Dónde se cita | Clase | En Nodo | En cobertura.md |
|---|---|---|---|---|
| WS14 | Operación, hueco búsqueda por API desde la UI | productor necesario | sí | sí |
| WS42 | Operación, dividir y reunir en UI | productor necesario | sí | sí |
| WS29 | Operación, Impacto (Changes/Integrity en UI) | extensión opcional | sí (parche), como extensión, no prerrequisito | sí (parche), como extensión, no prerrequisito |
| WS20 | Operación, hueco guardado Markdown en bruto | productor necesario (precondición) | sí | sí (parche) |
| WS45 | Operación, hueco precondición de payload | productor necesario (precondición) | sí | sí (parche) |
| WS19 | Operación, hueco edición con conflicto visible | productor necesario | sí | sí |
| WS19.1 | ídem | productor necesario | sí, cubierto por WS19 | sí, cubierto por WS19 |
| WS19.2 | ídem | productor necesario | sí, cubierto por WS19 | sí, cubierto por WS19 |
| WS21 | Operación, mismo hueco (fuente según `source_mode`) | productor necesario | sí | sí |
| WS12 | Error, no definido | productor necesario | sí | sí |

## UF04

| ID | Dónde se cita | Clase | En Nodo | En cobertura.md |
|---|---|---|---|---|
| WS26 | Operación, hueco autoría/Board en UI | productor necesario | sí | sí |
| WS26.1 | ídem | productor necesario | sí, cubierto por WS26 (también explícito) | sí, cubierto por WS26 |
| WS26.2 | ídem | productor necesario | sí, cubierto por WS26 (también explícito) | sí, cubierto por WS26 |
| WS12 | Operación (contrato; vincular rituales) y Error | productor necesario | sí | sí |
| WS22 | Operación, hueco tablero agrupado/TaskDoc | productor necesario | sí | sí |

## UF05

| ID | Dónde se cita | Clase | En Nodo | En cobertura.md |
|---|---|---|---|---|
| WS27.1 | Operación, hueco diff Git | productor necesario | sí, cubierto por WS27 (también explícito) | sí, cubierto por WS27 |
| WS27.2 | Operación, hueco evidencia encontrada/verificada | productor necesario | sí, cubierto por WS27 (también explícito) | sí, cubierto por WS27 |
| WS28 | Operación, hueco closeout verify/handoff; Error | productor necesario | sí | sí |
| WS13.3 | Operación, hueco reabrir enlaces | productor necesario | sí (parche) | sí (parche) |
| WS23 | Operación, hueco renderer RitualDoc/StepDoc (añadido por el parche) | productor necesario | sí (parche) | sí (parche) |
| WS12 | Error (whitelist de campos protegidos; no definido) | productor necesario | sí | sí |

## UF06

| ID | Dónde se cita | Clase | En Nodo | En cobertura.md |
|---|---|---|---|---|
| WS32 | Operación, hueco intento/dispatch; Error | productor necesario | sí | sí (WS32–36) |
| WS32.1, WS32.2 | Operación, mismo hueco | productor necesario | sí, cubierto por WS32 | sí, cubierto por WS32 |
| WS33 | Operación, hueco vincular mensajes; Error | productor necesario | sí | sí (WS32–36) |
| WS33.1, WS33.2 | Operación, mismo hueco | productor necesario | sí, cubierto por WS33 | sí, cubierto por WS33 |
| WS34 | Operación, hueco dispatch y respuesta; Error | productor necesario | sí | sí (WS32–36) |
| WS34.1, WS34.2 | Operación, mismo hueco | productor necesario | sí, cubierto por WS34 | sí, cubierto por WS34 |
| WS35 | Operación, hueco UI seguimiento | productor necesario | sí | sí (WS32–36) |
| WS36 | Operación, hueco UI intervención | productor necesario | sí | sí (WS32–36) |
| WS44 | Operación, hueco contrato/acceso Scion; Error | productor necesario | sí (parche) | sí (parche) |

El hueco del bundle (sin productor en el DAG) no lleva fila: no cita ningún WS y se conserva.

## UF07

| ID | Dónde se cita | Clase | En Nodo | En cobertura.md |
|---|---|---|---|---|
| WS29 | Operación, Cambios e impacto y hueco criterio visible | productor necesario (prueba técnica propia, no gate humano) | sí | sí |
| WS15.1 | Operación, modo degradado y hueco criterio visible | productor necesario | sí, cubierto por WS15 (también explícito) | sí, cubierto por WS15 |
| WS11 | Operación (contrato del criterio) y Error | productor necesario | sí | sí |
| WS12 | Error, fallos parciales de una reparación | productor necesario | sí (parche) | sí (parche) |

## UF08

| ID | Dónde se cita | Clase | En Nodo | En cobertura.md |
|---|---|---|---|---|
| WS41 | Operación, hueco lectura entre desks; Error | productor necesario | sí | sí |
| WS13 | Operación, «con WS13, WS14, WS15» | productor necesario | sí | sí |
| WS14 | ídem | productor necesario | sí | sí |
| WS15 | ídem | productor necesario | sí | sí |
| WS11 | Error, no definido | productor necesario | sí | sí |

WS40 no se cita en Operación ni Error de UF08; la lista cerrada lo añade a cobertura.md por el campo Nodo (dos desks temporales), así que no lleva fila aquí.

## UF09

| ID | Dónde se cita | Clase | En Nodo | En cobertura.md |
|---|---|---|---|---|
| WS39 | Operación, hueco acceso a Schema/clase origen; Error | productor necesario | sí | sí |
| WS29 | Operación, Impacto (Changes/impacto avanzado) | extensión opcional | sí (parche), opcional, no bloquea WS31 | sí (parche), opcional |
| WS12 | Error, no definido (contrato) | productor necesario | sí | sí |

El hueco de RoleDoc/RuntimeProfileDoc (sin productor en el DAG) no lleva fila.

## UF10

| ID | Dónde se cita | Clase | En Nodo | En cobertura.md |
|---|---|---|---|---|
| WS15.2 | Operación, hueco orientación sin desk; Error | productor necesario | sí, cubierto por WS15 (también explícito) | sí, cubierto por WS15 |
| WS40 | Operación, hueco instrucciones y ejemplo Taller | productor necesario | sí | sí |
| WS17 | Operación, hueco índices authored | productor necesario | sí | sí |
| WS43 | Operación, hueco índices (publicación) | productor necesario (publicación) | sí | sí (parche) |
| WS11 | Error, no definido | productor necesario | sí (parche) | sí (parche) |

## Resultado

Ninguna fila de clase «productor necesario» queda con «no» en Nodo o en cobertura.md. Los dos «no» son WS22 en UF01 (citación contextual, a propósito).
