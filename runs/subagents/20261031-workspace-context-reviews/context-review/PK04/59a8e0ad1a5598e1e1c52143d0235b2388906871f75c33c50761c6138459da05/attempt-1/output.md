## REFORMULACION

**Propósito:** agrupar los entregables de navegación y representaciones del desk sobre una identidad común, sin ejecución propia.

**Resultado:** un paquete cuyos hijos permiten abrir los mismos documentos/soportes desde lista, tablero, dependencias, procedimiento y conocimiento; sin escribir status desde renderers ni marcar pasos por lectura; con índices que siguen sus fuentes. WS18 (ViewDoc) es extensión opcional probada sobre store real.

**Repo:** agrupación en `deskops`; hijos en `deskops`, `graph_ui` y `spec2viz`.

**Límites:** no autoriza tareas ni añade aristas; la revisión de comprensión no equivale a producto entregado; no se ejecuta nada.

## AMBIGUEDADES

1. «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada» frente a «ViewDoc concreto (WS18, opcional)… sin WS18 el resto del paquete puede completarse». Obliga a inventar si el cierre de PK04 exige o no la salida de WS18, que es hijo del paquete, cuando no exista recibo `G_SPEC_VIEW`.

## DRY-RUN

PK04 no se ejecuta: termina cuando terminan sus hijos. No hay aristas internas entre ellos; el orden lo fijan sus dependencias externas y gates.

- **WS17** parte de `WS11` y del manifiesto de `WS40`; escribe plantillas `ejemplo/nav/`. `WS40` produce dos repos temporales, stores, commits y manifiesto JSON; WS17 regenera el corpus con sus plantillas y valida enlaces contra roots/aliases del manifiesto, sin tocar el registry real. Transferencia: manifiesto → WS17; plantillas → corpus temporal.
- **WS22, WS23 y WS24** consumen `WS09` (catálogo) y `WS13` (lector, foco, historia). WS22 materializa Board lista/tablero/dependencias; WS23 rituales/pasos inertes; WS24 conocimiento, backlinks y vecindad. Comparten lector y abren los mismos TaskDoc/soportes; pueden ejecutarse en paralelo.
- **WS18** solo tras `G_SPEC_VIEW`; usa ViewDoc/NotationDoc de `WS09`/`WS11`, evaluador de `graph_ui` y store real. Su ausencia no bloquea a WS24.

**Validación integrada:** pruebas en `graph_ui`/`spec2viz` con corpus WS40 o store temporal; recorrer enlaces de WS17 sin UI; comprobar que lista, tablero, dependencias, procedimiento y conocimiento abren el mismo soporte; verificar ausencia de peticiones de escritura desde renderers y procedimientos; estados desde deskops, no desde `dag.yaml`; selección WS18 coincide con WS09/WS11. Gates: `G_UI_READ` (WS22/23/24 y WS40), `G_SPEC_VIEW` (WS18). Si falta contrato o gate, detenerse y registrar el hueco sin sustituto.

## FUTURO

`WS11`, `WS09`, `WS40` y `WS13` producen contratos, catálogo, corpus y lector; el receptor de cada repo emite recibos `G_UI_READ`/`G_SPEC_VIEW`; el TaskDoc de promoción fija archivos, pruebas y textos; `WS30` integra índices y `WS43` publica entradas reales.
