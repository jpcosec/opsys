## REFORMULACION

**Propósito:** cerrar el contrato técnico de operaciones y escritura del workspace documental: qué se lee o muta por operación/campo/modelo, por qué canal público, con qué actor, revisión esperada, efectos Git, protección de campos, permisos, fallos y closeout fuera del servidor UI.

**Resultado:** `contratos/operaciones.md` con whitelist por operación/campo/canal/actor/revisión/Git/efectos, matriz de capacidades y huecos con productor asignado.

**Repo:** `deskops`; solo contrato y enlaces, sin actas interrepo.

**Límites:** no ejecutar mutaciones, no diseñar un adaptador ausente, no inventar una lista universal de campos, no exigir habilitar ninguna mutación para cerrar, no sustituir pruebas de API ni actas de recepción por delta.

## AMBIGUEDADES

ninguna

## DRY-RUN

**Lecturas previstas:** guía, brief, alcance, decisiones, cobertura, nodo WS12 y gates; a través de WS11/WS08, los inventarios WS02–04 y el contrato de navegación. Nada se ejecuta.

**Cambios previstos:** redactar/actualizar `contratos/operaciones.md` y registrar enlaces a recibos externos en `deskops`; sin tocar código, tareas ni actas.

**Dependencias:** WS11 y WS08 cerrados; `G_WRITE_POLICY` ya satisfecho; las actas por delta las produce P01 en el repo receptor (`graph_ui`/`sldb`), no WS12; para raw-source, WS20 y `G_SOURCE`.

**Validaciones futuras:** checklist de aceptación, cita de path/símbolo/commit, matriz completa, campos protegidos por modelo/operación, huecos con dueño, evaluación de `G_WRITE_CONTRACT`/`G_UI_WRITE` solo por IDs/efecto y ausencia de mutaciones ejecutadas.

## FUTURO

P01/receptor del repo emitirá acta por delta al prepararlo; WS20 producirá la API pública y `G_SOURCE`, manteniendo WS21 bloqueado hasta ese recibo; los nodos de implementación consumirán la whitelist. WS12 no habilita mutaciones ni acredita pruebas de API.
