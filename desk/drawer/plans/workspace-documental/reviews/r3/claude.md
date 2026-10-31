# R3 — claude: workspace documental (revisión 3)

## Veredicto: REQUIERE CORRECCIONES

Quedan dos bloqueantes pequeños; cada uno se corrige en pocas líneas de `dag.yaml`. La estructura y las entregas lector/manual están bien. No hace falta otra reestructuración.

Comprobé `build_plan.py --check` (coherente) y busqué ciclos con un script propio, incluidos los productores de gates: no hay. No ejecuté `validate_plan.py` porque reescribe `validation.txt`.

## Bloqueantes

**B1. Falta la arista WS40→WS41 [V].** La aceptación de WS41 exige "UF08 lectura sobre dos stores de WS40", pero WS41 depende solo de WS13 y WS11. Al llegar sus prerrequisitos no puede cerrarse.
*Corrección:* añadir WS40 a `depends_on` de WS41. No crea ciclo: WS40 depende de WS11 y WS08.

**B2. G_SCION queda sin actor si WS05 cierra `unverified` [V].** WS05 permite cerrar el inventario sin el gate y pide un "nuevo probe documentado antes de WS33", pero ningún nodo lo tiene asignado. `produced_by: WS05` ya estaría cerrado y WS33 quedaría bloqueado sin ejecutor.

Además, WS32 no requiere G_SCION. El ticket que refina dice "resolver primero el contrato de identidad disponible en API Scion". Así podría fijar la identidad de intento sobre una API sin comprobar.
*Corrección:* crear un nodo de probe, o declarar que el preflight de WS32 lo repite y produce el gate. Añadir G_SCION a `requires` de WS32.

Solo afecta al ramal opcional E, pero impide ejecutarlo.

## Resueltos desde R2

- **Gates:** ciclo de escritura (POLICY/CONTRACT), productores en YAML, aceptación por repo tras contratos.
- **Implementación:** explorador y divisiones en WS13, corpus único WS40, lectura multidesk WS41, operaciones de conocimiento WS42.
- **Control:** mutaciones con G_HUMAN_READ; WS26/28 lo reciben como arista de gate.
- **Otros:** G_CLOSEOUT fuera de WS12, WS27 por tarea, variantes de P04, UF10, WS10 con G_PRODUCT.

Los gates pendientes son futuros intencionales; no los marco como defecto.

## Sugerencias no bloqueantes

1. **README L93 y `build_plan.py` L61:** dicen "WS42 (Schema)" y lo llaman extensión no prerrequisito. WS42 es conocimiento y sí precede a WS30; Schema es WS39. Debe decir WS39. El YAML manda, pero el texto contradice la cobertura.
2. **WS13:** dice "si WS06 eligió usar ticket draft", pero WS06 solo propone. Debe remitir al acta de WS11.
3. **WS12:** exige aceptación del responsable de sldb incluso con `source_mode=read_only`, cuando WS20 queda excluido. Condicionar G_SLDB_WRITE a `editable`.
4. **UF10:** pide instrucciones reproducibles de instalación, y `alcance.md` las atribuye a WS16/17, pero ninguna de esas fichas las incluye. Asignarlas a WS40 o WS15.
5. **UF02:** "responder" puede ser una escritura hacia otro desk, y P07 excluye la mutación cruzada. Aclarar en WS08 que en el baseline solo aplica ack local, salvo que WS12 lo autorice.
6. **WS11:** no depende de WS08, así que los deltas de lectura se aceptan antes de fijar criterios de flujo. Valorar la arista WS08→WS11.
7. **`manual.md` §17:** ya no menciona UF01–UF08 en texto vigente; no requiere cambio.
