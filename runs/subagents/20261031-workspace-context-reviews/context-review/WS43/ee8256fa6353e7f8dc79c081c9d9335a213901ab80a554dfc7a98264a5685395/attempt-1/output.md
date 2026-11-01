REFORMULACION

WS43 es un nodo de entrega documental en `deskops`: tras validar WS17 (plantillas/índices) y WS30 (acta manual), publicar en el desk real el README, el mapa/índices authored y átomos de acuerdos durables, enlazando todos los repos de `deskops list repositories` sin escribir en ellos. Resultado: mapa publicado trazable a las entradas WS17 y al acta WS30, con acta de publicación en `runs/subagents/workspace-documental-acceptance/publicacion/acta.md` y commit. Límites: no modificar repos hermanos, no imponer modelos nuevos, no publicar el ejemplo como ecosistema real, no inventar entradas para repos sin entrada; operaciones solo por contrato WS11/WS12 y gates.

AMBIGUEDADES

ninguna

DRY-RUN

No es agregado; es ejecutable tras promoción. Lecturas: `dag.yaml` (WS43, WS17, WS30), brief/alcance/decisiones, contrato WS11 `contratos/navegacion.md`, contrato WS12 `contratos/operaciones.md` y recibo per_delta de WS43, plantillas WS17, acta WS30 con paths/hashes, `desk/registry/repo-*.md`, `desk/README.md`, salida de `deskops list repositories` y átomos existentes. Cambios previstos: crear/actualizar `desk/README.md`; crear mapa/índices authored en la ubicación que fijen P09, WS11 y TaskDoc; crear o enlazar átomos de acuerdos durables según la regla P01/P02/P07/P09 y P03–P06/P08 si aplica; escribir el acta de publicación; commit por `deskops closeout commit`. Dependencias/gates: consume WS17 validado por WS30 y contratos WS11/WS12; G_PRODUCT ya satisfecho; G_HUMAN_MANUAL y G_WRITE_CONTRACT deben estar producidos antes de publicar. Errores: contrato ausente → detenerse y registrar hueco con repo dueño, sin sustituto; link que no resuelve → fallo; repo sin entrada authored → enlazar registry y dejar follow-up, sin omitir ni fabricar. Validación esperada: recorrido humano del Markdown y UI reales, roots/aliases y links resolubles, átomos con etiquetas/fuentes, correspondencia WS17→publicación en acta y commit verificable.

FUTURO

WS17 entrega plantillas; WS30 produce el acta y satisface G_HUMAN_MANUAL; WS11 y WS12 producen navegación y operaciones, y WS12 verifica el recibo per_delta de WS43. El participante P08 decide/realiza el recorrido de publicación. Nada de esto es ambigüedad del nodo.
