## REFORMULACION
**Propósito:** convertir el índice y las convenciones de WS10, junto con lo demostrado en WS30 y publicado en WS43, en un manual documental básico verificable.
**Resultado:** `docs/workspace-user-manual.md`, sus assets y átomos enlazados, con instrucciones trazables a actas y contratos.
**Repo dueño:** `deskops`, con `output_base: deskops:repository_root/`.
**Límites:** no implementa UI ni sustituye actas; no atomiza Pxx pendientes; Scion queda como capítulo propuesto; los extras de modelos/impacto se etiquetan o comprueban sin bloquear el manual básico.

## AMBIGUEDADES
1. **Base de rutas de los insumos.** Cita: «incorporar el índice de borradores/manual.md» y «cada contrato en contratos/». El nodo no fija si `borradores/manual.md` y `contratos/` se resuelven desde el paquete de plan, desde `deskops:repository_root/` o desde otro repo. Obligaría a inventar la ruta base para localizar el índice y los contratos de WS11/WS12, pese a que sus productores sí están nombrados.

## DRY-RUN
**Lecturas previstas:** guía, brief, alcance, decisiones, cobertura, `borradores/manual.md`, nodos WS10/WS30/WS43 y gates `G_HUMAN_MANUAL`, `G_HUMAN_MODEL`; actas de WS30 y WS43; contratos de WS11/WS12.
**Cambios previstos:** redactar capítulos e índice en `docs/workspace-user-manual.md`; incorporar capturas en `docs/assets/workspace-user-manual/`; crear y enlazar átomos de Pxx aceptadas y contratos; marcar Scion como propuesto.
**Dependencias:** acta humana de WS30; publicación y acta de WS43; índice de WS10; contratos transitivos de WS11/WS12; `G_HUMAN_MANUAL`.
**Validaciones futuras:** cada instrucción remite a acta; etiquetas, links y `atom->doc` verificados; ningún Pxx pendiente atomizado; capítulos de personalización/impacto comprobados o marcados propuestos; capturas del sistema real.

## FUTURO
WS30 produce el acta y satisface `G_HUMAN_MANUAL`; WS43 publica el desk real y su acta; WS38 añade delegación verificada; el humano acepta Pxx y fija P08. La promoción fijará archivos exactos, pills, escenarios de prueba y preflight de solo tarea.
