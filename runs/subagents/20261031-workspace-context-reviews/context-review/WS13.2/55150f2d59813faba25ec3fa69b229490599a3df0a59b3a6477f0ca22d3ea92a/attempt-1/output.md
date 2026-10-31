## REFORMULACION
**Propósito:** definir un explorador que permita descubrir y abrir documentos modelados del store y Markdown no modelado del desk sin conocer IDs ni exigir índices nuevos.
**Resultado:** componente de explorador en `graph_ui`, apoyado en las rutas de lectura y seguridad que fije WS11, con refresco explícito de catálogo.
**Repo dueño:** `graph_ui`.
**Límites:** solo exploración/lectura; reutiliza catálogo/filtro existente para modelados; no crea otro workspace, índices nuevos ni edición; no implementa APIs fuera del contrato WS11.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas previstas:** nodo WS13.2 y aristas WS11/WS13.1; `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`; gates `G_UI_READ`.
**Cambios previstos:** componentes bajo `frontends/mindmap/views/workspace/explorer/`; consumo de rutas de lectura definidas por WS11; pruebas en `tests/`. Sin ejecución.
**Dependencias:** contrato de identidad/navegación y API/seguridad para no modelados de WS11; lectura, contexto y foco de WS13.1; catálogo/filtro existente; matriz de promoción WS06 de forma transitiva; recibo `G_UI_READ` por delta.
**Validaciones futuras:** abrir un documento modelado y uno no modelado sin conocer su ID ni usar índices nuevos; altas en store temporal y Markdown del desk visibles tras refresco explícito, sin reiniciar servidor ni cambiar código; pruebas con store temporal real o corpus WS40.

## FUTURO
WS11 debe entregar el contrato de navegación y determinar API/seguridad para documentos no modelados; si falta, aplican las reglas comunes y el nodo se detiene sin sustituto. El receptor P01/repo `graph_ui` produce el acta `G_UI_READ` del delta concreto. WS06 reconcilia la promoción con el ticket receptor y evita duplicar implementación. El TaskDoc de promoción fijará archivos, pruebas y textos de pantalla dentro de esta aceptación. La aceptación humana del delta y el cierre del agregado WS13 corresponden a nodos/personas posteriores, no a este revisor.
