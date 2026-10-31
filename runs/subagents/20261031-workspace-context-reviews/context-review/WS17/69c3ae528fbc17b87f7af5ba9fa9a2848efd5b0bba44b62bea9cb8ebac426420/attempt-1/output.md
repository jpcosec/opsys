## REFORMULACION

**Propósito:** escribir entradas e índices authored del desk de ejemplo como plantillas Markdown versionadas en el paquete del plan. **Resultado:** plantillas bajo `ejemplo/nav/` que WS40 materializa en su corpus temporal, verificables recorriendo links sin UI y resolviendo roots/stores de los dos desks del manifiesto. **Repo dueño:** deskops. **Límites:** no es productor del corpus; no copia inventarios derivados ni duplica el registry; no escribe repos reales; puede escribirse antes de WS16; promoción no autorizada.

## AMBIGUEDADES

1. «sin copiar inventarios derivados» frente a «Escribir solo entradas/índices authored»: no define la frontera entre índice authored e inventario derivado; obliga a inventar qué listados pueden escribirse.

2. «source versionado y destino temporal no son registros independientes»: no define “registro independiente” ni cómo comprobarlo; obliga a inventar el criterio de verificación.

3. «Verificar al regenerar que cada plantilla resuelve el root/store de procedencia de los dos desks del manifiesto WS40»: “resuelve” no fija forma del enlace (relativo, absoluto, alias) ni si cada plantilla cubre ambos desks; obliga a inventar la comprobación.

4. «no duplicar el registry de deskops»: el registry no está definido en las fuentes suministradas; obliga a inventar su forma y contenido para evitarlo.

## DRY-RUN

**Lecturas previstas:** nodo WS17 y aristas WS11/WS40/WS30/WS43 en `dag.yaml`; guía, brief, alcance, decisiones y cobertura; en ejecución futura, contrato de navegación WS11 y generador/manifiesto WS40.

**Cambios previstos:** crear plantillas Markdown authored bajo `deskops:desk/drawer/plans/workspace-documental/ejemplo/nav/`; ningún corpus, repo real ni registry.

**Dependencias:** WS11 (identidad/enlaces) y WS40 (generador con parámetro de plantillas y manifiesto).

**Validaciones futuras:** regenerar corpus WS40 con `ejemplo/nav/`; recorrer links Markdown sin UI; verificar roots/stores de ambos desks y ausencia de duplicación del registry; WS30 integra después y WS43 publica en el desk real.

## FUTURO

WS40 debe aceptar la ruta de plantillas y emitir manifiesto; WS30 realiza validación humana; WS43 publica tras validar; la promoción humana fija TaskDoc, archivos exactos y pruebas; WS11 entrega el contrato de navegación. Nada de esto es ambigüedad del nodo.
