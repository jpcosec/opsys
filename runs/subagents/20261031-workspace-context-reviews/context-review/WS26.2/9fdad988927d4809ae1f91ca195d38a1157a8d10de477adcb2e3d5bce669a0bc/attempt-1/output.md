## REFORMULACION

**Propósito:** que Board muestre el enrutamiento explícito y una representación de “capa lista” según dependencias/no solapamiento, sin confundir esa vista con ejecución.

**Resultado:** código de enrutamiento y representación en `graph_ui`, con pruebas, y comportamiento de promoción sujeto al canal autorizado que respete commits previos y estado real.

**Repo:** `graph_ui`, en `frontends/mindmap/views/workspace/routing/` y `tests/`; endpoints según contrato WS12.

**Límites:** `promotion: not_authorized`; no se autoriza ejecutar promoción ni implementar fuera del alcance declarado. Depende de WS12, WS22 y WS26.1, y de los gates listados.

## AMBIGUEDADES

1. “representación de capa lista por dependencias/no solapamiento” — no se define qué es una “capa lista”, qué la hace estar lista, qué representa visualmente ni qué significa “no solapamiento”. Obliga a inventar definición, criterio y forma de representación.
2. “Enrutamiento explícito en Board” — no se especifica si “enrutamiento” es ruta URL, flujo de estados, relación de dependencias o navegación entre tareas. Obliga a inventar su semántica y comportamiento observable.
3. “Board real refleja el enrutamiento sin confundirlo con ejecución; el canal de promoción respeta commits previos y estado real” — la aceptación no fija evidencia, observable ni quién la certifica. Obliga a inventar la prueba de aceptación.

## DRY-RUN

- **Lecturas previstas:** nodo WS26.2, `task-ws26-2.md` al promoverse, contrato WS12, salidas de WS22 y WS26.1, definiciones de gates.
- **Cambios previstos:** módulo de routing en la ruta indicada y pruebas; ningún cambio fuera de `graph_ui`.
- **Dependencias:** contrato WS12 (endpoints, commits, canal); Board WS22; autoría WS26.1; G_UI_WRITE, G_WRITE_CONTRACT, G_CLOSEOUT y G_HUMAN_READ.
- **Validaciones futuras:** demostrar en Board real el enrutamiento y la “capa lista”; comprobar que la promoción no altera commits previos ni estado; aceptación del delta graph_ui.

## FUTURO

- WS12 produce la whitelist/endpoints y acepta el delta de `graph_ui`.
- WS16 produce G_HUMAN_READ.
- El humano designa responsable de `graph_ui` y autoriza la promoción; el preflight de task/pills corresponde a la promoción, no a este nodo.
- G_CLOSEOUT depende de un resolver externo.
