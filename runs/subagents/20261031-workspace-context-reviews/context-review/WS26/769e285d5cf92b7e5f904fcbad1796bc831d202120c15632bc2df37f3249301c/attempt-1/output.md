## REFORMULACION

**Propósito:** integrar en el workspace la autoría explícita desde candidato, la evidencia declarada, las dependencias y el binding de contexto/pills, además del enrutamiento en Board y la representación de capa lista.

**Resultado:** nodo `aggregate` no ejecutable; se cumple cuando WS26.1 y WS26.2 cumplen su aceptación. No produce artefacto propio: su `output_scope` es el agregado de las salidas de sus hijos.

**Repo dueño:** `graph_ui` (`output_base: graph_ui:repository_root/`).

**Límites:** no ejecutar; `promotion: not_authorized`; no confundir ruta de Board con ejecución; toda operación sin contrato/dueño queda en handoff y no disponible; los gates pendientes son intencionales.

## AMBIGUEDADES

Ninguna. El nodo es agregado no ejecutable, su aceptación remite a hijos identificados y las operaciones sin contrato tienen regla explícita en `alcance.md`. Los gates `G_CLOSEOUT`, `G_UI_WRITE`, `G_HUMAN_READ` y `G_WRITE_CONTRACT` están pendientes de forma intencional, no son defecto.

## DRY-RUN

- **Lecturas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`; en `dag.yaml`, WS26, WS26.1, WS26.2, WS12, WS22 y bloque `gates`. Sin herramientas ni ejecución.
- **Cambios previstos:** ninguno; esta revisión es solo lectura.
- **Dependencias:** WS12 (contrato de operaciones/escritura y closeout), WS22 (representación de Board), WS26.1 y WS26.2 (hijos).
- **Validaciones futuras:** aceptación de ambos hijos; `G_WRITE_CONTRACT` y `G_UI_WRITE` producidos por WS12; `G_CLOSEOUT` externo; `G_HUMAN_READ` por WS16; recorrido UF04 en WS30.

## FUTURO

- WS07: resolver P01/P03–P06 y designar responsables, incluido el operador Scion.
- WS12: emitir whitelist/canal/efectos y aceptar el delta de `G_UI_WRITE` en `graph_ui`.
- Humano: aceptar actas y evidencia de closeout.
- WS26.1/WS26.2: implementar y aportar pruebas dentro de su alcance.
- WS30: validación humana bajo protocolo.
