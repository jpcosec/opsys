## REFORMULACION

**Propósito:** declarar ViewDoc y NotationDoc concretos para selecciones y notación ya soportadas por spec2viz, reutilizando el evaluador y rutas de graph_ui y la notación de spec2viz.

**Resultado:** artefactos de proyección y pruebas que demuestren, sobre un store real, que la selección evaluada coincide con la declarada y que el ViewDoc documenta qué selecciona.

**Repo:** spec2viz (`output_base: repository_root`), con salida en `sldb/views/` y `tests/`.

**Límites:** no crear UI declarativa ficticia, servicio, CLI ni runtime fuera de graph_ui; no extraer/compartir el evaluador; no pedir portabilidad genérica; no inventar selección; deskops no escribe en spec2viz; promoción `not_authorized`; G_SPEC_VIEW pendiente y por delta.

## AMBIGUEDADES

1. «reutilizando el evaluador y las rutas de graph_ui (C-37) y la notación de spec2viz (C-49)». Los identificadores C-37/C-49 no se definen en las fuentes suministradas. Obligaría a inventar qué contrato, ruta o capacidad concreta designan y si están disponibles; no basta con saber que existen evaluador y notación.

2. «la selección coincide con la declarada». No indica si «declarada» es la selección del catálogo WS09, la del contrato WS11 o la que el propio ViewDoc escribe. Obligaría a elegir una fuente de verdad ante discrepancia, aunque el `scope` apunta a WS09/WS11.

## DRY-RUN

**Lecturas previstas:** WS18 en dag.yaml; salidas de WS09 (catálogo) y WS11 (contrato); capacidades WS03; brief/alcance/decisiones; estado de G_SPEC_VIEW; evaluador/rutas de graph_ui y notación existente en spec2viz.

**Cambios previstos:** crear ViewDoc/NotationDoc en la ruta confirmada al promover y pruebas en spec2viz. Ninguno ahora.

**Dependencias:** WS09 debe fijar selección mínima; WS11, identidad/enlaces; G_SPEC_VIEW, recibo por delta del receptor spec2viz. Si falta selección, detener promoción y corregir WS09.

**Validaciones futuras:** ejecutar el camino existente de graph_ui sobre store real, comparar selección declarada/evaluada, revisar documentación del ViewDoc, evitar alegar equivalencia de payload completo con dos stores, y preflight de TaskDoc en spec2viz.

## FUTURO

WS09 produce el catálogo y WS11 el contrato; P01/receptor de spec2viz emite el acta G_SPEC_VIEW por delta; el supervisor/Executor de spec2viz promueve y ejecuta la TaskDoc; la aceptación humana decide la recepción.
