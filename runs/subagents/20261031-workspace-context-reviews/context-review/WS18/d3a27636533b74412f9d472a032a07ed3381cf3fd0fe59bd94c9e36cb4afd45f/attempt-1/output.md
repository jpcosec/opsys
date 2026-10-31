## REFORMULACION

**Propósito:** declarar una proyección de grafo reutilizable —ViewDoc con su NotationDoc— para selecciones y notación ya soportadas por spec2viz, sin crear UI declarativa ficticia.

**Resultado:** un ViewDoc portable que renderiza sobre un store real la selección declarada, coincide con ella y documenta qué selecciona, más sus pruebas.

**Repo:** `owner_repo: spec2viz`; salida prevista en `sldb/views/` y `tests/`, con rutas confirmadas por el dueño de spec2viz al promover. El paquete deskops no escribe en spec2viz.

**Límites:** no inventar selección; si WS09/WS11 no fijan una selección mínima, detener la promoción y corregir el contrato. No crear páginas declarativas ficticias.

**Dependencias:** WS09 (catálogo), WS11 (contrato) y G_SPEC_VIEW por delta.

## AMBIGUEDADES

ninguna.

## DRY-RUN

**Lecturas:** WS09 (`vistas.md`), contrato de navegación WS11, capacidades WS03, documentación/código existente de ViewDoc y NotationDoc en spec2viz, store/corpus real y pruebas actuales.

**Cambios previstos:** añadir el ViewDoc/NotationDoc y pruebas en spec2viz; ningún cambio en deskops.

**Dependencias:** WS09/WS11 disponibles; G_SPEC_VIEW recibido para este delta antes de promover; dueño de spec2viz confirma rutas.

**Validaciones futuras:** preflight de promoción, render sobre store real, comparación con la selección declarada, documentación de la selección, recepción G_SPEC_VIEW y revisión del delta. Sin ejecutar.

## FUTURO

WS09 produce el catálogo y la selección mínima; WS11 el contrato; WS03 las capacidades contrastadas. Si faltan, se detiene la promoción y se corrige en el repo productor. P01/receptor emite el acta G_SPEC_VIEW por delta con commit verificable; el dueño de spec2viz confirma rutas y promueve la TaskDoc; esta fija archivos, escenarios y textos; el Executor de spec2viz ejecuta y la aceptación humana valida el delta.
