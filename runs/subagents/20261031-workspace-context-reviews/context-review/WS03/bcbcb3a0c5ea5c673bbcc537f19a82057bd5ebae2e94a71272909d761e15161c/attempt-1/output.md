REFORMULACION
Propósito: auditar en solo lectura persistencia, consultas y notaciones en `sldb/pron/spec2viz`, con Kimun solo como referencia. Resultado: un documento `auditoria/infraestructura.md`, sin cambios interrepo, que distinga API comprobada con lectura citada, ausencia y hueco. Repo dueño: `deskops`. Límites: solo lectura; depende de WS01; promoción no autorizada; el TaskDoc de promoción fija archivos, pills, átomos y evidencia, con preflight task-only.

AMBIGUEDADES
1. «referencias documentales, búsquedas (índices o consultas expuestas)»: no delimita qué referencias ni qué búsquedas inventariar, ni qué hace «expuesta» a una consulta. Obliga a inventar categorías y umbral de comprobación.
2. Título «Inventariar persistencia, consultas y notaciones» frente a scope «alcance real ViewDoc»: no aclara si «notaciones» equivale solo a notación/layout de ViewDoc o incluye otras. Obliga a inventar el universo auditado y el criterio de «real».
3. «distinguir API comprobada (lectura citada del estado actual), ausencia y hueco»: no define la frontera entre ausencia y hueco ni la evidencia mínima. Obliga a inventar una clasificación.
4. «lectura citada del estado actual»: no fija revisión, snapshot o fuente de estado para cada repo objetivo. Obliga a elegir qué estado citar.

DRY-RUN
Lecturas: input, guía, brief, alcance, decisiones y dag; después, solo lectura del estado de `sldb/pron/spec2viz`. Cambios previstos: únicamente `auditoria/infraestructura.md`. Dependencias: WS01; acceso/estado de los repos objetivo; si falta permiso o contrato, aplica la regla común de detenerse y registrar el hueco. Validaciones futuras: revisar que el documento separe comprobado, ausencia y hueco; la promoción requerirá evidencia, archivos cambiados y preflight. Nada ejecutado.

FUTURO
WS06 consumirá esta auditoría para su matriz; WS07 designará responsables receptores y WS11/12 registrarán aceptación de acceso. El TaskDoc de promoción fijará archivos y evidencia; un humano autoriza la promoción.
