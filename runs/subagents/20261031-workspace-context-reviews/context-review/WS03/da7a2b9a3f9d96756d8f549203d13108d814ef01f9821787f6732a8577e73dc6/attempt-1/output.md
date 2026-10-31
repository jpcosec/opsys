## REFORMULACION

**Propósito:** auditar en solo lectura la persistencia, consultas, notaciones y límites reales de `sldb/pron/spec2viz`, incluyendo concurrencia/locks, referencias documentales, búsquedas y alcance ViewDoc.

**Resultado:** un documento `auditoria/infraestructura.md`, bajo `output_base` de `deskops`, que distinga API comprobada mediante lectura citada, ausencia y hueco.

**Repo dueño:** `deskops`. **Límites:** sin cambios interrepo, sin implementación, Kimun solo como referencia, promoción no autorizada.

## AMBIGUEDADES

1. Cita: «distinguir API comprobada (lectura citada del estado actual), ausencia y hueco».
   Obligaría a inventar el criterio que separa «ausencia» de «hueco» y la evidencia exigida para cada categoría. Sin esa definición, la aceptación no es del todo comprobable.

2. Cita: «lectura citada del estado actual».
   No fija revisión, commit ni fecha de observación. Obligaría a decidir qué snapshot del repo se considera «actual» y cómo citarlo de forma verificable.

## DRY-RUN

- **Lecturas previstas:** `dag.yaml`, `brief.md`, `alcance.md`, `decisiones.md`, guía de revisión y estado de solo lectura de `sldb/pron/spec2viz`.
- **Cambios previstos:** únicamente crear/editar `auditoria/infraestructura.md` en `deskops`; ningún cambio en repos auditados.
- **Dependencias:** `WS01` como prerrequisito directo; sin `requires`. `WS06` consumirá después la auditoría.
- **Validaciones futuras:** revisar que la salida cite lecturas, distinga comprobado/ausente/hueco y no introduzca cambios interrepo; promoción posterior mediante TaskDoc con archivos, pills y evidencia, sujeta a preflight.
- **No se ejecuta nada** en este nodo.

## FUTURO

- `WS06` usará los hallazgos para la matriz de correspondencia por repo dueño.
- La promoción fijará archivos, escenarios y evidencia dentro de la aceptación.
- El coordinador o revisor humano comparará esta revisión y dispondrá hallazgos.
- `WS11/WS12` producirán contratos y recepción por delta; `WS18` cubre ViewDoc de forma opcional.
- Ninguna aprobación de implementación, API o uso se presume por este nodo.
