REFORMULACION
Propósito: declarar en spec2viz ViewDocs reutilizables, cada uno con su NotationDoc, para selecciones y notación ya soportadas. Resultado: ViewDoc portable que, sobre un store real, materializa y coincide con la selección declarada y la documenta; pruebas en `tests/`. Repo dueño: spec2viz (`output_base: spec2viz:repository_root/`), con `output_scope: sldb/views/ ... tests/` y `promotion: not_authorized`. Límites: no crear UI pages declarativas ficticias; exige G_SPEC_VIEW; no modificar su repo desde este plan; no ejecutar.

AMBIGUEDADES
1. «no modificar su repo desde este plan» frente a «owner_repo: spec2viz» y «output_scope: sldb/views/ ... tests/». Obliga a inventar si la ejecución de WS18 puede escribir en spec2viz o solo preparar handoff; la frase puede leerse como prohibición de tocar el repo que el propio nodo declara como dueño.
2. «Vista portable (el mismo ViewDoc sin código específico del host) renderiza sobre un store real la selección declarada». No se nombra renderer ni harness, ni si WS18 debe construir uno; el scope solo habla de ViewDoc/NotationDoc y prohíbe UI pages. Obliga a inventar el medio de renderizado y el alcance del código de prueba.

DRY-RUN
Lecturas: WS18 en `dag.yaml`; WS09/WS11 como contratos vecinos; gate G_SPEC_VIEW; brief, alcance y decisiones; documentación de spec2viz al promover. Cambios previstos: declaraciones ViewDoc/NotationDoc en `sldb/views/` y pruebas en `tests/`; sin UI pages. Dependencias: catálogo WS09, contrato/acta WS11-G_SPEC_VIEW, dueño designado y promoción receptora. Validaciones futuras: render sobre store temporal/real, igualdad con la selección, portabilidad sin código de host, aceptación y preflight task-only.

FUTURO
WS11 produce el contrato y el acta G_SPEC_VIEW, que fija el conjunto «ya soportado»; WS07/P01 designa al responsable de spec2viz; ese dueño promueve las tareas receptoras. WS24 consume los ViewDoc. La aprobación humana de P01/P04 y la promoción quedan fuera de este nodo.
