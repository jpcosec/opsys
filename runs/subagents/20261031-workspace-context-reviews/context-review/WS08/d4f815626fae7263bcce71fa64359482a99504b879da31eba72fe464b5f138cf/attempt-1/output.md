## REFORMULACION

**Propósito:** precisar los user-flows UF01–UF10 como encargo de planificación, mapeando cada uno a operaciones existentes, entradas/salidas, errores, nodo del DAG y gate humano, distinguiendo prueba técnica propia de aceptación humana.

**Resultado:** `borradores/user-flows.md` actualizado en deskops, sin prometer funciones fuera de alcance y marcando como hueco toda operación ausente.

**Repo dueño:** deskops. **Límites:** no implementa UI/API, no habilita delegación Scion, no crea operaciones ni contratos, no reabre decisiones resueltas; G_PRODUCT ya está satisfecho vía WS07.

## AMBIGUEDADES

1. «cubrir manual, captura, revisión, cambios (UF07/WS29), arranque, multidesk, schemas y modo degradado» frente a la aceptación, que solo exige «Cubrir todas UF01–UF10» y campos por UF. Obligaría a inventar si “manual” requiere contenido propio en `user-flows.md`, una sección diferenciada o queda absorbido por los UFs, y qué criterio lo valida.

## DRY-RUN

**Lecturas previstas:** guía, brief, alcance, decisiones, cobertura, validacion-humana, borrador `user-flows.md`, nodo WS08 y aristas WS07/WS09/WS11/WS12/WS16/WS40; auditorías `{deskops,infraestructura,ui}.md` por dependencia transitiva.

**Cambios previstos:** editar únicamente `borradores/user-flows.md`, completando por UF entrada/salida, operación, error, nodo, gate humano y hueco cuando falte operación; documentar delegación condicionada a G_SCION/G_EXEC sin habilitarla.

**Dependencias:** WS07 resuelto; G_PRODUCT satisfecho; operaciones tomadas de auditorías transitivas, sin sustituirlas.

**Validaciones futuras:** comprobar cobertura UF01–UF10; que cada fila tenga todos los campos; que operaciones ausentes queden como hueco; que WS16/30/37/39 se distingan de la prueba técnica WS29; que “ninguno adicional” aparezca cuando corresponda; que no se prometa función fuera de alcance.

## FUTURO

WS09 y WS11 consumirán los UFs para catálogo y navegación; WS12 definirá operaciones pendientes como ack local; WS29 ejecutará su prueba técnica; WS16/30/37/39 aportarán actas humanas; WS40 suministrará el corpus. La persona responsable decide cualquier cambio de alcance o aceptación, no este nodo.
