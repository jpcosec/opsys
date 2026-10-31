## REFORMULACION
**Propósito:** convertir los user-flows en un encargo ejecutable y comprobable, mapeando UF01–UF10 a operaciones, errores, nodos y gates.
**Resultado:** `borradores/user-flows.md` actualizado con entrada/salida, operación, error, nodo DAG y gate humano por UF; operaciones ausentes marcadas como hueco.
**Repo dueño:** deskops.
**Límites:** no implementar ni prometer funciones fuera de alcance; no habilitar Scion ni delegación; no inventar operaciones; no sustituir contratos de WS12/WS11; entrega limitada a `borradores/user-flows.md`.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas previstas:** guía, brief, alcance, decisiones, cobertura, validación humana, borrador de user-flows, nodo WS08 y fuentes citadas; inventarios `auditoria/{deskops,infraestructura,ui}.md` por dependencia transitiva WS06/WS07.
**Cambios previstos:** completar las diez UF con los campos exigidos; corregir afirmaciones que excedan alcance; marcar huecos de operación/contrato; condensar pasos de intención sin presentarlos como implementación.
**Dependencias:** WS07/G_PRODUCT satisfecho; inventarios WS02–WS04 vía WS06/WS07; contrato WS12 para ack local aún pendiente; WS29 como prueba técnica propia; WS16/30/37/39 como gates humanos; WS40 para corpus.
**Validaciones futuras:** cubrir UF01–UF10; cada operación ausente queda como hueco con dueño; no prometer envío interdesk, cierre HTTP, edición binaria ni permisos Scion; distinguir gate humano de prueba técnica; verificar que delegación queda condicionada a G_SCION/G_EXEC sin habilitarla; comprobar coherencia con cobertura y validación humana.

## FUTURO
La promoción y el TaskDoc fijarán archivos, pills, átomos y evidencia. WS09/WS11/WS12 consumirán el mapa de operaciones; WS16/30/37/39 ejecutarán las actas humanas correspondientes; WS40 aportará el corpus; WS29 mantendrá su prueba técnica separada. La autorización de promoción y cualquier cambio de alcance corresponden a otro nodo o a un humano.
