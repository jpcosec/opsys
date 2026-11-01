## REFORMULACION

**Propósito:** nodo de implementación en `graph_ui` que muestra, junto a la TaskDoc, evidencia declarada, encontrada y verificada, sin crear modelo de comentarios.

**Resultado:** representación en `frontends/mindmap/views/workspace/evidence/` que distingue estados (declarada sin artefacto, artefacto no declarado, verificación fallida, ausente) y abre soportes Markdown del workspace; fuera de ese caso muestra ruta y declara no soportado.

**Repo dueño:** `graph_ui`.

**Límites:** solo lectura; no infiere evidencia por extensión; verificada = resultado de `deskops closeout verify`/gate, no prueba independiente; no muta ni crea API o modelo; depende de WS13 (lector) y WS12 (contrato), con `G_UI_READ` pendiente por delta.

## AMBIGUEDADES

Ninguna. Las posibles dudas —correspondencia por tipo de evidencia, artefactos soporte, formato de salida de `deskops closeout verify` y rutas de lectura— tienen productor nombrado (WS12 y WS11) y `alcance.md` fija qué hacer si faltan: detenerse y registrar el hueco, sin inventar sustituto. La aceptación enumera estados comprobables y el límite de apertura.

## DRY-RUN

**Lecturas futuras:** `contratos/operaciones.md` de WS12; contrato WS11; código actual de `shell/registry.js`, vistas workspace y lector de `graph_ui`; modelo TaskDoc/closeout en deskops; tests existentes; acta de `G_UI_READ`.

**Cambios previstos:** archivos nuevos bajo `.../workspace/evidence/` y `tests/`; sin backend, modelos ni mutaciones.

**Dependencias:** WS13 (lector y apertura de soporte), WS12 (correspondencia y salida pública de closeout verify), `G_UI_READ` (acta por delta concreto). No requiere WS27.1 ni corpus WS40 para implementar.

**Validaciones futuras:** casos de aceptación con los cuatro estados sin colapsar; apertura Markdown dentro del workspace; ruta + no soportado fuera; ausencia/fallo como no verificable; pruebas con store temporal real y acta P01.

## FUTURO

- WS12 publica el contrato de correspondencia y salida de `closeout verify`.
- WS13 entrega el lector con el que se abre el soporte.
- P01 emite el acta por delta de `G_UI_READ`.
- La promoción fija TaskDoc, archivos exactos, escenarios y textos.
- Si falta contrato o permiso al ejecutar, el ejecutor se detiene según reglas comunes; no lo decide este nodo.
