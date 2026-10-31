## REFORMULACION

**Propósito:** inventariar las superficies concretas de Deskops (archivos, comandos públicos y modelos registrados) y la operación que cada una expone, con estado verificado.
**Resultado:** `auditoria/deskops.md`, una fila por superficie.
**Repo dueño:** `deskops` (nodo `planning`, depende de WS01).
**Límites:** no inferir modelo por carpeta; lo no comprobado se marca «no comprobado» con causa; solo lectura citada (`archivo:línea` o comando read-only); sin ejecución autorizada.

## AMBIGUEDADES

1. «Superficie = cada archivo, comando público o modelo registrado concreto de las categorías enumeradas» + «inbox/drawer/issues/FAQ/crossroads/pills/fases/rituales/registry/roles/runs».
La enumeración mezcla áreas de almacenamiento, conceptos y artefactos sin decir qué cuenta como «archivo» de cada categoría. Obliga a inventar la unidad de fila (¿un archivo por pill?, ¿todo `desk/drawer/`?, ¿un ítem por «rol» o «run»?).

2. «Modelos y Markdown no modelado» frente a «Modelado = tiene modelo registrado en el store».
No queda claro si el Markdown no modelado es superficie inventariable (y con qué ubicación/operación) o solo una clasificación de estado. Obliga a decidir si cada `.md` del desk genera fila o solo los que tienen contrato.

3. «firmas públicas, efectos Git y cierre» frente a «la operación expuesta (comando o método que la lee o muta, o «dato pasivo»)».
No se especifica si cada firma pública (CLI/`DeskopsOperations`) es fila propia o atributo de la superficie que opera. Obliga a fijar granularidad y evita saber cuándo el inventario está completo.

## DRY-RUN

**Lecturas previstas:** brief.md, alcance.md, decisiones.md, cobertura.md, `dag.yaml` (WS02 y vecinos), guía; en ejecución futura, repo Deskops y `sldb models list`.
**Cambios previstos:** ninguno en este nodo de revisión; el nodo produciría `auditoria/deskops.md`.
**Dependencias:** WS01 (brief/glosario). WS06/WS10 consumen la auditoría; WS03/WS04 llegan transitivamente.
**Validaciones futuras:** cada fila con ubicación y operación; citas `archivo:línea` o salida read-only; marcas «no comprobado» con causa; sin modelo inferido por carpeta.

## FUTURO

- TaskDoc de promoción: archivos exactos, pills/átomos y preflight (no autorizado aún).
- WS06 usa el inventario para su matriz de correspondencias; WS10 lo usa para el manual.
- WS07 designa responsables receptores; WS11/12 registran aceptación.
- Cualquier hueco de API detectado se registra con repo dueño, no se sustituye.
