REFORMULACION
Propósito: publicar el manual documental básico y las entradas del desk real sobre recorridos ya demostrados. Resultado: `docs/workspace-user-manual.md` versionado con instrucciones trazables a actas/versiones, `desk/README.md` y mapa authored probados, átomos de decisiones/contratos y links/provenance atom→doc verificados; Scion, modelos y Changes no demostrados quedan propuestos sin bloquear el manual básico. Repo dueño: deskops; WS30 valida en graph_ui. Límites: agrupación sin ejecución propia; no crea aristas ni autoriza tareas, no publica el ejemplo como ecosistema real, no escribe repos hermanos ni atomiza permisos/aceptación inexistentes.

AMBIGUEDADES
Ninguna. Las frases «WS30 acta manual y WS17 entradas alimentan WS43» y «WS31 reúne WS10, WS30 y WS43» coinciden con `depends_on`; el orden de `children` no crea secuencia. WS31 acota contratos y etiquetas, y WS43 identifica al participante P08 y resuelve el repo sin entrada.

DRY-RUN
Ejecución hipotética por aristas:
1. WS10 (deskops) lee auditorías WS02–04, brief y decisiones; escribe `borradores/manual.md` con índice, definiciones y ejemplo futuro. Gate G_PRODUCT ya registrado.
2. WS17 (deskops) lee contrato WS11 y manifiesto WS40; escribe `ejemplo/nav/` con plantillas que cubren ambos desks y valida roots/aliases contra WS40, sin duplicar registry.
3. WS30 (graph_ui) consume plantillas WS17 materializadas por WS40 y WS21–28/WS42; persona recorre UF01–05; produce acta en `runs/subagents/workspace-documental-acceptance/manual/` con plantillas, paths/hashes y recorridos. Un fallo de guion bloquea el gate y abre tarea en el nodo causante.
4. WS43 (deskops) consume plantillas WS17, acta WS30 y `contratos/navegacion.md`; escribe `desk/README.md`, mapa/índices, átomos P01/P02/P07/P09 y acta de publicación; recorre `deskops list repositories`: enlaza entrada o registry y deja follow-up, sin fabricar entradas; cierra con `deskops closeout commit`.
5. WS31 (deskops) consume índice WS10, actas WS30/WS43 y contratos; escribe manual, assets y un átomo por Pxx/contrato; marca Scion propuesto; Executor comprueba links resolubles, etiquetas contra actas/commits y atom→doc; Tester independiente valida antes del cierre.
Errores: contrato ausente → detenerse y registrar hueco, sin sustituto; WS43 sin entrada authored → registry y follow-up; WS31 sin prueba WS29 → capítulo propuesto.
Validación integrada: mapa publicado corresponde a plantillas/paths validados en WS30; cada instrucción cita acta/versión; links y provenance resuelven; G_HUMAN_MANUAL pendiente no se simula.

FUTURO
Actas humanas de WS30/WS43 (G_HUMAN_MANUAL/G_PRODUCT), prueba WS29 y capítulo Scion WS38; decisión humana de aceptación del paquete.
