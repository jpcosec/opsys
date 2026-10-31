## REFORMULACION
**Propósito:** refinar el ticket Scion para que la identidad de intento no se confunda con slug/agente y para separar `dispatch intent` de `confirmed`, sin crear un segundo pipeline. **Resultado:** cambios en `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/` que registren ids de intento propios y permitan comprobar dos intentos del mismo agente y un dispatch fallido; los cambios de RunDoc pasan por CLI sldb. **Repo dueño:** deskops. **Límites:** no segundo pipeline, no edición ad hoc de RunDoc, `promotion: not_authorized`; depende de WS05/WS12 y de G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT.

## AMBIGUEDADES
1. «dispatch intent (intención registrada) y confirmed (Scion aceptó) como hechos separados del RunDoc». «del RunDoc» admite leer “separados de” o “hechos del”. Obliga a inventar si viven fuera del RunDoc o como campos nuevos dentro.
2. «evidenciadas por ids de intento propios». No dice quién genera el id de intento ni con qué forma o garantía; `confirmed` remite a la identidad de la API, pero `intent` no. Obliga a inventar autoridad y generación del id (local/API/derivado).
3. «un dispatch fallido (rechazo o timeout de la API)». Un timeout no equivale a rechazo: la API pudo aceptar sin respuesta. Obliga a inventar si `confirmed` queda falso, desconocido o se reconcilia después.
4. «cambios de RunDoc por el flujo SLDB de modelos (registro y edición de documento trackeado con CLI sldb), no edición ad hoc». No define evidencia ni criterio observable de “no ad hoc”. Obliga a inventar cómo se demuestra en aceptación.

## DRY-RUN
**Lecturas (al ejecutar):** nodo/aristas, brief, alcance, decisiones, guía; en deskops `runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`, plantilla RunDoc, ticket `external_references.scion`; salidas de WS05 (`auditoria/scion.md`) y WS12 (`contratos/operaciones.md`); evidencia de gates. **Cambios previstos:** lógica y modelo para id de intento y estados `dispatch intent`/`confirmed`; tests; actualización de RunDoc por CLI sldb. **Dependencias:** WS05, WS12; G_SCION vía WS44, G_WRITE_CONTRACT y G_CLOSEOUT. **Validaciones futuras:** pruebas de dos intentos y dispatch fallido con ids distintos; comprobación del canal sldb; WS32.2 verificará idempotencia/manifiesto; WS37 aceptará UF06.

## FUTURO
WS32.2 define el manifiesto canónico y la idempotencia; WS44 ejecuta el probe que produce G_SCION; WS12 cierra el contrato; WS07 designa operador Scion; el humano resuelve Pxx; la promoción fija TaskDoc, archivos exactos y pruebas. Nada de eso se decide aquí.
