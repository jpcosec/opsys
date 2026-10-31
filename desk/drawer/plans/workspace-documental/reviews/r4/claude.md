# R4 — claude: delta revisión 4

## Veredicto: REQUIERE CORRECCIONES

Queda un bloqueante, introducido por este delta y de corrección mínima.

`validate_plan.py --check` y `build_plan.py --check` dan PASS. Mi búsqueda propia de ciclos, con variantes y productores, no halló ninguno.

## Bloqueante

**B1. Las actas humanas de graph_ui caen en una ruta ignorada por git [V].** `git check-ignore` confirma que `.gitignore:10` (`runs/*`) cubre `graph_ui:runs/acceptance/workspace-documental/lectura/acta.md`. El mismo patrón alcanza `manual/`, `delegacion/` y `modelos/`.

Afecta a G_HUMAN_READ, G_HUMAN_MANUAL, G_HUMAN_DELEGATE y G_HUMAN_MODEL, de los que dependen mutaciones y manuales. WS16 y WS30 no pueden commitear su evidencia sin forzarla, así que el gate depende de un archivo local que un clon no ve.

*Corrección:* mover las actas a una ruta versionada de graph_ui, o incluir en WS16 una negación explícita `!runs/acceptance/` aceptada por el responsable. Ajustar `dag.yaml` y `validacion-humana.md`. El acta de WS43 en deskops no está ignorada.

## Verificado del delta

- WS41 depende de WS40.
- WS44 produce G_SCION, y WS32 lo exige.
- README nombra bien WS39.
- `output_base` está en los 44 nodos.
- WS40 genera entrada e instrucciones.
- WS30 incluye UF01.
- `scope_nodes` cubre WS40/41.
- G_SLDB_WRITE es condicional.
- WS13 remite a WS11.

## Sugerencias no bloqueantes

1. El `scope` de WS07 en YAML no designa al operador Scion; solo lo hace `decisiones.md`. Añadirlo.
2. WS05 conserva "nuevo probe antes de WS33"; ahora es WS44 antes de WS32.
3. UF02 sigue diciendo "responder/ack", sin la precisión de que no hay envío interdesk en sus pasos.
