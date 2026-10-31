REFORMULACION  
Propósito: que spec2viz declare ViewDoc más su NotationDoc reutilizables para selecciones y notación ya soportadas, sin convertir ViewDoc en contrato universal de UI ni crear páginas declarativas ficticias. Resultado: un ViewDoc portable que, sobre un store real, renderiza y coincide con la selección que documenta, con pruebas y promoción de tareas receptoras por el dueño de spec2viz. Repo: `spec2viz` (`output_base: spec2viz:repository_root/`); `output_scope`: `sldb/views/` y `tests/`, rutas confirmadas por el dueño al promover. Límites: solo selecciones/notación ya soportadas; no modificar el repo desde este plan; promoción no autorizada; depende de WS09/WS11 y exige `G_SPEC_VIEW`.

AMBIGUEDADES  
Ninguna. La condición «para selecciones y notación ya soportadas por spec2viz» acota el resultado sin exigir inventar un catálogo nuevo; el «store real» queda resuelto por las reglas comunes de alcance (store temporal real o corpus WS40). El gate pendiente es intencional.

DRY-RUN  
Lecturas: `dag.yaml` del nodo WS18, aristas WS09/WS11/WS24 y gate `G_SPEC_VIEW`; guía, brief, alcance, decisiones y cobertura. Cambios previstos, sin ejecutar: en `spec2viz`, añadir ViewDoc(s) y NotationDoc bajo `sldb/views/` y pruebas en `tests/`; no tocar el repo hasta promoción. Dependencias: catálogo WS09, contrato/acta WS11 y `G_SPEC_VIEW`; WS24 consumirá los ViewDoc. Validaciones futuras: promoción por dueño con tarea receptora, rutas y no solapamiento; prueba con store temporal real o corpus WS40; comprobar render sin código específico del host, coincidencia con la selección declarada y documentación de esa selección.

FUTURO  
WS11 produce/resuelve el acta de `G_SPEC_VIEW`; WS07 designa al responsable de spec2viz; el dueño de spec2viz confirma rutas y promueve tareas receptoras; WS24 consume los ViewDoc; una persona autoriza la promoción. Nada de esto es ambigüedad del nodo.
