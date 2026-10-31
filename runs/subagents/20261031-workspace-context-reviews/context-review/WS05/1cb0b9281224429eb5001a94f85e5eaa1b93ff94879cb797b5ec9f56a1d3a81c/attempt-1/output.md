## REFORMULACION
**Propósito:** inventariar la identidad y la API pública de Scion para separar slug, agente, intento, dispatch, mensaje, conversación y permisos, distinguiendo lo que es interfaz pública de lo interno.
**Resultado:** `auditoria/scion.md` en el repo dueño `deskops`, leyendo también `../scion`.
**Límites:** solo lectura de código, documentación y configuración sin secretos; sin contactar endpoints vivos, usar credenciales, crear agentes, enviar mensajes ni modificar configuración. No produce `G_SCION`; eso corresponde a WS44.
**Aceptación:** comprobable: no usar tablas internas como interfaz, señalar campos internos ausentes de la API pública y capabilities que exigen API real, separar los seis conceptos y permisos, y marcar las capabilities que requieren WS32/WS33.

## AMBIGUEDADES
ninguna

## DRY-RUN
**Lecturas previstas:** `dag.yaml` (WS05), brief, alcance, decisiones y cobertura; código/documentación de `deskops` (`runtime/templates`, `models/run.py`); API pública documentada o exportada en `../scion`; configuración sin secretos.
**Cambios previstos:** crear únicamente `auditoria/scion.md`.
**Dependencias:** WS01 (brief autorado). No requiere `G_PRODUCT`; `G_SCION`, WS07 y WS44 operan fuera de este nodo. WS12 definirá después el contrato de registro por intento.
**Validaciones futuras:** revisar que el inventario no trate tablas internas como interfaz, separe slug/agente/intento/dispatch/mensaje/conversación y permisos, señale campos internos y capabilities dependientes de API real, WS32 y WS33; confirmar ausencia de contacto vivo, credenciales y secretos; cotejar todo con la aceptación y la guía.

## FUTURO
WS44 ejecutará el probe real y producirá `G_SCION`; WS32.1, WS32.2 y WS33 consumirán este inventario; WS12 aportará el contrato del registro por intento. La promoción sigue `not_authorized` y el TaskDoc fijará archivos, pruebas y textos exactos. No corresponde a este nodo decidir aceptación de deltas ni autorizar implementación, API o Scion.
