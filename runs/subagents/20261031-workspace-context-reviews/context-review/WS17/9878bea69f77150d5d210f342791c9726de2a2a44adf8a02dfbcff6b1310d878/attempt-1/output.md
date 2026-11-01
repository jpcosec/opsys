REFORMULACION
WS17 es un encargo de documentación en `deskops`: escribir plantillas Markdown de entradas e índices authored del desk ejemplo bajo `ejemplo/nav/`, usando WS11 y WS40, sin producir el corpus. No es agregado: es documentación ejecutable. El resultado es un conjunto de plantillas fuente única que WS40 materializa en root temporal y que WS30 valida y WS43 publica. Límites: no escribir repos reales, no copiar inventarios/registry ni listados completos, no editar el destino temporal como registro competidor; puede escribirse antes de WS16.

AMBIGUEDADES
1. «conjunto de plantillas cubre ambos desks, no cada plantilla individual» y «texto curado y enlaces de entrada elegidos para recorrido»: no definen qué documentos, índices o enlaces debe incluir ni qué significa “cubrir” un desk. Obliga a inventar la selección, extensión y criterio de aceptación comprobable.

DRY-RUN
Tras promoción autorizada, el ejecutor leería `contratos/navegacion.md` (WS11), el generador y manifiesto de WS40, y el inventario WS02 disponible transitivamente por WS11. Crearía/modificaría solo plantillas bajo `desk/drawer/plans/workspace-documental/ejemplo/nav/`; no tocaría WS40, registry real, repos temporales ni checkout real. Ejecutaría el generador WS40 con la ruta de plantillas, revisaría el manifiesto y recorrería los links Markdown; comprobaría roots/aliases, ausencia de duplicación del registry, cobertura de ambos desks y que el destino temporal no se commitea. Errores esperados: falta de campos del contrato WS11, el generador no materializa las plantillas, link irresoluble o duplicación; ante ello, detenerse y registrar el hueco con repo dueño, sin sustituto. WS17 no tiene gate propio; consume G_PRODUCT (WS11) y G_UI_READ (WS40); promoción `not_authorized`.

FUTURO
WS40 materializa las plantillas; WS16 prueba lectura; WS30 valida manualmente las entradas; WS43 publica en deskops real. La persona autoriza promoción/TaskDoc y fija archivos, pills y evidencias; no es ambigüedad.
