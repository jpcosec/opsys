## REFORMULACION
**Propósito:** convertir los user-flows en un encargo de planificación preciso y observable. **Resultado:** `borradores/user-flows.md` con cada UF mapeada a operaciones, errores, nodo y gate humano. **Repo dueño:** deskops. **Límites:** no prometer funciones fuera de alcance; UF08 es solo lectura; envío interdesk fuera de baseline; UF02 responde solo en desk/contexto local. No se ejecuta nada.

## AMBIGUEDADES
1. «Mapear UF a operaciones de WS02/03/04»: WS08 solo declara `depends_on: WS07`; no se suministran las operaciones de WS02/03/04 ni qué hacer si no existen. Obliga a inventar el catálogo de operaciones o su correspondencia.
2. «cubrir manual, captura, revisión, cambios, arranque, multidesk, schemas y modo degradado»: «modo degradado» no está definido en brief, alcance ni user-flows. Obliga a inventar qué estados cubre (backend ausente, link roto, CDN, etc.) y su comportamiento esperado.
3. «ack local disponible según contrato»: no identifica qué contrato ni qué nodo lo produce. Obliga a inventar si el ack existe y qué operación lo respalda.
4. «Cada UF tiene entrada/salida, operación, error, nodo y gate humano»: «nodo» no distingue nodo del DAG, nodo de operación o nodo documental. Obliga a inventar la columna y su granularidad.

## DRY-RUN
**Lecturas:** guía, brief, alcance, decisiones, cobertura, validacion-humana, user-flows y ficha WS08 de `dag.yaml`. **Cambios previstos:** solo `borradores/user-flows.md`. **Dependencias:** WS07 con G_PRODUCT pendiente; WS02/03/04 citados pero no declarados como dependencias; WS11/12 consumen la salida. **Validaciones futuras:** comprobar por UF entrada/salida/operación/error/nodo/gate; contrastar gates con `cobertura.md` y `validacion-humana.md`; verificar que UF08 no prometa envío interdesk.

## FUTURO
WS07 registra decisiones P01–P09 y G_PRODUCT con actor/fecha. WS12 produce la whitelist final de operaciones; WS11 cierra navegación e identidad. El humano confirma P08 y los gates de uso. WS16/30/37/39 ejecutan las validaciones humanas correspondientes. Nada de esto se resuelve en WS08.
