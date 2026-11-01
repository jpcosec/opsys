## REFORMULACION

**Propósito:** validar UF06 con un agente Scion real: pregunta, intervención, corrección, evidencia, decisión humana y cierre mediante el handoff de WS28.

**Resultado:** acta en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/` y resolución de `G_HUMAN_DELEGATE`; no produce código de producto.

**Repo dueño:** `graph_ui` (`output_base: graph_ui:repository_root/`).

**Límites:** no sustituir la integración por mocks ni `completed` por aprobación; no bloquea WS31; `promotion: not_authorized` exige TaskDoc, archivos/pills/átomos/evidencia precisos y preflight task-only.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas:** `dag.yaml` (WS37, WS36, WS30, gates `G_EXEC`/`G_SCION`/`G_HUMAN_DELEGATE`), `validacion-humana.md`, UF06 de `user-flows.md`, acta de WS30, entrega de WS36, autorización externa de `G_EXEC` y probe/contrato de `G_SCION` producido por WS44. Corpus: Taller de WS40.

**Cambios previstos:** crear `delegacion/acta.md` y soportes bajo `runs/subagents/workspace-documental-acceptance/delegacion/`: guion, versiones/commits, comandos públicos, timestamps, resultados, capturas/grabación, observaciones y decisión explícita del participante humano. Incluir el acta en el commit atómico del repo dueño. Sin cambios de código.

**Dependencias y gates:** esperar WS36 (UI de intervención/revisión) y WS30 (base manual aceptada); WS28 llega transitivamente por WS30. No ejecutar sin `G_EXEC` autorizado y `G_SCION` verificado; si faltan, detenerse y registrar el hueco con repo dueño, sin sustituto.

**Validación esperada:** el participante completa UF06 sin rutas memorizadas ni correcciones verbales; el acta vincula actor humano, versión, guion, resultado y soportes; se distingue completado de aprobado; no hay mocks; el gate `G_HUMAN_DELEGATE` queda respaldado por acta versionada y blob verificable.

**Errores:** gate ausente o no verificado → parada; Scion inaccesible → parada, no simulación; intento duplicado o respuesta al intento equivocado → fallo; cierre no verificado por Deskops → fallo; acta solo local o sin commit → no válida.

## FUTURO

WS36 entrega la integración; WS30 su acta manual; WS44 produce `G_SCION`; el humano/designee designa operador y autoriza `G_EXEC`; WS37 produce el acta y `G_HUMAN_DELEGATE`; WS38 publica los capítulos verificados. WS31 no queda bloqueado.
