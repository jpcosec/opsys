## REFORMULACION
**Propósito:** redactar las entradas e índices authored del desk ejemplo como plantillas Markdown versionadas en el repo `deskops`, bajo `ejemplo/nav/` del paquete del plan.
**Resultado:** contenido de navegación que el generador de WS40 acepta y materializa en su root temporal.
**Repo dueño:** `deskops`.
**Límites:** no es productor del corpus, no redacta inventarios derivados, no escribe repos reales y no bloquea el lector temprano (WS16); WS30 integra estos índices.

## AMBIGUEDADES
1. «Registrar el root/store de procedencia al resolver los dos desks del manifiesto WS40; no duplicar el registry de deskops».
   Obliga a inventar el artefacto, formato y ubicación del registro: ¿va dentro de las plantillas versionadas, en un documento aparte o se relee del manifiesto WS40? Un root temporal no puede fijarse en plantillas reproducibles sin contradecir su materialización. La aceptación no define cómo comprobar ese registro ni quién lo produce.

## DRY-RUN
- **Lecturas previstas:** `contratos/navegacion.md` (salida WS11), `dag.yaml` y manifiesto JSON de WS40, `cobertura.md`, corpus temporal generado.
- **Cambios previstos:** añadir plantillas Markdown authored bajo `ejemplo/nav/`; ningún otro archivo.
- **Dependencias:** WS11 aporta resolución repo/store y enlaces; WS40 aporta generador, parámetro de plantillas y manifiesto con roots/stores/commits. WS08 es transitiva.
- **Validaciones futuras:** regenerar el corpus WS40 con la ruta de plantillas, recorrer enlaces Markdown sin UI, comprobar procedencia y ausencia de registry duplicado; WS30 recorre UF01 con estos índices.

## FUTURO
WS40 produce el generador y el manifiesto, y materializa las plantillas. WS11 entrega el contrato de navegación. WS30 valida la integración en UF01. WS43 publica en el desk real tras P09, `G_PRODUCT`, `G_HUMAN_MANUAL` y `G_WRITE_CONTRACT`. La decisión P09 corresponde a un humano; no se resuelve aquí.
