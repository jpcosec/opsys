## REFORMULACION

**Propósito:** auditar en solo lectura la persistencia, consultas y notaciones reales de sldb/pron/spec2viz, incluyendo fuente/payload, conflictos y control de concurrencia (CAS por revisión/hash, locks), referencias documentales, búsquedas y alcance ViewDoc.

**Resultado:** una salida documental en `auditoria/infraestructura.md`.

**Repo dueño:** `deskops` para la salida; los repos auditados son sldb/pron/spec2viz.

**Límites:** solo lectura, sin cambios interrepo; Kimun solo como referencia. El nodo es candidato y no tiene ejecución autorizada.

**Aceptación:** el documento debe distinguir API comprobada —con lectura citada del estado actual—, ausencia y hueco.

**Dependencia:** WS01.

## AMBIGUEDADES

Ninguna. El alcance enumera los aspectos a auditar, el repo de salida está fijado, el límite de solo lectura es explícito y la aceptación exige una clasificación comprobable. La mención a «notaciones» en el título queda cubierta por «alcance real ViewDoc» y por el glosario, que incluye notación/layout. No hace falta inventar resultado, actor, repo ni permiso.

## DRY-RUN

- **Lecturas previstas:** `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `dag.yaml` y, en promoción, `task-ws03.md`; consulta de solo lectura a rutas/código de sldb/pron/spec2viz.
- **Cambios previstos:** únicamente crear el documento de `output_scope: auditoria/infraestructura.md` en `deskops`. Ningún cambio interrepo.
- **Dependencias:** WS01 como prerrequisito; `requires: []`. Si falta un contrato, API, dato o permiso de una dependencia, aplica la regla común: detenerse y registrar el hueco sin crear sustituto.
- **Validaciones futuras:** revisar que cada aspecto del alcance aparezca clasificado como API comprobada, ausencia o hueco; que las APIs comprobadas citen lectura del estado actual; y que no existan cambios fuera de `deskops`.

## FUTURO

WS06 consumirá esta auditoría para la correspondencia de alcance por repo dueño. La promoción fijará archivos exactos, pills, átomos y evidencia dentro del TaskDoc. La aceptación humana o revisión del delta corresponde al responsable designado, no a este nodo.
