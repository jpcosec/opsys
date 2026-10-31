## REFORMULACION
Propósito: registrar una decisión humana sobre un intento Scion —aprobar o pedir corrección— con actor humano identificado, referencia al intento y a su tarea. Resultado: un registro de decisión con resultado explícito; la corrección exige texto. Repo dueño: `deskops` (`runtime/` con adaptador definido por contrato, modelos/reportes y tests). Límites: solo escribe la decisión mediante la operación que fije el contrato WS12; si falta, hueco con dueño. No escribe estados `validated` ni `closed` (testing/closeout de deskops), ni convierte `completed` del agente en aprobación. Depende de WS32 (identidad de intento/cierre), WS33.1 (vinculación mensajes/resultados) y G_SCION; WS12 llega transitivamente.

## AMBIGUEDADES
Ninguna. Los elementos que podrían parecer huecos tienen productor nombrado: el actor y la operación provienen del contrato WS12; la identidad de intento, de WS32; la accesibilidad y API pública, de G_SCION/WS44. La aceptación es comprobable (actor, referencia a intento y tarea, resultado aprobar/corregir, texto obligatorio en corrección, `completed` no aprobado). Archivos exactos y textos quedan delegados al TaskDoc de promoción, que la guía excluye explícitamente.

## DRY-RUN
Lecturas previstas: nodo WS33.2 y vecinos WS32/WS33.1 en `dag.yaml`; contrato WS12 (operación y actor); contrato público Scion vía WS44; salidas de WS32.1/WS32.2 (identidad de intento, manifiesto/RunDoc); salidas de WS33.1 (referencias intento-mensaje-resultado); `reconciliacion.md` y Board del repo receptor antes de promover.

Cambios previstos: adaptador en `deskops/runtime/` para la operación de decisión; modelo/reporte de decisión con actor, intento, tarea y resultado; tests.

Dependencias: WS32 y WS33.1 completos; G_SCION verificado por WS44; contrato WS12 disponible. Si falta cualquiera, detenerse y registrar hueco con repo dueño, sin sustituto.

Validaciones futuras: decisión aprobada registra actor/intento/tarea; corrección sin texto se rechaza; `completed` del agente no se mapea a aprobado; estados validated/closed no se escriben desde este nodo; pruebas sobre store temporal real; ninguna ejecución ahora.

## FUTURO
WS44 resuelve G_SCION con probe real; WS12 publica el contrato de operación/actor; WS32.1/WS32.2 fijan identidad de intento y manifiesto; WS33.1 aporta referencias de mensajes/resultados; el TaskDoc de promoción fija archivos, escenarios y textos; WS06 integra el delta en ticket receptor; la recepción humana por delta y el cierre de WS33 como agregado corresponden a actores y nodos posteriores, no a este nodo.
