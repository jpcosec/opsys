## REFORMULACION
Propósito: orientar a quien abre un proyecto sin desk. Resultado: pantalla de orientación con la ruta absoluta del proyecto y el comando `deskops init <ruta>`, sin inicializar desde la UI; tras un init externo, una lectura refrescada muestra el desk real. Repo dueño: graph_ui. Límites: solo lectura, nunca mutar por GET; el init lo ejecuta un actor externo; las rutas de lectura las fija WS11; promoción no autorizada.

## AMBIGUEDADES
1. «un proyecto sin desk muestra orientación»: no se define cómo detectar «sin desk». Obligaría a inventar el criterio (ausencia de `desk/`, de `.deskops`, de store, respuesta 503 u otro) y cuándo mostrar orientación en vez de lector o error.
2. «Tras init externo real, refrescar lectura» / «refrescar muestra el desk real»: no se concreta qué significa refrescar. Obligaría a inventar si basta recargar la página, hace falta un control, una relectura automática o invalidar el catálogo, y cómo probarlo.
3. «la ruta absoluta del proyecto como destino»: «destino» no está definido. Obligaría a inventar si la ruta se muestra como texto, se copia, se usa como argumento del comando o si «destino» designa otra cosa.

## DRY-RUN
Lecturas previstas: nodo WS15.2, aristas WS13/WS15, gate G_UI_READ y fuentes de alcance/decisiones/reconciliación; sin ejecutar. Cambios previstos: vista de orientación bajo `frontends/mindmap/views/workspace/orientation/` y tests; rutas de lectura según WS11. Dependencias: WS13 como lector previo, contrato WS11, recibo G_UI_READ por delta y `deskops init` externo (C-62). Validaciones futuras: abrir proyecto sin desk muestra orientación, ruta y comando sin mutar; ejecutar init fuera y refrescar muestra el desk real; comprobar que GET no inicializa.

## FUTURO
WS11 fija las rutas de lectura; el receptor P01 emite el acta G_UI_READ del delta; el TaskDoc de promoción concreta archivos, textos y pruebas; una persona ejecuta el init externo y valida el refresco.
