## REFORMULACION

**Propósito:** fijar el índice, la convención editorial y los criterios de etiquetado del manual documental. **Resultado:** `borradores/manual.md` con capítulos conceptuales, ejemplo fijo y definiciones verificables de disponible/propuesto/bloqueado. **Repo:** `deskops`. **Límites:** no escribir pasos ni capturas ficticios; no implementar UI; no editar nodos; promoción no autorizada.

## AMBIGUEDADES

Ninguna.

Las posibles dudas quedan cubiertas por fuentes suministradas: el ejemplo fijo depende de P08 y de `G_PRODUCT`, que WS07 debe registrar; el manual CLI a reutilizar es `docs/operator-manual.md`; la auditoría WS02–WS04 está declarada como acceso transitivo; y las etiquetas se apoyan en el estado comprobado de WS02. Que `G_PRODUCT` siga pendiente es intencional, no un defecto del nodo.

## DRY-RUN

**Lecturas previstas:** `dag.yaml` (nodo, dependencias, gate), `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/manual.md`, `auditoria/deskops.md` de WS02 y, de forma transitiva, la auditoría UI de WS04; registro de WS07 si ya existe.

**Cambios previstos:** actualizar únicamente `borradores/manual.md`: índice, convención por capítulo, ejemplo fijo y definiciones de estado con criterio comprobable.

**Dependencias:** WS02 aporta superficies y estados comprobados; WS07 debe registrar decisiones y satisfacer `G_PRODUCT`. Sin ese gate, el nodo no puede cerrar.

**Validaciones futuras:** contraste de cada etiqueta con evidencia de WS02; revisión de que no haya pasos ni capturas ficticios; preflight de promoción con archivos, pills, átomos y evidencia; consumo posterior por WS09 y WS31.

## FUTURO

- WS07 y el actor humano resuelven P01–P09 y registran `G_PRODUCT`, incluido el ejemplo fijo.
- WS40 produce el corpus de ejemplo; WS31 publica el manual probado.
- WS09 usará las definiciones de disponible/propuesto/bloqueado.
- La promoción fijará archivos, pills, átomos y evidencia en el TaskDoc.
- Cualquier cambio de alcance corresponde a un humano o a otro nodo, no a este revisor.
