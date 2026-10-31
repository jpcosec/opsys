REFORMULACION
Propósito: convertir los user-flows borrador en un encargo de planificación verificable, mapeando cada UF a operaciones reales de WS02/03/04 y a criterios observables. Resultado: `borradores/user-flows.md` actualizado con entrada/salida, operación, error, nodo del DAG y gate humano por UF; los huecos se marcan, no se inventan. Repo dueño: deskops. Límites: no prometer funciones fuera de alcance; UF08 solo lectura y envío interdesk fuera de baseline; UF02 ack local no disponible hasta WS12; no implementa UI, no ejecuta ni cierra gates humanos.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas previstas: `user-flows.md`, `cobertura.md`, `validacion-humana.md`, `decisiones.md`, `brief.md`, `alcance.md`, nodos WS07/WS09/WS11/WS12/WS16/WS40 y auditorías `auditoria/{deskops,infraestructura,ui}.md` por dependencia transitiva. Cambios previstos: editar solo `borradores/user-flows.md`; por cada UF ajustar operación, error, nodo y gate; marcar operación ausente como hueco. Dependencias: `WS07` y `G_PRODUCT` —pendiente intencional—; operaciones e inventarios vía WS06/WS07. Sin ejecución ni promoción. Validaciones futuras: comprobar que cada UF tiene los campos de aceptación y que ningún flujo promete fuera de alcance; los gates se verifican en nodos posteriores, no aquí.

FUTURO
WS07 y el humano resuelven P01–P09 y `G_PRODUCT`; WS11/WS12 producen los contratos de navegación y operaciones, incluido el ack local; WS29/WS39 y las validaciones humanas WS16/30/37/39 producen evidencia; una promoción futura fijará archivos, pills, átomos y preflight.
