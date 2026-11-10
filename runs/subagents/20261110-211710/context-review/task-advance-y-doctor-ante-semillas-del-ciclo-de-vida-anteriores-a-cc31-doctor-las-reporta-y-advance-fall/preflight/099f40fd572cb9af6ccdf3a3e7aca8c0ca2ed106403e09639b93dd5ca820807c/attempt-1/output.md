## REFORMULACION

Encargo ejecutable (no agregado): corregir dos defectos en deskops. d1: `deskops doctor` debe detectar y reportar las semillas managed de `desk/lifecycle/` desactualizadas respecto del paquete, un hallazgo por archivo, indicando diferencias y el fix `deskops desk update --apply`, reutilizando `seed_desk(root, apply=False, restore_managed=True)`. d2: `deskops advance` debe fallar antes de escribir cuando una arista no trae `attributes.sets.status` o su efecto no alcanza el estado exigido, nombrando archivo y `relation_type`, explicando que falta o difiere el efecto sets y sugiriendo `deskops desk update --apply`; sin `ValidationError` de pydantic y sin cambios en disco. Resultado: ambos arreglos con causa raíz escrita, tests de reproducción verdes, doc en `docs/` y `CHANGELOG.md`. Límites: fuera el validador CC37, la migración del kit y la gramática del CLI; no editar a mano `desk/` ni `.sldb/`; no `git add -A`; tests individuales con `TMPDIR=/dev/shm` y guarda pgrep; goldens de ayuda idénticos.

## AMBIGUEDADES

1. «severidad alert o error a decidir y justificar en el informe»: obliga a inventar cuál severidad elegir y el criterio de justificación.
2. «puesta vía sldb (fields update)»: no se detalla el comando ni el esquema exacto de campos; obliga a inventar la invocación reproducible.
3. «una tarea con recibos de activación»: no se define formato, ubicación ni contenido de esos recibos; obliga a inventarlos.
4. «la guarda de pgrep anclada»: no se especifica patrón ni comando; obliga a inventar la guarda.
5. «los mensajes nuevos de d1 y d2, que llevan golden propio»: no se da el texto esperado; obliga a inventar el mensaje exacto y su golden.
6. «4 pasos del workflow de deskops en clon limpio los corre el coordinador»: no se enumeran aquí; obliga a inferirlos si se validaran en este nodo.

## DRY-RUN

Lecturas: los siete archivos de `files`, tests existentes, docs y CHANGELOG, además del informe de reproducción y la nota 5106e3f8. Cambios previstos: hallazgo de doctor basado en `seed_desk`; prechequeo en advance antes de persistir; tests de reproducción y de doctor; golden de mensajes; doc de operador y CHANGELOG. Dependencias: semilla managed del paquete, `desk update --apply`, entorno limpio vía `deskops init` y creación de la arista mediante sldb. Validaciones futuras: reproducción del fallo, desaparición del hallazgo tras update, transición draft→active, goldens de ayuda idénticos, tests individuales con `TMPDIR=/dev/shm`, y cuatro pasos del workflow en clon limpio.

## FUTURO

El dueño del kit Chatbot_Infra ejecuta `deskops desk update --apply`; el coordinador corre los cuatro pasos del workflow en clon limpio; un humano decide y justifica la severidad del hallazgo d1 si no queda fijada en el informe.
