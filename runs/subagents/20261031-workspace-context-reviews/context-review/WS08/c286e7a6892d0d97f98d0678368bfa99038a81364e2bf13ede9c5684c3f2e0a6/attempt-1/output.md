## REFORMULACION

Propósito: revisar WS08 como encargo de planificación que precisa los user-flows y criterios observables. Resultado: `borradores/user-flows.md` con cada UF01–UF10 mapeada a entrada/salida, operación, error, nodo del DAG y gate humano, marcando huecos sin inventar operaciones. Repo dueño: `deskops`. Límites: no implementar, no prometer funciones fuera de alcance, no habilitar Scion, no dar por disponible el ack de UF02, no convertir UF08 en escritura interdesk y no revisar contratos de nodos vecinos.

## AMBIGUEDADES

ninguna

## DRY-RUN

Lecturas previstas: guía, brief, alcance, decisiones, cobertura, validación humana, borrador de user-flows y nodo WS08 de `dag.yaml`; auditorías `auditoria/{deskops,infraestructura,ui}.md` por dependencia transitiva vía WS06/WS07. Cambios previstos: solo `borradores/user-flows.md`. Dependencias: WS07 y G_PRODUCT satisfecho; WS12 pendiente para ack local; G_SCION/G_EXEC condicionan UF06 sin habilitarla. Validaciones futuras: comprobar cobertura UF01–UF10, listas completas de operación/nodo/gate, distinción WS16/30/37/39 frente a prueba técnica WS29, y que cada operación ausente quede como hueco con productor. Sin ejecución.

## FUTURO

WS09 consumirá los UFs para el catálogo de renderizaciones; WS11/WS12 contrastarán navegación y operaciones; el solicitante P01 y los gates humanos WS16/30/37/39 producirán actas en repos receptores; WS29 tendrá prueba técnica propia; WS40 aportará el corpus; WS43 publicará navegación real tras validación. Nada de ello se ejecuta ni se aprueba aquí.
