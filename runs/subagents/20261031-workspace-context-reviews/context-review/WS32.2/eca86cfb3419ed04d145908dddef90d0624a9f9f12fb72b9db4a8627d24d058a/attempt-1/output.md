## REFORMULACION
Propósito: fijar un encargo de planificación para que manifiesto, RunDoc y cierre sean consistentes e idempotentes sobre el intento correcto, identificado por el id citado en el cierre. Resultado: implementación en `deskops` de registro canónico por intento, con campos mínimos definidos y aceptación repetible. Repo dueño: `deskops`. Límites: no ejecutar; depende de WS05, WS12 y WS32.1, y de G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT.

## AMBIGUEDADES
1. «manifiesto, RunDoc e índice de cierre coinciden en id de intento, hash de sesión y evidencia». El «hash de sesión» no aparece entre los campos mínimos del manifiesto ni se define su origen. Obliga a inventar qué sesión se hashea, cómo se obtiene y cómo se compara.
2. «índice de cierre» aparece en aceptación, mientras el scope habla de «registros de closeout». Obliga a inventar si es un artefacto distinto, su formato, ubicación y dueño.
3. «Una finalización repetida sobre el mismo id de intento conserva identidad y evidencia sin crear registros nuevos». No define qué ocurre si la repetición trae evidencia o commit de cierre distintos. Obliga a inventar si se rechaza, se conserva lo primero o se sobrescribe.

## DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS32.2 y contratos vecinos WS05/WS12/WS32.1. Cambios previstos: `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`. Dependencias: WS05 aporta inventario de identidad/API; WS12, contrato de operaciones; WS32.1, separación intento/dispatch. Validaciones futuras: repetir finalización sobre el mismo id, comprobar ausencia de registros nuevos y coincidencia de id, hash de sesión y evidencia; preflight de promoción sin ejecutar.

## FUTURO
WS05/WS44 producen el inventario y el probe de API pública; WS12 cierra la whitelist y efectos; WS07 designa actores; el TaskDoc de promoción fija archivos, pruebas y textos; el humano resuelve Pxx y gates. Nada de ello se decide aquí.
