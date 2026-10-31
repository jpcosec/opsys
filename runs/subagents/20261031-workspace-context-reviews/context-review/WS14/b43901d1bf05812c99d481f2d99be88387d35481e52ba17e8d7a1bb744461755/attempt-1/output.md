## REFORMULACION

**Propósito:** integrar en el workspace una búsqueda navegable sobre la API real existente, sin parser propio.

**Resultado:** búsqueda por teclado que abre resultados con identidad y ruta de origen; al volver conserva consulta y foco; distingue sin resultados, error de backend y búsqueda degradada; no carga el grafo completo en cada tecla.

**Repo:** `graph_ui`, con salidas en `frontends/mindmap/source/`, `views/workspace/` y `tests/`.

**Límites:** solo texto/campos/semántica que ofrezca la API real; no implementa backend ni parser; el mecanismo concreto de tecleo se fija en TaskDoc; depende de WS13 y del gate `G_UI_READ`; el contrato de búsqueda y la auditoría vienen de WS11/WS03 de forma transitiva.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** `dag.yaml` de WS14, `auditoria/infraestructura.md` de WS03, contrato WS11, TaskDoc de promoción, código actual del workspace y pruebas existentes. Sin ejecutar.

**Cambios previstos:** código de búsqueda en `frontends/mindmap/source/`, integración en `views/workspace/` y pruebas en `tests/`; archivos exactos quedan para el TaskDoc.

**Dependencias:** WS13 como lector integrado; `G_UI_READ` pendiente por delta; WS11 y WS03 transitivos; API `sldb find` o ruta de `sldb serve`.

**Validaciones futuras:** recorrido por teclado buscar–abrir–volver con consulta y foco conservados; tres estados diferenciados; prueba de peticiones que teclear no dispara carga completa del grafo.

## FUTURO

WS03 produce la auditoría de infraestructura; WS11 el contrato de navegación/búsqueda; WS13 la base del lector; el TaskDoc fija teclas, textos, archivos y pruebas. El receptor humano P01 registra el recibo `G_UI_READ` por delta. WS16 realizará la validación humana posterior. Nada de esto autoriza implementación ni ejecución en este nodo.
