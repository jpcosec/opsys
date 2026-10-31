## REFORMULACION
**Propósito:** agrupar WS33.1 y WS33.2 para vincular mensajes y resultados a un intento existente y registrar una decisión humana explícita, con deduplicación y procedencia.
**Resultado:** nodo `aggregate` no ejecutable; se cierra cuando ambos hijos cumplen su aceptación.
**Repo:** `deskops`.
**Límites:** backend documental, independiente del editor UI; no tocar tablas Scion; depende de `G_SCION` y de la matriz que llega por WS11/WS12.

## AMBIGUEDADES
Ninguna.

El alcance del agregado remite a WS33.1/WS33.2, que concretan claves de deduplicación, procedencia, actor y resultado. `Hub` y el contrato público quedan cubiertos por `G_SCION`, producido por WS44; si falta, aplican las reglas comunes de alcance. La ausencia de TaskDoc detallado no cuenta: la promoción lo fijará.

## DRY-RUN
**Lecturas previstas:** nodo WS33 y aristas de WS32, WS11, WS33.1, WS33.2 y WS34; guía de revisión; `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`, `brief.md`; TaskDoc referenciado, si existe.
**Cambios previstos:** ninguno; el nodo no es ejecutable.
**Dependencias:** WS32 y WS11 como prerrequisitos; WS33.1 y WS33.2 como hijos; `G_SCION` resuelto por WS44 con operador designado en WS07. WS12 condiciona la operación de registro de decisión; su ausencia se registra como hueco, no se sustituye.
**Validaciones futuras:** aceptación de ambos hijos; importación repetida sin duplicados; decisión con actor, intento, tarea y resultado; `G_SCION` verificado; contrato WS12 para la operación de decisión. No se ejecuta ninguna.

## FUTURO
WS44 produce la prueba real de `G_SCION`; WS07 designa operador y responsables; WS12 fija la operación de decisión humana; la promoción genera TaskDoc, archivos y evidencia; una persona autoriza la promoción. Nada de ello se decide en esta revisión.
