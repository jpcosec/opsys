## REFORMULACION

**Propósito**: implementar en graph_ui la lectura solo lectura de documento/fuente, panel de contexto (identidad, relaciones, origen), enlaces y Code local con selección por documento/nodo, conforme al contrato WS11. **Resultado**: delta conciliado sobre el workspace integrado a1b2b22, con evidencia de aceptación ampliada (Markdown no modelado/fuente, enlaces y foco), sin duplicar workspace ni depender de IDs. **Repo**: graph_ui (`frontends/mindmap/views/workspace/`, rutas de lectura del contrato WS11, `tests/`). **Límites**: depende de WS11; requiere `G_UI_READ`; `promotion: not_authorized`; no inventar mapeo texto→código; el cierre no se infiere de f16fcd1/134a665.

## AMBIGUEDADES

1. «la respuesta que entrega ambos lleva la revisión (hash de bytes) de la lectura de la que salieron los dos, **o** los dos se derivan de una sola lectura de bytes» (navegacion §4): dos mecanismos alternativos; obliga a inventar cuál se implementa y cómo se valida «mismo origen».
2. «Mientras ese delta no tenga su recibo propio (sección 12), WS13.1 no puede declararse cumplido en foco texto/code/graph» frente a la aceptación del nodo que exige ese foco: obliga a inventar si H-03/H-03b/H-04 entran en este nodo o son prerrequisito externo.
3. «la reutilización con un descriptor y `model=None` se verifica al implementar WS13.1» (§C5b): no fija criterio ni qué hacer si falla; obligaría a inventar el criterio de verificación.
4. «El soporte, el formato y el punto de carga de la configuración son implementación de WS41» y, sin configuración, «usan `local`» (§3.2): WS13.1 necesita ese alias pero no se dice de dónde lo obtiene antes de WS41; obliga a inventar la fuente.

## DRY-RUN

Lecturas: contrato WS11, nodo WS13.1, F17, y código citado (`GU/workspace_routes.py`, `sldb_adapter.py`, `shell/api.js`, `views/workspace/`). Cambios previstos: ruta de fuente propia con guardias §3.3 y lectura única para IR+hash; preservar `files`/`references` y posición antes de concatenar; exponer metadata de aristas `schema`; foco por sección/span y campo; `request()` conserva el status HTTP. Dependencias: contrato WS11; sin WS41 para el desk propio. Gate: `G_UI_READ` más recibo externo del delta (sin acta). Errores: E5/E7 en UI; E-MD1–4 no aplican al desk propio. Validación futura: tests en graph_ui, mismo origen observable y store sin cambios tras la lectura.

## FUTURO

P01 registra el acta y el recibo del delta de foco; WS41 define formato/carga de la configuración de aliases; WS40 genera el corpus de dos desks y sus enlaces; WS13.2 declara la lista de permitidos del explorador; WS13.3 fija la sintaxis de la clave de sesión; WS12 aporta el contrato de escritura.
