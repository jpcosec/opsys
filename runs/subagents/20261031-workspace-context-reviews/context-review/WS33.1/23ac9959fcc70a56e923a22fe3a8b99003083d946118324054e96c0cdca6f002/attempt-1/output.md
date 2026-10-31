## REFORMULACION

- **Propósito:** vincular mensajes y resultados de Scion a un intento existente, conservando procedencia y evitando duplicados.
- **Resultado:** importación idempotente por Hub/proyecto/conversación/mensaje y por Hub/proyecto/intento/id de fuente; los mensajes sin intento resoluble quedan como hueco de procedencia.
- **Repo dueño:** `deskops`, con salidas en `runtime/`, modelos/reportes y tests.
- **Límites:** no tocar tablas Scion, no depender del editor UI, no vincular sin id de intento existente; `G_SCION` pendiente y promoción no autorizada.

## AMBIGUEDADES

Ninguna. Las referencias a WS05/WS44 y `G_SCION` tienen productor nombrado y la regla común de ejecución cubre su ausencia; los archivos, campos y casos concretos quedan delegados al TaskDoc de promoción.

## DRY-RUN

- **Lecturas:** input completo, guía, nodo WS33.1 y aristas contractuales, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y `reconciliacion.md`.
- **Cambios previstos:** adaptador en `runtime/`, modelos/reportes y tests; sin tocar tablas Scion ni UI.
- **Dependencias:** WS32 aporta identidad de intento; WS05/WS44 confirman el identificador de fuente; `G_SCION` lo produce WS44; WS12 llega de forma transitiva.
- **Validaciones futuras:** probe real de `G_SCION`; importación repetida sin duplicados; no atribución de conversación completa a un intento; mensajes no vinculados registrados como hueco; ausencia de escritura en tablas Scion; preflight del TaskDoc. Nada ejecutado.

## FUTURO

WS44 produce el probe y satisface `G_SCION`; WS32.1/WS32.2 fijan identidad de intento y cierre; WS05/WS44 inventarían el identificador de fuente; WS06/WS11/WS12 aportan matriz y contratos transitivos; una persona autoriza la promoción.
